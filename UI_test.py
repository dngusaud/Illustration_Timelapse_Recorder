import tkinter as tk
from threading import Thread
import queue
import time
from functools import partial

# Create a queue for communication between threads
data_queue = queue.Queue()

# Flag to signal threads to stop
exit_flag = False

# Consumer function that processes the data
def consumer():
    while not exit_flag:
        try:
            data = data_queue.get(timeout=1)  # Get data from queue with timeout
            if data == "Hello World":
                print(data)  # Output Hello World when data is consumed
        except queue.Empty:
            continue  # Skip if no data in the queue

# Tkinter button callback that starts the producer
def on_button_click(queue):
    queue.put("Hello World")  # Put data in the queue when button is clicked

# Tkinter exit callback to signal threads to stop
def on_exit_button(root):
    global exit_flag
    print("Exiting program...")
    exit_flag = True  # Signal threads to stop
    root.quit()  # Quit the Tkinter event loop, terminating the program

# Tkinter GUI setup
def setup_gui():
    root = tk.Tk()
    root.title("Producer-Consumer Example")

    # Button to trigger the producer-consumer cycle
    button = tk.Button(root, text="Click me!", command=partial(on_button_click, data_queue))
    button.pack(pady=20)

    # Exit button to terminate the program
    exit_button = tk.Button(root, text="Exit", command=partial(on_exit_button, root))
    exit_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    # Start the producer and consumer threads
    consumer_thread = Thread(target=consumer, daemon=True)
    consumer_thread.start()

    # Set up the Tkinter GUI
    setup_gui()

    # After Tkinter GUI closes, join threads to ensure they exit cleanly
    consumer_thread.join()
    print("Program terminated.")
