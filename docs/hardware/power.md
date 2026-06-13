# Power

Power planning is central to WILD experiments because battery selection, microSD choice, recording mode, selected preview signals, stimulation, and camera use all affect runtime.

## Power Architecture

The WILD device conditions the selected battery through a converter and regulator chain before powering analog acquisition, digital control, and peripheral subsystems. Battery choice should therefore follow the validated hardware-revision guidance rather than a single nominal-voltage number.

Boot, microSD writes, camera use, stimulation, and live preview can create different peak-load conditions. Validate the complete experiment mode on the bench before using a battery in an animal session.

## Battery

The WILD device should use a battery approved for the specific hardware revision and experiment mode. Before mounting the device, confirm that the battery can boot the device without voltage sag, start recording, and sustain the planned sensors, preview state, stimulation, or camera load.

![Battery examples](../images/WIrelessEphys_Github_9_batteries.jpg){ .wild-readable-figure }

The [battery selection table](https://github.com/ayalab1/Neurologger/blob/main/docs/LipoBattery_selection.csv) provides baseline capacity and runtime-planning references.

## microSD Power

The microSD card is part of the power and reliability budget. Format cards with WILD_console before recording, and validate the selected card in the same sampling and modality mode planned for the experiment.

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
