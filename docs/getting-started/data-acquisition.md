# Data Acquisition

WILD_console is the main operator interface for BLE connection, synchronization, recording configuration, low-bandwidth live preview, closed-loop control, and SD-card export.

WILD is a local-storage neurologger: high-bandwidth neural and multimodal data are written to the microSD card on the device. BLE supports setup, timing calibration, status messages, command delivery, and selected preview signals.

## Connect

1. Launch `WILD_console.exe`.
2. Select the WILD device from the Port drop-down. The drop-down performs BLE discovery.
3. Connect and wait for synchronization.
4. Confirm the TX/RX indicators update. If BLE connects but synchronization does not start, check the microSD card and timing setup first.

## Record

1. Configure sampling speed and channels.
2. Configure closed-loop settings if stimulation or online detection is needed.
3. Use Wait for start when coordinating multiple WILD_console instances.
4. Click Recording Start to begin local logging on the device.
5. Click Recording Stop when the experiment is complete.

## Live Display

The real-time view supports selected neural previews, auxiliary signals, IMU and DSP states, stimulation triggers, and threshold overlays.

![WILD live visualization](../images/WIrelessEphys_Github_4_onlineAPI.jpg){ .wild-readable-figure }

Disable preview to save power and BLE bandwidth when live monitoring is not needed. Recover full-resolution recording data from the microSD card after the session.

## Download

Insert the SD card and use Save to Disk. WILD_console exports recordings into timestamped folders with neural, auxiliary, ADC, camera, metadata, and parameter files.

![WILD offline download interface](../images/WIrelessEphys_Github_5_offlineAPI.jpg){ .wild-readable-figure }
