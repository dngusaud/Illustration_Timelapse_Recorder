import cv2
import numpy as np
import pyautogui
import time
import os
from datetime import datetime
import threading
import mss
from pynput.mouse import Listener
from screeninfo import get_monitors
import tkinter as tk
from tkinter import filedialog

# Scaling for 3rd screen.
res_scale = 1.5

keep_record = True

def on_click(x, y, button, pressed):
    if pressed:
        print("Clicked!!")
        return True  # Return True if the mouse is clicked
    return False

def wait_for_click():
    # Start the listener to detect mouse events
    with Listener(on_click=on_click) as listener:
        listener.join()

def get_monitor_size(index = 0):
    monitor = get_monitors()[index]
    x = monitor.x
    y = monitor.y
    width = round(monitor.width )
    height = round(monitor.height)

    return x, y, width, height


def take_shot(x, y, w, h):
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

def get_unique_filename(filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.isfile(new_filename):
        new_filename = f"{base}_({counter}){extension}"
        counter += 1
    
    return new_filename

def main(x, y, w, h):
    # Start the listener in a separate thread
    listener_thread = threading.Thread(target=wait_for_click)
    listener_thread.start()

    # Now you can add other code to run in parallel
    #print("Listener is running in the background...")
    take_shot(x, y, w, h)
    # Optionally, wait for listener to finish before ending the program
    listener_thread.join()

def get_file_destination():
    # Hide the root window
    root = tk.Tk()
    root.withdraw()

    # Open a dialog to choose a directory
    directory_path = filedialog.askdirectory(title="Choose a folder to save the file")

    return directory_path

def check_stop_recording():
    response = input("Would you like to stop record? (y/n): ")
    if response == "y":
        return True
    else:
        return False
    
def on_button_click():
    global keep_record
    keep_record = False
    print("Stop Recording!!")

def run_GUI():
    # Create the main window
    root = tk.Tk()
    root.title("Timelapse Recorder")

    # Create a label widget
    label = tk.Label(root, text="Welcome to Tkinter!")
    label.pack(pady=10)

    # Create a button widget
    button = tk.Button(root, text="Click Me", command=on_button_click)
    button.pack(pady=10)

    # Run the GUI loop
    root.mainloop()

if __name__ == "__main__":

    thread1 = threading.Thread(target=run_GUI)
    thread1.start()

    path = get_file_destination()

    x,y,w,h = get_monitor_size(0)

    title = "test"#input("Record Title: ")
    date = datetime.now().strftime("%Y_%m_%d")
    filename = get_unique_filename(f"{path}/{title}_{date}.mp4") 

    # Set up codec and output video file
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output = cv2.VideoWriter(filename, fourcc, 20.0, (w, h))
    
    timer = 10
    end_time = time.time() + timer

    try:
        while keep_record:#time.time() < end_time:
            main(x, y, w, h)
        print("Recording complete!")
    except KeyboardInterrupt:
        print("Recording stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Release the video writer
        output.release()
        print(f"Recording saved to {filename}")
        # Release the video writer object
        cv2.destroyAllWindows()
    
    thread1.join()


