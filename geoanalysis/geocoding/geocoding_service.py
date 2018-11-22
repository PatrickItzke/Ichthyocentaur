
import json
import time
import pika
#from . import geocoder
import geoanalysis.geocoding.geocoder as geocoder

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='geocoding_task_queue', durable=False)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    body = json.loads(body)
    coordinate = geocoder.geocode(body['address'])
    body['longitude'] = coordinate[0]
    body['latitude'] = coordinate[1]
    print(" [x] Geocoded with %r" % coordinate[0])   
    print(" [x] Done")

CHANNEL.basic_consume(callback, queue='geocoding_task_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
CHANNEL.start_consuming()
