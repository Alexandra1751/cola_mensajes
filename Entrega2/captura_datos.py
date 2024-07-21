import json
import pika
import random


def generar_formulario():
    formulario = {
        "id": random.randint(1, 1000),
        "nombre": "Nombre_" + str(random.randint(1, 100)),
        "edad": random.randint(18, 99),
        "ciudad": "Ciudad_" + str(random.randint(1, 50)),
    }
    return formulario


def enviar_formulario(formulario):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="cola_formularios", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="cola_formularios",
        body=json.dumps(formulario),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()


if __name__ == "__main__":
    for _ in range(100):
        formulario = generar_formulario()
        enviar_formulario(formulario)
