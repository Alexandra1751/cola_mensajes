import json
import pika


def validar_formulario(formulario):
    # Lógica de validación
    print("Validando formulario:", formulario)


def callback(ch, method, properties, body):
    formulario = json.loads(body)
    validar_formulario(formulario)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumir_formularios():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="cola_formularios", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="cola_formularios", on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    consumir_formularios()
