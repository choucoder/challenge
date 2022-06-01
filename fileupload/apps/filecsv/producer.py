import json
import pika

params = pika.URLParameters(
    "amqps://nqvzwpcc:WnWWMcqbL2AsDS72969v2QcBp2swq8tY@woodpecker.rmq.cloudamqp.com/nqvzwpcc")

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='challenge',
                          body=json.dumps(body), properties=properties)
