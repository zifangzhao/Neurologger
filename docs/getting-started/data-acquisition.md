# Data Acquisition

WILD_console is the main operator interface for BLE connection, recording configuration, live display, closed-loop control, and data download.

## Connect

1. Launch `WILD_console.exe`.
2. Select the WILD device from the Port drop-down. The drop-down performs BLE discovery.
3. Connect and wait for synchronization.
4. Confirm the TX/RX indicators update. If BLE connects but synchronization does not start, check the microSD card first.

## Record

1. Configure sampling speed and channels.
2. Configure closed-loop settings if stimulation or online detection is needed.
3. Use Wait for start when coordinating multiple WILD_console instances.
4. Click Recording Start.
5. Click Recording Stop when the experiment is complete.

## Live Display

The real-time view supports neural previews, auxiliary signals, IMU and DSP states, stimulation triggers, and threshold overlays.

![WILD live visualization](../images/WIrelessEphys_Github_4_onlineAPI.jpg)

Preview can be disabled to save power and BLE bandwidth.

## Download

Insert the SD card and use Save to Disk. WILD_console exports recordings into timestamped folders with neural, auxiliary, ADC, camera, metadata, and parameter files.

![WILD offline download interface](../images/WIrelessEphys_Github_5_offlineAPI.jpg)
