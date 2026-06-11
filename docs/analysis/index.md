# Analysis

The analysis documentation should make WILD data easy to move into established neuroscience workflows without requiring users to reverse-engineer the export format.

## Entry Points

<div class="wild-grid">
  <div class="wild-card">
    <h3>Python</h3>
    <p>Camera decoding, video/audio handling, GPIO logging, and future SpikeInterface examples.</p>
  </div>
  <div class="wild-card">
    <h3>MATLAB</h3>
    <p>Header generation, preprocessing, IMU processing, and compatibility with existing lab scripts.</p>
  </div>
  <div class="wild-card">
    <h3>Spike Sorting</h3>
    <p>Export recordings into layouts usable by common spike sorting pipelines.</p>
  </div>
</div>

## Reproducibility Checklist

- Record firmware binary filename.
- Record WILD_console version.
- Preserve raw export folder.
- Preserve `CE_params.bin`.
- Record probe, channel map, sampling rate, and stimulation configuration.
- Track post-processing script version or commit hash.
