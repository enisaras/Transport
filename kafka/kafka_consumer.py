import csv
from collections import defaultdict
import json

import arrow
from kafka import KafkaConsumer

class MTATrainTracker(object):
    def __init__(self):
        self.kafka_consumer = KafkaConsumer(
             bootstrap_servers=['localhost:9092'],
             group_id= 'test_consumer_group',
             auto_offset_reset  = 'smallest',
        )
        self.kafka_topic = 'test'
        with open('csvs/trip_endpoints.json') as reader:
            self.endpoints = json.loads(reader.read())
        self.topics_list = []
        for i in self.endpoints.keys():
            self.topics_list.append(i+'_topic')

        # subway line number -> (stop_id, direction) -> next arrival time
        self.arrival_times = defaultdict(lambda: defaultdict(lambda: -1))
        self.stations = {}
        with open('static/mta_stations.csv') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                self.stations[row['GTFS Stop ID']] = row['Stop Name']

    def process_vehicle_message(self, message):
        vehicle = json.loads(message)
        vehicle_updates = vehicle.get('vehicle')
        # print(vehicle_updates)
        if not vehicle_updates:
            return
        current_stop = vehicle_updates['stopId']
        trip_id = vehicle_updates['trip']['tripId']
        if(trip_id == "091900_7..N"):
            print(vehicle_updates)
        

    def process_trip_message(self, topic_id, timestamp, message):
        trip_update = json.loads(message)
        trip_header = trip_update.get('trip_update')
        if not trip_header:
            return
        # print(trip_header)

        route_id = trip_header['routeId']
        trip_id = trip_header['tripId']
        if(trip_id == "091900_7..N"):
            print(trip_header)
        stop_time_updates = trip_update.get('stopTimeUpdate')
        if not stop_time_updates:
            return
        for update in stop_time_updates:
            if 'arrival' not in update or 'stopId' not in update:
                continue

            stop_id, direction = update['stopId'][0:3], update['stopId'][3:]
            new_arrival_ts = int(update['arrival']['time'])

            next_arrival_ts = self.arrival_times[route_id][(stop_id, direction)]
            now = arrow.now(tz='US/Eastern')

            if new_arrival_ts >= now.timestamp() and \
                    (next_arrival_ts == -1 or new_arrival_ts < next_arrival_ts):
                self.arrival_times[route_id][(stop_id, direction)] = new_arrival_ts

                # convert time delta to minutes
                time_delta = arrow.get(new_arrival_ts) - now
                minutes = divmod(divmod(time_delta.seconds, 3600)[1], 60)[0]

                if(stop_id != 'A29' and stop_id != 'F10'):
                    self.save_trip_message(topic_id, timestamp, stop_id, direction, next_arrival_ts, trip_id)


    def save_trip_message(self, topic_id: str, timestamp, stop_id, direction, next_arrival, trip_id):
        file_name = topic_id.replace("_topic", "")
        csvRow = f"{timestamp},{stop_id},{direction},{next_arrival},{trip_id}\n"
        with open('csvs/'+file_name+'_data.csv', 'a') as writer:
                writer.write(csvRow)


    def run(self):

        self.kafka_consumer.subscribe(self.topics_list)

        while True:
            msg = self.kafka_consumer.poll(1.0)
            if msg is None or not msg.values():
                continue
            # if msg.error() and msg.error().code() != KafkaError._PARTITION_EOF:
            #    raise ValueError('Kafka consumer exception: {}'.format(msg.error()))

            for tp, messages in msg.items():
                for message in messages:
                    self.process_vehicle_message(message.value.decode('utf-8'))
                    self.process_trip_message(tp.topic, message.timestamp, message.value.decode('utf-8'))
o = MTATrainTracker()
o.run()