from flask import Flask, request, jsonify
from threading import Lock, Thread
import requests
import json

app = Flask(__name__)
storage = {}
lock = Lock()
followers = []

@app.route('/formulario', methods=['POST'])
def guardar_formulario():
    data = request.json
    form_id = data.get('id')
    with lock:
        if form_id in storage:
            return jsonify({'message': 'Formulario duplicado'}), 409
        storage[form_id] = data
        replicate(form_id, data)
    return jsonify({'message': 'Formulario guardado'}), 201

@app.route('/formulario/<form_id>', methods=['GET'])
def obtener_formulario(form_id):
    with lock:
        form = storage.get(form_id)
    if form is None:
        return jsonify({'message': 'Formulario no encontrado'}), 404
    return jsonify(form), 200

@app.route('/formularios', methods=['GET'])
def obtener_todos_formularios():
    with lock:
        forms = list(storage.values())
    return jsonify(forms), 200

@app.route('/formulario/<form_id>', methods=['DELETE'])
def eliminar_formulario(form_id):
    with lock:
        if form_id in storage:
            del storage[form_id]
            return jsonify({'message': 'Formulario eliminado'}), 200
    return jsonify({'message': 'Formulario no encontrado'}), 404

@app.route('/formulario/<form_id>', methods=['PUT'])
def reemplazar_formulario(form_id):
    data = request.json
    with lock:
        storage[form_id] = data
    return jsonify({'message': 'Formulario reemplazado'}), 200

def replicate(form_id, data):
    for follower in followers:
        requests.post(f"{follower}/formulario", json=data)

@app.route('/add_follower', methods=['POST'])
def add_follower():
    follower_url = request.json.get('url')
    followers.append(follower_url)
    return jsonify({'message': 'Follower added'}), 200

@app.route('/leader', methods=['POST'])
def promote_leader():
    new_leader_url = request.json.get('url')
    Thread(target=sync_data_with_leader, args=(new_leader_url,)).start()
    return jsonify({'message': 'Leader promoted'}), 200

def sync_data_with_leader(leader_url):
    global storage
    response = requests.get(f"{leader_url}/formularios")
    if response.status_code == 200:
        forms = response.json()
        with lock:
            for form in forms:
                form_id = form.get('id')
                storage[form_id] = form
    print("Synchronization with new leader completed")

def run_server(port):
    app.run(port=port, threaded=True)

if __name__ == '__main__':
    port = int(input("Enter the port number: "))
    Thread(target=run_server, args=(port,)).start()
