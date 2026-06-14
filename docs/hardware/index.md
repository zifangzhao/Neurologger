# Hardware

Hardware documentation covers the WILD device architecture, board fabrication assets, mechanical assembly, power choices, and release-image compatibility for each supported device revision.

<div class="wild-grid two">
  <div class="wild-card">
    <h3>Device Overview</h3>
    <p>Core device specifications, supported modalities, local storage path, wireless control, and closed-loop output paths.</p>
  </div>
  <div class="wild-card">
    <h3>PCB</h3>
    <p>Board packages, fabrication outputs, assembly files, revision notes, and inspection points for manufactured boards.</p>
  </div>
  <div class="wild-card">
    <h3>Mechanical</h3>
    <p>Printable parts, baseplates, camera mounts, enclosure orientation, and fit checks for head-mounted assemblies.</p>
  </div>
  <div class="wild-card">
    <h3>Power</h3>
    <p>Battery and microSD guidance covering boot current, recording runtime, preview load, stimulation, and camera use.</p>
  </div>
  <div class="wild-card">
    <h3>Release Images</h3>
    <p>Validated WILD device images linked to compatible hardware revisions and experiment metadata.</p>
  </div>
</div>

## Hardware Asset Map

| Hardware area | Repository path |
| --- | --- |
| Datalogger PCB | [PCB/Datalogger](https://github.com/ayalab1/Neurologger/tree/main/PCB/Datalogger) |
| Opto module | [PCB/Optomodule](https://github.com/ayalab1/Neurologger/tree/main/PCB/Optomodule) |
| Camera unit | [PCB/CameraUnit](https://github.com/ayalab1/Neurologger/tree/main/PCB/CameraUnit) |
| Mechanical parts | [3Dprint](https://github.com/ayalab1/Neurologger/tree/main/3Dprint) |
| Battery table | [LipoBattery_selection.csv](https://github.com/ayalab1/Neurologger/blob/main/docs/LipoBattery_selection.csv) |
| Prebuilt device images | [Latest GitHub release](https://github.com/ayalab1/Neurologger/releases/latest) |

## Compatibility Record

Document the following for each supported WILD hardware build or dataset:

| Record | Why it matters |
| --- | --- |
| PCB or device revision | Distinguishes connector layout, sensor options, and supported release images. |
| Release tag and image filename | Ties behavior to a reproducible device image. |
| WILD_console version | Defines the export and control tool behavior used in the session. |
| SD card model | Affects boot reliability and long-session write stability. |
| Battery model | Affects boot margin, runtime, and peak-load behavior. |
| Enabled modalities | States whether the session used ephys, IMU, audio, video, stimulation, or external sync. |

## Bring-Up Checklist

Before the first recording on a newly assembled WILD device:

1. Confirm the intended release image and hardware revision match.
2. Confirm battery polarity and boot stability.
3. Confirm microSD insertion and basic discoverability.
4. Confirm BLE connection and synchronization state.
5. Run a short recording, export it, and verify the expected files before any animal session.

## Visual Asset Policy

Public hardware visuals are limited to real WILD device material: device photographs, CAD or EDA exports, microscope images, measured drawings, screenshots from project tools, or hand-authored diagrams derived from measured hardware. AI-generated device photographs or device-like renders are excluded from WILD hardware documentation.
