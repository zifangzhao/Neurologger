# PCB

The repository contains fabrication and assembly packages for the datalogger, opto module, and camera unit.

## Fabrication Files

| Board | Files |
| --- | --- |
| Datalogger | [Gerbers, drill files, assembly files](https://github.com/zifangzhao/Neurologger/tree/main/PCB/Datalogger) |
| Opto module | [Gerbers, drill files, assembly files](https://github.com/zifangzhao/Neurologger/tree/main/PCB/Optomodule) |
| Camera unit | [Gerbers, drill files, assembly files](https://github.com/zifangzhao/Neurologger/tree/main/PCB/CameraUnit) |

## Manufacturing Notes

- Review PCB stackup, impedance constraints, and connector orientation before ordering.
- Confirm component availability against the assembly files.
- Inspect the microSD socket, battery connector, BLE UART pins, sensor connectors, and stimulation output path after assembly.
- Keep manufacturing revisions tied to compatible release images.

## Recommended Public Additions

- Board render images for top and bottom layers.
- A short bring-up checklist after assembly.
- Known-good manufacturer settings.
- Revision history table mapping PCB revisions to release-image compatibility.
