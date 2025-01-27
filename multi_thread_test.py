import threading
import queue
import time

# Function that produces data
def producer(q):
    for i in range(5):
        print(f"Producer producing: {i}")
        q.put(i)  # Put data in the queue
        time.sleep(1)

# Function that consumes data
def consumer(q):
    while True:
        data = q.get()  # Get data from the queue
        if data is None:  # Exit condition for consumer
            break
        print(f"Consumer consumed: {data}")
        time.sleep(1)

# Create a Queue to share data
q = queue.Queue()

# Create and start the producer thread
producer_thread = threading.Thread(target=producer, args=(q,))
producer_thread.start()

# Create and start the consumer thread
consumer_thread = threading.Thread(target=consumer, args=(q,))
consumer_thread.start()

# Wait for the producer thread to finish
producer_thread.join()

# Signal the consumer thread to stop (by sending None to the queue)
q.put(None)

# Wait for the consumer thread to finish
consumer_thread.join()

print("Data transfer between threads is complete!")
