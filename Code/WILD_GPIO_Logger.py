import serial
import serial.tools.list_ports
import time
from datetime import datetime
import os

# --- GUI folder picker (built-in) ---
import tkinter as tk
from tkinter import filedialog


def list_comports():
    ports = serial.tools.list_ports.comports()
    for i, port in enumerate(ports):
        print(f"{i + 1}. {port}")
    selected_port = int(input("Please select a port: ")) - 1
    return ports[selected_port].device


def select_save_folder_gui(initial_dir=None):
    """
    Opens a GUI dialog to select the folder where the log file will be saved.
    Returns the selected folder path, or None if user cancels.
    """
    root = tk.Tk()
    root.withdraw()  # hide the main window
    root.attributes("-topmost", True)  # bring dialog to front (useful on Windows)

    folder = filedialog.askdirectory(
        title="Select folder to save log file",
        initialdir=initial_dir or os.getcwd(),
        mustexist=True
    )

    root.destroy()
    return folder if folder else None


def create_log_file_in_folder(folder_path):
    # Timestamped filename: YYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    filename = f"comport_data_{timestamp}.txt"
    filepath = os.path.join(folder_path, filename)

    print(f"Saving data to: {filepath}")
    return filepath


def listen_to_comport(port):
    ser = serial.Serial(port, 119200, timeout=0)

    save_folder = select_save_folder_gui()
    if not save_folder:
        print("No folder selected. Exiting.")
        return

    log_path = create_log_file_in_folder(save_folder)

    # Open once and stream writes
    with open(log_path, "a", encoding="utf-8") as f:
        while True:
            ser.read_until(b"\x3c")  # read until 0x3c
            while ser.inWaiting() < 4:
                time.sleep(0.01)

            data = ser.read(4)

            if data[3] == ord(b"\x3e"):
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                if data[1] == ord(b"\x83"):
                    f.write(f"Time: {current_time}, Data: {data[2]}\n")
                    f.flush()  # ensure data is written immediately

                print(f"Received Signal: {data[2]} Time: {current_time}")


if __name__ == "__main__":
    comport = list_comports()
    listen_to_comport(comport)
