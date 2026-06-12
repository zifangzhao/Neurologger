# Artificial Intelligence

WILD supports onboard biomarker detection and behavioral classification for responsive stimulation.

Current releases are intentionally conservative: AI models are curated into validated release images and reviewed for RAM use, compute timing, sampling schedules, and closed-loop latency.

## Current Model Integration

Current AI support uses validated, experiment-specific models rather than arbitrary runtime uploads.

- Models are distributed as part of validated release images.
- RAM use is curated before deployment.
- Inference timing is checked against acquisition, storage, BLE, and DSP tasks.
- Model output is integrated with device state reporting and closed-loop logic.
- Record release image and model identity with each experiment.

This approach keeps timing behavior predictable on resource-constrained embedded hardware.

## Generic Model Support

Generic model loading is not part of the stable public workflow yet. Current releases prioritize predictable timing, memory use, and closed-loop behavior.

Before a model is used in closed-loop experiments, confirm that the release defines:

- Accepted model format and quantization requirements.
- Maximum model size and tensor arena limits.
- Input and output tensor conventions.
- Inference scheduling relative to acquisition and DSP.
- Validation procedure before animal experiments.
- How model version, release image, and experiment metadata are recorded.

!!! warning "Deployment discipline"
    Treat embedded AI models as part of the validated device release. A model that passes desktop inference tests may still be unsafe for closed-loop use if RAM pressure or inference timing affects acquisition, storage, or stimulation behavior.
