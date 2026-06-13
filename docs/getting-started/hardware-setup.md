# Hardware Setup

This checklist covers the physical preparation before connecting WILD to software.

## Device and Connectors

Connector images identify the stimulation, auxiliary, sensor, sync, and battery interfaces before board power-up.

![WILD connector overview](../images/WIrelessEphys_Github_8_connectors.jpg){ .wild-readable-figure }

The WILD device uses these connectors to keep acquisition, storage, wireless control, synchronization, and optional stimulation in a compact head-mounted unit. Before powering the device, confirm which interfaces are actually part of the planned session.

## Preparation Checklist

1. Inspect the PCB and connectors for visible damage.
2. Confirm battery polarity on the JST-SH connector.
3. Insert a tested microSD card.
4. Confirm the recording probe or flexible-probe connection.
5. Confirm the stimulation output, IMU, microphone, camera, and external sync connections needed for the experiment.
6. Confirm the device is running the expected released device image for the experiment.

## microSD Card

Format the card from WILD_console before recording. The microSD card affects both reliability and power draw.

![microSD power comparison](../images/WIrelessEphys_Github_10_SDcard_power.jpg){ .wild-readable-figure }

Battery and SD guidance are part of the experimental protocol, not optional accessory setup.

![Battery examples](../images/WIrelessEphys_Github_9_batteries.jpg){ .wild-readable-figure }

## Released Device Image

Public setup documentation is based on prebuilt WILD release images. The release image is matched to the hardware revision and experimental configuration, with the release tag and image filename kept in dataset metadata.

Release images are distributed through the [latest GitHub release](https://github.com/ayalab1/Neurologger/releases/latest). Follow the release notes for the specific image used in the experiment.

Treat the released device image as part of the hardware setup record. The WILD device, WILD_console version, SD card, battery, and analysis scripts should all be traceable to the dataset.
