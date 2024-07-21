import threading
import queue
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
cola_mensajes = queue.Queue()

@app.route('/cola', methods=['POST'])
def encolar_mensaje():
    datos = request.json
    cola_mensajes.put(datos)
    return jsonify({'mensaje': 'Mensaje encolado'}), 200

def procesar_cola():
    while True:
        datos = cola_mensajes.get()
        if datos is None:
            break
        print(f"Datos desencolados: {datos}")
        respuesta = requests.post("http://localhost:5003/validar", json=datos)
        if respuesta.status_code == 200:
            print(f"Datos enviados al módulo de validación: {datos}")
        cola_mensajes.task_done()

if __name__ == "__main__":
    threading.Thread(target=procesar_cola).start()
    app.run(port=5002)
