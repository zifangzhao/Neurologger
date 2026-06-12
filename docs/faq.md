# FAQ

## Is WILD a replacement for wired acquisition?

WILD is designed for wireless and naturalistic experiments where tethered acquisition is limiting. The correct choice depends on channel count, runtime, signal quality, synchronization, and behavioral constraints.

## Is WILD a BLE telemetry system?

No. WILD is primarily a local-storage neurologger. High-bandwidth neural and multimodal data are recorded to the device microSD card. BLE is used for discovery, configuration, synchronization support, status, selected low-bandwidth preview, and control commands.

## Will WILD have an iOS controller?

An iOS-based WILD controller app is in development for device discovery, BLE connection, synchronization support, status checks, and low-bandwidth commands. It is expected to provide more consistent wireless-control performance than typical PC BLE adapters, but full-resolution recordings will still be stored locally on the device microSD card.

## What is the current recording scale?

The current open-source workflow is the 64-channel WILD system. Neuropixels-compatible and active-SPI-probe variants are higher-performance research targets and are separate from the current public release.

## How do I install the PC software?

The latest installer is available from the [latest GitHub release](https://github.com/zifangzhao/Neurologger/releases/latest), with setup details in the acquisition guide.

## BLE connects, but recording does not start

The microSD card is the first item to verify. SD format and card compatibility are common causes when BLE connects but synchronization does not begin.

## Does WILD support TinyML?

WILD supports online inference of curated, experiment-specific models through validated release images. Runtime generic model loading is not part of the stable public workflow yet.

## How do I cite WILD?

The under-review platform manuscript entry is listed on the [Publications](publications/index.md) page. Reproducible methods include the WILD hardware revision, release image, WILD_console version, and analysis-script version.

## Where do new diagrams go?

Source diagrams are best kept editable where possible, with web-ready images exported into `docs/images/`. For readable architecture diagrams, Mermaid in Markdown is preferred.
