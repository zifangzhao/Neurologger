# Software

Use this section to install WILD_console, run acquisition workflows, export SD-card recordings, and process data for analysis.

## Software Components

<div class="wild-grid two">
  <div class="wild-card">
    <h3>WILD_console</h3>
    <p>Windows GUI for BLE connection, synchronization, recording setup, selected preview display, closed-loop configuration, and SD-card export.</p>
  </div>
  <div class="wild-card">
    <h3>Artificial Intelligence</h3>
    <p>Curated embedded models for validated closed-loop releases, with generic model loading not yet part of the stable workflow.</p>
  </div>
  <div class="wild-card">
    <h3>API and CLI operations</h3>
    <p>Use documented operations for data export, batch post-processing, video/audio decoding, GPIO logging, and validation utilities.</p>
  </div>
  <div class="wild-card">
    <h3>Analysis scripts</h3>
    <p>MATLAB and Python scripts for headers, timing, IMU processing, video decoding, and downstream analysis.</p>
  </div>
</div>

## Install

Download WILD_console from the [latest GitHub release](https://github.com/zifangzhao/Neurologger/releases/latest). The link always opens the newest published WILD release.

## Requirements

- Windows 10 or later.
- .NET Framework 4.8 for the current GUI.
- Bluetooth 4.0 or later.
- Administrator privileges for some SD formatting workflows.

## Optional Runtime Files

- `dll_upfirdn.dll` for resampling.
- WILD BLE backend DLL for BLE support in older installer layouts.
- `ffmpeg.exe` for some camera processing workflows.
