# Python

Python utilities cover camera decoding, audio handling, GPIO logging, and validation after SD-card export.

## Scripts

| Script | Purpose |
| --- | --- |
| [`WILD_VideoDecodewAudio.py`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_VideoDecodewAudio.py) | Decode camera data with audio handling. |
| [`WILD_VideoDecodewAudio_v2.py`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_VideoDecodewAudio_v2.py) | Alternative video decode pipeline. |
| [`WILD_VideoDecodewAudio_folder.py`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_VideoDecodewAudio_folder.py) | Batch folder processing. |
| [`WILD_GPIO_Logger.py`](https://github.com/ayalab1/Neurologger/blob/main/Code/WILD_GPIO_Logger.py) | GPIO logging utility. |

## Typical Use

- Decode camera or audio files after exporting a recording folder.
- Batch-process multiple recording folders with the folder variants.
- Log GPIO or serial events during synchronization validation.
- Keep generated media and logs separate from the raw SD export.

## Interactive Commands

Run the Python tools from the repository `Code` folder:

```powershell
cd C:\code\github\Neurologger\Code
python .\WILD_VideoDecodewAudio.py
python .\WILD_VideoDecodewAudio_folder.py
python .\WILD_GPIO_Logger.py
```

- `WILD_VideoDecodewAudio.py` opens a file picker for one `misc.dat` recording and expects the matching `adc.dat` file when audio is present.
- `WILD_VideoDecodewAudio_folder.py` opens a folder picker and recursively processes `misc.dat` files below that root.
- `WILD_GPIO_Logger.py` prompts for a COM port and output folder, then writes a timestamped text log.

## Expected Outputs

```text
example_recording/
  misc.dat
  adc.dat
  adc.wav
  adc.mp3
  misc.mp4
  misc_wAudio.mp4
```

Output names depend on the script path and whether audio is present, but the public decoder workflow writes reviewable media next to the source export by default.
