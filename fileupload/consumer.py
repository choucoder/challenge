import json
import pika

params = pika.URLParameters(
    "amqps://nqvzwpcc:WnWWMcqbL2AsDS72969v2QcBp2swq8tY@woodpecker.rmq.cloudamqp.com/nqvzwpcc")

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='challenge')


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        print("A file has been uploaded for processing: ")
    except:
        print("Str info:")
    print(data)


channel.basic_consume("challenge", on_message_callback=callback, auto_ack=True)

print("Starting consuming")

channel.start_consuming()
channel.close()
