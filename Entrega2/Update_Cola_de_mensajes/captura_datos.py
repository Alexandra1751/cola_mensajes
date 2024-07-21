import threading
import queue
from concurrent.futures import ThreadPoolExecutor


class DataCapture:
    def __init__(self):
        self.data_queue = queue.Queue()

    def capture_data(self, data):
        self.data_queue.put(data)
        print(f"Captured data: {data}")

    def process_data(self):
        while True:
            data = self.data_queue.get()
            if data is None:
                break
            print(f"Processing data: {data}")
            # Add data processing logic here
            self.data_queue.task_done()

    def run(self, num_instances=2):
        with ThreadPoolExecutor(max_workers=num_instances) as executor:
            for _ in range(num_instances):
                executor.submit(self.capture_data, "Example data")
                executor.submit(self.process_data)


if __name__ == "__main__":
    data_capture = DataCapture()
    data_capture.run()
