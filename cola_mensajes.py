from flask import Flask, request, jsonify
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
message_queue = queue.Queue()

@app.route('/queue', methods=['POST'])
def enqueue_message():
    data = request.json
    message_queue.put(data)
    return jsonify({'message': 'Message enqueued'}), 200

def process_queue():
    while True:
        data = message_queue.get()
        if data is None:
            break
        print(f"Dequeued data: {data}")
        response = requests.post("http://localhost:5003/validate", json=data)
        if response.status_code == 200:
            print(f"Data sent to validation module: {data}")
        message_queue.task_done()

if __name__ == "__main__":
    threading.Thread(target=process_queue).start()
    app.run(port=5002)
