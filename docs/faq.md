# FAQ

## Is WILD a replacement for wired acquisition?

WILD is designed for wireless and naturalistic experiments where tethered acquisition is limiting. The correct choice depends on channel count, runtime, signal quality, synchronization, and behavioral constraints.

## Is WILD a BLE telemetry system?

No. WILD is primarily a local-storage neurologger. High-bandwidth neural and multimodal data are recorded to the device microSD card. BLE is used for discovery, configuration, synchronization support, status, selected low-bandwidth preview, and control commands.

## What is the current recording scale?

The current open-source workflow is the 64-channel WILD system. Neuropixels-compatible and active-SPI-probe variants are higher-performance development targets and are separate from the current public release.

## How do I install the PC software?

Download the latest installer from the [latest GitHub release](https://github.com/zifangzhao/Neurologger/releases/latest), then follow the acquisition guide.

## What should I check if BLE connects but recording does not start?

Check the microSD card first. The current usage notes call out SD format and compatibility as a common cause when BLE connects but synchronization does not begin.

## Does WILD support TinyML?

WILD supports online inference of pre-compiled, experiment-specific models in firmware. Runtime generic model loading is documented as under development.

## How should I cite WILD?

Use the in-press platform manuscript citation on the [Publications](publications/index.md) page. For reproducibility, include the WILD hardware revision, firmware image, WILD_console version, and analysis-script version used in your methods.

## Where should new diagrams live?

Keep source diagrams editable where possible, and export web-ready images into `docs/images/`. For architecture diagrams, Mermaid in Markdown is preferred when it is readable.
