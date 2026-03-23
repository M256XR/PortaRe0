/** @file
  Minimal PlatformBootManagerLib for A733 - boots directly to UEFI Shell in FV.

  Copyright (c) 2026, PortaRe0 Project. All rights reserved.
  SPDX-License-Identifier: BSD-2-Clause-Patent
**/

#include <Library/BaseLib.h>
#include <Library/BaseMemoryLib.h>
#include <Library/DebugLib.h>
#include <Library/DevicePathLib.h>
#include <Library/MemoryAllocationLib.h>
#include <Library/PrintLib.h>
#include <Library/PcdLib.h>
#include <Library/UefiBootManagerLib.h>
#include <Library/UefiBootServicesTableLib.h>
#include <Library/UefiLib.h>
#include <Protocol/BlockIo.h>
#include <Protocol/DevicePath.h>
#include <Protocol/FirmwareVolume2.h>
#include <Protocol/SimpleFileSystem.h>
#include <Guid/SerialPortLibVendor.h>
#include <Guid/PcAnsi.h>

#define DP_NODE_LEN(Type)  { (UINT8)sizeof (Type), (UINT8)(sizeof (Type) >> 8) }

#pragma pack (1)
typedef struct {
  VENDOR_DEVICE_PATH            SerialDxe;
  UART_DEVICE_PATH              Uart;
  VENDOR_DEFINED_DEVICE_PATH    TermType;
  EFI_DEVICE_PATH_PROTOCOL      End;
} A733_SERIAL_CONSOLE_DEVPATH;
#pragma pack ()

STATIC A733_SERIAL_CONSOLE_DEVPATH  mSerialConsole = {
  //
  // VenHw(EDKII_SERIAL_PORT_LIB_VENDOR_GUID) - matches SerialDxe handle
  //
  {
    { HARDWARE_DEVICE_PATH, HW_VENDOR_DP, DP_NODE_LEN (VENDOR_DEVICE_PATH) },
    EDKII_SERIAL_PORT_LIB_VENDOR_GUID
  },

  //
  // UART messaging node - use PCD defaults (SerialDxe was configured with these)
  //
  {
    { MESSAGING_DEVICE_PATH, MSG_UART_DP, DP_NODE_LEN (UART_DEVICE_PATH) },
    0,                                       // Reserved
    FixedPcdGet64 (PcdUartDefaultBaudRate),  // BaudRate
    FixedPcdGet8  (PcdUartDefaultDataBits),  // DataBits
    FixedPcdGet8  (PcdUartDefaultParity),    // Parity
    FixedPcdGet8  (PcdUartDefaultStopBits)   // StopBits
  },

  //
  // Terminal type vendor node - GUID filled in at runtime
  //
  {
    { MESSAGING_DEVICE_PATH, MSG_VENDOR_DP, DP_NODE_LEN (VENDOR_DEFINED_DEVICE_PATH) }
    // Guid filled in BeforeConsole
  },

  //
  // End node
  //
  {
    END_DEVICE_PATH_TYPE, END_ENTIRE_DEVICE_PATH_SUBTYPE,
    DP_NODE_LEN (EFI_DEVICE_PATH_PROTOCOL)
  }
};

// Shell application GUID (ShellPkg/Application/Shell/Shell.inf)
STATIC EFI_GUID  mShellFileGuid = {
  0x7C04A583, 0x9E3E, 0x4F1C,
  { 0xAD, 0x65, 0xE0, 0x52, 0x68, 0xD0, 0xB4, 0xD1 }
};

STATIC CONST CHAR16  mRemovableBootPath[] = L"\\EFI\\BOOT\\BOOTAA64.EFI";

#if 0
STATIC
VOID
DumpBlockIoProbe (
  IN EFI_BLOCK_IO_PROTOCOL  *BlockIo,
  IN UINT32                 HandleIndex
  )
{
  STATIC CONST EFI_LBA  mProbeLbas[] = { 0, 1, 2, 256 };
  EFI_STATUS            Status;
  UINTN                 Index;
  UINT8                 *Buffer;
  UINT32                Head;
  UINT32                Tail;
  UINT32                MbrEntryStart;
  UINT32                MbrEntryType;
  UINT32                GptSigLow;
  UINT32                GptSigHigh;
  UINT32                StoredHeaderCrc;
  UINT32                CalculatedHeaderCrc;
  UINT32                HeaderSize;
  UINT32                EntryCount;
  UINT32                EntrySize;
  UINT32                EntryArrayCrc;
  UINT64                MyLba;
  UINT64                AlternateLba;
  UINT64                EntryLba;
  EFI_STATUS            CrcStatus;
  UINT8                 SavedCrc[4];

  if ((BlockIo == NULL) || (BlockIo->Media == NULL)) {
    return;
  }

  DEBUG ((
    DEBUG_INFO,
    "[A733] BLK%d: BlockSize=%d LastBlock=0x%lx Logical=%d Present=%d\n",
    (INT32)HandleIndex,
    (INT32)BlockIo->Media->BlockSize,
    (UINT64)BlockIo->Media->LastBlock,
    (INT32)BlockIo->Media->LogicalPartition,
    (INT32)BlockIo->Media->MediaPresent
    ));

  if (!BlockIo->Media->MediaPresent || (BlockIo->Media->BlockSize < 512)) {
    return;
  }

  Buffer = AllocateZeroPool (BlockIo->Media->BlockSize);
  if (Buffer == NULL) {
    DEBUG ((DEBUG_ERROR, "[A733] BLK%d: AllocateZeroPool failed\n", (INT32)HandleIndex));
    return;
  }

  for (Index = 0; Index < ARRAY_SIZE (mProbeLbas); Index++) {
    if (mProbeLbas[Index] > BlockIo->Media->LastBlock) {
      continue;
    }

    SetMem (Buffer, BlockIo->Media->BlockSize, 0xA5);
    Status = BlockIo->ReadBlocks (
                        BlockIo,
                        BlockIo->Media->MediaId,
                        mProbeLbas[Index],
                        BlockIo->Media->BlockSize,
                        Buffer
                        );
    if (EFI_ERROR (Status)) {
      DEBUG ((
        DEBUG_ERROR,
        "[A733] BLK%d LBA=0x%lx ReadBlocks failed: %r\n",
        (INT32)HandleIndex,
        (UINT64)mProbeLbas[Index],
        Status
        ));
      continue;
    }

    Head = ((UINT32)Buffer[3] << 24) | ((UINT32)Buffer[2] << 16) |
           ((UINT32)Buffer[1] << 8)  | (UINT32)Buffer[0];
    Tail = ((UINT32)Buffer[511] << 8) | (UINT32)Buffer[510];
    DEBUG ((
      DEBUG_INFO,
      "[A733] BLK%d LBA=0x%lx head=0x%08x tail=0x%04x\n",
      (INT32)HandleIndex,
      (UINT64)mProbeLbas[Index],
      Head,
      Tail
      ));

    if (mProbeLbas[Index] == 0) {
      MbrEntryStart = ((UINT32)Buffer[449] << 24) | ((UINT32)Buffer[448] << 16) |
                      ((UINT32)Buffer[447] << 8)  | (UINT32)Buffer[446];
      MbrEntryType  = ((UINT32)Buffer[461] << 24) | ((UINT32)Buffer[460] << 16) |
                      ((UINT32)Buffer[459] << 8)  | (UINT32)Buffer[458];
      DEBUG ((
        DEBUG_INFO,
        "[A733] BLK%d LBA0 MBR[446..449]=0x%08x MBR[458..461]=0x%08x Sig=0x%02x%02x\n",
        (INT32)HandleIndex,
        MbrEntryStart,
        MbrEntryType,
        Buffer[511],
        Buffer[510]
        ));
    } else if (mProbeLbas[Index] == 1) {
      GptSigLow  = ((UINT32)Buffer[3] << 24) | ((UINT32)Buffer[2] << 16) |
                   ((UINT32)Buffer[1] << 8)  | (UINT32)Buffer[0];
      GptSigHigh = ((UINT32)Buffer[7] << 24) | ((UINT32)Buffer[6] << 16) |
                   ((UINT32)Buffer[5] << 8)  | (UINT32)Buffer[4];
      HeaderSize = ReadUnaligned32 ((CONST UINT32 *)&Buffer[12]);
      StoredHeaderCrc = ReadUnaligned32 ((CONST UINT32 *)&Buffer[16]);
      MyLba = ReadUnaligned64 ((CONST UINT64 *)&Buffer[24]);
      AlternateLba = ReadUnaligned64 ((CONST UINT64 *)&Buffer[32]);
      EntryLba = ReadUnaligned64 ((CONST UINT64 *)&Buffer[72]);
      EntryCount = ReadUnaligned32 ((CONST UINT32 *)&Buffer[80]);
      EntrySize = ReadUnaligned32 ((CONST UINT32 *)&Buffer[84]);
      EntryArrayCrc = ReadUnaligned32 ((CONST UINT32 *)&Buffer[88]);
      CopyMem (SavedCrc, &Buffer[16], sizeof (SavedCrc));
      ZeroMem (&Buffer[16], sizeof (SavedCrc));
      CalculatedHeaderCrc = 0;
      CrcStatus = gBS->CalculateCrc32 (
                         Buffer,
                         MIN (HeaderSize, (UINT32)BlockIo->Media->BlockSize),
                         &CalculatedHeaderCrc
                         );
      CopyMem (&Buffer[16], SavedCrc, sizeof (SavedCrc));
      DEBUG ((
        DEBUG_INFO,
        "[A733] BLK%d LBA1 GPTSIG=0x%08x 0x%08x Rev=0x%02x%02x%02x%02x\n",
        (INT32)HandleIndex,
        GptSigLow,
        GptSigHigh,
        Buffer[11],
        Buffer[10],
        Buffer[9],
        Buffer[8]
        ));
      DEBUG ((
        DEBUG_INFO,
        "[A733] BLK%d LBA1 HdrSize=%d StoredCrc=0x%08x CalcCrc=0x%08x CrcStatus=%r\n",
        (INT32)HandleIndex,
        HeaderSize,
        StoredHeaderCrc,
        CalculatedHeaderCrc,
        CrcStatus
        ));
      DEBUG ((
        DEBUG_INFO,
        "[A733] BLK%d LBA1 MyLba=0x%lx AltLba=0x%lx EntryLba=0x%lx EntCnt=%d EntSize=%d EntCrc=0x%08x\n",
        (INT32)HandleIndex,
        MyLba,
        AlternateLba,
        EntryLba,
        EntryCount,
        EntrySize,
        EntryArrayCrc
        ));
    }
  }

  FreePool (Buffer);
}

STATIC
VOID
DumpAllBlockIoProbes (
  VOID
  )
{
  EFI_STATUS             Status;
  EFI_HANDLE             *Handles;
  EFI_BLOCK_IO_PROTOCOL  *BlockIo;
  UINTN                  HandleCount;
  UINTN                  Index;

  Status = gBS->LocateHandleBuffer (
                  ByProtocol,
                  &gEfiBlockIoProtocolGuid,
                  NULL,
                  &HandleCount,
                  &Handles
                  );
  if (EFI_ERROR (Status)) {
    DEBUG ((DEBUG_ERROR, "[A733] LocateHandleBuffer(BlockIo) failed: %r\n", Status));
    return;
  }

  DEBUG ((DEBUG_INFO, "[A733] BlockIo handles: %d\n", (INT32)HandleCount));
  for (Index = 0; Index < HandleCount; Index++) {
    Status = gBS->HandleProtocol (
                    Handles[Index],
                    &gEfiBlockIoProtocolGuid,
                    (VOID **)&BlockIo
                    );
    if (EFI_ERROR (Status)) {
      DEBUG ((DEBUG_ERROR, "[A733] BLK%d HandleProtocol failed: %r\n", (INT32)Index, Status));
      continue;
    }

    DumpBlockIoProbe (BlockIo, (UINT32)Index);
  }

  FreePool (Handles);
}
#endif

/**
  Build an FV-based device path for a file in the FV that contains the
  currently running image.

  @param  FileGuid   GUID of the file inside the FV.
  @return Allocated device path, or NULL on failure.
**/
STATIC
EFI_DEVICE_PATH_PROTOCOL *
BuildFvFilePath (
  IN EFI_GUID  *FileGuid
  )
{
  EFI_STATUS                         Status;
  UINTN                              HandleCount;
  EFI_HANDLE                         *Handles;
  EFI_HANDLE                         FvHandle;
  EFI_FIRMWARE_VOLUME2_PROTOCOL      *Fv;
  EFI_FV_FILETYPE                    FileType;
  EFI_FV_FILE_ATTRIBUTES             Attributes;
  UINTN                              Size;
  UINT32                             AuthStatus;
  UINTN                              Index;
  MEDIA_FW_VOL_FILEPATH_DEVICE_PATH  FileNode;
  EFI_DEVICE_PATH_PROTOCOL           *FvDevPath;
  EFI_DEVICE_PATH_PROTOCOL           *FilePath;

  Status = gBS->LocateHandleBuffer (
                  ByProtocol,
                  &gEfiFirmwareVolume2ProtocolGuid,
                  NULL,
                  &HandleCount,
                  &Handles
                  );
  if (EFI_ERROR (Status)) {
    return NULL;
  }

  FilePath = NULL;
  for (Index = 0; Index < HandleCount; Index++) {
    Status = gBS->HandleProtocol (
                    Handles[Index],
                    &gEfiFirmwareVolume2ProtocolGuid,
                    (VOID **)&Fv
                    );
    if (EFI_ERROR (Status)) {
      continue;
    }

    Status = Fv->ReadFile (
                   Fv,
                   FileGuid,
                   NULL,
                   &Size,
                   &FileType,
                   &Attributes,
                   &AuthStatus
                   );
    if (!EFI_ERROR (Status)) {
      FvHandle = Handles[Index];
      FvDevPath = DevicePathFromHandle (FvHandle);

      EfiInitializeFwVolDevicepathNode (&FileNode, FileGuid);
      FilePath = AppendDevicePathNode (FvDevPath, (EFI_DEVICE_PATH_PROTOCOL *)&FileNode);
      break;
    }
  }

  FreePool (Handles);
  return FilePath;
}

STATIC
BOOLEAN
BootDevicePathOnce (
  IN CHAR16                    *Description,
  IN EFI_DEVICE_PATH_PROTOCOL  *DevicePath
  )
{
  EFI_STATUS                    Status;
  EFI_BOOT_MANAGER_LOAD_OPTION  BootOption;
  EFI_STATUS                    BootStatus;

  if (DevicePath == NULL) {
    return FALSE;
  }

  Status = EfiBootManagerInitializeLoadOption (
             &BootOption,
             LoadOptionNumberUnassigned,
             LoadOptionTypeBoot,
             LOAD_OPTION_ACTIVE,
             Description,
             DevicePath,
             NULL,
             0
             );
  if (EFI_ERROR (Status)) {
    DEBUG ((DEBUG_ERROR, "[A733] Failed to init boot option: %r\n", Status));
    return FALSE;
  }

  DEBUG ((DEBUG_ERROR, "[A733] Booting option\n"));
  EfiBootManagerBoot (&BootOption);
  BootStatus = BootOption.Status;
  EfiBootManagerFreeLoadOption (&BootOption);

  if (EFI_ERROR (BootStatus)) {
    DEBUG ((DEBUG_ERROR, "[A733] Boot result: %r\n", BootStatus));
  } else {
    DEBUG ((DEBUG_ERROR, "[A733] Boot result: EFI_SUCCESS\n"));
  }
  return !EFI_ERROR (BootStatus);
}

STATIC
BOOLEAN
TryBootRemovableMediaPath (
  IN CHAR16  *RelativePath
  )
{
  EFI_STATUS                Status;
  EFI_HANDLE                *Handles;
  EFI_DEVICE_PATH_PROTOCOL  *FilePath;
  UINTN                     HandleCount;
  UINTN                     Index;
  BOOLEAN                   Booted;

  Status = gBS->LocateHandleBuffer (
                  ByProtocol,
                  &gEfiSimpleFileSystemProtocolGuid,
                  NULL,
                  &HandleCount,
                  &Handles
                  );
  if (EFI_ERROR (Status)) {
    DEBUG ((DEBUG_ERROR, "[A733] LocateHandleBuffer(SimpleFileSystem) failed: %r\n", Status));
    return FALSE;
  }

  Booted = FALSE;
  for (Index = 0; Index < HandleCount; Index++) {
    FilePath = FileDevicePath (Handles[Index], RelativePath);
    if (FilePath == NULL) {
      continue;
    }

    DEBUG ((DEBUG_ERROR, "[A733] Trying fs candidate %u\n", (UINT32)Index));
    Booted = BootDevicePathOnce (L"Removable Media Boot", FilePath);
    FreePool (FilePath);
    if (Booted) {
      break;
    }
  }

  FreePool (Handles);
  return Booted;
}

VOID
EFIAPI
PlatformBootManagerBeforeConsole (
  VOID
  )
{
  //
  // Use VT100 terminal type (TeraTerm default).
  // PcdDefaultTerminalType index 1 = VT100.
  //
  CopyGuid (&mSerialConsole.TermType.Guid, &gEfiVT100Guid);

  DEBUG ((DEBUG_INFO, "[A733] PlatformBootManagerBeforeConsole: registering serial console\n"));

  EfiBootManagerUpdateConsoleVariable (ConIn,  (EFI_DEVICE_PATH_PROTOCOL *)&mSerialConsole, NULL);
  EfiBootManagerUpdateConsoleVariable (ConOut, (EFI_DEVICE_PATH_PROTOCOL *)&mSerialConsole, NULL);
  EfiBootManagerUpdateConsoleVariable (ErrOut, (EFI_DEVICE_PATH_PROTOCOL *)&mSerialConsole, NULL);
}

VOID
EFIAPI
PlatformBootManagerAfterConsole (
  VOID
  )
{
  EFI_DEVICE_PATH_PROTOCOL      *ShellPath;

  DEBUG ((DEBUG_INFO, "[A733] PlatformBootManagerAfterConsole\n"));

  // Connect all drivers so storage / console devices are available.
  EfiBootManagerConnectAll ();

  // Second ConnectAll: SdDxe installs BlockIo during the first ConnectAll,
  // but ConnectAll may have already scanned that handle. A second pass lets
  // DiskIoDxe and PartitionDxe connect to the newly-available BlockIo handle.
  DEBUG ((DEBUG_INFO, "[A733] ConnectAll (2nd pass for storage drivers)\n"));
  EfiBootManagerConnectAll ();

  if (TryBootRemovableMediaPath ((CHAR16 *)mRemovableBootPath)) {
    return;
  }

  // Fallback to the shell embedded in FV when no external boot file exists.
  ShellPath = BuildFvFilePath (&mShellFileGuid);
  if (ShellPath == NULL) {
    DEBUG ((DEBUG_ERROR, "[A733] Shell not found in any FV!\n"));
    return;
  }

  if (!BootDevicePathOnce (L"UEFI Shell", ShellPath)) {
    DEBUG ((DEBUG_ERROR, "[A733] Failed to boot FV shell\n"));
  }
  FreePool (ShellPath);
}

VOID
EFIAPI
PlatformBootManagerWaitCallback (
  UINT16  TimeoutRemain
  )
{
}

VOID
EFIAPI
PlatformBootManagerUnableToBoot (
  VOID
  )
{
  DEBUG ((DEBUG_ERROR, "[A733] PlatformBootManagerUnableToBoot - no boot device found\n"));
}
