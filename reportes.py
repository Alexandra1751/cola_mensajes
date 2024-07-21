from flask import Flask, request, jsonify

app = Flask(__name__)
storage = {}  # Esto debe ser compartido con el módulo de almacenamiento

@app.route('/reportes/<reporte_tipo>', methods=['GET'])
def generar_reporte(reporte_tipo):
    if reporte_tipo == 'genero':
        hombres = sum(1 for form in storage.values() if form.get('genero') == 'M')
        mujeres = sum(1 for form in storage.values() if form.get('genero') == 'F')
        return jsonify({'hombres': hombres, 'mujeres': mujeres}), 200
    elif reporte_tipo == 'educacion':
        educacion = {}
        for form in storage.values():
            nivel = form.get('nivel_educacion')
            if nivel not in educacion:
                educacion[nivel] = 0
            educacion[nivel] += 1
        return jsonify(educacion), 200
    return jsonify({'message': 'Reporte no encontrado'}), 404

if __name__ == "__main__":
    port = int(input("Enter the port number for the report server: "))
    app.run(port=port)
