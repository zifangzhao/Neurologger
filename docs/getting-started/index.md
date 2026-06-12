# Getting Started

WILD setup has three practical stages: prepare the hardware, record data, and run post-processing.

<div class="wild-grid two">
  <div class="wild-card">
    <h3>1. Hardware setup</h3>
    <p>Check the device, connectors, microSD card, battery, probe or sensor cabling, and confirm the matching release image for the experiment.</p>
  </div>
  <div class="wild-card">
    <h3>2. Data acquisition</h3>
    <p>Use WILD_console for BLE discovery, synchronization, recording configuration, closed-loop control, and data export.</p>
  </div>
  <div class="wild-card">
    <h3>3. Data analysis</h3>
    <p>Generate compatible headers and timing files, decode camera streams, process IMU data, and prepare spike-sorting inputs.</p>
  </div>
</div>

## Before You Begin

- Windows 10 or later for WILD_console.
- Bluetooth 4.0 or later for BLE control.
- A tested microSD card. The current user guide recommends Samsung EVO series or Lexar cards and warns that some SanDisk cards may be unreliable.
- A battery that can provide the required peak current during boot and recording.

## Repository Assets

| Asset | Location |
| --- | --- |
| Prebuilt device images | [Latest GitHub release](https://github.com/zifangzhao/Neurologger/releases/latest) |
| WILD_console installers | [Latest GitHub release](https://github.com/zifangzhao/Neurologger/releases/latest) |
| PCB fabrication files | [PCB](https://github.com/zifangzhao/Neurologger/tree/main/PCB) |
| 3D-print files | [3Dprint](https://github.com/zifangzhao/Neurologger/tree/main/3Dprint) |
| MATLAB and Python analysis scripts | [Code](https://github.com/zifangzhao/Neurologger/tree/main/Code) |

!!! tip "Recommended first path"
    If this is your first device, work through Hardware Setup, Data Acquisition, and Data Analysis in order. Most acquisition failures are easier to diagnose when the SD card, battery, release image, and boot state are known.
