# Hardware

WILD hardware documentation should let a new lab understand the device, manufacture boards, assemble mechanical parts, choose safe power options, and connect each hardware revision to a validated release image.

<div class="wild-grid two">
  <div class="wild-card">
    <h3>Device Overview</h3>
    <p>System-level description of the head-mounted logger, sensors, storage, wireless control, and closed-loop outputs.</p>
  </div>
  <div class="wild-card">
    <h3>PCB</h3>
    <p>Board files, Gerbers, assembly files, fabrication notes, and inspection checks.</p>
  </div>
  <div class="wild-card">
    <h3>Mechanical</h3>
    <p>3D-print files, baseplates, camera mounts, and enclosure considerations.</p>
  </div>
  <div class="wild-card">
    <h3>Power</h3>
    <p>Battery selection, microSD power draw, boot current, and long-duration recording constraints.</p>
  </div>
  <div class="wild-card">
    <h3>Release Images</h3>
    <p>Ready-to-use device images, hardware compatibility, and release-version discipline.</p>
  </div>
</div>

## Hardware Asset Map

| Hardware area | Repository path |
| --- | --- |
| Datalogger PCB | [PCB/Datalogger](https://github.com/zifangzhao/Neurologger/tree/main/PCB/Datalogger) |
| Opto module | [PCB/Optomodule](https://github.com/zifangzhao/Neurologger/tree/main/PCB/Optomodule) |
| Camera unit | [PCB/CameraUnit](https://github.com/zifangzhao/Neurologger/tree/main/PCB/CameraUnit) |
| Mechanical parts | [3Dprint](https://github.com/zifangzhao/Neurologger/tree/main/3Dprint) |
| Battery table | [LipoBattery_selection.csv](https://github.com/zifangzhao/Neurologger/blob/main/docs/LipoBattery_selection.csv) |
| Prebuilt device images | [Latest GitHub release](https://github.com/zifangzhao/Neurologger/releases/latest) |

## Visual Asset Policy

Hardware visuals on the public site should be traceable to real WILD material: device photographs, CAD or EDA exports, microscope images, measured drawings, screenshots from project tools, or hand-authored diagrams derived from measured hardware. AI-generated device photographs or device-like renders should not be used for WILD hardware.
