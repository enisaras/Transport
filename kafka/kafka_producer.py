import time

import requests
from google.protobuf.json_format import MessageToJson
from kafka import KafkaProducer

import gtfs_realtime_pb2


class MTARealTime(object):

    def __init__(self):
        with open('.mta_api_key', 'r') as key_in:
            self.api_key = key_in.read().strip()

        self.mta_api_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace'
        self.kafka_topic = 'test'
        self.kafka_producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    def produce_trip_updates(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(self.mta_api_url, headers={'x-api-key': self.api_key})
        feed.ParseFromString(response.content)
        for entity in feed.entity:
            print(entity)
            if entity.HasField('trip_update'):
                update_json = MessageToJson(entity.trip_update)
                print(update_json)
                self.kafka_producer.send(
                    self.kafka_topic, update_json.encode('utf-8'))

        self.kafka_producer.flush()

    def run(self):
        while True:
            self.produce_trip_updates()
            time.sleep(30)


o = MTARealTime()
o.run()