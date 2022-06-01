import json

import pika
import requests
from aiohttp import ClientSession
from decouple import config

from helpers import PostcodeAPI


params = pika.URLParameters(
    "amqps://nqvzwpcc:WnWWMcqbL2AsDS72969v2QcBp2swq8tY@woodpecker.rmq.cloudamqp.com/nqvzwpcc")

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='challenge')


def callback(ch, method, properties, body):
    data = json.loads(body)
    response = requests.get(
        f"http://{config('host')}:8000/api/filecsv{data['file_url']}", allow_redirects=True)

    with open(data['filename'], 'wb') as f:
        f.write(response.content)
        postcodeApi = PostcodeAPI(data['filename'], chunks=40)
        postcodeApi.start()


channel.basic_consume("challenge", on_message_callback=callback, auto_ack=True)

print("Starting consuming process for get postcodes from uploaded files")
channel.start_consuming()
channel.close()
