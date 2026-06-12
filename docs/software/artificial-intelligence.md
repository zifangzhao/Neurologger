# Artificial Intelligence

WILD supports embedded AI workflows for online model-based processing on the device. This should be described as onboard biomarker detection and behavioral classification for responsive stimulation, not as a general-purpose brain-computer interface.

The current implementation is intentionally conservative: AI models are pre-compiled into firmware and reviewed with careful attention to RAM use, compute timing, sampling schedules, and closed-loop latency.

## Current Model Integration

Current AI support is designed for validated, experiment-specific models rather than arbitrary runtime uploads or generic model deployment.

- Models are compiled with the firmware image.
- RAM use is curated before deployment.
- Inference timing is checked against acquisition, storage, BLE, and DSP tasks.
- Model output is integrated with device state reporting and closed-loop logic.
- Firmware version and model identity should be recorded with each experiment.

This approach keeps timing behavior predictable on resource-constrained embedded hardware.

## Generic Model Support

Support for generic model loading is currently under development. The goal is to make model deployment more flexible while preserving the timing and memory guarantees needed for closed-loop neuro-behavioral experiments.

Generic model loading is not part of the current stable workflow. Before a model is used in closed-loop experiments, the release must define:

- Accepted model format and quantization requirements.
- Maximum model size and tensor arena limits.
- Input and output tensor conventions.
- Inference scheduling relative to acquisition and DSP.
- Validation procedure before animal experiments.
- How model version, firmware version, and experiment metadata are recorded.

!!! warning "Deployment discipline"
    Treat embedded AI models as part of the firmware release. A model that passes desktop inference tests may still be unsafe for closed-loop use if RAM pressure or inference timing affects acquisition, storage, or stimulation behavior.
