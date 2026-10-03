# code for publisher
import pika
from rabbitmq.config import config_reader

url = config_reader.amqp_connection_string()
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.exchange_declare(exchange="business_events", exchange_type="fanout")

message = "CLIENT_ARRIVED"
channel.basic_publish(exchange="business_events", routing_key="", body=message)

print(message, "happened.")

connection.close()