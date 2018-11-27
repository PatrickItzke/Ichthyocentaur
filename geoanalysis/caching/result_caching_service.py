
import json
import time
import pika
import redis

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='geoanalysis_result_queue', durable=False)

redisStore = redis.Redis(
    host='localhost',
    port=6379)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    des_body = json.loads(body)    
    processingId = des_body['processingid']
    redisStore.lpush(processingId, body)

    print(" [x] Pushed to Redis cache: %r" % body)   
    print(" [x] Done")

CHANNEL.basic_consume(callback, queue='geoanalysis_result_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
CHANNEL.start_consuming()
