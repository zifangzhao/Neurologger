# Power

Power planning is central to WILD experiments because battery selection, microSD choice, recording mode, selected preview signals, stimulation, and camera use all affect runtime.

## Battery

The current usage guide notes that WILD accepts a wide battery input range and requires enough peak power during boot.

![Battery examples](../images/WIrelessEphys_Github_9_batteries.jpg){ .wild-readable-figure }

Use the [battery selection table](https://github.com/zifangzhao/Neurologger/blob/main/docs/LipoBattery_selection.csv) as the starting point for runtime planning.

## microSD Power

microSD choice can affect power consumption and reliability. Format cards with WILD_console before recording.

![microSD power comparison](../images/WIrelessEphys_Github_10_SDcard_power.jpg){ .wild-readable-figure }

## Runtime Reporting

Runtime depends on sampling rate, active modalities, preview state, stimulation use, microSD card model, battery capacity, and ambient conditions. When reporting a WILD recording mode, include:

- Release image.
- SD card model and format state.
- Battery model and capacity.
- Sampling rate and enabled modalities.
- Preview state.
- Stimulation or TinyML state, if used.
- Session environment, especially for outdoor or long-duration recordings.
