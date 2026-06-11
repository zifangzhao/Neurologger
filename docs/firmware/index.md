# Firmware

WILD firmware coordinates sensor acquisition, local storage, BLE control, closed-loop DSP, stimulation outputs, and application updates.

## Reference Firmware Tree

The current public release binaries live in [Firmware](https://github.com/ayalab1/Neurologger/tree/main/Firmware). The CE64 reference project contains STM32 sources and Keil MDK project files used for WILD64-style firmware development.

## Firmware Topics

<div class="wild-grid two">
  <div class="wild-card">
    <h3>Architecture</h3>
    <p>Bootloader, application image, acquisition pipeline, storage, BLE, DSP, stimulation, and sensor tasks.</p>
  </div>
  <div class="wild-card">
    <h3>Build Instructions</h3>
    <p>Toolchain setup, project files, build outputs, and release image handling.</p>
  </div>
  <div class="wild-card">
    <h3>BLE</h3>
    <p>Wireless discovery, command and status messages, preview streaming, and synchronization behavior.</p>
  </div>
  <div class="wild-card">
    <h3>DSP</h3>
    <p>Online filtering, arbitrary referencing, Hilbert modes, thresholds, and stimulation triggers.</p>
  </div>
</div>

!!! warning "Version discipline"
    Firmware behavior should be documented with the exact binary name or commit hash used for validation.
