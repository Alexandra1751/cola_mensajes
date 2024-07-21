from flask import Flask, request, jsonify
import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
ruta_formularios_invalidos = "formularios_invalidos"
ruta_formularios_duplicados = "formularios_duplicados"
os.makedirs(ruta_formularios_invalidos, exist_ok=True)
os.makedirs(ruta_formularios_duplicados, exist_ok=True)

class Validacion:
    def __init__(self):
        self.formularios_validos = []
        self.formularios_invalidos = []

    def validar_formulario(self, formulario):
        if self.es_valido(formulario):
            if self.es_duplicado(formulario):
                self.guardar_formulario(formulario, ruta_formularios_duplicados)
                print(f"Formulario duplicado: {formulario}")
            else:
                self.formularios_validos.append(formulario)
                print(f"Formulario válido: {formulario}")
                respuesta = requests.post("http://localhost:5004/formulario", json=formulario)
                return respuesta.json(), respuesta.status_code
        else:
            self.formularios_invalidos.append(formulario)
            self.guardar_formulario(formulario, ruta_formularios_invalidos)
            print(f"Formulario inválido: {formulario}")

    def es_valido(self, formulario):
        return len(formulario.keys()) == 20

    def es_duplicado(self, formulario):
        respuesta = requests.get(f"http://localhost:5004/formulario/{formulario['id']}")
        return respuesta.status_code == 200

    def guardar_formulario(self, formulario, ruta):
        id_formulario = formulario.get('id')
        with open(os.path.join(ruta, f"{id_formulario}.json"), 'w') as f:
            json.dump(formulario, f)

    def procesar_formularios(self, formularios):
        with ThreadPoolExecutor() as ejecutor:
            ejecutor.map(self.validar_formulario, formularios)

validacion = Validacion()

@app.route('/validar', methods=['POST'])
def validar_formulario():
    datos = request.json
    validacion.procesar_formularios([datos])
    return jsonify({'mensaje': 'Validación completada'}), 200

if __name__ == "__main__":
    app.run(port=5003)
