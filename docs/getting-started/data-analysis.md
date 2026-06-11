# Data Analysis

The repository includes MATLAB and Python scripts for converting WILD recordings into analysis-ready files.

## Standard Post-processing

1. Export data from WILD_console.
2. Run `WILD_PreProcess.m` to generate corrected headers and timing files.
3. Run `WILD_processIMU.m` for IMU processing.
4. Run `WILD_VideoDecodewAudio.py` or the folder variants for camera recordings.
5. Prepare spike-sorting inputs from `amplifier.dat`.

## Script Locations

| Task | Script |
| --- | --- |
| Header and time correction | [`WILD_PreProcess.m`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_PreProcess.m) |
| IMU processing | [`WILD_processIMU.m`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_processIMU.m) |
| Camera decode with audio | [`WILD_VideoDecodewAudio.py`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_VideoDecodewAudio.py) |
| Intan header generation | [`WILD_genIntanHeader.m`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_genIntanHeader.m) |

!!! note
    Keep raw SD exports unchanged. Run conversion scripts into a separate analysis folder so the original recording can be reprocessed if metadata or analysis settings change.
