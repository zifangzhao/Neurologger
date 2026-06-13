# MATLAB

MATLAB scripts currently provide the main preprocessing path for WILD recordings.

## Scripts

| Script | Purpose |
| --- | --- |
| [`WILD_PreProcess.m`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_PreProcess.m) | Generate corrected headers, timing files, and event outputs. |
| [`WILD_PreProcessFolder.m`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_PreProcessFolder.m) | Process multiple recordings. |
| [`WILD_ReadHeader.m`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_ReadHeader.m) | Read WILD parameter headers. |
| [`WILD_processIMU.m`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_processIMU.m) | Process IMU data. |
| [`WILD_scaleIMU.m`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_scaleIMU.m) | Scale IMU signals. |
| [`WILD_genIntanHeader.m`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_genIntanHeader.m) | Generate Intan-compatible header output. |

## Minimal Workflow

```matlab
recording_path = "C:\WILD\example_recording";
WILD_PreProcess(recording_path);
WILD_processIMU(fullfile(recording_path, "analogin.dat"), 100);
```

Adjust paths and sampling assumptions for your recording mode.
