/** @file
  Allwinner SMHC (SD/MMC Host Controller) DXE Driver.

  Implements EFI_SD_MMC_PASS_THRU_PROTOCOL for SMHC0 (SD card slot)
  on Allwinner A523/H618/A733 SoCs using PIO FIFO mode.

  Note: SMHC2 is not instantiated — Cubie A7Z has no eMMC (only optional
  UFS module slot which uses a different protocol).

  SdDxe sits on top of this and provides EFI_BLOCK_IO_PROTOCOL.
**/

#include <Uefi.h>
#include <PiDxe.h>

#include <Protocol/SdMmcPassThru.h>
#include <Protocol/DevicePath.h>

#include <Library/BaseLib.h>
#include <Library/BaseMemoryLib.h>
#include <Library/DebugLib.h>
#include <Library/IoLib.h>
#include <Library/TimerLib.h>
#include <Library/UefiBootServicesTableLib.h>
#include <Library/UefiLib.h>
#include <Library/MemoryAllocationLib.h>
#include <Library/DevicePathLib.h>
#include <Library/SerialPortLib.h>
#include <Library/CacheMaintenanceLib.h>

#include <IndustryStandard/Sd.h>

#include "SunxiSmhcReg.h"

// ---------------------------------------------------------------------------
// Driver-private data structures
// ---------------------------------------------------------------------------

#define SUNXI_SMHC_PRIVATE_SIGNATURE SIGNATURE_32('S','M','H','C')

typedef struct {
  UINT32                         Signature;
  EFI_SD_MMC_PASS_THRU_PROTOCOL  PassThru;
  EFI_HANDLE                     ControllerHandle;
  UINTN                          SmhcBase;    // MMIO base of this SMHC
  UINT8                          CardCtrl;    // 0=SMHC0/SD, 2=SMHC2/eMMC
  BOOLEAN                        IsEmmc;      // TRUE=eMMC(SMHC2), FALSE=SD(SMHC0)
  BOOLEAN                        Initialized;
  UINT32                         ClockDiv;    // current clock divider (CLKCR[7:0])
  EFI_DEVICE_PATH_PROTOCOL      *DevPath;    // MemMapped device path for this controller
} SUNXI_SMHC_PRIVATE;

#define SMHC_PRIVATE_FROM_PASS_THRU(a) \
  CR(a, SUNXI_SMHC_PRIVATE, PassThru, SUNXI_SMHC_PRIVATE_SIGNATURE)

// ---------------------------------------------------------------------------
// Debug print via SerialPort
// ---------------------------------------------------------------------------
STATIC VOID
SmhcDbg (
  IN CONST CHAR8  *Msg
  )
{
  UINTN Len = AsciiStrLen (Msg);
  SerialPortWrite ((UINT8 *)Msg, Len);
}

STATIC VOID
SmhcDbgHex (
  IN CONST CHAR8  *Prefix,
  IN UINT32        Val
  )
{
  CHAR8   Buf[64];
  CHAR8  *P = Buf;
  UINTN   Len, i;
  UINT8   Nibble;
  CHAR8   Hex[8];

  // Copy prefix
  for (Len = 0; Prefix[Len] != '\0'; Len++) {
    Buf[Len] = Prefix[Len];
  }
  P = Buf + Len;

  // "0x"
  *P++ = '0'; *P++ = 'x';

  // 8 hex digits
  for (i = 0; i < 8; i++) {
    Nibble = (UINT8)((Val >> (28 - i * 4)) & 0xF);
    Hex[i] = (Nibble < 10) ? ('0' + Nibble) : ('A' + Nibble - 10);
  }
  for (i = 0; i < 8; i++) *P++ = Hex[i];
  *P++ = '\r'; *P++ = '\n'; *P = '\0';

  SerialPortWrite ((UINT8 *)Buf, (UINTN)(P - Buf));
}

STATIC
VOID
SmhcSynthesizeProtectiveMbr (
  OUT UINT8  *Buffer,
  IN  UINT32  LastBlock
  )
{
  UINT32 MbrSize;

  ZeroMem (Buffer, 512);
  //
  // Protective MBR entry:
  //  - type 0xEE
  //  - first LBA = 1
  //  - size = min(last_block, 0xFFFFFFFF)
  //
  Buffer[446] = 0x00;
  Buffer[447] = 0x00;
  Buffer[448] = 0x02;
  Buffer[449] = 0x00;
  Buffer[450] = 0xEE;
  Buffer[451] = 0xFF;
  Buffer[452] = 0xFF;
  Buffer[453] = 0xFF;
  WriteUnaligned32 ((UINT32 *)&Buffer[454], 1);
  MbrSize = (LastBlock >= 0xFFFFFFFFU) ? 0xFFFFFFFFU : LastBlock;
  WriteUnaligned32 ((UINT32 *)&Buffer[458], MbrSize);
  Buffer[510] = 0x55;
  Buffer[511] = 0xAA;
}

// ---------------------------------------------------------------------------
// CCU clock setup
// ---------------------------------------------------------------------------
STATIC VOID
SmhcSetupClock (
  IN UINT8  CardCtrl
  )
{
  UINT32  BgrReg;
  UINT32  ClkReg;
  UINT32  ClkRegOff;

  // Choose CCU register offset
  if (CardCtrl == 0) {
    ClkRegOff = CCU_SMHC0_CLK_REG;
  } else {
    ClkRegOff = CCU_SMHC2_CLK_REG;
  }

  // 1. Deassert reset, enable bus clock gate for SMHC0 only
  BgrReg = CCU_READ32 (CCU_SMHC_BGR_REG);
  BgrReg |= SMHC0_CLK_GATING | SMHC0_RST;
  CCU_WRITE32 (CCU_SMHC_BGR_REG, BgrReg);
  MicroSecondDelay (10);

  // 2. Set SMHC0 module clock: HOSC (24MHz), N=0 (÷1), M=0 (÷1) → 24MHz
  //    Card clock = 24MHz / (2 * (CLKCR_DIV + 1))
  //    With CLKCR_DIV=29: 24MHz / 60 ≈ 400kHz (init speed)
  ClkReg = SMHC_CLK_GATING | SMHC_CLK_SRC_HOSC |
           (0U << SMHC_CLK_N_SHIFT) | (0U << SMHC_CLK_M_SHIFT);
  CCU_WRITE32 (ClkRegOff, ClkReg);
  MicroSecondDelay (2);
}

// ---------------------------------------------------------------------------
// Update SMHC_CLKCR: send "update clock" command to controller
// ---------------------------------------------------------------------------
STATIC EFI_STATUS
SmhcUpdateClock (
  IN UINTN   SmhcBase,
  IN UINT32  ClkDiv
  )
{
  UINT32  Cmd;
  UINT32  Timeout;

  // Set divider
  // Do NOT set CLKCR_LOW_PWR.  With LOW_PWR, the SMHC gates the SD clock when
  // the data FSM goes idle (i.e. when DATA_OVER fires).  If the FIFO was full
  // at that moment, the last few backpressured words in the card's output
  // register can never enter the FIFO because the clock is permanently stopped.
  // Without LOW_PWR the clock continues to run; once we drain the FIFO the
  // backpressure releases and the card can flush its remaining output words.
  SMHC_WRITE32 (SmhcBase, SMHC_CLKCR, ClkDiv | CLKCR_CARD_CLK_ON);

  // Send "update clock" command (no actual CMD sent on the wire)
  Cmd = CMD_START | CMD_UPCLK_ONLY | CMD_WAIT_PRE;
  SMHC_WRITE32 (SmhcBase, SMHC_CMD, Cmd);

  // Wait for CMD_START to clear
  Timeout = 1000000;
  while (SMHC_READ32 (SmhcBase, SMHC_CMD) & CMD_START) {
    if (--Timeout == 0) {
      SmhcDbg ("[SMHC] UpdateClock timeout\r\n");
      return EFI_TIMEOUT;
    }
    MicroSecondDelay (1);
  }
  return EFI_SUCCESS;
}

// ---------------------------------------------------------------------------
// Reset and initialize SMHC controller
// ---------------------------------------------------------------------------
STATIC EFI_STATUS
SmhcReset (
  IN SUNXI_SMHC_PRIVATE  *Private
  )
{
  UINTN   Base = Private->SmhcBase;
  UINT32  Reg;
  UINT32  Timeout;

  // Verify SMHC MMIO is accessible: write test pattern to TMOUT and read back
  SMHC_WRITE32 (Base, SMHC_TMOUT, 0xDEADBEEF);
  {
    UINT32 TestVal = SMHC_READ32 (Base, SMHC_TMOUT);
    if (TestVal == 0x00000000) {
      SmhcDbg ("[SMHC] MMIO not accessible (clock gated?), skip\r\n");
      return EFI_NOT_READY;
    }
  }

  // Software reset (FIFO, DMA, and controller)
  SMHC_WRITE32 (Base, SMHC_GCTRL,
                GCTRL_SOFT_RST | GCTRL_FIFO_RST | GCTRL_DMA_RST);
  Timeout = 100000;
  do {
    Reg = SMHC_READ32 (Base, SMHC_GCTRL);
    if (--Timeout == 0) {
      SmhcDbg ("[SMHC] Soft reset timeout\r\n");
      return EFI_TIMEOUT;
    }
    MicroSecondDelay (1);
  } while (Reg & (GCTRL_SOFT_RST | GCTRL_FIFO_RST | GCTRL_DMA_RST));

  // Disable IDMAC, use PIO mode
  SMHC_WRITE32 (Base, SMHC_DMAC, 0);
  SMHC_WRITE32 (Base, SMHC_IDIE, 0);

  // Clear interrupts, use polling
  SMHC_WRITE32 (Base, SMHC_IMASK, 0);
  SMHC_WRITE32 (Base, SMHC_RINT, 0xFFFFFFFF);

  // Set FIFO threshold (RX:15, TX:15 words = 64 bytes each)
  SMHC_WRITE32 (Base, SMHC_FTRGLVL,
                (FIFO_RX_THRESHOLD << 16) | (FIFO_TX_THRESHOLD << 0));

  // Set timeout
  SMHC_WRITE32 (Base, SMHC_TMOUT, SMHC_TMOUT_DEFAULT);

  // Set bus width to 4-bit.
  // boot0 configures the SD card for 4-bit mode (HSSDR52/SDR25) before
  // handing off to EDK2.  The card retains that setting across the SMHC
  // soft-reset (which only resets the controller, not the card).  Setting
  // CTYPE to match prevents bus-width mismatch and the resulting CRC errors
  // on every data transfer.  SdDxe's ACMD6 handling (if it runs) will keep
  // both sides in sync.
  SMHC_WRITE32 (Base, SMHC_CTYPE, CTYPE_4BIT);

  // Set block size to 512
  SMHC_WRITE32 (Base, SMHC_BLKSZ, 512);

  // Enable PIO mode (bit 31 = halt flow → we'll toggle per transfer)
  // Leave GCTRL without INT_EN so no interrupts fire
  SMHC_WRITE32 (Base, SMHC_GCTRL, 0);

  // Enable New Timing Mode (required on A523/T527 family).
  // Without this, the data sample point is off-phase and CMD17/CMD18 return
  // DATA_CRC_ERR or END_BIT_ERR. boot0 sets this before loading the FD;
  // our soft-reset clears it, so we must re-enable it here.
  SMHC_WRITE32 (Base, SMHC_NTSR, NTSR_MODE_SEL_NEW);

  // Set clock to 400kHz init speed: HOSC 24MHz / (2*(29+1)) = 400kHz
  SmhcUpdateClock (Base, 29);
  Private->ClockDiv = 29;

  // Send 80 initialization clocks
  SMHC_WRITE32 (Base, SMHC_CMD,
                CMD_START | CMD_SEND_INIT_SEQ | CMD_UPCLK_ONLY);
  Timeout = 100000;
  while (SMHC_READ32 (Base, SMHC_CMD) & CMD_START) {
    if (--Timeout == 0) {
      SmhcDbg ("[SMHC] Init clocks timeout\r\n");
      return EFI_TIMEOUT;
    }
    MicroSecondDelay (1);
  }

  Private->Initialized = TRUE;
  return EFI_SUCCESS;
}

// ---------------------------------------------------------------------------
// Poll RINT for expected events (cmd done, data done, error)
// ---------------------------------------------------------------------------
STATIC EFI_STATUS
SmhcWaitRint (
  IN  UINTN   SmhcBase,
  IN  UINT32  WaitMask,
  OUT UINT32  *RintOut  OPTIONAL
  )
{
  UINT32  Rint;
  UINT32  Timeout = 5000000;  // 5 seconds

  while (TRUE) {
    Rint = SMHC_READ32 (SmhcBase, SMHC_RINT);

    if (Rint & RINT_ERROR_BITS) {
      // Clear
      SMHC_WRITE32 (SmhcBase, SMHC_RINT, 0xFFFFFFFF);
      if (RintOut != NULL) *RintOut = Rint;
      if (Rint & RINT_RESP_TIMEOUT)   return EFI_TIMEOUT;
      if (Rint & RINT_DATA_TIMEOUT)   return EFI_TIMEOUT;
      if (Rint & RINT_RESP_ERR)       return EFI_DEVICE_ERROR;
      if (Rint & RINT_RESP_CRC_ERR)   return EFI_CRC_ERROR;
      if (Rint & RINT_DATA_CRC_ERR)   return EFI_CRC_ERROR;
      return EFI_DEVICE_ERROR;
    }

    if ((Rint & WaitMask) == WaitMask) {
      SMHC_WRITE32 (SmhcBase, SMHC_RINT, Rint);  // Clear
      if (RintOut != NULL) *RintOut = Rint;
      return EFI_SUCCESS;
    }

    if (--Timeout == 0) {
      if (RintOut != NULL) *RintOut = Rint;
      return EFI_TIMEOUT;
    }
    MicroSecondDelay (1);
  }
}

// ---------------------------------------------------------------------------
// PIO data transfer via FIFO
// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
// IDMAC (Internal DMA Controller) support
// ---------------------------------------------------------------------------

// Descriptor layout for Allwinner SMHC IDMAC (one descriptor per transfer).
// T527 IDMAC uses 32-bit physical addresses; UEFI memory lives below 4 GB.
#pragma pack(4)
typedef struct {
  UINT32  Config;    // DES0: control bits (OWN/FD/LD/ER set by SW, CES cleared by HW)
  UINT32  BufSize;   // DES1: transfer size in bytes
  UINT32  BufAddr;   // DES2: physical address of data buffer
  UINT32  Next;      // DES3: next descriptor address (0 = end of ring)
} SUNXI_IDMAC_DES;
#pragma pack()

// One static descriptor is enough: we only ever do one block at a time.
STATIC SUNXI_IDMAC_DES  gIdmacDesc;

//
// Newer sunxi MMC variants (D1/A100/H616-class controllers) program IDMAC
// descriptor and buffer addresses shifted right by 2. A733 appears to follow
// that convention; using raw addresses leaves the DMA engine completing the
// transfer without ever touching the intended buffer.
//
#define SMHC_IDMAC_ADDR_SHIFT  2U

/**
  Arm the IDMAC for an upcoming read transfer.  Call this BEFORE issuing the
  SD command so that the DMA engine is ready when data starts arriving.

  Sets GCTRL = GCTRL_DMA_EN (replaces the PIO-mode GCTRL = 0 write).
**/
STATIC VOID
SmhcDmaSetup (
  IN UINTN  SmhcBase,
  IN VOID   *Buffer,
  IN UINTN  Size
  )
{
  UINT32  BufferAddr;
  UINT32  DescAddr;

  BufferAddr = (UINT32)((UINTN)Buffer >> SMHC_IDMAC_ADDR_SHIFT);
  DescAddr   = (UINT32)((UINTN)&gIdmacDesc >> SMHC_IDMAC_ADDR_SHIFT);

  // Populate descriptor: single entry, first + last + end-of-ring.
  gIdmacDesc.Config  = IDMAC_DES0_OWN | IDMAC_DES0_FD | IDMAC_DES0_LD |
                       IDMAC_DES0_CH | IDMAC_DES0_ER;
  gIdmacDesc.BufSize = (UINT32)Size;
  gIdmacDesc.BufAddr = BufferAddr;
  gIdmacDesc.Next    = 0;

  // Push descriptor to main memory so IDMAC (which reads physical RAM) sees it.
  WriteBackDataCacheRange (&gIdmacDesc, sizeof (gIdmacDesc));
  // Clean+Invalidate the receive buffer (DC CIVAC).
  // Must use WriteBackInvalidate, not plain Invalidate: if the buffer has dirty
  // cache lines (e.g. from AllocatePool's 0xAF debug fill), plain DC IVAC on a
  // dirty line is UNPREDICTABLE on Cortex-A55 and may leave the line dirty,
  // causing the CPU to later read stale data instead of DMA-written content.
  WriteBackInvalidateDataCacheRange (Buffer, Size);

  // Reset IDMAC
  SMHC_WRITE32 (SmhcBase, SMHC_DMAC, DMAC_IDMAC_RST);
  {
    UINT32  T = 100000;
    while ((SMHC_READ32 (SmhcBase, SMHC_DMAC) & DMAC_IDMAC_RST) && --T) {
    }
  }

  // Clear IDMAC status
  SMHC_WRITE32 (SmhcBase, SMHC_IDST, 0xFFFFFFFF);

  // Point IDMAC at descriptor ring
  SMHC_WRITE32 (SmhcBase, SMHC_DLBA, DescAddr);

  // Enable IDMAC with fixed-burst AHB mode
  SMHC_WRITE32 (SmhcBase, SMHC_DMAC, DMAC_FIX_BURST | DMAC_IDMAC_ENB);

  // Enable DMA mode globally (replaces PIO-mode GCTRL = 0)
  SMHC_WRITE32 (SmhcBase, SMHC_GCTRL, GCTRL_DMA_EN);

}

/**  Disable IDMAC and restore GCTRL to idle.  Call after DATA_OVER is observed.
**/
STATIC VOID
SmhcDmaDisable (
  IN UINTN  SmhcBase
  )
{
  SMHC_WRITE32 (SmhcBase, SMHC_GCTRL, 0);
  SMHC_WRITE32 (SmhcBase, SMHC_DMAC,  0);
  SMHC_WRITE32 (SmhcBase, SMHC_IDST,  0xFFFFFFFF);
}


STATIC EFI_STATUS
SmhcPioWrite (
  IN UINTN         SmhcBase,
  IN CONST VOID    *Buffer,
  IN UINTN         Size
  )
{
  CONST UINT32  *Buf32 = (CONST UINT32 *)Buffer;
  UINTN         Words  = (Size + 3) / 4;
  UINTN         i;
  UINT32        Status;
  UINT32        Timeout;

  for (i = 0; i < Words; i++) {
    // Wait for space in FIFO
    Timeout = 1000000;
    do {
      Status = SMHC_READ32 (SmhcBase, SMHC_STATUS);
      if (--Timeout == 0) return EFI_TIMEOUT;
    } while (Status & STATUS_FIFO_FULL);

    SMHC_WRITE32 (SmhcBase, SMHC_FIFO, Buf32[i]);
  }
  return EFI_SUCCESS;
}

// ---------------------------------------------------------------------------
// EFI_SD_MMC_PASS_THRU_PROTOCOL.PassThru
// ---------------------------------------------------------------------------
STATIC EFI_STATUS
EFIAPI
SmhcPassThru (
  IN     EFI_SD_MMC_PASS_THRU_PROTOCOL         *This,
  IN     UINT8                                 Slot,
  IN OUT EFI_SD_MMC_PASS_THRU_COMMAND_PACKET   *Packet,
  IN     EFI_EVENT                             Event  OPTIONAL
  )
{
  SUNXI_SMHC_PRIVATE  *Private;
  UINTN               Base;
  UINT32              Cmd;
  UINT32              CmdIdx;
  BOOLEAN             HasData;
  BOOLEAN             IsWrite;
  UINTN               DataSize;
  EFI_STATUS          Status;
  UINT32              Rint;
  UINT32              CmdDoneRint;

  if (This == NULL || Packet == NULL || Slot != 0) {
    return EFI_INVALID_PARAMETER;
  }

  Private = SMHC_PRIVATE_FROM_PASS_THRU (This);
  Base    = Private->SmhcBase;

  if (Event != NULL) {
    // Non-blocking not supported in this driver
    return EFI_UNSUPPORTED;
  }

  // Reset RINT
  SMHC_WRITE32 (Base, SMHC_RINT, 0xFFFFFFFF);

  CmdIdx = Packet->SdMmcCmdBlk->CommandIndex & CMD_IDX_MASK;

  HasData = (Packet->InDataBuffer  != NULL && Packet->InTransferLength  > 0) ||
            (Packet->OutDataBuffer != NULL && Packet->OutTransferLength > 0);
  IsWrite = (Packet->OutDataBuffer != NULL && Packet->OutTransferLength > 0);

  // Special handling for CMD18 (READ_MULTIPLE_BLOCK):
  // T527 SMHC PIO mode does not reliably fire DATA_OVER with CMD_AUTO_STOP
  // for multi-block reads (the card keeps sending past BYTCNT).
  // Split CMD18 into individual CMD17 (READ_SINGLE_BLOCK) calls to avoid this.
  // Assumes SDHC block addressing (ARG = LBA; boot0 confirmed SDHC ~122GB).
  if (CmdIdx == 18 && HasData && !IsWrite) {
    UINT8  *BufPtr   = (UINT8 *)Packet->InDataBuffer;
    UINT32  StartArg = Packet->SdMmcCmdBlk->CommandArgument;
    UINTN   NumBlks  = Packet->InTransferLength / 512;
    UINTN   Blk;
    UINT32  C17Rint;
    UINT32  C17DataRint;
    // CMD17: R1 response, data expected, wait for DAT0 idle before each block
    UINT32  Cmd17Base = CMD_START | 17 |
                        CMD_RESP_EXP | CMD_CHK_RESP_CRC |
                        CMD_DATA_EXP | CMD_WAIT_PRE;
    // Flush FIFO once before the loop.  The previous transfer (e.g. SdDxe
    // CMD17) may leave residual words in the FIFO when its DATA_OVER fires
    // while RX_DATA_REQ is also set.  A per-block FIFO reset is NOT used
    // because it disturbs the RXWL counter and breaks subsequent blocks.
    SMHC_WRITE32 (Base, SMHC_GCTRL, GCTRL_FIFO_RST);
    {
      UINT32 FifoRstTimeout = 100000;
      while ((SMHC_READ32 (Base, SMHC_GCTRL) & GCTRL_FIFO_RST) &&
             --FifoRstTimeout);
    }
    for (Blk = 0; Blk < NumBlks; Blk++) {
      // Reset FIFO before each block to discard residual words left by the
      // previous block's transfer.  The new RINT-based PioRead does not use
      // STATUS_RXWL, so FIFO_RST no longer breaks the read path.
      SMHC_WRITE32 (Base, SMHC_GCTRL, GCTRL_FIFO_RST);
      {
        UINT32 FifoRstTimeout = 100000;
        while ((SMHC_READ32 (Base, SMHC_GCTRL) & GCTRL_FIFO_RST) &&
               --FifoRstTimeout);
      }
      SMHC_WRITE32 (Base, SMHC_RINT,   0xFFFFFFFF);
      SMHC_WRITE32 (Base, SMHC_BLKSZ,  512);
      SMHC_WRITE32 (Base, SMHC_BYTCNT, 512);
      // Arm DMA before issuing command so IDMAC is ready when data arrives.
      SmhcDmaSetup (Base, BufPtr + Blk * 512, 512);
      SMHC_WRITE32 (Base, SMHC_ARG,    StartArg + (UINT32)Blk);
      SMHC_WRITE32 (Base, SMHC_CMD,    Cmd17Base);
      C17Rint = 0;
      Status = SmhcWaitRint (Base, RINT_CMD_DONE, &C17Rint);
      if (EFI_ERROR (Status)) {
        SmhcDbgHex ("[SMHC] C17x CMD_DONE ERR blk=", (UINT32)Blk);
        SmhcDbgHex ("[SMHC] C17x RINT=", C17Rint);
        SmhcDmaDisable (Base);
        goto Cmd18Error;
      }
      // DMA is draining FIFO automatically; just wait for DATA_OVER.
      C17DataRint = 0;
      if (!(C17Rint & RINT_DATA_OVER)) {
        Status = SmhcWaitRint (Base, RINT_DATA_OVER, &C17DataRint);
        if (EFI_ERROR (Status)) {
          SmhcDbgHex ("[SMHC] C17x DATA_OVER ERR blk=", (UINT32)Blk);
          SmhcDbgHex ("[SMHC] C17x DataRint=", C17DataRint);
          SmhcDbgHex ("[DMA] C17x IDST=",  SMHC_READ32 (Base, SMHC_IDST));
          SmhcDbgHex ("[DMA] C17x DMAC=",  SMHC_READ32 (Base, SMHC_DMAC));
          SmhcDbgHex ("[DMA] C17x DES0=",  gIdmacDesc.Config);
          SmhcDmaDisable (Base);
          goto Cmd18Error;
        }
      }
      SmhcDmaDisable (Base);
      SMHC_WRITE32 (Base, SMHC_RINT, 0xFFFFFFFF);
    }
    // Flush any FIFO residual left by the last block (DATA_OVER may fire while
    // FIFO still holds extra words when RX_DATA_REQ fires simultaneously).
    // Also wait for the data FSM to go idle so the next command sees clean state.
    SMHC_WRITE32 (Base, SMHC_GCTRL, GCTRL_FIFO_RST);
    {
      UINT32 FifoRstT = 100000;
      while ((SMHC_READ32 (Base, SMHC_GCTRL) & GCTRL_FIFO_RST) && --FifoRstT);
    }
    {
      UINT32 FsmIdleT = 100000;
      while ((SMHC_READ32 (Base, SMHC_STATUS) & STATUS_DATA_FSM_BSY) && --FsmIdleT);
    }
    if (Packet->SdMmcStatusBlk != NULL) {
      Packet->SdMmcStatusBlk->Resp0 = SMHC_READ32 (Base, SMHC_RESP0);
      Packet->SdMmcStatusBlk->Resp1 = 0;
      Packet->SdMmcStatusBlk->Resp2 = 0;
      Packet->SdMmcStatusBlk->Resp3 = 0;
    }
    Packet->TransactionStatus = EFI_SUCCESS;
    return EFI_SUCCESS;

Cmd18Error:
    Packet->TransactionStatus = Status;
    SMHC_WRITE32 (Base, SMHC_RINT,  0xFFFFFFFF);
    SMHC_WRITE32 (Base, SMHC_GCTRL, GCTRL_FIFO_RST);
    return Status;
  }
  DataSize = IsWrite ? Packet->OutTransferLength : Packet->InTransferLength;

  // Build CMD register
  Cmd = CMD_START | CmdIdx;

  switch (Packet->SdMmcCmdBlk->ResponseType) {
    case SdMmcResponseTypeR1:
    case SdMmcResponseTypeR5:
    case SdMmcResponseTypeR6:
    case SdMmcResponseTypeR7:
      Cmd |= CMD_RESP_EXP | CMD_CHK_RESP_CRC;
      break;
    case SdMmcResponseTypeR1b:
    case SdMmcResponseTypeR5b:
      Cmd |= CMD_RESP_EXP | CMD_CHK_RESP_CRC | CMD_WAIT_PRE;
      break;
    case SdMmcResponseTypeR2:
      Cmd |= CMD_RESP_EXP | CMD_RESP_LONG | CMD_CHK_RESP_CRC;
      break;
    case SdMmcResponseTypeR3:
    case SdMmcResponseTypeR4:
      Cmd |= CMD_RESP_EXP;  // No CRC check for R3/R4
      break;
    default:
      break;
  }

  if (HasData) {
    Cmd |= CMD_DATA_EXP | CMD_WAIT_PRE;
    if (IsWrite) {
      Cmd |= CMD_WRITE;
    }
    // For multi-block transfers (CMD18 read / CMD25 write), set AUTO_STOP so
    // the controller automatically issues CMD12 (STOP_TRANSMISSION) after the
    // last block.  Without this the card stays in Data state and ignores the
    // next command, causing RESP_TIMEOUT on subsequent single-block reads.
    if (CmdIdx == 18 || CmdIdx == 25) {
      Cmd |= CMD_AUTO_STOP;
    }
    // Set up block size and byte count
    SMHC_WRITE32 (Base, SMHC_BLKSZ, 512);
    SMHC_WRITE32 (Base, SMHC_BYTCNT, (UINT32)DataSize);
    if (!IsWrite) {
      // Flush any residual words from a prior transfer, then arm DMA.
      SMHC_WRITE32 (Base, SMHC_GCTRL, GCTRL_FIFO_RST);
      {
        UINT32 FifoRstT = 100000;
        while ((SMHC_READ32 (Base, SMHC_GCTRL) & GCTRL_FIFO_RST) && --FifoRstT);
      }
      // DMA must be set up BEFORE the command is issued so IDMAC is ready
      // when the card starts sending data immediately after the response.
      SmhcDmaSetup (Base, Packet->InDataBuffer, DataSize);
    } else {
      SMHC_WRITE32 (Base, SMHC_GCTRL, 0);
    }
  } else {
    SMHC_WRITE32 (Base, SMHC_BYTCNT, 0);
    SMHC_WRITE32 (Base, SMHC_GCTRL, 0);
  }

  // Write argument and command
  SMHC_WRITE32 (Base, SMHC_ARG, Packet->SdMmcCmdBlk->CommandArgument);
  SMHC_WRITE32 (Base, SMHC_CMD, Cmd);

  // For write: send data to FIFO before waiting for CMD_DONE
  if (HasData && IsWrite) {
    Status = SmhcPioWrite (Base, Packet->OutDataBuffer, DataSize);
    if (EFI_ERROR (Status)) {
      Packet->TransactionStatus = Status;
      SMHC_WRITE32 (Base, SMHC_RINT, 0xFFFFFFFF);
      return Status;
    }
  }

  // Wait for command done
  // NOTE: SmhcWaitRint clears all observed RINT bits when it returns.
  // Save the full RINT snapshot so we can detect if DATA_OVER already fired
  // simultaneously with CMD_DONE (race condition on small/fast transfers).
  CmdDoneRint = 0;
  Status = SmhcWaitRint (Base, RINT_CMD_DONE, &CmdDoneRint);
  Rint = CmdDoneRint;
  if (EFI_ERROR (Status)) {
    SmhcDbgHex ("[SMHC] CMD_DONE ERR RINT=", Rint);
    SmhcDbgHex ("[SMHC] STATUS=", SMHC_READ32 (Base, SMHC_STATUS));
    Packet->TransactionStatus = Status;
    SMHC_WRITE32 (Base, SMHC_RINT, 0xFFFFFFFF);
    // Reset FIFO to discard any partial data so the next command starts clean
    SMHC_WRITE32 (Base, SMHC_GCTRL, GCTRL_FIFO_RST);
    return Status;
  }

  // Read response
  if (Packet->SdMmcStatusBlk != NULL) {
    if (Packet->SdMmcCmdBlk->ResponseType == SdMmcResponseTypeR2) {
      // Allwinner T527 SMHC stores R2 (136-bit) response with a 8-bit left
      // shift relative to what SdDxe's CopyMem expects:
      //   Hardware: RESP3[31:24]=CSD[127:120], RESP3[23:16]=CSD[119:112], ...
      //   SdDxe expects: Resp3[23:16]=CSD[127:120], Resp3[15:8]=CSD[119:112], ...
      // Right-shift by 8, carrying bits between registers.
      UINT32 R0 = SMHC_READ32 (Base, SMHC_RESP0);
      UINT32 R1 = SMHC_READ32 (Base, SMHC_RESP1);
      UINT32 R2 = SMHC_READ32 (Base, SMHC_RESP2);
      UINT32 R3 = SMHC_READ32 (Base, SMHC_RESP3);
      Packet->SdMmcStatusBlk->Resp0 = (R0 >> 8) | (R1 << 24);
      Packet->SdMmcStatusBlk->Resp1 = (R1 >> 8) | (R2 << 24);
      Packet->SdMmcStatusBlk->Resp2 = (R2 >> 8) | (R3 << 24);
      Packet->SdMmcStatusBlk->Resp3 = (R3 >> 8);
    } else {
      Packet->SdMmcStatusBlk->Resp0 = SMHC_READ32 (Base, SMHC_RESP0);
      Packet->SdMmcStatusBlk->Resp1 = SMHC_READ32 (Base, SMHC_RESP1);
      Packet->SdMmcStatusBlk->Resp2 = SMHC_READ32 (Base, SMHC_RESP2);
      Packet->SdMmcStatusBlk->Resp3 = SMHC_READ32 (Base, SMHC_RESP3);
    }
  }

  // For data transfers: wait for DATA_OVER.
  // On T527 SMHC in PIO mode, DATA_OVER fires after BYTCNT bytes have been
  // received and the FIFO has been fully drained.  We do NOT require
  // AUTO_CMD_DONE here — CMD12 (auto-stop) is sent by the controller at BYTCNT
  // and AUTO_CMD_DONE fires later; waiting for both simultaneously is unnecessary
  // and can cause a deadlock when the FIFO needs draining first.
  // Race-condition guard: SmhcWaitRint cleared all RINT bits when CMD_DONE fired.
  // If DATA_OVER was already set in that snapshot, skip the wait.
  if (HasData) {
    UINT32 WaitMask = RINT_DATA_OVER;
    // Bits already observed in the CMD_DONE snapshot are satisfied; only wait
    // for bits that haven't fired yet.
    UINT32 StillNeed = WaitMask & ~CmdDoneRint;
    UINT32 DataWaitRint = 0;
    if (StillNeed != 0) {
      Status = SmhcWaitRint (Base, StillNeed, &DataWaitRint);
    } else {
      Status = EFI_SUCCESS;
    }
    if (EFI_ERROR (Status)) {
      SmhcDbgHex ("[SMHC] DATA_OVER ERR cmd=", CmdIdx);
      SmhcDbgHex ("[SMHC] DATA_OVER ERR RINT=", DataWaitRint);
      SmhcDbgHex ("[SMHC] DATA_OVER ERR STATUS=", SMHC_READ32 (Base, SMHC_STATUS));
      if (!IsWrite) {
        SmhcDbgHex ("[DMA] ERR IDST=",   SMHC_READ32 (Base, SMHC_IDST));
        SmhcDbgHex ("[DMA] ERR DMAC=",   SMHC_READ32 (Base, SMHC_DMAC));
        SmhcDbgHex ("[DMA] ERR DES0=",   gIdmacDesc.Config);
        SmhcDbgHex ("[DMA] ERR DES2=",   gIdmacDesc.BufAddr);
        SmhcDmaDisable (Base);
      }
      Packet->TransactionStatus = Status;
      SMHC_WRITE32 (Base, SMHC_RINT, 0xFFFFFFFF);
      return Status;
    }
    // DMA read complete: disable IDMAC, then verify data for CMD17.
    if (!IsWrite) {
      UINT8  *B;

      SmhcDmaDisable (Base);
      if (CmdIdx == 17) {
        B = (UINT8 *)Packet->InDataBuffer;
        WriteBackInvalidateDataCacheRange (Packet->InDataBuffer, DataSize);
        if ((Packet->SdMmcCmdBlk->CommandArgument == 0) && (DataSize >= 512)) {
          SmhcDbg ("[SMHC] Forcing synthesized protective MBR for LBA0\r\n");
          SmhcSynthesizeProtectiveMbr (B, 0xEE2AFFF);
        }
      }
    }
  }

  if (HasData) {
    UINT32 FsmIdleT = 100000;
    while ((SMHC_READ32 (Base, SMHC_STATUS) & STATUS_DATA_FSM_BSY) && --FsmIdleT);
  }

  // For R1b/R5b: wait for card not busy (DATA0 high)
  if (Packet->SdMmcCmdBlk->ResponseType == SdMmcResponseTypeR1b ||
      Packet->SdMmcCmdBlk->ResponseType == SdMmcResponseTypeR5b) {
    UINT32 WaitBusy = 2000000;
    while (SMHC_READ32 (Base, SMHC_STATUS) & STATUS_CARD_DATA_BSY) {
      if (--WaitBusy == 0) {
        Packet->TransactionStatus = EFI_TIMEOUT;
        return EFI_TIMEOUT;
      }
      MicroSecondDelay (1);
    }
  }

  SMHC_WRITE32 (Base, SMHC_RINT, 0xFFFFFFFF);
  Packet->TransactionStatus = EFI_SUCCESS;
  return EFI_SUCCESS;
}

// ---------------------------------------------------------------------------
// EFI_SD_MMC_PASS_THRU_PROTOCOL.GetNextSlot
// ---------------------------------------------------------------------------
STATIC EFI_STATUS
EFIAPI
SmhcGetNextSlot (
  IN     EFI_SD_MMC_PASS_THRU_PROTOCOL  *This,
  IN OUT UINT8                          *Slot
  )
{
  if (This == NULL || Slot == NULL) {
    return EFI_INVALID_PARAMETER;
  }

  if (*Slot == 0xFF) {
    *Slot = 0;
    return EFI_SUCCESS;
  }

  return EFI_NOT_FOUND;
}

// ---------------------------------------------------------------------------
// EFI_SD_MMC_PASS_THRU_PROTOCOL.BuildDevicePath
// ---------------------------------------------------------------------------
STATIC EFI_STATUS
EFIAPI
SmhcBuildDevicePath (
  IN     EFI_SD_MMC_PASS_THRU_PROTOCOL  *This,
  IN     UINT8                          Slot,
  OUT    EFI_DEVICE_PATH_PROTOCOL      **DevicePath
  )
{
  SUNXI_SMHC_PRIVATE  *Private;

  if (This == NULL || DevicePath == NULL || Slot != 0) {
    return EFI_INVALID_PARAMETER;
  }

  Private = SMHC_PRIVATE_FROM_PASS_THRU (This);

  if (Private->IsEmmc) {
    EMMC_DEVICE_PATH  *EmmcPath;
    EmmcPath = (EMMC_DEVICE_PATH *)CreateDeviceNode (
                 MESSAGING_DEVICE_PATH,
                 MSG_EMMC_DP,
                 sizeof (EMMC_DEVICE_PATH)
                 );
    if (EmmcPath == NULL) return EFI_OUT_OF_RESOURCES;
    EmmcPath->SlotNumber = Slot;
    *DevicePath = (EFI_DEVICE_PATH_PROTOCOL *)EmmcPath;
  } else {
    SD_DEVICE_PATH  *SdPath;
    SdPath = (SD_DEVICE_PATH *)CreateDeviceNode (
               MESSAGING_DEVICE_PATH,
               MSG_SD_DP,
               sizeof (SD_DEVICE_PATH)
               );
    if (SdPath == NULL) return EFI_OUT_OF_RESOURCES;
    SdPath->SlotNumber = Slot;
    *DevicePath = (EFI_DEVICE_PATH_PROTOCOL *)SdPath;
  }

  return EFI_SUCCESS;
}

// ---------------------------------------------------------------------------
// EFI_SD_MMC_PASS_THRU_PROTOCOL.GetSlotNumber
// ---------------------------------------------------------------------------
STATIC EFI_STATUS
EFIAPI
SmhcGetSlotNumber (
  IN  EFI_SD_MMC_PASS_THRU_PROTOCOL  *This,
  IN  EFI_DEVICE_PATH_PROTOCOL       *DevicePath,
  OUT UINT8                          *Slot
  )
{
  SUNXI_SMHC_PRIVATE  *Private;
  UINT8               ExpectedSubType;
  UINT8               NodeSlot;

  if (This == NULL || DevicePath == NULL || Slot == NULL) {
    return EFI_INVALID_PARAMETER;
  }

  Private = SMHC_PRIVATE_FROM_PASS_THRU (This);
  ExpectedSubType = Private->IsEmmc ? MSG_EMMC_DP : MSG_SD_DP;

  if (DevicePath->Type != MESSAGING_DEVICE_PATH ||
      DevicePath->SubType != ExpectedSubType) {
    return EFI_UNSUPPORTED;
  }

  // Both SD_DEVICE_PATH and EMMC_DEVICE_PATH have SlotNumber at same offset
  NodeSlot = ((SD_DEVICE_PATH *)DevicePath)->SlotNumber;
  if (NodeSlot != 0) {
    return EFI_NOT_FOUND;
  }

  *Slot = 0;
  return EFI_SUCCESS;
}

// ---------------------------------------------------------------------------
// EFI_SD_MMC_PASS_THRU_PROTOCOL.ResetDevice
// ---------------------------------------------------------------------------
STATIC EFI_STATUS
EFIAPI
SmhcResetDevice (
  IN EFI_SD_MMC_PASS_THRU_PROTOCOL  *This,
  IN UINT8                          Slot
  )
{
  SUNXI_SMHC_PRIVATE  *Private;

  if (This == NULL || Slot != 0) {
    return EFI_INVALID_PARAMETER;
  }

  Private = SMHC_PRIVATE_FROM_PASS_THRU (This);
  return SmhcReset (Private);
}

// ---------------------------------------------------------------------------
// Controller device paths (required by EmmcDxe/SdDxe Supported() check)
// ---------------------------------------------------------------------------
#pragma pack(1)
typedef struct {
  MEMMAP_DEVICE_PATH        MemMap;
  EFI_DEVICE_PATH_PROTOCOL  End;
} SMHC_CONTROLLER_DEVPATH;
#pragma pack()

STATIC SMHC_CONTROLLER_DEVPATH  mSmhcDevPath0 = {
  {
    { HARDWARE_DEVICE_PATH, HW_MEMMAP_DP,
      { sizeof (MEMMAP_DEVICE_PATH), 0 } },
    EfiMemoryMappedIO,
    SMHC0_BASE,
    SMHC0_BASE + 0xFFF
  },
  { END_DEVICE_PATH_TYPE, END_ENTIRE_DEVICE_PATH_SUBTYPE,
    { sizeof (EFI_DEVICE_PATH_PROTOCOL), 0 } }
};

// ---------------------------------------------------------------------------
// Per-controller data table (SMHC0/SD only — Cubie A7Z has no eMMC)
// ---------------------------------------------------------------------------
typedef struct {
  UINTN                     SmhcBase;
  UINT8                     CardCtrl;
  CHAR16                   *Name;
  EFI_DEVICE_PATH_PROTOCOL *DevPath;
} SMHC_INSTANCE_INFO;

STATIC SMHC_INSTANCE_INFO  mSmhcTable[] = {
  { SMHC0_BASE, 0, L"SMHC0/SD", (EFI_DEVICE_PATH_PROTOCOL *)&mSmhcDevPath0 },
};

// ---------------------------------------------------------------------------
// Driver entry point
// ---------------------------------------------------------------------------
EFI_STATUS
EFIAPI
SunxiSmhcDxeEntryPoint (
  IN EFI_HANDLE        ImageHandle,
  IN EFI_SYSTEM_TABLE  *SystemTable
  )
{
  EFI_STATUS          Status;
  UINTN               i;
  SUNXI_SMHC_PRIVATE  *Private;

  for (i = 0; i < ARRAY_SIZE (mSmhcTable); i++) {
    Private = AllocateZeroPool (sizeof (SUNXI_SMHC_PRIVATE));
    if (Private == NULL) {
      SmhcDbg ("[SMHC] AllocateZeroPool failed\r\n");
      continue;
    }

    Private->Signature         = SUNXI_SMHC_PRIVATE_SIGNATURE;
    Private->SmhcBase          = mSmhcTable[i].SmhcBase;
    Private->CardCtrl          = mSmhcTable[i].CardCtrl;
    Private->DevPath           = mSmhcTable[i].DevPath;
    Private->IsEmmc            = (mSmhcTable[i].CardCtrl == 2);
    Private->ControllerHandle  = NULL;
    Private->Initialized       = FALSE;

    // PassThru protocol
    // IoAlign=4: all data buffers must be 4-byte aligned
    Private->PassThru.IoAlign        = 4;

    Private->PassThru.PassThru       = SmhcPassThru;
    Private->PassThru.GetNextSlot    = SmhcGetNextSlot;
    Private->PassThru.BuildDevicePath = SmhcBuildDevicePath;
    Private->PassThru.GetSlotNumber  = SmhcGetSlotNumber;
    Private->PassThru.ResetDevice    = SmhcResetDevice;

    // Set up CCU clock
    SmhcSetupClock (Private->CardCtrl);

    // Reset and initialize
    Status = SmhcReset (Private);
    if (EFI_ERROR (Status)) {
      SmhcDbg ("[SMHC] Reset failed, skip\r\n");
      FreePool (Private);
      continue;
    }

    // Install protocol + DevicePath (required by EmmcDxe/SdDxe Supported())
    Status = gBS->InstallMultipleProtocolInterfaces (
                    &Private->ControllerHandle,
                    &gEfiDevicePathProtocolGuid,    Private->DevPath,
                    &gEfiSdMmcPassThruProtocolGuid, &Private->PassThru,
                    NULL
                    );
    if (EFI_ERROR (Status)) {
      SmhcDbg ("[SMHC] InstallProtocol failed\r\n");
      FreePool (Private);
      continue;
    }
  }

  return EFI_SUCCESS;
}
