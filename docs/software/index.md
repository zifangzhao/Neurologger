# Software

Software documentation covers how to connect to the WILD device, configure recordings in WILD_console, export data from the device microSD card, and process recordings for analysis.

## Software Components

<div class="wild-grid two">
  <div class="wild-card">
    <h3>WILD_console</h3>
    <p>Windows GUI for connecting to the WILD device over BLE, synchronizing the session, setting up recordings, previewing selected signals, configuring closed-loop behavior, and exporting SD-card data.</p>
  </div>
  <div class="wild-card">
    <h3>iOS controller</h3>
    <p>In-development app for WILD device discovery, BLE connection, synchronization support, status checks, and low-bandwidth control, with more consistent BLE performance expected than typical PC adapters.</p>
  </div>
  <div class="wild-card">
    <h3>Artificial Intelligence</h3>
    <p>Curated embedded models for validated closed-loop releases, with generic model loading not yet part of the stable workflow.</p>
  </div>
  <div class="wild-card">
    <h3>API and CLI operations</h3>
    <p>Documented operations for data export, batch post-processing, video/audio decoding, GPIO logging, and validation utilities.</p>
  </div>
  <div class="wild-card">
    <h3>Analysis scripts</h3>
    <p>MATLAB and Python scripts for headers, timing, IMU processing, video decoding, and downstream analysis.</p>
  </div>
</div>

## Install

Download WILD_console from the [latest GitHub release](https://github.com/ayalab1/Neurologger/releases/latest). The link always opens the newest published WILD release.

## Wireless Control

WILD_console remains the stable public control and export workflow. The iOS-based controller app is being developed as a lighter wireless-control path for BLE discovery, connection, synchronization support, status checks, and low-bandwidth commands. The iOS workflow is expected to perform better than PC BLE in many setups because it avoids variability across Windows Bluetooth adapters and drivers.

Full-resolution WILD recordings remain local to the device microSD card and are exported after the session.

## Requirements

- Windows 10 or later.
- .NET Framework 4.8 for the current GUI.
- Bluetooth 4.0 or later.
- Administrator privileges for some SD formatting workflows.

## Optional Runtime Files

- `dll_upfirdn.dll` for resampling.
- WILD BLE backend DLL for BLE support in older installer layouts.
- `ffmpeg.exe` for some camera processing workflows.
