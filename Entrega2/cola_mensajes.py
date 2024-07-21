import pika


def crear_cola():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="cola_formularios", durable=True)
    connection.close()


if __name__ == "__main__":
    crear_cola()
