# Spike Sorting

WILD neural data can be organized for downstream spike sorting after export and preprocessing.

## Recommended Workflow

1. Preserve the raw WILD export folder.
2. Run WILD preprocessing to generate `info.rhd`, `time.dat`, and corrected metadata.
3. Confirm sampling rate, channel count, channel ordering, and probe geometry.
4. Prepare a sorter-specific working directory.
5. Run quality-control checks before interpreting units.

## Recommended Sorter

Kilosort is the recommended starting point for spike sorting exported WILD electrophysiology recordings. Keep the sorter working directory separate from the raw SD export and keep channel-map files with the processed dataset.

!!! note
    Do not assume a generic channel map. Document the exact probe and channel ordering used for each dataset.
