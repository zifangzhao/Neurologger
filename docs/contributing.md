# Contributing

WILD is an open-source hardware and software project. Contributions are welcome when they make the system easier to reproduce, validate, or extend.

## Ways to Contribute

- Improve setup and troubleshooting documentation.
- Add hardware assembly notes or photos.
- Report firmware or WILD_console issues with version details.
- Add analysis examples and validation datasets.
- Improve closed-loop or TinyML examples.
- Add compatibility notes for probes, SD cards, batteries, and BLE adapters.

## Pull Request Checklist

1. Describe the hardware revision, firmware version, and software version used for testing.
2. Keep documentation in Markdown.
3. Add images under `docs/images/` only when they are useful for assembly, operation, or validation.
4. Do not use AI-generated imagery for any WILD device depiction. Device photos, device illustrations, PCB renders, CAD renders, connector diagrams, pinouts, and schematics must come from real photographs, project CAD/EDA exports, measurements, or hand-authored diagrams derived from source files.
5. Use clear filenames and alt text for figures.
6. Avoid claims that are not tied to a tested configuration.
7. Run `mkdocs build --strict` before submitting documentation changes.

## Documentation Style

- Prefer short procedural steps for setup pages.
- Prefer diagrams and tables for architecture pages.
- Keep WILD hardware visuals traceable to real hardware, CAD, PCB, or firmware sources.
- Separate validated behavior from planned features.
- Keep safety, protocol, and animal-use details local to approved lab procedures unless they are public and reviewed.
