# FAQ

## Is WILD a replacement for wired acquisition?

WILD is designed for wireless and naturalistic experiments where tethered acquisition is limiting. The correct choice depends on channel count, runtime, signal quality, synchronization, and behavioral constraints.

## How do I install the PC software?

Download the latest installer from [Software](https://github.com/ayalab1/Neurologger/tree/main/Software), then follow the acquisition guide.

## What should I check if BLE connects but recording does not start?

Check the microSD card first. The current usage notes call out SD format and compatibility as a common cause when BLE connects but synchronization does not begin.

## Does WILD support TinyML?

WILD supports online inference of pretrained TensorFlow Lite models in firmware. Runtime model loading is documented as under development.

## How should I cite WILD?

Use the repository citation on the [Publications](publications/index.md) page until a formal platform paper is available, and include the firmware and software versions used in your methods.

## Where should new diagrams live?

Keep source diagrams editable where possible, and export web-ready images into `docs/images/`. For architecture diagrams, Mermaid in Markdown is preferred when it is readable.
