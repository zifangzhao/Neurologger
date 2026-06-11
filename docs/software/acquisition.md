# Acquisition

The acquisition workflow starts in WILD_console and ends with exported recording folders.

## Typical Session

1. Start WILD_console.
2. Scan for the WILD device.
3. Connect over BLE.
4. Read or configure device parameters.
5. Configure sampling, closed-loop, camera, stimulation, and GPIO options as needed.
6. Start recording.
7. Monitor preview and state signals.
8. Stop recording.
9. Export data from the SD card.

## Exported Files

The exported folder can include:

- `amplifier.dat`.
- `analogin.dat`.
- `digitalin.dat`.
- `adc.dat`.
- `misc.dat`.
- `supply.dat`.
- `time.dat`.
- `info.rhd`.
- `CE_params.bin`.

See [Data Format](data-format.md) for field descriptions.
