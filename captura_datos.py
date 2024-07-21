import threading
import queue
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import random
import string

class CapturaDatos:
    def __init__(self):
        self.data_queue = queue.Queue()

    def generar_formulario(self, id_formulario):
        formulario = {
            "id": id_formulario,
            "nombre": ''.join(random.choices(string.ascii_letters, k=10)),
            "edad": random.randint(1, 100),
            "genero": random.choice(['M', 'F']),
            "direccion": ''.join(random.choices(string.ascii_letters + string.digits, k=15)),
            "telefono": ''.join(random.choices(string.digits, k=10)),
            "email": ''.join(random.choices(string.ascii_letters, k=7)) + "@ejemplo.com",
            "ocupacion": random.choice(['Ingeniero', 'Doctor', 'Profesor']),
            "nivel_educacion": random.choice(['Ninguno', 'Primaria', 'Secundaria', 'Universidad']),
            "estado_civil": random.choice(['Soltero', 'Casado']),
            "numero_hijos": random.randint(0, 5),
            "ingreso_mensual": random.randint(100, 10000),
            "vivienda_propia": random.choice([True, False]),
            "vehiculo_propio": random.choice([True, False]),
            "servicios_basicos": random.sample(['electricidad', 'agua', 'internet', 'gas'], k=3),
            "discapacidad": random.choice([True, False]),
            "etnia": random.choice(['Hispano', 'Indígena', 'Afro-Ecuatoriano']),
            "lengua_materna": random.choice(['Español', 'Kichwa', 'Shuar']),
            "nacionalidad": "Ecuatoriana",
            "ciudad_residencia": random.choice(['Guayaquil', 'Quito', 'Cuenca'])
        }
        return formulario

    def capturar_datos(self, num_formularios):
        for i in range(num_formularios):
            formulario = self.generar_formulario(f"formulario_{i}")
            self.data_queue.put(formulario)
            print(f"Datos capturados: {formulario}")

    def procesar_datos(self):
        while True:
            datos = self.data_queue.get()
            if datos is None:
                break
            print(f"Procesando datos: {datos}")
            respuesta = requests.post("http://localhost:5002/cola", json=datos)
            if respuesta.status_code == 200:
                print(f"Datos enviados a la cola de mensajes: {datos}")
            self.data_queue.task_done()

    def ejecutar(self, num_instancias=2, num_formularios=10):
        with ThreadPoolExecutor(max_workers=num_instancias) as ejecutor:
            ejecutor.submit(self.capturar_datos, num_formularios)
            for _ in range(num_instancias):
                ejecutor.submit(self.procesar_datos)

if __name__ == "__main__":
    captura_datos = CapturaDatos()
    while True:
        num_formularios = int(input("Ingrese el número de formularios a generar: "))
        captura_datos.ejecutar(num_formularios=num_formularios)
        continuar = input("¿Desea generar más formularios? (sí/no): ")
        if continuar.lower() != 'sí':
            break
