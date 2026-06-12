# FAQ

## Is WILD a replacement for wired acquisition?

WILD is designed for wireless and naturalistic experiments where tethered acquisition is limiting. The correct choice depends on channel count, runtime, signal quality, synchronization, and behavioral constraints.

## Is WILD a BLE telemetry system?

No. WILD is primarily a local-storage neurologger. High-bandwidth neural and multimodal data are recorded to the device microSD card. BLE is used for discovery, configuration, synchronization support, status, selected low-bandwidth preview, and control commands.

## What is the current recording scale?

The current open-source workflow is the 64-channel WILD system. Neuropixels-compatible and active-SPI-probe variants are higher-performance research targets and are separate from the current public release.

## How do I install the PC software?

Download the latest installer from the [latest GitHub release](https://github.com/zifangzhao/Neurologger/releases/latest), then follow the acquisition guide.

## BLE connects, but recording does not start

Check the microSD card first. The current usage notes call out SD format and compatibility as a common cause when BLE connects but synchronization does not begin.

## Does WILD support TinyML?

WILD supports online inference of curated, experiment-specific models through validated release images. Runtime generic model loading is not part of the stable public workflow yet.

## How do I cite WILD?

Use the under-review platform manuscript entry on the [Publications](publications/index.md) page. For reproducibility, include the WILD hardware revision, release image, WILD_console version, and analysis-script version used in your methods.

## Where do new diagrams go?

Keep source diagrams editable where possible, and export web-ready images into `docs/images/`. For architecture diagrams, Mermaid in Markdown is preferred when it is readable.
