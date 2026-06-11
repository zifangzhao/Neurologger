# Hardware Setup

This checklist covers the physical preparation before connecting WILD to software.

## Device and Connectors

Use the connector images to identify the programming, stimulation, auxiliary, sensor, and battery interfaces before powering the board.

![WILD connector overview](../images/WIrelessEphys_Github_8_connectors.jpg)

## Preparation Checklist

1. Inspect the PCB and connectors for visible damage.
2. Confirm battery polarity on the JST-SH connector.
3. Insert a tested microSD card.
4. Confirm the recording probe, stimulation output, IMU, microphone, camera, and sync connections needed for the experiment.
5. Keep the programming cable available for first-time bootloader flashing or recovery.

## microSD Card

Format the card from WILD_console before recording. The microSD card affects both reliability and power draw.

![microSD power comparison](../images/WIrelessEphys_Github_10_SDcard_power.jpg)

The battery and SD guidance should be treated as part of the experimental protocol, not as optional accessory setup.

![Battery examples](../images/WIrelessEphys_Github_9_batteries.jpg)
