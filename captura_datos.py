import threading
import queue
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import random
import string

class DataCapture:
    def __init__(self):
        self.data_queue = queue.Queue()

    def generate_form(self, form_id):
        form = {
            "id": form_id,
            "field1": ''.join(random.choices(string.ascii_letters, k=5)),
            "field2": ''.join(random.choices(string.ascii_letters, k=5)),
            "field3": ''.join(random.choices(string.ascii_letters, k=5)),
            "field4": ''.join(random.choices(string.ascii_letters, k=5)),
            "field5": ''.join(random.choices(string.ascii_letters, k=5)),
            "field6": ''.join(random.choices(string.ascii_letters, k=5)),
            "field7": ''.join(random.choices(string.ascii_letters, k=5)),
            "field8": ''.join(random.choices(string.ascii_letters, k=5)),
            "field9": ''.join(random.choices(string.ascii_letters, k=5)),
            "field10": ''.join(random.choices(string.ascii_letters, k=5)),
            "field11": ''.join(random.choices(string.ascii_letters, k=5)),
            "field12": ''.join(random.choices(string.ascii_letters, k=5)),
            "field13": ''.join(random.choices(string.ascii_letters, k=5)),
            "field14": ''.join(random.choices(string.ascii_letters, k=5)),
            "field15": ''.join(random.choices(string.ascii_letters, k=5)),
            "field16": ''.join(random.choices(string.ascii_letters, k=5)),
            "field17": ''.join(random.choices(string.ascii_letters, k=5)),
            "field18": ''.join(random.choices(string.ascii_letters, k=5)),
            "field19": ''.join(random.choices(string.ascii_letters, k=5)),
            "field20": ''.join(random.choices(string.ascii_letters, k=5)),
        }
        return form

    def capture_data(self, num_forms):
        for i in range(num_forms):
            form = self.generate_form(f"form_{i}")
            self.data_queue.put(form)
            print(f"Captured data: {form}")

    def process_data(self):
        while True:
            data = self.data_queue.get()
            if data is None:
                break
            print(f"Processing data: {data}")
            response = requests.post("http://localhost:5002/queue", json=data)
            if response.status_code == 200:
                print(f"Data sent to message queue: {data}")
            self.data_queue.task_done()

    def run(self, num_instances=2, num_forms=10):
        with ThreadPoolExecutor(max_workers=num_instances) as executor:
            executor.submit(self.capture_data, num_forms)
            for _ in range(num_instances):
                executor.submit(self.process_data)

if __name__ == "__main__":
    data_capture = DataCapture()
    data_capture.run(num_forms=20)
