import connexion
from connexion import NoContent
import uuid
import pika
import sys
import json
import redis
import time


redisStore = redis.Redis(
    host='ichthyocentaur_redis_1',
    port=6379)


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
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='ichthyocentaur_rabbitmq_1'))
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

    redisStore.set(processing_id + '_requesttime', time.gmtime.__str__())
    redisStore.set(processing_id + '_starttime', time.time.__str__())
    
    req_counter = 0
    for req in body:
        req_counter += 1
        req['processingid'] = processing_id
        geocoding_queue.queue_for_geocoding(req)

    redisStore.set(processing_id + '_request_count', int(1))
        
    eta = determine_processing_time()
    response = PutResponse(processing_id, eta)

    serialized_response = response.serialize()    

    return serialized_response, 202 


def geoanalysis_status(processingid):
    if len(redisStore.keys(processingid + '*')) == 0:
        return None, 404
    
    response = dict()
    response['processingid'] = processingid

    processed_req_count = redisStore.llen(processingid)
    processing_total_count = int(redisStore.get(processingid + '_request_count'))

    if processed_req_count < processing_total_count:
        response['status'] = 'In Progress'
    else:
        response['status'] = 'Done'

    response['finishedlocations'] = processed_req_count
    response['totallocations'] = processing_total_count

    return response, 200

def geoanalysis_get(processingid):

    location_topic_values = dict()
    #get values from redis for processingid    
    location_values = redisStore.lrange(processingid, 0, redisStore.llen(processingid)-1)

    for location_entry in location_values:
        
        #print(location_entry)
        #entry_string = str(location_entry)
        print(location_entry.__str__())

        entry_dict = json.loads(location_entry)
        key =  entry_dict['latitude'].__str__() + '_' + entry_dict['longitude'].__str__()
        
        if location_topic_values.__contains__(key) == False:
            location_topic_values[key] = dict()

        if location_topic_values[key].__contains__('latitude') == False:
            location_topic_values[key]['latitude'] = entry_dict['latitude']

        if location_topic_values[key].__contains__('longitude') == False:
            location_topic_values[key]['longitude'] = entry_dict['longitude']

        if location_topic_values[key].__contains__('topics') == False:
            location_topic_values[key]['topics'] = [{'topic': entry_dict['topic_name'],
                                                     'topic_value': entry_dict['topic_value']}]
        else:
            location_topic_values[key]['topics'].append({'topic': entry_dict['topic_name'],
                                                     'topic_value': entry_dict['topic_value']})
    
    response = []
    for coordinate_values in location_topic_values.values():
        response.append(coordinate_values)

    return response, 200

          
def determine_processing_time() -> int:
    return 500


    




