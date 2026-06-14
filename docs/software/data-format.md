# Data Format

Each WILD device recording session exports a folder with neural data, auxiliary signals, metadata, and optional camera or audio files.

## Files

| File | Verified public handling | Notes |
| --- | --- |
| `amplifier.dat` | Read by `WILD_PreProcess.m` as channel-interleaved 16-bit neural data. | Sample count is computed as `file_bytes / 2 / Nch`, with `Nch` read from `CE_params.bin`. |
| `analogin.dat` | Used as the auxiliary stream for digital inputs, IMU, and timing-related channels. | Public MATLAB scripts read this stream as 16 channels at 1250 Hz for preprocessing and IMU extraction. |
| `digitalin.dat` | Optional digital-input export artifact. | Not every workflow generates a separate file; public trigger generation currently derives digital events from `analogin.dat`. |
| `adc.dat` | ADC or audio stream used by microphone workflows. | Public Python decode scripts read this file as `uint16` mono audio and generate `.wav` or `.mp3` outputs. |
| `misc.dat` | Raw camera payload stream. | Public Python decode scripts convert this file into reviewable video outputs. |
| `time.dat` | Generated sample-index timeline. | Public MATLAB preprocessing writes `0:(Nsamples-1)` as `int32`. |
| `info.rhd` | Intan-compatible metadata header. | Generated from `CE_params.bin` by `WILD_genIntanHeader.m`. |
| `CE_params.bin` | WILD parameter binary for system and DSP settings. | The public docs refer to this as the WILD parameter binary; MATLAB tools use the filename `CE_params.bin`. |

## Export Decoding

The WILD device records compact local streams on its microSD card. During the current SD-card download workflow, WILD_console decodes the on-device recording into analysis-facing files: neural samples are written to `amplifier.dat`, auxiliary and timing words to `analogin.dat`, ADC or audio streams to `adc.dat`, camera payloads to `misc.dat`, and session parameters to the WILD parameter binary.

The exported folder is therefore the decoded public data interface. Raw device storage blocks are not the expected analysis input; downstream MATLAB and Python tools operate on the downloaded files and generate derived outputs such as `info.rhd`, `time.dat`, event files, media files, IMU outputs, and spike-sorting inputs.

![WILD_console runtime screenshot of the offline export workflow](../images/WIrelessEphys_Github_5_offlineAPI.jpg){ .wild-readable-figure }

## Time Synchronization

The WILD device keeps high-bandwidth recordings local while WILD_console provides PC-device coordination over BLE. At connection and recording setup, the console synchronizes device state with the PC session and records timing context with the exported dataset.

Timing metadata should be interpreted as a layered system: device sample counts provide the primary sample timeline, PC-device timing coordination supports session-level alignment, and external I/O or digital events provide the most direct alignment path for external cameras, behavior systems, stimulation hardware, and multi-device sessions.

`time.dat` stores the sample-index timeline used by Intan-style workflows, while the WILD parameter binary preserves device-side recording time, hardware version, release image identity, sampling configuration, and DSP settings. External sync lines and digital inputs in `analogin.dat` or generated event files should be retained with the export whenever the experiment depends on cross-device or behavior alignment.

PC-device time synchronization is useful for session organization, export metadata, and cross-device coordination. It should not be treated as a substitute for hardware sync or digital event channels when the analysis requires high-precision alignment.

## Verified Script Assumptions

The following public assumptions are visible in the repository scripts and should be treated as the current documented behavior unless a release note states otherwise:

- `WILD_PreProcess.m` reads `amplifier.dat` as 16-bit neural samples and uses `CE_params.bin` to determine channel count and sampling rate.
- `time.dat` is written as a monotonically increasing `int32` sample index.
- `WILD_processIMU.m` reads channels `2:10` from `analogin.dat`, assumes a 1250 Hz source rate, and writes `IMU.mat` after resampling to 100 Hz by default.
- `WILD_PreProcess.m` reads channel `1` of `analogin.dat` as a `uint16` digital bitfield and generates `device_event.*.evt` files from its bit transitions.
- `WILD_VideoDecodewAudio.py` reads `adc.dat` as `uint16` audio, converts it to signed audio outputs, and assumes a 160 kHz audio path.
- `WILD_VideoDecodewAudio.py` reads `misc.dat` in `320 * 500` byte frame blocks and writes 320 x 320, 16 Hz decoded video outputs.

Where a file layout depends on a specific release image or modality, report the exact release tag and mode together with the dataset. Do not assume that every export contains every optional modality file.

## Multi-Device and Behavior Alignment

For multi-logger sessions, keep the raw export folder for each device and store merge or sync-estimation outputs alongside the derived files. Useful validation checks include matched `amplifier.dat` duration and file size, stable estimated sample offsets, continuous external TTL or digital events, and no unexpected gaps in camera frames.

Behavior datasets should state whether video, UWB, IMU, and ephys streams are expressed on corrected timestamps. Camera calibration, coordinate transforms, identity curation, and delay correction are part of the dataset metadata, especially for outdoor multi-animal work.

When a behavior pipeline produces files such as `behavior_all.mat`, document whether fields are aligned to corrected timestamps such as `timestamps_corrected` and which correction was used. Post-hoc delay estimation or time warping can help evaluate a session, but it should not replace acquisition-side sync validation.

## Intan-Compatible Layout

WILD exports are arranged to be familiar to users of Intan-style recording folders while preserving WILD-specific metadata for sensors, DSP, stimulation, and camera workflows.

## Best Practice

Keep three folders per experiment:

1. Raw SD export.
2. Converted analysis copy.
3. Downstream results from spike sorting, behavior alignment, or machine-learning analysis.
