# Live Visualization

WILD_console includes a real-time display for previewing selected neural and auxiliary signals during recording.

The live view is a monitoring and control tool. It should not be described as the main recording path for high-channel-count data; full-resolution recordings are written locally to the device microSD card.

![WILD online API and live display](../images/WIrelessEphys_Github_4_onlineAPI.jpg){ .wild-readable-figure }

## Display Controls

- Select neural preview channels.
- Select auxiliary signals from IMU and DSP outputs.
- Adjust display length.
- Adjust display gain.
- Show threshold overlays when closed-loop channels are selected.
- Monitor internal state, stimulation triggers, DSP state, and TinyML state messages.

## Power and Bandwidth

Live preview consumes device power and BLE bandwidth. Disable preview when the experiment prioritizes maximum runtime over live monitoring, and recover the full dataset from microSD after the session.

## Status Checks

- Confirm connection and TX/RX counters after BLE discovery.
- Confirm synchronization before starting a recording.
- Confirm recording state before handling the animal.
- Confirm export completion after removing the microSD card.
- Treat SD, BLE, low-battery, and release-image mismatch messages as session blockers until resolved.
