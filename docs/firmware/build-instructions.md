# Build Instructions

This page is the public build checklist for firmware contributors.

## Toolchain

- Keil MDK for the reference STM32 project.
- STM32CubeProgrammer for flashing and recovery.
- Git for tracking firmware and release assets.

## Build Flow

1. Open the firmware project in the configured IDE.
2. Select the correct target for the hardware revision.
3. Build the application image.
4. Archive the binary with hardware revision, date, and short commit identifier.
5. Flash directly for development or stage the image for microSD bootloader update.
6. Record the binary filename in experiment notes.

## Release File Naming

Prefer names that can be traced later:

```text
WILD64X_release_YYYYMMDD_HHMM.bin
```

## Public Checklist

- Hardware revision tested.
- Bootloader compatibility verified.
- BLE discovery verified.
- SD formatting and recording verified.
- Closed-loop modes smoke-tested if changed.
- Data export and preprocessing verified on a short recording.
