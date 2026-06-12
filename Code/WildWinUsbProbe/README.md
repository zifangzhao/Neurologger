# WILD WinUSB Experiment

This folder is the host-side experiment package for moving the WILD camera preview path away from raw-disk MSC access and onto a WinUSB bulk stream.

## What Is In Here

- `Program.cs`
  - Console tool with:
    - `probe`
    - `paths`
    - `bench-winusb`
    - `bench-msc`
- `WILD_FS_Bridge_WinUSB.inf`
  - Local WinUSB binding package for `USB\VID_0483&PID_572A`
  - Registers the recovered interface GUID `{6C303587-B774-4A8B-8AFF-20557620207A}`
- `Install-WildWinUsbDriver.ps1`
  - Admin install helper for the local INF and a forced device restart
- `Register-WildWinUsbGuid.ps1`
  - Elevated helper that injects `DeviceInterfaceGUIDs` into the live device hardware key and restarts it
- `Reenumerate-WildDevice.ps1`
  - Elevated helper that removes the device and forces a fresh scan after the GUID injection
- `Recover-WildWinUsbGuid.ps1`
  - Read-only SWD helper that dumps the first 512 KB of flash and extracts the WinUSB identity markers

## Current Device Facts

- The shipped desktop app is still on the old MSC/raw-disk path.
  - Installed `WILD_console.exe` still contains `GetPhysicalDriveList`, `CE32_diskIO`, and volume lock/dismount strings.
- The currently attached board is already running a WinUSB firmware image.
  - USB identity: `VID_0483`, `PID_572A`
  - Product string from flash: `WILD USB FS Bridge`
  - Interface string from flash: `WinUSB Stream`
  - WinUSB interface GUID from flash:
    - `{6C303587-B774-4A8B-8AFF-20557620207A}`
- The firmware-side MS OS descriptor block in flash is populated with:
  - `MSFT100`
  - `WINUSB`
  - `DeviceInterfaceGUIDs`
  - the recovered GUID above

## Why The Probe Still Fails On This Machine

Windows currently exposes only the generic USB device interface:

- `\\?\USB#VID_0483&PID_572A#2004BF1A0800#{a5dcbf10-6530-11d2-901f-00c04fb951ed}`

Observed state:

- `winusb.inf` is bound to the device through `USB\MS_COMP_WINUSB`
- the recovered custom GUID is not present under `HKLM\SYSTEM\CurrentControlSet\Control\DeviceClasses`
- `WinUsb_Initialize` on the generic USB interface path fails with `ERROR_INVALID_HANDLE (6)`

So the board is on the WinUSB driver stack, but this host has not exposed an openable user-mode interface for the recovered GUID yet.

## What Was Tried On This Machine

1. Elevated install of `WILD_FS_Bridge_WinUSB.inf`
   - Windows rejected it because the package is unsigned.
2. Elevated write of `DeviceInterfaceGUIDs` directly into:
   - `HKLM\SYSTEM\CurrentControlSet\Enum\USB\VID_0483&PID_572A\2004BF1A0800`
3. Elevated `pnputil /restart-device`
4. Elevated `pnputil /remove-device` followed by `pnputil /scan-devices`

Result after every attempt:

- only the generic `{a5dcbf10-6530-11d2-901f-00c04fb951ed}` USB interface is published
- `WinUsb_Initialize` still fails with `ERROR_INVALID_HANDLE (6)`

The log files for those runs are stored next to the scripts:

- `install-driver.log`
- `register-guid.log`
- `reenumerate-device.log`

## Build

```powershell
dotnet build Code\WildWinUsbProbe\WildWinUsbProbe.csproj -c Release
```

## Probe The Current WinUSB State

```powershell
dotnet Code\WildWinUsbProbe\bin\Release\net8.0-windows\WildWinUsbProbe.dll probe
```

Print candidate interface paths only:

```powershell
dotnet Code\WildWinUsbProbe\bin\Release\net8.0-windows\WildWinUsbProbe.dll paths
```

## Benchmark The WinUSB Path

```powershell
dotnet Code\WildWinUsbProbe\bin\Release\net8.0-windows\WildWinUsbProbe.dll bench-winusb --seconds 5 --read-bytes 16384 --frame-bytes 163840
```

Defaults:

- instance id: `USB\VID_0483&PID_572A\2004BF1A0800`
- start request: `0x40`
- stop request: `0x41`
- status request: `0x42`
- equivalent frame size: `320 * 512 = 163840` bytes

## Benchmark The Legacy MSC Path

The old Python preview loop reads one fixed `163840` byte window from:

- offset `0x1000 * 512 = 0x200000`

Use the console benchmark the same way:

```powershell
dotnet Code\WildWinUsbProbe\bin\Release\net8.0-windows\WildWinUsbProbe.dll bench-msc --path \\.\PhysicalDrive3 --seconds 5
```

## Register The WinUSB Interface On This Host

The local INF is intended to give Windows a stable interface registration for the recovered GUID:

```powershell
powershell -ExecutionPolicy Bypass -File Code\WildWinUsbProbe\Install-WildWinUsbDriver.ps1
```

This requires an elevated shell. If Windows rejects the package because it is unsigned, use it as the template for a signed driver package in the real source tree.

## Recover The GUID Again From SWD

This requires:

- ST-LINK connected
- `STM32CubeProgrammer` installed
- read-only SWD access to the board

```powershell
powershell -ExecutionPolicy Bypass -File Code\WildWinUsbProbe\Recover-WildWinUsbGuid.ps1
```

## Measurement Goal

The intended experiment flow is:

1. Measure the old MSC path with `bench-msc` on an MSC firmware image.
2. Rebind the live WinUSB image with the local interface GUID.
3. Measure the WinUSB bulk path with `bench-winusb`.
4. Compare the equivalent frames per second from both runs.

If step 2 does not succeed on this machine, the remaining gap is host driver registration, not missing firmware-side WinUSB identity data.
