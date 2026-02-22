import cv2
import numpy as np
import os
from tkinter import Tk
from tkinter import filedialog
import wave
from scipy.signal import butter, filtfilt
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip
import lameenc
import matplotlib.pyplot as plt
import time
import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Relaunch as admin
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        " ".join(sys.argv),
        None,
        1
    )
    sys.exit(0)
    
def list_windows_disks():
    print("Available drives (physical):")
    for i in range(10):
        device_path = f"\\\\.\\PhysicalDrive{i}"
        try:
            with open(device_path, 'rb+'):
                print(f"[{i}] {device_path}")
        except PermissionError:
            print(f"[{i}] {device_path} (Permission Denied - run as admin)")
        except Exception:
            pass

def select_disk():
    list_windows_disks()
    index = input("Enter the disk index to read (e.g., 0): ")
    if(index==0):
        return None;
    return f"\\\\.\\PhysicalDrive{index}"
    
def readmulti_frank(file, byte_offset, byte_length, dtype):
    """ Function to read binary data from file """
    with open(file, 'rb+',buffering=0) as f:
        f.seek(byte_offset)
        data = f.read(byte_length)
    return np.frombuffer(data, dtype=dtype)


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
        print("No Drive Selected.")
        return

    SECTOR_SIZE = 512
    byte_per_img = 320 * 500
    last_time = time.time()
    frame_count = 0
    fps=0
    # 1. Create a resizable window BEFORE showing the image
    cv2.namedWindow("Live Preview", cv2.WINDOW_NORMAL)  # This makes the window resizable

    # Optional: Set minimum size
    cv2.resizeWindow("Live Preview", 320, 320)
    # Reading the total file size
    while(1):
        width_initial, height_initial = 320, 320

        data_raw = readmulti_frank(file, 0x1000*SECTOR_SIZE, 320*512, np.uint8)
        print("image read successfully")
        frame_count += 1
        current_time = time.time()
        elapsed = current_time - last_time

        if elapsed >= 1.0:  # Every 1 second
            fps = frame_count / elapsed
            frame_count = 0
            last_time = current_time
        img = np.reshape(data_raw[:320 * 492], (-1, 492)).T
        img = img[12:,:].T  # Remove first 12 rows
        img = img.flatten()
        img = img.astype(np.uint16)

        new_img = np.zeros(len(img) * 2 // 3, dtype=np.uint16)
        new_img[0::2] = np.bitwise_or(np.bitwise_and(np.left_shift(img[0::3], 3).astype(np.uint16), 0x3f8),
                                    np.right_shift(img[1::3], 5).astype(np.uint16))
        new_img[1::2] = np.bitwise_or(np.bitwise_and(np.left_shift(img[1::3], 7).astype(np.uint16), 0x380),
                                    np.right_shift(img[2::3], 1).astype(np.uint16))

        new_img = new_img/4
        new_img = np.reshape(new_img, (-1, 320))
        new_img = np.rot90(new_img, 2)

        # Debayering the image (convert Bayer pattern to RGB)
        debayered_img = cv2.demosaicing(new_img.astype(np.uint16), cv2.COLOR_BAYER_BGGR2RGB)
        #debayered_img = (debayered_img / debayered_img.max() * 255).astype(np.uint8)
        
         # === Get window size ===
        
        win_x, win_y, win_w, win_h = cv2.getWindowImageRect("Live Preview")


        # === Compute square region ===
        if win_w>0:
            side = min(win_w, win_h)
            offset_x = (win_w - side) // 2
            offset_y = (win_h - side) // 2

        # === Resize image to square size ===
        resized = cv2.resize(debayered_img, (side, side), interpolation=cv2.INTER_LINEAR)

        # === Create black canvas ===
        display = np.zeros((win_h, win_w, 3), dtype=np.uint8)

        # === Paste square image into center of canvas ===
        display[offset_y:offset_y+side, offset_x:offset_x+side] = resized


        cv2.putText(display, f"FPS: {fps:.2f}", (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (230, 216, 173), 2)
        cv2.imshow("Live Preview", display.astype(np.uint8))
        
        # === Press ESC to break ===
        if cv2.waitKey(1) & 0xFF == 27:
            break
        #time.sleep(0.2)
        #plt.imshow(debayered_img.astype(np.uint8))
        #plt.show()

        # Normalize each channel
        # for k in range(3):
        #     debayered_img[:, :, k] = cv2.normalize(debayered_img[:, :, k], None, 0, 255, cv2.NORM_MINMAX).astype(
        #         np.uint8)



        # Apply the CCM if needed (optional)
        # debayered_img = np.dot(debayered_img.reshape((-1, 3)), CCM).reshape(debayered_img.shape)
        # debayered_img = np.clip(debayered_img, 0, 255)


            


if __name__ == "__main__":
    disk = select_disk()
    WILD_Camera_Decode(disk)
