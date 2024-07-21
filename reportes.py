from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Dirección de la réplica del módulo de almacenamiento
url_almacenamiento = "http://localhost:5004"

@app.route('/reportes/genero', methods=['GET'])
def reporte_genero():
    respuesta = requests.get(f"{url_almacenamiento}/formularios")
    if respuesta.status_code == 200:
        formularios = respuesta.json()
        hombres = sum(1 for form in formularios if form.get('genero') == 'M')
        mujeres = sum(1 for form in formularios if form.get('genero') == 'F')
        total = hombres + mujeres
        if total == 0:
            return jsonify({'hombres': 0, 'mujeres': 0}), 200
        return jsonify({'hombres': (hombres / total) * 100, 'mujeres': (mujeres / total) * 100}), 200
    return jsonify({'mensaje': 'Error al obtener los datos'}), 500

@app.route('/reportes/educacion_mujeres', methods=['GET'])
def reporte_educacion_mujeres():
    respuesta = requests.get(f"{url_almacenamiento}/formularios")
    if respuesta.status_code == 200:
        formularios = respuesta.json()
        educacion = {}
        for form in formularios:
            if form.get('genero') == 'F' and form.get('edad') > 18:
                nivel = form.get('nivel_educacion')
                if nivel not in educacion:
                    educacion[nivel] = 0
                educacion[nivel] += 1
        return jsonify(educacion), 200
    return jsonify({'mensaje': 'Error al obtener los datos'}), 500

@app.route('/reportes/edad', methods=['GET'])
def reporte_edad():
    respuesta = requests.get(f"{url_almacenamiento}/formularios")
    if respuesta.status_code == 200:
        formularios = respuesta.json()
        edades = {}
        for form in formularios:
            edad = form.get('edad')
            if edad not in edades:
                edades[edad] = 0
            edades[edad] += 1
        return jsonify(edades), 200
    return jsonify({'mensaje': 'Error al obtener los datos'}), 500

if __name__ == "__main__":
    port = int(input("Ingrese el número de puerto para el servidor de reportes: "))
    app.run(port=port)
