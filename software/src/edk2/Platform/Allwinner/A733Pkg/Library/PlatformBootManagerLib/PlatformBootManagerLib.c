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
#include <Library/PcdLib.h>
#include <Library/UefiBootManagerLib.h>
#include <Library/UefiBootServicesTableLib.h>
#include <Library/UefiLib.h>
#include <Protocol/DevicePath.h>
#include <Protocol/FirmwareVolume2.h>
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
  EFI_STATUS                    Status;
  EFI_BOOT_MANAGER_LOAD_OPTION  ShellOption;
  EFI_DEVICE_PATH_PROTOCOL      *ShellPath;

  DEBUG ((DEBUG_INFO, "[A733] PlatformBootManagerAfterConsole\n"));

  // Connect all drivers so storage / console devices are available.
  EfiBootManagerConnectAll ();

  // Build a boot option pointing to the Shell EFI in the FV.
  ShellPath = BuildFvFilePath (&mShellFileGuid);
  if (ShellPath == NULL) {
    DEBUG ((DEBUG_ERROR, "[A733] Shell not found in any FV!\n"));
    return;
  }

  Status = EfiBootManagerInitializeLoadOption (
             &ShellOption,
             LoadOptionNumberUnassigned,
             LoadOptionTypeBoot,
             LOAD_OPTION_ACTIVE,
             L"UEFI Shell",
             ShellPath,
             NULL,
             0
             );
  FreePool (ShellPath);

  if (EFI_ERROR (Status)) {
    DEBUG ((DEBUG_ERROR, "[A733] Failed to init Shell boot option: %r\n", Status));
    return;
  }

  // Second ConnectAll: SdDxe installs BlockIo during the first ConnectAll,
  // but ConnectAll may have already scanned that handle. A second pass lets
  // DiskIoDxe and PartitionDxe connect to the newly-available BlockIo handle.
  DEBUG ((DEBUG_INFO, "[A733] ConnectAll (2nd pass for storage drivers)\n"));
  EfiBootManagerConnectAll ();

  DEBUG ((DEBUG_INFO, "[A733] Booting UEFI Shell...\n"));
  EfiBootManagerBoot (&ShellOption);
  EfiBootManagerFreeLoadOption (&ShellOption);
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
