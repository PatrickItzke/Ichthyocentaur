
import json
import time
import pika
import geoanalysis.raster.raster_lookup as raster_lookup
import rasterio

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='precipiation_lookup_task_queue', durable=False)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    body = json.loads(body)
    with rasterio.open('./tests/TRMM_3B43M_2016-08-01_rgb_1440x720.tiff') as src:
            
            reader = raster_lookup.RasterValueReader(src, windowed_read=True)
            value = reader.getCoordinateBandValue(body['latitude'], body['longitude'], 1)
            body['precipiation'] = value
    print(" [x] Raster lookup: %r" % json.dumps(body))   
    print(" [x] Done")

CHANNEL.basic_consume(callback, queue='geocoding_task_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
CHANNEL.start_consuming()
