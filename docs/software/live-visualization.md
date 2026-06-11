# Live Visualization

WILD_console includes a real-time display for previewing neural and auxiliary signals during recording.

![WILD online API and live display](../images/WIrelessEphys_Github_4_onlineAPI.jpg)

## Display Controls

- Select neural preview channels.
- Select auxiliary signals from IMU and DSP outputs.
- Adjust display length.
- Adjust display gain.
- Show threshold overlays when closed-loop channels are selected.
- Monitor internal state, stimulation triggers, DSP state, and TinyML state messages.

## Power and Bandwidth

Live preview consumes device power and BLE bandwidth. Disable preview when the experiment prioritizes maximum runtime over live monitoring.

## Documentation Targets

- Screenshots for each main acquisition panel.
- Expected status indicators during connection, sync, recording, and download.
- Failure-state examples for SD, BLE, low battery, and firmware mismatch conditions.
