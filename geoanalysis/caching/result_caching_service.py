
import json
import time
import pika
import redis

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters('ichthyocentaur_rabbitmq_1', heartbeat=5))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='geoanalysis_result_queue', durable=False)

redisStore = redis.Redis(
    host='ichthyocentaur_redis_1',
    port=6379)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    des_body = json.loads(body)    
    processingId = des_body['processingid']
    redisStore.lpush(processingId, body)

    #confirm delivery of message back to origin
    CHANNEL.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Pushed to Redis cache: %r" % body)   
    print(" [x] Done")


CHANNEL.basic_consume(callback, queue='geoanalysis_result_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
CHANNEL.start_consuming()
