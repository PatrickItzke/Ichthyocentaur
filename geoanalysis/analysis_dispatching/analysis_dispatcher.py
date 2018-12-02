
import json
import time
import pika


CONNECTION = pika.BlockingConnection(pika.ConnectionParameters('ichthyocentaur_rabbitmq_1'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='analysis_task_queue', durable=False)

queues = {
    'precipitation': 'precipiation_lookup_task_queue'
}

#Iterate over the queues dict and initialize queues
for key, value in queues.items():
    CHANNEL.queue_declare(queue=value, durable=False)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    body = json.loads(body)
    
    for topic in body['topics']:
       CHANNEL.basic_publish('', queues[topic], json.dumps(body))

    #confirm delivery of this message back to origin
    CHANNEL.basic_ack(delivery_tag=method.delivery_tag)

    print(" [x] Topic dispatching: %r" % json.dumps(body))   
    print(" [x] Done")

CHANNEL.basic_consume(callback, queue='analysis_task_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
CHANNEL.start_consuming()
