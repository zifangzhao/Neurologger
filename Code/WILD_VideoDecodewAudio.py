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




def WILD_Camera_Decode(file=None):
    if file is None:
        # Hide the main tkinter window
        root = Tk()
        root.withdraw()

        # Open file dialog to select a file
        file = filedialog.askopenfilename(
            title="Select WILD video file",
            filetypes=[("WILD video file", "*misc.dat"), ("All files", "*.*")]
        )
        if not file:
            print("No file selected.")
            return
        audio_file = file.replace('misc.dat','adc.dat')
    if not os.path.exists(file):
        raise FileNotFoundError("File not found")
    if not os.path.exists(audio_file):
        raise FileNotFoundError("Audio file not found")
    
    #save audio file
    print('Converting audio...')
    audio_file_output = audio_file.replace('.dat','.wav')
    if not os.path.exists(audio_file_output): #only converting if file not exist
        try:
            save_binary_audio_to_wav(audio_file,160000,audio_file_output)
        except:
            print('Error generating wav')
    audio_file_output = audio_file.replace('.dat','.mp3')


    if not os.path.exists(audio_file_output): #only converting if file not exist
        save_binary_audio_to_mp3(audio_file,160000,audio_file_output)

    byte_per_img = 320 * 500
    # Reading the total file size
    with open(file, 'rb') as f:
        f.seek(0, 2)
        fb = f.tell()

    frames = fb // byte_per_img
    width_initial, height_initial = 320, 320

    # Replace '.dat' with '.mp4' for video output file
    
    v_out = file.replace('.dat', '.mp4')

    if not os.path.exists(v_out.replace('.mp4','_wAudio.mp4')): #only converting if file not exist
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        v = cv2.VideoWriter(v_out, fourcc, 16, (320, 320), isColor=True)

        if not v.isOpened():
            print(f"Error: Could not open video writer for file {v_out}")
            return

        for idx in range(frames):
            print("Converting:" + str(idx/frames*100)+"%")
            # Read the raw binary data for the current frame
            data_raw = readmulti_frank(file, idx * byte_per_img, byte_per_img, np.uint8)

            img = np.reshape(data_raw[:320 * 492], (-1, 492)).T
            img = img[12:,:].T  # Remove first 12 rows
            img = img.flatten()
            img = img.astype(np.uint16)

            new_img = np.zeros(len(img) * 2 // 3, dtype=np.uint16)
            new_img[0::2] = np.bitwise_or(np.left_shift(np.bitwise_and(img[0::3], 0x7f), 3).astype(np.uint16),
                                        np.right_shift(np.bitwise_and(img[1::3],0xE0), 5).astype(np.uint16))
            new_img[1::2] = np.bitwise_or(np.left_shift(np.bitwise_and(img[1::3], 0x07), 7).astype(np.uint16),
                                        np.right_shift(np.bitwise_and(img[2::3],0xFE), 1).astype(np.uint16))

            new_img = new_img/4
            new_img = np.reshape(new_img, (-1, 320))
            
            bad_pixels = [7140,6820,6500,6501,6502,13647,13327,13007,13008,13009,33158,32838,32518,32519,32520,85188,84868,84548,84549,84550,20154,19834,19514,19515,19516,26652,26332,26012,26013,26014,39666,39346,39026,39027,39028,46164,45844,45524,45525,45526,52671,52351,52031,52032,52033,59178,58858,58538,58539,58540,65676,65356,65036,65037,65038,72183,71863,71543,71544,71545,78690,78370,78050,78051,78052,91695,91375,91055,91056,91057,98202,97882,97562,97563,97564]
            bad_pixel_coords = [((i-1) // 320, (i-1) % 320) for i in bad_pixels]

            def local_median_filter(img, x, y):
                """ Apply median filter locally around a pixel (x, y) in a 3x3 window """
                x_min, x_max = max(x-1, 0), min(x+2, img.shape[0])  # Ensure within bounds
                y_min, y_max = max(y-1, 0), min(y+2, img.shape[1])
                
                # Extract the 3x3 neighborhood
                neighborhood = img[x_min:x_max, y_min:y_max]
                
                # Compute median and return it
                return np.median(neighborhood)

            # Replace only the bad pixels
            for x, y in bad_pixel_coords:
                new_img[x, y] = local_median_filter(new_img, x, y)
            # filtered_image = scipy.ndimage.median_filter(new_img, size=3)
            # for x, y in bad_pixel_coords:
            #     new_img[x, y] = filtered_image[x, y]
            # Debayering the image (convert Bayer pattern to RGB)
            new_img = np.rot90(new_img, 2)
            debayered_img = cv2.demosaicing(new_img.astype(np.uint16), cv2.COLOR_BAYER_BGGR2RGB)

            # Normalize each channel
            # for k in range(3):
            #     debayered_img[:, :, k] = cv2.normalize(debayered_img[:, :, k], None, 0, 255, cv2.NORM_MINMAX).astype(
            #         np.uint8)



            # Apply the CCM if needed (optional)
            # debayered_img = np.dot(debayered_img.reshape((-1, 3)), CCM).reshape(debayered_img.shape)
            # debayered_img = np.clip(debayered_img, 0, 255)



            # Convert back to 8-bit format for saving in the video
            frame = debayered_img.astype(np.uint8)
            # Apply auto exposure compensation to each frame
            #frame = auto_exposure_compensation(frame)
            frame = adjust_brightness_contrast(frame, target_brightness=160)
            v.write(frame)  # Write the frame to the video

        v.release()
        print("Video written successfully.")

     # Add audio using moviepy
    video_clip = VideoFileClip(v_out)
    audio_clip = AudioFileClip(audio_file_output)
    video_with_audio = video_clip.with_audio(audio_clip)

    # Write the final video
    video_with_audio.write_videofile(v_out.replace('.mp4','_wAudio.mp4'), codec="libx264", audio_codec="aac")
    print("Video with audio written successfully.")

if __name__ == "__main__":
    WILD_Camera_Decode()
