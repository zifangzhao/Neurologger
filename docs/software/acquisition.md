# Acquisition

The acquisition workflow starts in WILD_console and ends with exported recording folders from the device microSD card.

WILD records high-bandwidth neural and multimodal data locally. BLE is used for discovery, synchronization, configuration, status, selected preview, and control commands rather than continuous full-bandwidth data streaming.

## Typical Session

1. Start WILD_console.
2. Scan for the WILD device.
3. Connect over BLE.
4. Read or configure device parameters.
5. Configure sampling, closed-loop, camera, stimulation, and GPIO options as needed.
6. Start local recording.
7. Monitor selected preview and state signals.
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
- WILD parameter binary.

See [Data Format](data-format.md) for field descriptions.
