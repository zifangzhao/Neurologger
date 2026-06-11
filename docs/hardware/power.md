# Power

Power planning is central to WILD experiments because battery selection, microSD choice, recording mode, preview streaming, stimulation, and camera use all affect runtime.

## Battery

The current usage guide notes that WILD accepts a wide battery input range and requires enough peak power during boot.

![Battery examples](../images/WIrelessEphys_Github_9_batteries.jpg)

Use the [battery selection table](https://github.com/ayalab1/Neurologger/blob/main/docs/LipoBattery_selection.csv) as the starting point for runtime planning.

## microSD Power

microSD choice can affect power consumption and reliability. Format cards with WILD_console before recording.

![microSD power comparison](../images/WIrelessEphys_Github_10_SDcard_power.jpg)

## Documentation Targets

Add validated runtime tables for:

- Neural-only recording.
- Neural plus IMU.
- Neural plus camera.
- Closed-loop stimulation sessions.
- Outdoor or long-duration experiments.

Each table should include firmware version, SD card model, battery model, sampling mode, preview-streaming state, and ambient conditions.
