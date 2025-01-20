import cv2
import numpy as np
import pyautogui
from pynput.mouse import Listener
import threading
import time

def on_click(x, y, button, pressed):
    if pressed:
        print("Mouse clicked!")
        return True  # Return True if the mouse is clicked
    return False

def wait_for_click():
    # Create a new listener instance for each thread
    listener = Listener(on_click=on_click)
    listener.start()  # Start listener in a non-blocking manner
    listener.join()   # Keep the listener running

def take_shot():
    # Capture the screen
    screenshot = pyautogui.screenshot()

    # Convert to a NumPy array
    frame = np.array(screenshot)

    # Convert RGB to BGR (OpenCV uses BGR format)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Write the frame to the video file
    output.write(frame)



# Example of how to call the function in a separate thread
def main():
    # Start the listener in a separate thread
    listener_thread = threading.Thread(target=wait_for_click)
    listener_thread.start()

    # Now you can add other code to run in parallel
    print("Listener is running in the background...")
    take_shot()
    # Optionally, wait for listener to finish before ending the program
    listener_thread.join()



# Start the main function
if __name__ == "__main__":
    # Define screen resolution
    screen_size = pyautogui.size()

    # Set up codec and output video file
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    output = cv2.VideoWriter("screen_record_with_cursor.avi", fourcc, 20.0, (screen_size.width, screen_size.height))

    # Record time duration (in seconds)
    record_duration = 10  # Adjust as needed
    end_time = time.time() + record_duration
    prev_time = time.time()

    print("Recording...")
    while time.time() < end_time:
        main()

    # Release the video writer object
    output.release()
    cv2.destroyAllWindows()