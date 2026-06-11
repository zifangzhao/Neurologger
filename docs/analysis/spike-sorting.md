# Spike Sorting

WILD neural data can be organized for downstream spike sorting after export and preprocessing.

## Recommended Workflow

1. Preserve the raw WILD export folder.
2. Run WILD preprocessing to generate `info.rhd`, `time.dat`, and corrected metadata.
3. Confirm sampling rate, channel count, channel ordering, and probe geometry.
4. Prepare a sorter-specific working directory.
5. Run quality-control checks before interpreting units.

## Documentation Targets

- SpikeInterface loader example.
- Kilosort-compatible folder preparation.
- Channel map templates for supported probes.
- Example quality-control notebook.
- Known limitations for camera, IMU, and closed-loop event alignment.

!!! note
    Do not assume a generic channel map. Document the exact probe and channel ordering used for each dataset.
