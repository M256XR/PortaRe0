/** @file
  Small external EFI app used to verify removable-media EFI execution.
**/

#include <Uefi.h>

#include <Library/BaseLib.h>
#include <Library/DebugLib.h>
#include <Library/PrintLib.h>
#include <Library/UefiBootServicesTableLib.h>
#include <Library/UefiLib.h>

EFI_STATUS
EFIAPI
UefiMain (
  IN EFI_HANDLE        ImageHandle,
  IN EFI_SYSTEM_TABLE  *SystemTable
  )
{
  UINTN  Index;

  Print (L"\r\n");
  Print (L"[BootProbe] External EFI app started from fs0:\\EFI\\BOOT\\TESTA7Z.EFI\r\n");
  Print (L"[BootProbe] If you can read this, external EFI launch works.\r\n");

  for (Index = 3; Index > 0; Index--) {
    Print (L"[BootProbe] Returning to caller in %u...\r\n", (UINT32)Index);
    gBS->Stall (1000 * 1000);
  }

  Print (L"[BootProbe] Done.\r\n");
  return EFI_SUCCESS;
}
