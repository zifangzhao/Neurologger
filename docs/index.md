---
hide:
  - navigation
  - toc
---

<section class="wild-hero">
  <div>
    <h1>WILD: Open-source Wireless Neurotechnology for Naturalistic Neuroscience</h1>
    <p>Lightweight multimodal neural recording, behavioral sensing, and closed-loop stimulation for freely behaving animals.</p>
    <div class="wild-actions">
      <a class="md-button md-button--primary" href="getting-started/">Get Started</a>
      <a class="md-button" href="hardware/">Hardware</a>
      <a class="md-button" href="software/">Software</a>
      <a class="md-button" href="https://github.com/ayalab1/Neurologger">GitHub</a>
    </div>
    <div class="wild-signal-row">
      <span>Neural electrophysiology</span>
      <span>Closed-loop DSP</span>
      <span>IMU</span>
      <span>USV audio</span>
      <span>Camera</span>
    </div>
  </div>
  <figure class="wild-hero-media">
    <img src="images/WIrelessEphys_Github_1_devicePicture.jpg" alt="WILD wireless neurologger device">
    <figcaption class="wild-caption">WILD integrates neural recording, behavioral sensing, stimulation control, local storage, and wireless configuration in a compact head-mounted platform.</figcaption>
  </figure>
</section>

<section class="wild-section">
  <h2>Key Features</h2>
  <p>WILD is organized around field-ready neural data collection with a path from hardware assembly to analysis.</p>
  <div class="wild-grid">
    <div class="wild-card">
      <h3>Wireless Recording</h3>
      <p>BLE-based setup and monitoring with local microSD recording for long sessions.</p>
    </div>
    <div class="wild-card">
      <h3>Closed-loop Stimulation</h3>
      <p>Embedded DSP filters, thresholds, and stimulation timing for online experiments.</p>
    </div>
    <div class="wild-card">
      <h3>Neuropixels Support</h3>
      <p>Documentation structure supports Neuropixels-compatible workflows and high-density probe integration.</p>
    </div>
    <div class="wild-card">
      <h3>TinyML on Edge Devices</h3>
      <p>MCU inference support for pretrained TensorFlow Lite models, with runtime loading under development.</p>
    </div>
    <div class="wild-card">
      <h3>Multimodal Sensing</h3>
      <p>Neural signals, IMU, auxiliary inputs, ultrasonic audio, camera data, and digital events.</p>
    </div>
    <div class="wild-card">
      <h3>Long-term Recording</h3>
      <p>Local storage, battery guidance, and robust export tools for naturalistic studies.</p>
    </div>
  </div>
</section>

<section class="wild-section">
  <h2>System Overview</h2>
  <p>The documentation follows the same path as an experiment: assemble the device, record from sensors, synchronize sessions, and analyze data.</p>
  <div class="wild-flow" aria-label="WILD system overview">
    <div>Animal</div>
    <div>Device</div>
    <div>Sensors</div>
    <div>Storage</div>
    <div>Synchronization</div>
    <div>Analysis</div>
  </div>
  <figure class="wild-image-frame">
    <img src="images/WIrelessEphys_Github_2_deviceDiagram.jpg" alt="WILD system diagram">
  </figure>
</section>

<section class="wild-section">
  <h2>Research Highlights</h2>
  <div class="wild-grid">
    <div class="wild-card">
      <h3>Outdoor recordings</h3>
      <p>Wireless control and local storage support naturalistic environments where tethering is impractical.</p>
    </div>
    <div class="wild-card">
      <h3>Multi-animal experiments</h3>
      <p>Synchronization workflows are documented for coordinating multiple devices and consoles.</p>
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
      <p>IMU, video, USV, and neural data can be processed together after acquisition.</p>
    </div>
    <div class="wild-card">
      <h3>Open hardware iteration</h3>
      <p>PCB, mechanical, firmware, software, and analysis assets are kept in the public repository.</p>
    </div>
  </div>
</section>

<section class="wild-section wild-quickstart">
  <h2>Quick Start</h2>
  <div class="wild-grid two">
    <div class="wild-card wild-step">
      <h3>Hardware setup</h3>
      <p>Review connectors, battery polarity, microSD recommendations, and probe or sensor cabling.</p>
    </div>
    <div class="wild-card wild-step">
      <h3>Firmware flashing</h3>
      <p>Flash the bootloader with STM32CubeProgrammer, then stage application images on the microSD card.</p>
    </div>
    <div class="wild-card wild-step">
      <h3>Data acquisition</h3>
      <p>Install WILD_console, connect over BLE, configure recording and closed-loop settings, then start logging.</p>
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
      <h3>WILD platform repository</h3>
      <p>Cite the repository while the formal platform manuscript or protocol is being prepared.</p>
    </div>
    <div class="wild-card">
      <h3>Publication cards</h3>
      <p>Add peer-reviewed articles, preprints, protocols, and datasets as they become available.</p>
    </div>
  </div>

```bibtex
@misc{wild_neurologger,
  title        = {WILD: Open-source Wireless Neurotechnology for Naturalistic Neuroscience},
  author       = {WILD contributors},
  year         = {2026},
  howpublished = {\url{https://github.com/ayalab1/Neurologger}}
}
```
</section>

<section class="wild-section">
  <h2>Community</h2>
  <div class="wild-grid">
    <div class="wild-card">
      <h3>GitHub</h3>
      <p><a href="https://github.com/ayalab1/Neurologger">Browse source, hardware files, firmware releases, and analysis scripts.</a></p>
    </div>
    <div class="wild-card">
      <h3>Discussions</h3>
      <p>Use GitHub Discussions for experiment design questions, integration planning, and troubleshooting.</p>
    </div>
    <div class="wild-card">
      <h3>Contributing</h3>
      <p><a href="contributing/">Open an issue or pull request with hardware notes, firmware fixes, analysis examples, or documentation improvements.</a></p>
    </div>
  </div>
</section>
