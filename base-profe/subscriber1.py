# each subscriber run this code
import pika
from rabbitmq.config import config_reader

url = config_reader.amqp_connection_string()
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.exchange_declare(exchange="business_events", exchange_type="fanout")

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange="business_events", queue=queue_name)

print("Waiting for COMMAND|DOCUMENT|EVENT...")


def callback(ch, method, properties, body):
    print("Event received:", body.decode())

# implicit ack
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
