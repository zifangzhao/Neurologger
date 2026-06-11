# Hardware

WILD hardware documentation should let a new lab understand the device, manufacture boards, assemble mechanical parts, and choose safe power options.

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
</div>

## Hardware Asset Map

| Hardware area | Repository path |
| --- | --- |
| Datalogger PCB | [PCB/Datalogger](https://github.com/ayalab1/Neurologger/tree/main/PCB/Datalogger) |
| Opto module | [PCB/Optomodule](https://github.com/ayalab1/Neurologger/tree/main/PCB/Optomodule) |
| Camera unit | [PCB/CameraUnit](https://github.com/ayalab1/Neurologger/tree/main/PCB/CameraUnit) |
| Mechanical parts | [3Dprint](https://github.com/ayalab1/Neurologger/tree/main/3Dprint) |
| Battery table | [LipoBattery_selection.csv](https://github.com/ayalab1/Neurologger/blob/main/docs/LipoBattery_selection.csv) |

## Recommended Figures

- Device photo with mass, connector labels, and scale bar.
- Exploded assembly view for the logger, battery, baseplate, probe, and optional camera.
- PCB top/bottom annotated renders.
- Power tree diagram showing battery input, regulators, SD, BLE, sensors, and stimulation rails.
