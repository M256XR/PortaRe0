/** @file
 * Allwinner A733 ArmPlatformLib implementation
 *
 * Handles platform initialization called from EDK2 SEC/PEI phase.
 * DDR is already initialized by boot0 (Allwinner SPL), so we skip
 * memory initialization here.
 **/

#include <Library/ArmPlatformLib.h>
#include <Library/DebugLib.h>
#include <Library/IoLib.h>
#include <Library/MemoryAllocationLib.h>
#include <Library/PcdLib.h>
#include <Library/SerialPortLib.h>
#include <Ppi/ArmMpCoreInfo.h>

// Direct UART write helper - works even before SerialPortInitialize (boot0 already set up UART)
STATIC VOID
DbgStr (CONST CHAR8 *Str)
{
  UINTN  Len = 0;
  while (Str[Len]) { Len++; }
  SerialPortWrite ((UINT8 *)Str, Len);
}

// A733 has 4 Cortex-A55 cores in a single cluster (Aff1=0, Aff0=0..3)
// Mailbox fields are zeroed - secondary cores not used in first milestone
STATIC ARM_CORE_INFO  mA733CoreInfoTable[] = {
  { 0x000000, 0, 0, 0, 0 },  // Core 0 (primary)
  { 0x000001, 0, 0, 0, 0 },  // Core 1
  { 0x000002, 0, 0, 0, 0 },  // Core 2
  { 0x000003, 0, 0, 0, 0 },  // Core 3
};

STATIC
EFI_STATUS
EFIAPI
A733GetMpCoreInfo (
  OUT UINTN          *CoreCount,
  OUT ARM_CORE_INFO  **ArmCoreTable
  )
{
  DbgStr ("[A733] GetMpCoreInfo called\r\n");
  *CoreCount    = ARRAY_SIZE (mA733CoreInfoTable);
  *ArmCoreTable = mA733CoreInfoTable;
  return EFI_SUCCESS;
}

STATIC ARM_MP_CORE_INFO_PPI  mMpCoreInfoPpi = { A733GetMpCoreInfo };

STATIC EFI_PEI_PPI_DESCRIPTOR  mPlatformPpiTable[] = {
  {
    EFI_PEI_PPI_DESCRIPTOR_PPI | EFI_PEI_PPI_DESCRIPTOR_TERMINATE_LIST,
    &gArmMpCoreInfoPpiGuid,
    &mMpCoreInfoPpi
  }
};

/**
  Return platform-specific PPI list.
  Provides ArmMpCoreInfoPpi required by PeilessSec on MP-core platforms.
**/
VOID
ArmPlatformGetPlatformPpiList (
  OUT UINTN                   *PpiListSize,
  OUT EFI_PEI_PPI_DESCRIPTOR  **PpiList
  )
{
  *PpiListSize = sizeof (mPlatformPpiTable);
  *PpiList     = mPlatformPpiTable;
}

/**
  Return the current Boot Mode.
  BOOT_WITH_FULL_CONFIGURATION is returned since boot0 handles early init.
**/
EFI_BOOT_MODE
ArmPlatformGetBootMode (VOID)
{
  return BOOT_WITH_FULL_CONFIGURATION;
}

/**
  Initialize controllers that must be setup in the normal world.
  Called from PEI phase after memory is ready.
**/
RETURN_STATUS
ArmPlatformInitialize (
  IN  UINTN  MpId
  )
{
  DbgStr ("[A733] ArmPlatformInitialize\r\n");
  return RETURN_SUCCESS;
}

/**
  Return the Virtual Memory Map of your platform.
  This is the memory map that will be used by the MMU.
**/
VOID
ArmPlatformGetVirtualMemoryMap (
  IN ARM_MEMORY_REGION_DESCRIPTOR **VirtualMemoryMap
  )
{
  ARM_MEMORY_REGION_ATTRIBUTES  CacheAttributes;
  UINTN                         Index = 0;
  ARM_MEMORY_REGION_DESCRIPTOR  *VirtualMemoryTable;

  ASSERT (VirtualMemoryMap != NULL);

  VirtualMemoryTable = AllocatePages (
                         EFI_SIZE_TO_PAGES (sizeof (ARM_MEMORY_REGION_DESCRIPTOR) * 16)
                         );
  if (VirtualMemoryTable == NULL) {
    return;
  }

  DbgStr ("[A733] GetVirtualMemoryMap called\r\n");

  VirtualMemoryTable = AllocatePages (
                         EFI_SIZE_TO_PAGES (sizeof (ARM_MEMORY_REGION_DESCRIPTOR) * 16)
                         );
  if (VirtualMemoryTable == NULL) {
    DbgStr ("[A733] AllocatePages FAILED\r\n");
    return;
  }
  DbgStr ("[A733] AllocatePages OK\r\n");

  CacheAttributes = ARM_MEMORY_REGION_ATTRIBUTE_WRITE_BACK;

  // System DRAM (1GB at 0x40000000)
  VirtualMemoryTable[Index].PhysicalBase = FixedPcdGet64 (PcdSystemMemoryBase);
  VirtualMemoryTable[Index].VirtualBase  = FixedPcdGet64 (PcdSystemMemoryBase);
  VirtualMemoryTable[Index].Length       = FixedPcdGet64 (PcdSystemMemorySize);
  VirtualMemoryTable[Index].Attributes   = CacheAttributes;
  Index++;

  // SoC peripherals region (0x00000000 - 0x10000000)
  // Covers: UART, GIC, Timers, pinctrl, etc.
  VirtualMemoryTable[Index].PhysicalBase = 0x00000000;
  VirtualMemoryTable[Index].VirtualBase  = 0x00000000;
  VirtualMemoryTable[Index].Length       = 0x10000000;
  VirtualMemoryTable[Index].Attributes   = ARM_MEMORY_REGION_ATTRIBUTE_DEVICE;
  Index++;

  // End of table
  VirtualMemoryTable[Index].PhysicalBase = 0;
  VirtualMemoryTable[Index].VirtualBase  = 0;
  VirtualMemoryTable[Index].Length       = 0;
  VirtualMemoryTable[Index].Attributes   = (ARM_MEMORY_REGION_ATTRIBUTES)0;

  DbgStr ("[A733] GetVirtualMemoryMap DONE\r\n");
  *VirtualMemoryMap = VirtualMemoryTable;
}
