# BLE

BLE provides wireless discovery, configuration, status, low-bandwidth preview signals, synchronization support, and recording control.

BLE is not the primary high-bandwidth neural data path. During normal experiments, electrophysiology and multimodal data are logged locally to microSD. BLE is used for interaction with the headstage: setup, command delivery, state reporting, selected previews, and synchronization workflows.

## User-visible Behavior

- WILD_console scans for devices through the Port drop-down.
- Connection status and TX/RX counters should update after connection.
- Selected preview signals can be enabled during recording, subject to BLE bandwidth and power constraints.
- Device messages and TinyML model states are displayed in the console status area.

## Synchronization Model

WILD synchronization should be described as a multi-stage timing workflow, not as simple BLE timestamps. Depending on the experiment, timing can combine wired synchronization lines, BLE calibration, and clock-frequency correction so multiple WILD devices and external systems remain aligned during local recording.

Document the synchronization path used for each dataset:

- Whether devices were started from one host or multiple hosts.
- Whether wired sync or external GPIO alignment was used.
- Whether BLE calibration was performed before recording.
- Which firmware, crystal calibration, and post-processing correction were used.

## Troubleshooting Checklist

| Symptom | First checks |
| --- | --- |
| Device is not discovered | Battery, firmware image, BLE adapter, distance, device reset |
| BLE connects but sync does not start | microSD card format and card compatibility |
| Preview is unreliable | BLE bandwidth, preview channel count, display length, host adapter |
| State messages are missing | Firmware mode, recording state, console version |

## Public Interface Boundary

The public documentation should describe stable operator behavior before exposing low-level packet details. Command IDs, BLE service maps, throughput limits, and timing guarantees should be published only for interfaces that are intended to remain compatible across releases.
