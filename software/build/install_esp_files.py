#!/usr/bin/env python3
"""Install BOOTAA64.EFI and optional startup.nsh onto a mounted ESP."""

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_BOOT_SOURCE = SCRIPT_DIR / "BootProbe.efi"
DEFAULT_TEST_APP_SOURCE = SCRIPT_DIR / "BootProbe.efi"
DEFAULT_STARTUP_CONTENT = (
    "@echo -off\r\n"
    "if exist fs0:\\EFI\\BOOT\\TESTA7Z.EFI then\r\n"
    "  fs0:\\EFI\\BOOT\\TESTA7Z.EFI\r\n"
    "endif\r\n"
    "if exist fs0:\\EFI\\Microsoft\\Boot\\bootmgfw.efi then\r\n"
    "  fs0:\\EFI\\Microsoft\\Boot\\bootmgfw.efi\r\n"
    "endif\r\n"
    "if exist fs0:\\EFI\\BOOT\\BOOTAA64.EFI then\r\n"
    "  echo BOOTAA64.EFI exists on fs0:, but startup.nsh is prioritizing TESTA7Z.EFI and bootmgfw.efi\r\n"
    "endif\r\n"
    "echo No external OS loader found on fs0:.\r\n"
    "echo Expected example: fs0:\\EFI\\Microsoft\\Boot\\bootmgfw.efi\r\n"
)


def fail(message: str) -> "NoReturn":
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalize_esp_root(path_text: str) -> Path:
    esp_root = Path(path_text)
    if not esp_root.is_absolute():
        fail(f"ESP path must be absolute: {path_text}")
    if not esp_root.exists():
        fail(f"ESP path does not exist: {esp_root}")
    return esp_root


def install_bootaa64(esp_root: Path, source: Path) -> Path:
    if not source.exists():
        fail(f"BOOTAA64 source not found: {source}")

    target = esp_root / "EFI" / "BOOT" / "BOOTAA64.EFI"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    return target


def install_test_app(esp_root: Path, source: Path) -> Path:
    if not source.exists():
        fail(f"Test EFI source not found: {source}")

    target = esp_root / "EFI" / "BOOT" / "TESTA7Z.EFI"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    return target


def install_startup_script(esp_root: Path, force: bool) -> Path | None:
    target = esp_root / "startup.nsh"
    if target.exists() and not force:
        print(f"Preserving existing startup.nsh: {target}")
        return None

    target.write_text(DEFAULT_STARTUP_CONTENT, encoding="ascii", newline="")
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy BOOTAA64.EFI and optional startup.nsh to a mounted ESP."
    )
    parser.add_argument(
        "--esp",
        required=True,
        help="Mounted ESP root path, for example S:\\ or E:\\",
    )
    parser.add_argument(
        "--bootaa64-source",
        default=str(DEFAULT_BOOT_SOURCE),
        help="Source EFI binary to copy as EFI\\BOOT\\BOOTAA64.EFI",
    )
    parser.add_argument(
        "--test-app-source",
        default=str(DEFAULT_TEST_APP_SOURCE),
        help="Source EFI binary to copy as EFI\\BOOT\\TESTA7Z.EFI",
    )
    parser.add_argument(
        "--with-startup-nsh",
        action="store_true",
        help="Also create a fallback startup.nsh in the ESP root.",
    )
    parser.add_argument(
        "--force-startup-nsh",
        action="store_true",
        help="Overwrite an existing startup.nsh when used with --with-startup-nsh.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    esp_root = normalize_esp_root(args.esp)
    boot_source = Path(args.bootaa64_source)
    test_app_source = Path(args.test_app_source)

    boot_target = install_bootaa64(esp_root, boot_source)
    print(f"Installed BOOTAA64.EFI: {boot_target}")
    test_target = install_test_app(esp_root, test_app_source)
    print(f"Installed TESTA7Z.EFI: {test_target}")

    if args.with_startup_nsh:
        startup_path = install_startup_script(esp_root, args.force_startup_nsh)
        if startup_path is not None:
            print(f"Installed startup.nsh: {startup_path}")


if __name__ == "__main__":
    main()
