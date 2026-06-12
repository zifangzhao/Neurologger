# Software

WILD software covers device control, synchronization, live preview, SD-card export, and post-processing entry points.

## Software Components

<div class="wild-grid two">
  <div class="wild-card">
    <h3>WILD_console</h3>
    <p>Windows GUI for BLE connection, synchronization, recording setup, selected preview display, closed-loop configuration, and SD-card export.</p>
  </div>
  <div class="wild-card">
    <h3>Artificial Intelligence</h3>
    <p>Pre-compiled embedded AI models with careful RAM, timing, and firmware integration review; generic model support is under development.</p>
  </div>
  <div class="wild-card">
    <h3>API and CLI operations</h3>
    <p>Current tool operations cover data export, batch post-processing, video/audio decoding, GPIO logging, and development utilities.</p>
  </div>
  <div class="wild-card">
    <h3>Analysis scripts</h3>
    <p>MATLAB and Python scripts for headers, timing, IMU processing, video decoding, and downstream analysis.</p>
  </div>
</div>

## Install

Download the latest WILD_console installer from [Software](https://github.com/zifangzhao/Neurologger/tree/main/Software). Public documentation uses the WILD name even when internal source folders use older development names.

## Requirements

- Windows 10 or later.
- .NET Framework 4.8 for the current GUI.
- Bluetooth 4.0 or later.
- Administrator privileges for some SD formatting workflows.

## Optional Runtime Files

- `dll_upfirdn.dll` for resampling.
- WILD BLE backend DLL for BLE support in older installer layouts.
- `ffmpeg.exe` for some camera processing workflows.
