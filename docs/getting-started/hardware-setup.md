# Hardware Setup

This checklist covers the physical preparation before connecting WILD to software.

## Device and Connectors

Use the connector images to identify the programming, stimulation, auxiliary, sensor, and battery interfaces before powering the board.

![WILD connector overview](../images/WIrelessEphys_Github_8_connectors.jpg){ .wild-readable-figure }

## Preparation Checklist

1. Inspect the PCB and connectors for visible damage.
2. Confirm battery polarity on the JST-SH connector.
3. Insert a tested microSD card.
4. Confirm the recording probe, stimulation output, IMU, microphone, camera, and sync connections needed for the experiment.
5. Keep the programming cable available for first-time bootloader flashing or recovery.

## microSD Card

Format the card from WILD_console before recording. The microSD card affects both reliability and power draw.

![microSD power comparison](../images/WIrelessEphys_Github_10_SDcard_power.jpg){ .wild-readable-figure }

The battery and SD guidance should be treated as part of the experimental protocol, not as optional accessory setup.

![Battery examples](../images/WIrelessEphys_Github_9_batteries.jpg){ .wild-readable-figure }

## Final Step: Firmware Flashing

Firmware flashing belongs at the end of hardware preparation because the bootloader, microSD card, battery, and programming connection must be ready before the device is used for acquisition.

### First-time Bootloader Flash

1. Connect the 4-pin IO-USB cable, but do not connect the cable to the PC yet.
2. Short the DFU mode select pin to VDD.
3. Connect USB to the PC while holding the short.
4. Release the short after the device powers up.
5. Open STM32CubeProgrammer.
6. Flash the bootloader image from [Firmware](https://github.com/zifangzhao/Neurologger/tree/main/Firmware).

### Application Update from microSD

1. Format the microSD card from WILD_console.
2. Copy the application image to the card.
3. Insert the card into WILD.
4. Power the device.
5. Wait for the bootloader LED pattern to finish. Application upgrade typically takes about 10 seconds, depending on image size.

### Firmware References

- Current repository release images are in [Firmware](https://github.com/zifangzhao/Neurologger/tree/main/Firmware).
- WILD firmware reference projects use STM32 firmware sources and Keil MDK project files.
- Keep a record of the firmware image used for each experiment so analysis metadata can be traced later.
