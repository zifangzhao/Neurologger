# API and CLI Operations

Use WILD_console and the listed scripts as the supported public interface for acquisition, export, post-processing, and validation.

WILD_console handles BLE discovery, synchronization, configuration, selected preview, and SD-card export. Full-resolution recordings are recovered from local storage rather than streamed continuously over BLE.

## Current Support

| Area | Current operation style | Purpose |
| --- | --- | --- |
| Acquisition | WILD_console | BLE discovery, connection, synchronization, recording setup, selected live preview, closed-loop configuration, and SD-card export. |
| Post-processing | MATLAB scripts | Header generation, timing correction, event export, IMU processing, and Intan-compatible output preparation. |
| Camera/audio decoding | Python scripts | Decode `misc.dat` and related audio data into reviewable media outputs. |
| Batch processing | Python and MATLAB scripts | Process folders of recordings after SD export. |
| GPIO logging | Python utility | Log serial/GPIO event data during validation or synchronization tests. |
| Release and model tracking | Release metadata workflow | Record release image, AI model identity, and tool version for reproducibility. |

## CLI-Style Tool Operations

Use these operations as the current public API surface:

- Export recording folders from WILD_console.
- Generate corrected `info.rhd` and `time.dat` outputs.
- Convert raw WILD camera/audio data into media files.
- Process IMU channels into calibrated signals.
- Batch-process recording folders.
- Log GPIO or serial synchronization events.
- Preserve software, release-image, and model versions in experiment notes.

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

WILD_console operations and documented processing scripts are the supported public surface. Treat script internals as implementation details unless a workflow is explicitly documented.
