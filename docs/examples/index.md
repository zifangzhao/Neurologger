# Examples

These example workflows summarize common WILD device use cases and the metadata needed to make each experiment reproducible.

## Workflow Index

| Example | Scope | Expected validation |
| --- | --- |
| Basic neural recording | Battery, SD format, BLE connect, recording, export, preprocessing. | `amplifier.dat`, `analogin.dat`, `time.dat`, `info.rhd`, `CE_params.bin`. |
| Closed-loop ripple detection | Filter setup, thresholding, stimulation configuration, validation waveform. | Event files, threshold traces, and stimulation timing review. |
| Theta phase stimulation | Hilbert mode setup, phase logic, stimulation timing, event export. | Phase-locked trigger timing and stimulation event checks. |
| Multi-animal synchronization | Multiple WILD_console instances, start timing, sync line, analysis alignment. | Matched durations, stable offsets, and retained sync events. |
| Outdoor recording | Power planning, SD choice, wireless checks, data integrity checks. | Complete export, no unexpected truncation, and logged power configuration. |
| Camera plus IMU | Camera decode, IMU processing, and behavioral alignment. | Reviewable video output and generated `IMU.mat`. |

## Required Metadata

For each public dataset or protocol, record:

- Goal.
- Hardware revision.
- Release image.
- Software version.
- Required accessories.
- Step-by-step protocol.
- Expected outputs.
- Troubleshooting notes.
- Example data or a small validation file.

## Priority for Expanded Protocol Pages

The highest-value example pages to expand next are:

1. Basic neural recording.
2. Multi-animal synchronization.
3. Closed-loop ripple detection.

These three paths cover the first successful dry run, cross-device timing, and one validated responsive-control workflow.
