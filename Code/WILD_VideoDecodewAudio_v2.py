import cv2
import numpy as np
import os
from tkinter import Tk
from tkinter import filedialog
import wave
import scipy.ndimage
from scipy.signal import butter, filtfilt
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip
import lameenc
import librosa


def readmulti_frank(file, byte_offset, byte_length, dtype):
    """ Function to read binary data from file """
    with open(file, 'rb') as f:
        f.seek(byte_offset)
        data = f.read(byte_length)
    return np.frombuffer(data, dtype=dtype)


def save_binary_audio_to_wav(audio_file, sample_rate, output_path):
    """
    Save binary audio data in uint16 format to a .wav file.
    :param audio_binary: Binary audio data in uint16 format.
    :param sample_rate: Sampling rate of the audio.
    :param output_path: Path to save the .wav file.
    """
    with open(audio_file, "rb") as f:
        # Read the entire binary file
        audio_binary = f.read()
    # Convert uint16 to int16
    audio_array = np.frombuffer(audio_binary, dtype=np.uint16)
    audio_array = (audio_array - 32768).astype(np.int16)  # Convert to signed int16
    print(f"Audio file sps: {audio_array.shape[0]}, fs: {sample_rate},duration: {audio_array.shape[0]/sample_rate}")
    #filtering
    # Design a Butterworth high-pass filter(DC-removal)
    nyquist = 0.5 * sample_rate
    normal_cutoff = 1 / nyquist
    b, a = butter(N=2, Wn=normal_cutoff, btype='high', analog=False)
    
    # Apply the filter using filtfilt for zero-phase filtering
    audio_array = filtfilt(b, a, audio_array)
    audio_array = (audio_array).astype(np.int16)  # Convert to signed int16
    with wave.open(output_path, 'wb') as wav_file:
        # Set the number of channels, sample width, and frame rate
        num_channels = 1  # Mono audio
        sample_width = 2  # 2 bytes per sample (16-bit PCM)
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        print(f"Audio file samples after preprocessing:{audio_array.shape[0]}")
        # Write the audio data as int16
        wav_file.writeframesraw(audio_array.tobytes())



def save_binary_audio_to_mp3(audio_file, sample_rate, output_path):
    """
    Save binary audio data in uint16 format to an MP3 file using lameenc.
    :param audio_file: Path to the input binary audio file.
    :param sample_rate: Sampling rate of the audio (Hz).
    :param output_path: Path to save the MP3 file.
    """
    with open(audio_file, "rb") as f:
        # Read the entire binary file
        audio_binary = f.read()

    # Convert uint16 to float
    audio_array = np.frombuffer(audio_binary, dtype=np.uint16)
    audio_array = (audio_array - 32768).astype(np.float32)  # Convert to float

    print(f"Audio file sps: {audio_array.shape[0]}, fs: {sample_rate},duration: {audio_array.shape[0]/sample_rate}")
    

    # Apply a Butterworth high-pass filter
    nyquist = 0.5 * sample_rate
    normal_cutoff = 20000 / nyquist  # High-pass filter with 1 Hz cutoff
    b, a = butter(N=2, Wn=normal_cutoff, btype="high", analog=False)
    filtered_audio = filtfilt(b, a, audio_array)

    # Shift pitch down by 2 octaves (factor of 4 in frequency)
    filtered_audio = librosa.effects.pitch_shift(filtered_audio, sr=sample_rate, n_steps=-24)

    # Resample from 160KHz to 48KHz
    filtered_audio = librosa.resample(filtered_audio, orig_sr=sample_rate, target_sr=48000)
    sample_rate=48000
    # Clip the audio to int16 range
    filtered_audio = np.clip(filtered_audio, -32768, 32767).astype(np.int16)

    # Encode to MP3 using lameenc
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(384)  # Set bitrate (e.g., 192 kbps)
    encoder.set_in_sample_rate(sample_rate)  # Input sample rate
    encoder.set_channels(1)  # Mono
    encoder.set_quality(0)  # Higher quality (0 is best, 9 is worst)

    mp3_data = encoder.encode(filtered_audio.tobytes()) + encoder.flush()

    # Write MP3 data to file
    with open(output_path, "wb") as mp3_file:
        mp3_file.write(mp3_data)

    print(f"Audio saved to {output_path}")


def adjust_brightness_contrast(image, target_brightness=128):
    # Calculate the current brightness of the image (mean pixel value)
    current_brightness = np.mean(image)

    # Calculate the brightness scaling factor
    brightness_factor = target_brightness / current_brightness

    # Adjust brightness by scaling pixel values
    adjusted_img = np.clip(image * brightness_factor, 0, 255).astype(np.uint8)
    return adjusted_img

def auto_exposure_compensation(image):
    # Convert the image to YUV color space
    yuv_img = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)

    # Apply histogram equalization to the luminance channel (Y channel)
    yuv_img[:, :, 0] = cv2.equalizeHist(yuv_img[:, :, 0])

    # Convert back to RGB color space
    result_img = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2RGB)
    return result_img


def WILD_Camera_Decode_FFV1(file=None, fps=16):
    """
    Decode WILD raw camera file into 16-bit lossless FFV1 video.
    Bad pixel correction removed.
    """

    import cv2
    import numpy as np
    import os
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
            print("No file selected.")
            return

    if not os.path.exists(file):
        raise FileNotFoundError("Video file not found")

    width = 320
    height = 320
    byte_per_img = 320 * 500

    with open(file, 'rb') as f:
        f.seek(0, 2)
        total_bytes = f.tell()

    frames = total_bytes // byte_per_img
    print(f"Total frames: {frames}")

    output_file = file.replace(".dat", "_FFV1_16bit.avi")

    # -------------------------------
    # FFmpeg command (lossless 16-bit)
    # -------------------------------
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb48le",     # 16-bit RGB input
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "pipe:0",
        "-c:v", "ffv1",
        "-level", "3",
        "-pix_fmt", "rgb48le",
        output_file
    ]

    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # -------------------------------
    # Decode loop
    # -------------------------------
    for idx in range(frames):

        if idx % 50 == 0:
            print(f"Processing {idx}/{frames}")

        raw = readmulti_frank(file, idx * byte_per_img, byte_per_img, np.uint8)

        img = np.reshape(raw[:320 * 492], (-1, 492)).T
        img = img[12:, :].T.flatten().astype(np.uint16)

        # Unpack packed 10-bit format
        unpacked = np.zeros(len(img) * 2 // 3, dtype=np.uint16)
        unpacked[0::2] = ((img[0::3] & 0x7F) << 3) | ((img[1::3] & 0xE0) >> 5)
        unpacked[1::2] = ((img[1::3] & 0x07) << 7) | ((img[2::3] & 0xFE) >> 1)

        unpacked = np.reshape(unpacked, (-1, 320))

        unpacked = np.rot90(unpacked, 2)

        # Edge-aware demosaic
        rgb = cv2.demosaicing(unpacked, cv2.COLOR_BAYER_BGGR2RGB_EA)

        # Normalize to full 16-bit range
        rgb = cv2.normalize(rgb, None, 0, 65535, cv2.NORM_MINMAX)
        rgb = rgb.astype(np.uint16)

        # Write raw 16-bit frame to FFmpeg
        process.stdin.write(rgb.tobytes())

    process.stdin.close()
    process.wait()

    print("FFV1 16-bit lossless video written:", output_file)


def WILD_Camera_Decode_HEVC(file=None, fps=16, crf=18):

    import cv2
    import numpy as np
    import os
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

    audio_file = file.replace('misc.dat', 'adc.dat')
    wav_file = audio_file.replace(".dat", ".wav")

    if not os.path.exists(file):
        raise FileNotFoundError("Video file not found")
    if not os.path.exists(audio_file):
        raise FileNotFoundError("Audio file not found")

    if not os.path.exists(wav_file):
        save_binary_audio_to_wav(audio_file, 160000, wav_file)

    width = 320
    height = 320
    byte_per_img = 320 * 500

    with open(file, 'rb') as f:
        f.seek(0, 2)
        total_bytes = f.tell()

    frames = total_bytes // byte_per_img
    print(f"Total frames: {frames}")

    # --------------------------------------------------
    # FFmpeg HEVC 10-bit pipeline
    # --------------------------------------------------
    output_file = file.replace(".dat", "_HEVC10bit.mp4")

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-thread_queue_size", "512",   # ← add this
        "-f", "rawvideo",
        "-pix_fmt", "rgb48le",
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "pipe:0",
        "-i", wav_file,
        "-c:v", "hevc_nvenc",
        "-preset", "p5",
        "-pix_fmt", "p010le",
        "-b:v", "20M",
        "-c:a", "aac",
        "-b:a", "320k",
        output_file
    ]


    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # --------------------------------------------------
    # Precompute bad pixel coordinates
    # --------------------------------------------------
    bad_pixels = []

    bad_coords = [((i-1)//320, (i-1)%320) for i in bad_pixels]

    # --------------------------------------------------
    # Frame decode loop
    # --------------------------------------------------
    for idx in range(frames):

        if idx % 50 == 0:
            print(f"Processing {idx}/{frames}")

        raw = readmulti_frank(file, idx * byte_per_img, byte_per_img, np.uint8)

        img = np.reshape(raw[:320 * 492], (-1, 492)).T
        img = img[12:, :].T.flatten().astype(np.uint16)

        unpacked = np.zeros(len(img) * 2 // 3, dtype=np.uint16)
        unpacked[0::2] = ((img[0::3] & 0x7F) << 3) | ((img[1::3] & 0xE0) >> 5)
        unpacked[1::2] = ((img[1::3] & 0x07) << 7) | ((img[2::3] & 0xFE) >> 1)

        unpacked = np.reshape(unpacked, (-1, 320))

        # Bad pixel correction
        filtered = cv2.medianBlur(unpacked.astype(np.uint16), 3)
        for x, y in bad_coords:
            unpacked[x, y] = filtered[x, y]

        unpacked = np.rot90(unpacked, 2)

        rgb = cv2.demosaicing(unpacked, cv2.COLOR_BAYER_BGGR2RGB_EA)

        # --------------------------------------------------
        # Scale to full 16-bit range properly
        # --------------------------------------------------
        rgb = cv2.normalize(rgb, None, 0, 65535, cv2.NORM_MINMAX)
        rgb = rgb.astype(np.uint16)

        # Write raw frame to ffmpeg
        process.stdin.write(rgb.tobytes())

    process.stdin.close()
    process.wait()

    print("HEVC 10-bit video written:", output_file)


def WILD_Camera_Decode_V2(file=None, fps=16, crf=18):
    """
    Decode WILD raw camera file into high-quality H.264 MP4 with audio.

    Parameters
    ----------
    file : str
        Path to misc.dat
    fps : int
        Frames per second
    crf : int
        H.264 quality (18 = visually lossless, 23 = default)
    """

    import cv2
    import numpy as np
    import os
    import tempfile
    from tkinter import Tk, filedialog
    from moviepy import VideoFileClip, AudioFileClip

    # -------------------------------------------------
    # File selection
    # -------------------------------------------------
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

    audio_file = file.replace('misc.dat', 'adc.dat')

    if not os.path.exists(file):
        raise FileNotFoundError("Video file not found")
    if not os.path.exists(audio_file):
        raise FileNotFoundError("Audio file not found")

    # -------------------------------------------------
    # Convert audio once to WAV (lossless)
    # -------------------------------------------------
    print("Converting audio...")
    wav_file = audio_file.replace(".dat", ".wav")
    if not os.path.exists(wav_file):
        save_binary_audio_to_wav(audio_file, 160000, wav_file)

    # -------------------------------------------------
    # Frame parameters
    # -------------------------------------------------
    width = 320
    height = 320
    byte_per_img = 320 * 500

    with open(file, 'rb') as f:
        f.seek(0, 2)
        total_bytes = f.tell()

    frames = total_bytes // byte_per_img
    print(f"Total frames: {frames}")

    # -------------------------------------------------
    # Temporary uncompressed video (FFV1 lossless)
    # -------------------------------------------------
    temp_video = tempfile.mktemp(suffix=".avi")
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    writer = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

    if not writer.isOpened():
        raise RuntimeError("Failed to open video writer")

    # -------------------------------------------------
    # Precompute bad pixel coordinates
    # -------------------------------------------------
    bad_pixels = []

    bad_coords = [((i-1)//320, (i-1)%320) for i in bad_pixels]

    # -------------------------------------------------
    # Decode loop
    # -------------------------------------------------
    for idx in range(frames):

        if idx % 50 == 0:
            print(f"Processing {idx}/{frames}")

        raw = readmulti_frank(file, idx * byte_per_img, byte_per_img, np.uint8)

        img = np.reshape(raw[:320 * 492], (-1, 492)).T
        img = img[12:, :].T.flatten().astype(np.uint16)

        # Unpack 10-bit packed format
        unpacked = np.zeros(len(img) * 2 // 3, dtype=np.uint16)
        unpacked[0::2] = ((img[0::3] & 0x7F) << 3) | ((img[1::3] & 0xE0) >> 5)
        unpacked[1::2] = ((img[1::3] & 0x07) << 7) | ((img[2::3] & 0xFE) >> 1)

        unpacked = np.reshape(unpacked, (-1, 320))

        # Fix bad pixels (vectorized median)
        filtered = cv2.medianBlur(unpacked.astype(np.uint16), 3)
        for x, y in bad_coords:
            unpacked[x, y] = filtered[x, y]

        # Rotate and demosaic (edge-aware)
        unpacked = np.rot90(unpacked, 2)
        rgb = cv2.demosaicing(unpacked, cv2.COLOR_BAYER_BGGR2RGB_EA)

        # Proper 16-bit → 8-bit scaling (preserve contrast)
        rgb_8 = cv2.normalize(rgb, None, 0, 255, cv2.NORM_MINMAX)
        rgb_8 = rgb_8.astype(np.uint8)

        writer.write(rgb_8)

    writer.release()
    print("Raw video written.")

    # -------------------------------------------------
    # Final H.264 encode (single compression)
    # -------------------------------------------------
    final_output = file.replace(".dat", "_wAudio.mp4")

    video_clip = VideoFileClip(temp_video)
    audio_clip = AudioFileClip(wav_file)

    video_with_audio = video_clip.with_audio(audio_clip)

    video_with_audio.write_videofile(
        final_output,
        codec="libx264",
        preset="slow",
        crf=crf,
        audio_codec="aac",
        audio_bitrate="320k",
        threads=4
    )

    print("Final video written:", final_output)

    os.remove(temp_video)
if __name__ == "__main__":
    WILD_Camera_Decode_HEVC()