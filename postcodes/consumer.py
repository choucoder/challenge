import json

import pika
import requests
from aiohttp import ClientSession
from decouple import config

from helpers import Manager


params = pika.URLParameters(
    "amqps://nqvzwpcc:WnWWMcqbL2AsDS72969v2QcBp2swq8tY@woodpecker.rmq.cloudamqp.com/nqvzwpcc")

connection = pika.BlockingConnection(params)
channel = connection.channel()
manager = None

channel.queue_declare(queue='challenge')


def callback(ch, method, properties, body):
    global manager

    data = json.loads(body)
    response = requests.get(
        f"http://{config('host')}:8000/api/filecsv{data['file_url']}", allow_redirects=True)

    with open(data['filename'], 'wb') as f:
        f.write(response.content)
        if manager == None or not manager.is_alive():
            manager = Manager(data['filename'])
            manager.start()
        else:
            print("[INFO] Manager is running for a file")


channel.basic_consume("challenge", on_message_callback=callback, auto_ack=True)

print("[INFO] Starting consuming process for get postcodes from uploaded files")
channel.start_consuming()
channel.close()
