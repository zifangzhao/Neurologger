# Data Acquisition

WILD_console is the main operator interface for BLE connection, synchronization, recording configuration, low-bandwidth live preview, closed-loop control, and SD-card export.

WILD is a local-storage neurologger: high-bandwidth neural and multimodal data are written to the microSD card on the device. BLE supports setup, timing calibration, status messages, command delivery, and selected preview signals.

The current public workflow uses WILD_console on Windows for BLE control. An iOS-based WILD controller app is in development for device discovery, connection, synchronization support, status checks, and low-bandwidth control. The iOS workflow is expected to provide more consistent BLE performance than typical PC BLE adapters, while full-resolution recordings will still be recovered from the device microSD card.

The WILD device does not need continuous full-bandwidth wireless streaming to preserve the recording. Keep BLE connected when the session needs online preview, parameter changes, or live commands; otherwise, use BLE for setup and timing coordination, then recover the full dataset from the microSD card.

!!! tip "First-session scope"
    For the first dry run, use only the minimum path needed to connect, record, stop, and export. Leave closed-loop, camera, stimulation, GPIO, and advanced parameter panels unchanged until the basic local-storage workflow is confirmed.

## First-Pass Button Path

For a basic dry run, only a small part of WILD_console is needed. The closed-loop, camera, stimulation, GPIO, and advanced parameter panels can stay unchanged until the device is already connecting, synchronizing, recording, and exporting reliably.

The online and live figures below are runtime screenshots from WILD_console during hardware sessions. Some window-title or device-list strings may still show older internal labels; the public documentation uses the WILD name consistently.

<div class="wild-operator-path">
  <div class="wild-operator-step">
    <span class="wild-button-label">Online tab</span>
    <p><strong>Connect to the device.</strong> Work in the Online tab for BLE discovery, synchronization, preview, and recording control.</p>
  </div>
  <div class="wild-operator-step">
    <span class="wild-button-label">Rescan</span>
    <p><strong>Find nearby WILD devices.</strong> If the device is not listed, rescan after confirming power, battery, and BLE status.</p>
  </div>
  <div class="wild-operator-step">
    <span class="wild-button-label">Device List</span>
    <p><strong>Select the target logger.</strong> The selected row updates device information, available space, and connection state.</p>
  </div>
  <div class="wild-operator-step">
    <span class="wild-button-label primary">Connect</span>
    <p><strong>Open the BLE session.</strong> Wait for the device state and synchronization labels before starting a recording.</p>
  </div>
  <div class="wild-operator-step">
    <span class="wild-button-label primary">Recording Start</span>
    <p><strong>Start local logging.</strong> Full-resolution data are written to the device microSD card, not streamed continuously over BLE.</p>
  </div>
  <div class="wild-operator-step">
    <span class="wild-button-label">Recording Stop</span>
    <p><strong>Close the recording cleanly.</strong> Stop before removing power or taking out the microSD card.</p>
  </div>
  <div class="wild-operator-step">
    <span class="wild-button-label">Offline tab</span>
    <p><strong>Move to export after recording.</strong> Insert the microSD card into the PC and use the Offline tab for SD-card download.</p>
  </div>
  <div class="wild-operator-step">
    <span class="wild-button-label primary">Save to Disk</span>
    <p><strong>Export the recording folder.</strong> WILD_console decodes the SD-card recording into the public analysis files.</p>
  </div>
</div>

<p class="wild-operator-note">
  First-session rule: ignore <span class="wild-button-label muted">Closed-loop</span>, <span class="wild-button-label muted">Camera</span>, <span class="wild-button-label muted">Advanced</span>, and parameter panels until a simple recording can be started, stopped, and exported.
</p>

![WILD_console runtime screenshot during connected acquisition](../images/WIrelessEphys_Github_4_onlineAPI.jpg){ .wild-readable-figure }

## Connect

1. Launch `WILD_console.exe`.
2. Click <span class="wild-button-label">Rescan</span> if the device is not listed.
3. Select the WILD device from <span class="wild-button-label">Device List</span>.
4. Click <span class="wild-button-label primary">Connect</span> and wait for device-state and synchronization updates.
5. Confirm the TX/RX indicators update. If BLE connects but synchronization does not start, check the microSD card and timing setup first.

**Expected signs of success**

- The device appears in the list after rescan.
- The selected row updates device information.
- Connect succeeds without repeated disconnect loops.
- Status labels move past simple discovery into an active connected state.

## Record

1. Confirm the expected sampling speed and channels.
2. Leave closed-loop and camera settings unchanged unless the experiment needs them.
3. Use `Wait for start` only when coordinating multiple WILD_console instances.
4. Click <span class="wild-button-label primary">Recording Start</span> to begin local logging on the device.
5. Click <span class="wild-button-label">Recording Stop</span> when the experiment is complete.

**Expected signs of success**

- Recording starts without a parameter or storage error.
- The session duration advances normally.
- The device remains stable through stop.
- Exported files are longer than a trivial test header and have plausible file sizes.

## Field Validation

Before a field or multi-animal session, run a short dry run with every WILD device that will be used.

1. Connect each device and confirm it reaches the synchronized state.
2. Start and stop a short local recording on each device.
3. Export the SD card immediately and confirm expected duration, file size, and representative channels.
4. Use the release image specified for the experiment and hardware revision.
5. For multi-device sessions, repeat the dry run with the planned start order, external I/O wiring, and any camera or TTL sync source attached.

A connected or synchronized GUI state is not, by itself, proof that data were written for the full intended duration. Treat unexpectedly short files, stalled file-size indicators, unstable offsets, frame drops, or missing channels as blockers before animal recordings.

## Live Display

The real-time view supports selected neural previews, auxiliary signals, IMU and DSP states, stimulation triggers, and threshold overlays. See [Live Visualization](../software/live-visualization.md) for the runtime preview screenshot and display controls.

Disable preview to save power and BLE bandwidth when live monitoring is not needed. Recover full-resolution recording data from the microSD card after the session.

## Download

Insert the SD card and click <span class="wild-button-label primary">Save to Disk</span>. WILD_console exports recordings into timestamped folders with neural, auxiliary, ADC, camera, metadata, and parameter files.

**Expected signs of success**

- Export finishes without stopping at the first folder.
- Core files appear in the export folder: `amplifier.dat`, `analogin.dat`, `CE_params.bin`.
- `time.dat` and `info.rhd` are generated by the documented preprocessing path.
- Optional `adc.dat` and `misc.dat` appear only when audio or camera were enabled.

<p class="wild-operator-note">
  Normal export does not require the red maintenance buttons. <span class="wild-button-label warning">Quick Format</span> is only for preparing a known empty card, and release-image maintenance is outside the routine recording path.
</p>

![WILD_console runtime screenshot of the offline export workflow](../images/WIrelessEphys_Github_5_offlineAPI.jpg){ .wild-readable-figure }

## Common Blockers

| Symptom | First check |
| --- | --- |
| Device not listed after rescan | Battery, power, BLE discoverability, and whether the expected release image is installed. |
| BLE connects but synchronization never settles | microSD presence, timing wiring, and whether the session is waiting on external sync conditions. |
| Recording starts but export is unexpectedly short | Stop sequence, SD-card write stability, battery stability, and whether the device remained powered through the run. |
| Export folder is missing expected files | Recording mode, whether audio or camera were enabled, and whether preprocessing was run after export. |
| Preview is unstable | Treat preview as optional; confirm local recording first, then revisit BLE preview bandwidth or adapter quality. |
