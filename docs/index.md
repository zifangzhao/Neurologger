---
hide:
  - navigation
  - toc
---

<section class="wild-hero">
  <div>
    <h1>A wireless modular platform for neuro-behavioral recording and closed-loop manipulation in small animals</h1>
    <p>Wireless, Interactive, Lightweight Datalogger (WILD) is an ultra-lightweight multimodal neurologger for local neural data logging, behavioral sensing, onboard processing, and responsive stimulation in freely behaving animals.</p>
    <div class="wild-actions">
      <a class="md-button md-button--primary" href="getting-started/">Get Started</a>
      <a class="md-button" href="hardware/">Hardware</a>
      <a class="md-button" href="software/">Software</a>
      <a class="md-button" href="https://github.com/zifangzhao/Neurologger">GitHub</a>
    </div>
    <div class="wild-signal-row">
      <span>64-Channel electrophysiology</span>
      <span>Closed-loop DSP</span>
      <span>9-axis IMU</span>
      <span>USV audio</span>
      <span>Camera</span>
    </div>
  </div>
  <figure class="wild-hero-media">
    <img src="images/WIrelessEphys_Github_1_devicePicture.jpg" alt="WILD wireless modular datalogger device">
    <figcaption class="wild-caption">WILD integrates local neural recording, behavioral monitoring, real-time embedded processing, microSD storage, and wireless control in a compact platform for naturalistic systems neuroscience experiments.</figcaption>
  </figure>
</section>

<section class="wild-zoom-tour" aria-label="WILD device zoom tour">
  <div class="wild-zoom-stage" aria-live="polite">
    <h2 id="wild-zoom-title">Embedded control at the headstage</h2>
    <p id="wild-zoom-description">The MCU, IMU, and board-level control electronics sit close to the animal, reducing external cabling while keeping timing-sensitive acquisition local.</p>
    <figure class="wild-zoom-frame">
      <img id="wild-zoom-device" src="images/WIrelessEphys_Github_1_devicePicture.jpg" alt="Real WILD device with labeled functional regions">
      <figcaption id="wild-zoom-label">MCU and IMU</figcaption>
    </figure>
  </div>

  <div class="wild-zoom-scroll" aria-hidden="true">
    <div class="wild-zoom-step" data-zoom-label="MCU and IMU" data-zoom-x="10%" data-zoom-y="10%" data-zoom-scale="2.5" data-zoom-title="Embedded control at the headstage" data-zoom-description="The MCU, IMU, and board-level control electronics sit close to the animal, reducing external cabling while keeping timing-sensitive acquisition local."></div>
    <div class="wild-zoom-step" data-zoom-label="microSD storage" data-zoom-x="10%" data-zoom-y="62%" data-zoom-scale="2.35" data-zoom-title="Local storage for long sessions" data-zoom-description="Recording data is stored on-device, preserving full-resolution datasets for long sessions while BLE remains available for control and preview."></div>
    <div class="wild-zoom-step" data-zoom-label="Amplifier and electrode pads" data-zoom-x="43%" data-zoom-y="82%" data-zoom-scale="2.3" data-zoom-title="Neural interface and probe connection" data-zoom-description="Amplifier and electrode-pad regions route neural signals into the acquisition stack for downstream preprocessing and analysis."></div>
    <div class="wild-zoom-step" data-zoom-label="Ext IO and battery connectors" data-zoom-x="47%" data-zoom-y="0%" data-zoom-scale="2.5" data-zoom-title="Modular power and IO" data-zoom-description="Connector regions support external modules, battery connection, synchronization, and configuration workflows for different experiment designs."></div>
    <div class="wild-zoom-step" data-zoom-label="Camera and microphone" data-zoom-x="115%" data-zoom-y="70%" data-zoom-scale="1.8" data-zoom-title="Behavioral sensing add-ons" data-zoom-description="Camera and microphone modules extend WILD from neural recording into synchronized neuro-behavioral datasets."></div>
  </div>
</section>

<section class="wild-section">
  <h2>Key Features</h2>
  <p>WILD is organized around field-ready neural data collection with a path from hardware assembly to analysis.</p>
  <div class="wild-grid">
    <div class="wild-card">
      <h3>Local Neural Logging</h3>
      <p>High-bandwidth electrophysiology is recorded locally to microSD, while BLE supports setup, synchronization, status, and low-bandwidth preview.</p>
    </div>
    <div class="wild-card">
      <h3>Responsive Stimulation</h3>
      <p>Onboard biomarker detection and behavioral classification can trigger stimulation without requiring continuous wireless data streaming.</p>
    </div>
    <div class="wild-card">
      <h3>TinyML on Edge Devices</h3>
      <p>Curated models run on the MCU through validated release images with RAM, timing, and closed-loop latency reviewed before deployment.</p>
    </div>
    <div class="wild-card">
      <h3>Multimodal Sensing</h3>
      <p>Neural signals, IMU, auxiliary inputs, ultrasonic audio, camera, and digital events.</p>
    </div>
    <div class="wild-card">
      <h3>Long-term Recording</h3>
      <p>Local storage, low power operations, and robust export tools for naturalistic studies.</p>
    </div>
  </div>
</section>

<section class="wild-section">
  <h2>System Overview</h2>
  <p>The documentation follows the same path as an experiment: assemble the device, record data locally, synchronize sessions, and analyze exported files.</p>
  <div class="wild-system-panels">
    <div class="wild-flow wild-flow-vertical" aria-label="WILD system overview">
      <div>Animal</div>
      <div>Device</div>
      <div>Sensors</div>
      <div>Storage</div>
      <div>Synchronization</div>
      <div>Analysis</div>
    </div>
    <figure class="wild-image-frame wild-system-figure">
      <img src="images/WIrelessEphys_Github_2_deviceDiagram.jpg" alt="WILD system diagram">
    </figure>
  </div>
</section>

<section class="wild-section">
  <h2>Research Highlights</h2>
  <div class="wild-grid">
    <div class="wild-card">
      <h3>Outdoor recordings</h3>
      <p>Local storage, low-power modes, and wireless control support recordings in large naturalistic environments where tethering is impractical.</p>
    </div>
    <div class="wild-card">
      <h3>Multi-animal experiments</h3>
      <p>Wired sync, BLE calibration, and clock correction workflows coordinate multiple WILD devices and external systems.</p>
    </div>
    <div class="wild-card">
      <h3>Ripple detection</h3>
      <p>DSP filters include ripple-band detection for closed-loop hippocampal experiments.</p>
    </div>
    <div class="wild-card">
      <h3>Theta phase stimulation</h3>
      <p>Hilbert and filter modes support phase-aware online control designs.</p>
    </div>
    <div class="wild-card">
      <h3>Naturalistic behavior</h3>
      <p>IMU, video, USV, and neural data support studies of social interaction, outdoor navigation, and other freely expressed behaviors.</p>
    </div>
    <div class="wild-card">
      <h3>Open hardware iteration</h3>
      <p>PCB, mechanical, release-image, software, and analysis assets are kept in the public repository.</p>
    </div>
  </div>
</section>

<section class="wild-section wild-quickstart">
  <h2>Quick Start</h2>
  <div class="wild-grid two">
    <div class="wild-card wild-step">
      <h3>Hardware setup</h3>
      <p>Review connectors, battery polarity, microSD recommendations, probe or sensor cabling, then confirm the matching release image for the experiment.</p>
    </div>
    <div class="wild-card wild-step">
      <h3>Data acquisition</h3>
      <p>Install WILD_console, connect over BLE, synchronize the device, configure recording and closed-loop settings, then start local logging.</p>
    </div>
    <div class="wild-card wild-step">
      <h3>Data analysis</h3>
      <p>Export recordings, generate Intan-style files, process IMU and camera data, and prepare spike-sorting inputs.</p>
    </div>
  </div>
</section>

<section class="wild-section">
  <h2>Publications and Citation</h2>
  <div class="wild-grid two">
    <div class="wild-card">
      <h3>Platform manuscript</h3>
      <p>The WILD platform manuscript is currently under review.</p>
    </div>
    <div class="wild-card">
      <h3>Repository and release versions</h3>
      <p>Report the hardware revision, release image, WILD_console version, and analysis scripts used for each dataset.</p>
    </div>
  </div>

```bibtex
@article{zhao_wild_neurologger,
  title        = {A wireless modular platform for neuro-behavioral recording and closed-loop manipulation in small animals},
  author       = {Zhao, Zifang and Chang, Hongyu and Paudel, Praveen and Park, Jaehyo and Liu, Can and Aurelio, Maria Q. and Oliva, Azahara and Fernandez-Ruiz, Antonio},
  year         = {2026},
  note         = {Under review}
}
```
</section>

<section class="wild-section">
  <h2>Community</h2>
  <div class="wild-grid">
    <div class="wild-card">
      <h3>GitHub</h3>
      <p><a href="https://github.com/zifangzhao/Neurologger">Browse hardware files, release images, WILD_console installers, and analysis scripts.</a></p>
    </div>
    <div class="wild-card">
      <h3>Discussions</h3>
      <p>Use GitHub Discussions for experiment design questions, integration planning, and troubleshooting.</p>
    </div>
    <div class="wild-card">
      <h3>Contributing</h3>
      <p><a href="contributing/">Open an issue or pull request with hardware notes, analysis examples, compatibility reports, or documentation improvements.</a></p>
    </div>
  </div>
</section>
