# WILD

**WILD** (Wireless Intelligent Logger) is an open-source wireless neurotechnology platform for naturalistic neuroscience. It supports lightweight multimodal neural recording, behavioral sensing, and closed-loop stimulation for freely behaving animals.

## Documentation

The documentation portal is built with MkDocs Material and is maintained through Markdown files in [`docs/`](docs/).

- [Getting Started](docs/getting-started/index.md)
- [Hardware](docs/hardware/index.md)
- [Firmware](docs/firmware/index.md)
- [Software](docs/software/index.md)
- [Analysis](docs/analysis/index.md)
- [Publications](docs/publications/index.md)

## Platform Scope

- Wireless electrophysiology recording
- Closed-loop stimulation and embedded DSP
- Neuropixels-compatible workflow documentation
- IMU, ultrasonic audio, camera, and digital event recording
- TinyML inference support on MCU firmware
- Long-term recording and multi-animal experiment workflows

## Repository Layout

| Path | Purpose |
| --- | --- |
| [`docs/`](docs/) | MkDocs documentation source |
| [`Firmware/`](Firmware/) | Released firmware images |
| [`Software/`](Software/) | WILD_console installers |
| [`Code/`](Code/) | MATLAB and Python analysis scripts |
| [`PCB/`](PCB/) | PCB fabrication and assembly files |
| [`3Dprint/`](3Dprint/) | Mechanical parts and CAD files |

## Local Documentation Build

```bash
pip install -r requirements.txt
mkdocs serve
```

The GitHub Pages workflow builds the site with:

```bash
mkdocs build --strict
```

## License

See [LICENSE](LICENSE).
