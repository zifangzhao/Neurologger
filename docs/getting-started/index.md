# Getting Started

WILD setup has four practical stages: prepare the hardware, flash firmware, record data, and run post-processing.

<div class="wild-grid two">
  <div class="wild-card">
    <h3>1. Hardware setup</h3>
    <p>Check the device, connectors, microSD card, battery, and probe or sensor cabling before powering the system.</p>
  </div>
  <div class="wild-card">
    <h3>2. Firmware flashing</h3>
    <p>Use STM32CubeProgrammer for first-time bootloader flashing and the microSD update workflow for application images.</p>
  </div>
  <div class="wild-card">
    <h3>3. Data acquisition</h3>
    <p>Use WILD_console for BLE discovery, synchronization, recording configuration, closed-loop control, and data export.</p>
  </div>
  <div class="wild-card">
    <h3>4. Data analysis</h3>
    <p>Generate compatible headers and timing files, decode camera streams, process IMU data, and prepare spike-sorting inputs.</p>
  </div>
</div>

## Before You Begin

- Windows 10 or later for WILD_console.
- Bluetooth 4.0 or later for BLE control.
- STM32CubeProgrammer for first-time bootloader flashing.
- A tested microSD card. The current user guide recommends Samsung EVO series or Lexar cards and warns that some SanDisk cards may be unreliable.
- A battery that can provide the required peak current during boot and recording.

## Repository Assets

| Asset | Location |
| --- | --- |
| Firmware releases | [Firmware](https://github.com/ayalab1/Neurologger/tree/main/Firmware) |
| WILD_console installers | [Software](https://github.com/ayalab1/Neurologger/tree/main/Software) |
| PCB fabrication files | [PCB](https://github.com/ayalab1/Neurologger/tree/main/PCB) |
| 3D-print files | [3Dprint](https://github.com/ayalab1/Neurologger/tree/main/3Dprint) |
| MATLAB and Python analysis scripts | [Code](https://github.com/ayalab1/Neurologger/tree/main/Code) |

!!! tip "Recommended first path"
    If this is your first device, work through Hardware Setup, Firmware Flashing, Data Acquisition, and Data Analysis in order. Most acquisition failures are easier to diagnose when the SD card, battery, and boot state are known.
