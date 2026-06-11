# BLE

BLE provides wireless discovery, configuration, status, preview signals, and recording control.

## User-visible Behavior

- WILD_console scans for devices through the Port drop-down.
- Connection status and TX/RX counters should update after connection.
- Preview signals can be enabled during recording.
- Device messages and TinyML model states are displayed in the console status area.

## Troubleshooting Checklist

| Symptom | First checks |
| --- | --- |
| Device is not discovered | Battery, firmware image, BLE adapter, distance, device reset |
| BLE connects but sync does not start | microSD card format and card compatibility |
| Preview is unreliable | BLE bandwidth, preview channel count, display length, host adapter |
| State messages are missing | Firmware mode, recording state, console version |

## Documentation Targets

Add packet formats, command IDs, connection timing, throughput limits, and expected service or characteristic maps after they are finalized for the public API.
