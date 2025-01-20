import cv2
import numpy as np
import pyautogui
import time
from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed:
        print("Mouse clicked!")
        return True  # Return True if the mouse is clicked
    return False

def wait_for_click():
    # Start the listener to detect mouse events
    with Listener(on_click=on_click) as listener:
        listener.join()

def take_shot():
    if wait_for_click():
        # Capture the screen
        screenshot = pyautogui.screenshot()

        # Convert to a NumPy array
        frame = np.array(screenshot)

        # Convert RGB to BGR (OpenCV uses BGR format)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the frame to the video file
        output.write(frame)

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
    first_shot = True

    print("Recording...")
    
    try:
        while time.time() < end_time:
            take_shot()

        print("Recording complete!")
    except KeyboardInterrupt:
        print("Recording stopped by user.")

    # Release the video writer object
    output.release()
    cv2.destroyAllWindows()