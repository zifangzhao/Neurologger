# Firmware Flashing

WILD uses a bootloader plus application-image workflow. The first flash programs the bootloader; later firmware updates can be staged through the microSD card.

## First-time Bootloader Flash

1. Connect the 4-pin IO-USB cable, but do not connect the cable to the PC yet.
2. Short the DFU mode select pin to VDD.
3. Connect USB to the PC while holding the short.
4. Release the short after the device powers up.
5. Open STM32CubeProgrammer.
6. Flash the bootloader image from [Firmware](https://github.com/ayalab1/Neurologger/tree/main/Firmware).

## Application Update from microSD

1. Format the microSD card from WILD_console.
2. Copy the application image to the card.
3. Insert the card into WILD.
4. Power the device.
5. Wait for the bootloader LED pattern to finish. The current guide notes that application upgrade takes about 10 seconds, depending on image size.

## Firmware References

- Current repository release images are in [Firmware](https://github.com/ayalab1/Neurologger/tree/main/Firmware).
- The CE64 reference project uses STM32 firmware sources and Keil MDK project files.
- Keep a record of the firmware image used for each experiment so analysis metadata can be traced later.
