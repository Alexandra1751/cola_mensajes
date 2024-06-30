import threading
import queue
from concurrent.futures import ThreadPoolExecutor


class MessageQueue:
    def __init__(self):
        self.message_queue = queue.Queue()

    def add_message(self, message):
        self.message_queue.put(message)
        print(f"Added message: {message}")

    def process_messages(self):
        while True:
            message = self.message_queue.get()
            if message is None:
                break
            print(f"Processing message: {message}")
            # Add message processing logic here
            self.message_queue.task_done()

    def run(self, num_instances=2):
        with ThreadPoolExecutor(max_workers=num_instances) as executor:
            for _ in range(num_instances):
                executor.submit(self.add_message, "Example message")
                executor.submit(self.process_messages)


if __name__ == "__main__":
    message_queue = MessageQueue()
    message_queue.run()
