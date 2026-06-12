# API and CLI Operations

WILD currently exposes operator-facing software through WILD_console and script-based utility operations. The public interface is organized around documented operations, input files, output files, and versioned tool behavior rather than a general-purpose SDK.

The current public software surface should be described conservatively. WILD_console controls BLE discovery, synchronization, configuration, selected preview, and SD-card export; it should not be framed as a continuous high-bandwidth BLE streaming API.

## Current Support

| Area | Current operation style | Purpose |
| --- | --- | --- |
| Acquisition | WILD_console | BLE discovery, connection, synchronization, recording setup, selected live preview, closed-loop configuration, and SD-card export. |
| Post-processing | MATLAB scripts | Header generation, timing correction, event export, IMU processing, and Intan-compatible output preparation. |
| Camera/audio decoding | Python scripts | Decode `misc.dat` and related audio data into reviewable media outputs. |
| Batch processing | Python and MATLAB scripts | Process folders of recordings after SD export. |
| GPIO logging | Python utility | Log serial/GPIO event data during validation or synchronization tests. |
| Firmware and model validation | Firmware-specific workflow | Record firmware image, AI model identity, and tool version for reproducibility. |

## CLI-Style Tool Operations

The following operations should be treated as the current API surface until a stable SDK is defined:

- Export recording folders from WILD_console.
- Generate corrected `info.rhd` and `time.dat` outputs.
- Convert raw WILD camera/audio data into media files.
- Process IMU channels into calibrated signals.
- Batch-process recording folders.
- Log GPIO or serial synchronization events.
- Preserve software, firmware, and model versions in experiment notes.

## Tool Metadata

For reproducible use, record the following metadata with tool outputs and example datasets:

- Tool name and version.
- Required operating system and dependencies.
- Input folder or file layout.
- Command or launch procedure used.
- Output files and naming convention.
- Expected runtime and memory requirements.
- Failure modes and troubleshooting notes.
- Validation file or representative dataset, when available.

## SDK Status

The current implementation is practical for lab workflows, but script internals should not be presented as a stable SDK. Treat WILD_console operations and documented processing scripts as the supported public surface.
