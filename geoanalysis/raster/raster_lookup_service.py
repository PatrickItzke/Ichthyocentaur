
import json
import time
import pika
import rasterio
import raster_lookup

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters('ichthyocentaur_rabbitmq_1'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='precipiation_lookup_task_queue', durable=False)
CHANNEL.queue_declare(queue='geoanalysis_result_queue', durable=False)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    body: dict = json.loads(body)
    with rasterio.open('/var/rasterdata/TRMM_3B43M_2016-08-01_rgb_1440x720.TIFF') as src:
            
            reader = raster_lookup.RasterValueReader(src, windowed_read=True)
            value = reader.getCoordinateBandValue(body['latitude'], body['longitude'], 1)            
            body['topic_name'] = 'precipiation' 
            body['topic_value'] = int(value)
    
    
    CHANNEL.basic_publish('', 'geoanalysis_result_queue', json.dumps(body))
    #confirm delivery of message back to origin
    CHANNEL.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Raster lookup: %r" % json.dumps(body))   
    print(" [x] Done")

CHANNEL.basic_consume(callback, queue='precipiation_lookup_task_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
CHANNEL.start_consuming()
