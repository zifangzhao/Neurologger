# Programmatic Workflows

WILD_console and the listed scripts form the supported public interface for acquisition, export, post-processing, and validation.

WILD_console handles BLE discovery, synchronization, configuration, selected preview, and SD-card export. Full-resolution recordings are recovered from local storage rather than streamed continuously over BLE.

An iOS-based WILD controller app is in development for wireless device control and is expected to provide more consistent BLE performance than typical PC BLE adapters. The current stable public export and post-processing workflow remains WILD_console plus the documented MATLAB and Python scripts.

!!! warning "No stable SDK yet"
    The supported public programmable surface is WILD_console plus the documented repository scripts. The project does not currently document a stable general-purpose SDK with a versioned command contract.

## Current Support

| Area | Current operation style | Purpose |
| --- | --- | --- |
| Acquisition | WILD_console | BLE discovery, connection, synchronization, recording setup, selected live preview, closed-loop configuration, and SD-card export. |
| Wireless control | iOS controller app, in development | BLE discovery, connection, synchronization support, status checks, and low-bandwidth commands. |
| Post-processing | MATLAB scripts | Header generation, timing correction, event export, IMU processing, and Intan-compatible output preparation. |
| Camera/audio decoding | Python scripts | Decode `misc.dat` and related audio data into reviewable media outputs. |
| Batch processing | Python and MATLAB scripts | Process folders of recordings after SD export. |
| GPIO logging | Python utility | Log serial/GPIO event data during validation or synchronization tests. |
| Release and model tracking | Release metadata workflow | Record release image, AI model identity, and tool version for reproducibility. |

## Supported Scripted Operations

The current public API surface is organized around these operations:

- Export recording folders from WILD_console.
- Generate corrected `info.rhd` and `time.dat` outputs.
- Convert raw WILD camera/audio data into media files.
- Process IMU channels into calibrated signals.
- Batch-process recording folders.
- Log GPIO or serial synchronization events.
- Preserve software, release-image, and model versions in experiment notes.

## Device Operation Categories

WILD_console and controller workflows expose device operations at a task level. Public documentation should describe these operations by purpose rather than by low-level command ID.

| Category | Typical operations |
| --- | --- |
| Recording control | Set recording parameters, start local recording, stop local recording, and confirm recording state. |
| Preview control | Start or stop selected-channel preview and choose preview channels without treating BLE as the full-resolution data path. |
| DSP and TinyML setup | Load curated DSP or model parameters from a validated release image and record the selected configuration in metadata. |
| Stimulation control | Configure stimulation intensity, thresholds, timing, and manual test triggers when the hardware revision supports stimulation. |
| Time and synchronization | Check the connection, coordinate PC-device time, set device time, and retain external I/O events for experiment-level alignment. |
| Device status | Read parameters, battery state, available storage, device identity, and release-image metadata. |
| Power state | Request sleep or reset only as part of the documented maintenance or field-session workflow. |
| External I/O | Route GPIO and synchronization signals to cameras, behavioral systems, stimulation modules, or additional WILD devices. |

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

WILD_console operations and documented processing scripts are the supported public surface. Script internals remain implementation details unless a workflow is explicitly documented.
