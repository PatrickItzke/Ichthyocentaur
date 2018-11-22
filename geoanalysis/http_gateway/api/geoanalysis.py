import connexion
from connexion import NoContent
import uuid
import pika
import sys
import json

class PutResponse(object):
    def __init__(self, processing_id: str, eta: int):
        self.processingid = processing_id
        self.eta = eta
    
    def serialize(self):
        return {
            'processingid': self.processingid,
            'eta': self.eta
        }


class QueuingService(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = channel = self.connection.channel()
        channel.queue_declare(queue='geocoding_task_queue', durable=False)

    def queue_for_geocoding(self, request: dict):
        """ Queues a request for geocoding """
        
        self.channel.basic_publish(exchange='',
                      routing_key='geocoding_task_queue',
                      body=self.json_serialize(request),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))


    def json_serialize(self, request: dict):
        return json.dumps(request)
    
    def __del__(self):
        """ destructor """
        self.connection.close()


geocoding_queue = QueuingService()


def geoanalysis_put(body):

    processing_id = uuid.uuid4().__str__()
    
    for req in body:
        req['processingid'] = processing_id
        geocoding_queue.queue_for_geocoding(req)
        
    eta = determine_processing_time()
    response = PutResponse(processing_id, eta)

    serialized_response = response.serialize()    

    return serialized_response, 202 


def determine_processing_time() -> int:
    return 500

