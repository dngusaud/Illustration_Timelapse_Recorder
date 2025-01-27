# Video Recording
import cv2
import os
import mss
from datetime import datetime
import numpy as np
from pynput.mouse import Listener

#GUI
import tkinter as tk
from tkinter import filedialog

# Architecture
import queue
from enum import Enum
from threading import Thread
from functools import partial

# Create a queue for communication between threads
data_queue = queue.Queue()

# Flag to signal threads to stop
exit_flag = False
on_air_flag = False


# Task enums in priority order
class Task(Enum):
    TAKE_SHOT = 1   # take a shot for timelapse record
    START_RECORD = 2
    STOP_RECORD = 3
    SET_OUTPUT_PATH = 4
    TERMINATE = 5

def on_click(x, y, button, pressed):
    if pressed:
        return True
    return False

def wait_for_click():
    # Start the listener to detect mouse events
    with Listener(on_click=on_click) as listener:
        listener.join()
    return True

#Main event producer from user click
def producer(task):
    data_queue.put(task)

def detect_click():
    while not exit_flag:
        while on_air_flag:
            if wait_for_click():
                data_queue.put(Task.TAKE_SHOT)
                print("Clicked")

# Consumer function that processes the data
def consumer():
    global on_air_flag
    while not exit_flag:
        try:
            data = data_queue.get(timeout=1)  # Get data from queue with timeout
            if data is Task.STOP_RECORD:
                print("Stop Recording")
                on_air_flag = False
                stop_record()
            elif data is Task.START_RECORD:
                print("Start Recording")
                on_air_flag = True
                #start_record()
            elif data is Task.SET_OUTPUT_PATH:
                print("Defining output Path")
            elif data is Task.TAKE_SHOT:
                print("Took a shot")
                take_shot()
        except queue.Empty:
            continue  # Skip if no data in the queue

# Tkinter exit callback to signal threads to stop
def on_exit_button(root):
    global exit_flag
    print("Exiting program...")
    exit_flag = True  # Signal threads to stop
    root.quit()  # Quit the Tkinter event loop, terminating the program

def get_unique_filename(filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.isfile(new_filename):
        new_filename = f"{base}_({counter}){extension}"
        counter += 1
    
    return new_filename

def get_file_destination():
    # Hide the root window
    root = tk.Tk()
    root.withdraw()

    # Open a dialog to choose a directory
    directory_path = filedialog.askdirectory(title="Choose a folder to save the file")

    return directory_path


def stop_record():
    # Release the video writer
    output.release()
    print(f"Recording saved")
    # Release the video writer object
    cv2.destroyAllWindows()

def take_shot(x = 0, y = 0, w = 1920, h = 1080):
    # Create an instance of mss
    with mss.mss() as sct:
        # Get information about all monitors
        monitor_region = {"top": y, "left": x, "width": w, "height": h}

        # Capture the screen
        screenshot = sct.grab(monitor_region)

        # Convert the screenshot to a NumPy array
        frame = np.array(screenshot)

        # Convert BGRA to BGR (OpenCV uses BGR format)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Write the frame to the video file
        output.write(frame)


# Tkinter GUI setup
def setup_gui():
    root = tk.Tk()
    root.title("Producer-Consumer Example")

    # Button to trigger the producer-consumer cycle
    button = tk.Button(root, text="Set Output Path", command=partial(producer, Task.SET_OUTPUT_PATH))
    button.pack(pady=20)

    # Button to trigger the producer-consumer cycle
    button = tk.Button(root, text="Start Record", command=partial(producer, Task.START_RECORD))
    button.pack(pady=20)

    # Button to trigger the producer-consumer cycle
    button = tk.Button(root, text="Stop Record", command=partial(producer, Task.STOP_RECORD))
    button.pack(pady=20)

    # Exit button to terminate the program
    exit_button = tk.Button(root, text="Exit", command=partial(on_exit_button, root))
    exit_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    # Start the producer and consumer threads
    click_detect_thread = Thread(target=detect_click, daemon=True)
    consumer_thread = Thread(target=consumer, daemon=True)
    click_detect_thread.start()
    consumer_thread.start()

    title = "test"#input("Record Title: ")
    date = datetime.now().strftime("%Y_%m_%d")
    path = get_file_destination()
    filename = get_unique_filename(f"{path}/{title}_{date}.mp4") 

    # Set up codec and output video file
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output = cv2.VideoWriter(filename, fourcc, 20.0, (1920, 1080))

    # Set up the Tkinter GUI
    setup_gui()

    # After Tkinter GUI closes, join threads to ensure they exit cleanly
    consumer_thread.join()
    click_detect_thread.join()
    print("Program terminated.")
