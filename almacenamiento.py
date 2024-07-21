from flask import Flask, request, jsonify
from threading import Lock, Thread
import requests
import json

app = Flask(__name__)
almacenamiento = {}
lock = Lock()
seguidores = []

@app.route('/formulario', methods=['POST'])
def guardar_formulario():
    datos = request.json
    print(f"Datos recibidos para guardar: {datos}")
    id_formulario = datos.get('id')
    with lock:
        if id_formulario in almacenamiento:
            print(f"Formulario duplicado: {id_formulario}")
            return jsonify({'mensaje': 'Formulario duplicado'}), 409
        almacenamiento[id_formulario] = datos
        print(f"Formulario guardado: {id_formulario}")
        replicar(id_formulario, datos)
    return jsonify({'mensaje': 'Formulario guardado'}), 201

@app.route('/formulario/<id_formulario>', methods=['GET'])
def obtener_formulario(id_formulario):
    print(f"Solicitando formulario: {id_formulario}")
    with lock:
        formulario = almacenamiento.get(id_formulario)
    if formulario is None:
        print(f"Formulario no encontrado: {id_formulario}")
        return jsonify({'mensaje': 'Formulario no encontrado'}), 404
    return jsonify(formulario), 200

@app.route('/formularios', methods=['GET'])
def obtener_todos_formularios():
    with lock:
        formularios = list(almmacenamiento.values())
    return jsonify(formularios), 200

@app.route('/formulario/<id_formulario>', methods=['DELETE'])
def eliminar_formulario(id_formulario):
    with lock:
        if id_formulario in almacenamiento:
            del almacenamiento[id_formulario]
            return jsonify({'mensaje': 'Formulario eliminado'}), 200
    return jsonify({'mensaje': 'Formulario no encontrado'}), 404

@app.route('/formulario/<id_formulario>', methods=['PUT'])
def reemplazar_formulario(id_formulario):
    datos = request.json
    with lock:
        almacenamiento[id_formulario] = datos
    return jsonify({'mensaje': 'Formulario reemplazado'}), 200

def replicar(id_formulario, datos):
    print(f"Iniciando replicación para: {id_formulario}")
    for seguidor in seguidores:
        try:
            print(f"Replicando datos a seguidor: {seguidor}")
            response = requests.post(f"{seguidor}/formulario", json=datos)
            if response.status_code == 201:
                print(f"Datos replicados correctamente en el seguidor: {seguidor}")
            else:
                print(f"Error al replicar datos en el seguidor: {seguidor}, Código de estado: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al replicar datos en el seguidor: {seguidor}, Error: {e}")

@app.route('/agregar_seguidor', methods=['POST'])
def agregar_seguidor():
    url_seguidor = request.json.get('url')
    if url_seguidor not in seguidores:
        seguidores.append(url_seguidor)
        print(f"Seguidor agregado: {url_seguidor}")
    return jsonify({'mensaje': 'Seguidor agregado'}), 200

@app.route('/lider', methods=['POST'])
def promover_lider():
    url_nuevo_lider = request.json.get('url')
    Thread(target=sincronizar_datos_con_lider, args=(url_nuevo_lider,)).start()
    return jsonify({'mensaje': 'Líder promovido'}), 200

def sincronizar_datos_con_lider(url_lider):
    global almacenamiento
    try:
        respuesta = requests.get(f"{url_lider}/formularios")
        if respuesta.status_code == 200:
            formularios = respuesta.json()
            with lock:
                for formulario in formularios:
                    id_formulario = formulario.get('id')
                    almacenamiento[id_formulario] = formulario
            print("Sincronización con el nuevo líder completada")
        else:
            print(f"Error al sincronizar datos con el nuevo líder: {url_lider}, Código de estado: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error al sincronizar datos con el nuevo líder: {url_lider}, Error: {e}")

def ejecutar_servidor(puerto):
    app.run(port=puerto, threaded=True)

if __name__ == '__main__':
    puerto = int(input("Ingrese el número de puerto: "))
    Thread(target=ejecutar_servidor, args=(puerto,)).start()
