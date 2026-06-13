# PCB

Board packages support ordering, assembly, and inspection for WILD hardware revisions.

## Fabrication Files

| Board | Files |
| --- | --- |
| Datalogger | [Gerbers, drill files, assembly files](https://github.com/ayalab1/Neurologger/tree/main/PCB/Datalogger) |
| Opto module | [Gerbers, drill files, assembly files](https://github.com/ayalab1/Neurologger/tree/main/PCB/Optomodule) |
| Camera unit | [Gerbers, drill files, assembly files](https://github.com/ayalab1/Neurologger/tree/main/PCB/CameraUnit) |

## Manufacturing Notes

- Review PCB stackup, impedance constraints, and connector orientation before ordering.
- Confirm component availability against the assembly files.
- Inspect the microSD socket, battery connector, BLE UART pins, sensor connectors, and stimulation output path after assembly.
- Keep manufacturing revisions tied to compatible release images.

## Assembly Checks

- Confirm top and bottom orientation against the board files.
- Inspect connectors, solder joints, and the microSD socket before power-up.
- Keep the PCB revision with the experiment metadata.
- Match each board revision to a compatible release image.
