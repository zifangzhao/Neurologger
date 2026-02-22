import cv2
import numpy as np
import os
from tkinter import Tk
from tkinter import filedialog
import wave
import scipy.ndimage
from scipy.signal import butter, filtfilt
from moviepy import VideoFileClip, AudioFileClip
import lameenc
import librosa


def readmulti_frank(file, byte_offset, byte_length, dtype):
    """ Function to read binary data from file """
    with open(file, 'rb') as f:
        f.seek(byte_offset)
        data = f.read(byte_length)
    return np.frombuffer(data, dtype=dtype)


def save_binary_audio_to_wav(audio_file, sample_rate, output_path):
    with open(audio_file, "rb") as f:
        audio_binary = f.read()

    audio_array = np.frombuffer(audio_binary, dtype=np.uint16)
    audio_array = (audio_array - 32768).astype(np.int16)
    print(f"Audio file sps: {audio_array.shape[0]}, fs: {sample_rate},duration: {audio_array.shape[0]/sample_rate}")

    nyquist = 0.5 * sample_rate
    normal_cutoff = 1 / nyquist
    b, a = butter(N=2, Wn=normal_cutoff, btype='high', analog=False)
    audio_array = filtfilt(b, a, audio_array).astype(np.int16)

    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        print(f"Audio file samples after preprocessing:{audio_array.shape[0]}")
        wav_file.writeframesraw(audio_array.tobytes())


def save_binary_audio_to_mp3(audio_file, sample_rate, output_path):
    with open(audio_file, "rb") as f:
        audio_binary = f.read()

    audio_array = np.frombuffer(audio_binary, dtype=np.uint16)
    audio_array = (audio_array - 32768).astype(np.float32)

    print(f"Audio file sps: {audio_array.shape[0]}, fs: {sample_rate},duration: {audio_array.shape[0]/sample_rate}")

    nyquist = 0.5 * sample_rate
    normal_cutoff = 20000 / nyquist
    b, a = butter(N=2, Wn=normal_cutoff, btype="high", analog=False)
    filtered_audio = filtfilt(b, a, audio_array)

    filtered_audio = librosa.effects.pitch_shift(filtered_audio, sr=sample_rate, n_steps=-24)
    filtered_audio = librosa.resample(filtered_audio, orig_sr=sample_rate, target_sr=48000)
    sample_rate = 48000

    filtered_audio = np.clip(filtered_audio, -32768, 32767).astype(np.int16)

    encoder = lameenc.Encoder()
    encoder.set_bit_rate(384)
    encoder.set_in_sample_rate(sample_rate)
    encoder.set_channels(1)
    encoder.set_quality(0)

    mp3_data = encoder.encode(filtered_audio.tobytes()) + encoder.flush()

    with open(output_path, "wb") as mp3_file:
        mp3_file.write(mp3_data)

    print(f"Audio saved to {output_path}")


def adjust_brightness_contrast(image, target_brightness=128):
    current_brightness = np.mean(image)
    brightness_factor = target_brightness / max(current_brightness, 1e-6)
    adjusted_img = np.clip(image * brightness_factor, 0, 255).astype(np.uint8)
    return adjusted_img

def compute_global_percentiles(file, frames, byte_per_img,
                               width, height,
                               sample_frames=200,
                               percentile_low=1,
                               percentile_high=99):

    import cv2
    import numpy as np

    accum = [[], [], []]

    with open(file, "rb") as f:

        for idx in range(min(sample_frames, frames)):

            f.seek(idx * byte_per_img)
            raw = np.frombuffer(f.read(byte_per_img), dtype=np.uint8)

            img = np.reshape(raw[:320 * 492], (-1, 492)).T
            img = img[12:, :].T.flatten().astype(np.uint16)

            unpacked = np.zeros(len(img) * 2 // 3, dtype=np.uint16)
            unpacked[0::2] = ((img[0::3] & 0x7F) << 3) | ((img[1::3] & 0xE0) >> 5)
            unpacked[1::2] = ((img[1::3] & 0x07) << 7) | ((img[2::3] & 0xFE) >> 1)

            unpacked = np.reshape(unpacked, (-1, 320))
            unpacked = unpacked * 64
            unpacked = np.rot90(unpacked, 2)

            rgb = cv2.demosaicing(unpacked, cv2.COLOR_BAYER_RG2RGB_EA)

            for c in range(3):
                accum[c].append(rgb[:,:,c].flatten())

    global_low = []
    global_high = []

    for c in range(3):
        vals = np.concatenate(accum[c])
        global_low.append(np.percentile(vals, percentile_low))
        global_high.append(np.percentile(vals, percentile_high))

    return global_low, global_high
def WILD_Camera_Decode_HQ(file=None,
                          fps=16,
                          output_codec="hevc",
                          percentile_low=1,
                          percentile_high=99,
                          sample_frames_for_stats=200):

    import os
    import cv2
    import numpy as np
    import subprocess
    from tkinter import Tk, filedialog

    # -------------------------------
    # File selection
    # -------------------------------
    if file is None:
        root = Tk()
        root.withdraw()
        file = filedialog.askopenfilename(
            title="Select WILD video file",
            filetypes=[("WILD video file", "*misc.dat")]
        )
        if not file:
            return

    if not os.path.exists(file):
        raise FileNotFoundError("Video file not found")

    file_size = os.path.getsize(file)
    if file_size == 0:
        print("Skipping empty file.")
        return

    width = 320
    height = 320
    byte_per_img = 320 * 500
    frames = file_size // byte_per_img

    if frames == 0:
        print("No valid frames.")
        return

    print(f"Total frames: {frames}")

    parent_dir = os.path.dirname(file)
    base_name = os.path.basename(parent_dir)

    # -------------------------------
    # Audio
    # -------------------------------
    audio_wav = file.replace("misc.dat", "adc.wav")
    use_audio = os.path.exists(audio_wav)

    # -------------------------------
    # Compute global percentile scaling
    # -------------------------------
    print("Computing global percentiles...")

    accum = [[], [], []]

    with open(file, "rb") as f:

        for _ in range(min(sample_frames_for_stats, frames)):

            raw = np.frombuffer(f.read(byte_per_img), dtype=np.uint8)

            img = raw[:320 * 492].reshape(-1, 492).T
            img = img[12:, :].T.flatten().astype(np.uint16)

            unpacked = np.empty(len(img) * 2 // 3, dtype=np.uint16)
            unpacked[0::2] = ((img[0::3] & 0x7F) << 3) | ((img[1::3] & 0xE0) >> 5)
            unpacked[1::2] = ((img[1::3] & 0x07) << 7) | ((img[2::3] & 0xFE) >> 1)

            unpacked = unpacked.reshape(-1, 320)
            unpacked <<= 6
            unpacked = unpacked[::-1, ::-1]

            rgb = cv2.demosaicing(unpacked, cv2.COLOR_BAYER_RG2RGB_EA)

            for c in range(3):
                accum[c].append(rgb[:, :, c].ravel())

    global_low = np.array([
        np.percentile(np.concatenate(accum[c]), percentile_low)
        for c in range(3)
    ], dtype=np.float32).reshape(1, 1, 3)

    global_high = np.array([
        np.percentile(np.concatenate(accum[c]), percentile_high)
        for c in range(3)
    ], dtype=np.float32).reshape(1, 1, 3)

    global_range = np.maximum(global_high - global_low, 1e-6)

    print("Global scaling computed.")

    # -------------------------------
    # Output configuration
    # -------------------------------
    if output_codec == "ffv1":

        output_file = os.path.join(parent_dir, f"{base_name}_LOSSLESS.mkv")

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-f", "rawvideo",
            "-pix_fmt", "rgb48le",
            "-s", f"{width}x{height}",
            "-r", str(fps),
            "-i", "pipe:0",
        ]

        if use_audio:
            ffmpeg_cmd += ["-i", audio_wav]

        ffmpeg_cmd += ["-c:v", "ffv1", "-level", "3"]

        if use_audio:
            ffmpeg_cmd += [
                "-c:a", "flac",
                "-map", "0:v:0",
                "-map", "1:a:0"
            ]

        ffmpeg_cmd.append(output_file)

    elif output_codec == "hevc":

        output_file = os.path.join(parent_dir, f"{base_name}_HEVC10bit.mp4")

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-f", "rawvideo",
            "-pix_fmt", "rgb48le",
            "-s", f"{width}x{height}",
            "-r", str(fps),
            "-i", "pipe:0",
        ]

        if use_audio:
            ffmpeg_cmd += ["-i", audio_wav]

        ffmpeg_cmd += [
            "-c:v", "hevc_nvenc",
            "-preset", "p5",
            "-rc", "vbr",
            "-cq", "14",
            "-pix_fmt", "p010le",
        ]

        if use_audio:
            ffmpeg_cmd += [
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "48000",
                "-map", "0:v:0",
                "-map", "1:a:0"
            ]

        ffmpeg_cmd.append(output_file)

    else:
        raise ValueError("output_codec must be 'ffv1' or 'hevc'")

    # -------------------------------
    # Launch encoder
    # -------------------------------
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # -------------------------------
    # Frame processing loop
    # -------------------------------
    with open(file, "rb") as f:

        for idx in range(frames):

            if idx % 50 == 0:
                print(f"Processing {idx}/{frames}")

            raw = np.frombuffer(f.read(byte_per_img), dtype=np.uint8)

            img = raw[:320 * 492].reshape(-1, 492).T
            img = img[12:, :].T.flatten().astype(np.uint16)

            unpacked = np.empty(len(img) * 2 // 3, dtype=np.uint16)
            unpacked[0::2] = ((img[0::3] & 0x7F) << 3) | ((img[1::3] & 0xE0) >> 5)
            unpacked[1::2] = ((img[1::3] & 0x07) << 7) | ((img[2::3] & 0xFE) >> 1)

            unpacked = unpacked.reshape(-1, 320)
            unpacked <<= 6
            unpacked = unpacked[::-1, ::-1]

            rgb = cv2.demosaicing(unpacked, cv2.COLOR_BAYER_RG2RGB_EA)
            rgb = rgb.astype(np.float32)

            rgb = (rgb - global_low) / global_range
            np.clip(rgb, 0, 1, out=rgb)

            rgb_16 = (rgb * 65535).astype(np.uint16)

            process.stdin.write(rgb_16.tobytes())

    process.stdin.close()
    process.wait()

    print("Done.")
    print("Output saved to:", output_file)


def WILD_Camera_Decode_HQ_(file=None,
                          fps=16,
                          output_codec="hevc",
                          percentile_low=1,
                          percentile_high=99):

    import os
    import cv2
    import numpy as np
    import subprocess
    from tkinter import Tk, filedialog

    # --------------------------------------------------
    # File selection
    # --------------------------------------------------
    if file is None:
        root = Tk()
        root.withdraw()
        file = filedialog.askopenfilename(
            title="Select WILD video file",
            filetypes=[("WILD video file", "*misc.dat")]
        )
        if not file:
            print("No file selected.")
            return

    if not os.path.exists(file):
        raise FileNotFoundError("Video file not found")

    # --------------------------------------------------
    # Skip empty file
    # --------------------------------------------------
    file_size = os.path.getsize(file)
    parent_dir = os.path.dirname(file)
    last_folder = os.path.basename(parent_dir)
    base_name = f"{last_folder}_misc"
    
    audio_wav = file.replace("misc.dat", "adc.wav")
    use_audio = os.path.exists(audio_wav)

    if file_size == 0:
        print(f"Skipping empty file: {file}")
        return

    width = 320
    height = 320
    byte_per_img = 320 * 500

    frames = file_size // byte_per_img

    if frames == 0:
        print(f"Skipping file with 0 valid frames: {file}")
        return

    print(f"Total frames: {frames}")

    # --------------------------------------------------
    # Output config
    # --------------------------------------------------
    if output_codec == "ffv1":

        output_file = os.path.join(parent_dir, f"{base_name}_LOSSLESS.mkv")

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",

            # ---- video input (pipe) ----
            "-f", "rawvideo",
            "-pix_fmt", "rgb48le",
            "-s", f"{width}x{height}",
            "-r", str(fps),
            "-i", "pipe:0",
        ]

        if use_audio:
            ffmpeg_cmd += ["-i", audio_wav]

        ffmpeg_cmd += [
            "-c:v", "ffv1",
            "-level", "3",
        ]

        if use_audio:
            ffmpeg_cmd += [
                "-c:a", "flac",     # lossless audio
                "-map", "0:v:0",
                "-map", "1:a:0",
            ]

        ffmpeg_cmd.append(output_file)

    elif output_codec == "hevc":

        output_file = os.path.join(parent_dir, f"{base_name}_HEVC10bit.mp4")

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",

            # ---- video input ----
            "-f", "rawvideo",
            "-pix_fmt", "rgb48le",
            "-s", f"{width}x{height}",
            "-r", str(fps),
            "-i", "pipe:0",
        ]

        if use_audio:
            ffmpeg_cmd += ["-i", audio_wav]

        ffmpeg_cmd += [
            "-c:v", "hevc_nvenc",
            "-rc", "constqp",
            "-qp", "12",
            "-preset", "p5",
            "-pix_fmt", "yuv444p10le",
        ]

        if use_audio:
            ffmpeg_cmd += [
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "48000",       # ← resample to 48kHz
                "-map", "0:v:0",
                "-map", "1:a:0",
            ]

        ffmpeg_cmd.append(output_file)

    else:
        raise ValueError("output_codec must be 'ffv1' or 'hevc'")

    # --------------------------------------------------
    # Launch encoder
    # --------------------------------------------------
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # --------------------------------------------------
    # Frame loop
    # --------------------------------------------------
    with open(file, "rb") as f:

        for idx in range(frames):

            if idx % 50 == 0:
                print(f"Processing {idx}/{frames}")

            f.seek(idx * byte_per_img)
            raw = np.frombuffer(f.read(byte_per_img), dtype=np.uint8)

            img = np.reshape(raw[:320 * 492], (-1, 492)).T
            img = img[12:, :].T.flatten().astype(np.uint16)

            unpacked = np.zeros(len(img) * 2 // 3, dtype=np.uint16)

            unpacked[0::2] = ((img[0::3] & 0x7F) << 3) | ((img[1::3] & 0xE0) >> 5)
            unpacked[1::2] = ((img[1::3] & 0x07) << 7) | ((img[2::3] & 0xFE) >> 1)

            unpacked = np.reshape(unpacked, (-1, 320))

            unpacked = unpacked * 64
            unpacked = np.rot90(unpacked, 2)

            rgb = cv2.demosaicing(unpacked, cv2.COLOR_BAYER_RG2RGB)
            rgb = rgb.astype(np.float32)

            # Per-channel normalization
            for c in range(3):
                ch = rgb[:, :, c]
                ch_min = np.min(ch)
                ch_max = np.max(ch)
                if ch_max > ch_min:
                    ch = (ch - ch_min) / (ch_max - ch_min)
                rgb[:, :, c] = ch

            # Percentile stretch
            for c in range(3):
                ch = rgb[:, :, c]
                p_low = np.percentile(ch, percentile_low)
                p_high = np.percentile(ch, percentile_high)

                if p_high > p_low:
                    ch = (ch - p_low) / (p_high - p_low)
                    ch = np.clip(ch, 0, 1)

                rgb[:, :, c] = ch

            rgb_16 = (rgb * 65535).astype(np.uint16)

            process.stdin.write(rgb_16.tobytes())

    process.stdin.close()
    process.wait()

    print("Done.")
    print("Output saved to:", output_file)


def process_file(file_path):
    """
    Worker wrapper for parallel execution.
    Must be top-level (not nested) for Windows multiprocessing.
    Returns (file_path, success, error_message)
    """
    try:
        if not os.path.exists(file_path):
            return file_path, False, "File does not exist"

        if os.path.getsize(file_path) == 0:
            return file_path, False, "Empty file"

        WILD_Camera_Decode_HQ(file=file_path)
        return file_path, True, None

    except Exception as e:
        return file_path, False, str(e)
def process_root_folder(root_dir=None, pattern="misc.dat"):
    """
    Recursively process all *misc.dat in root_dir and subfolders.
    """
    if root_dir is None:
        tk = Tk()
        tk.withdraw()
        root_dir = filedialog.askdirectory(title="Select root folder containing WILD recordings")
        if not root_dir:
            print("No folder selected.")
            return

    targets = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fn in filenames:
            if fn.endswith(pattern):
                targets.append(os.path.join(dirpath, fn))

    targets.sort()
    print(f"Found {len(targets)} files under: {root_dir}")

    ok = 0
    fail = 0
    for i, f in enumerate(targets, 1):
        print(f"\n[{i}/{len(targets)}] {f}")
        try:
            WILD_Camera_Decode_HQ(file=f)
            ok += 1
        except Exception as e:
            print(f"FAILED: {f}\n  -> {e}")
            fail += 1

    print(f"\nDone. OK={ok}, FAIL={fail}, TOTAL={len(targets)}")

if __name__ == "__main__":
    # Option A: pick a root folder interactively
    process_root_folder()

    # Option B: hardcode a root folder
    # process_root_folder(r"D:\data\WILD")
