import csv
from collections import defaultdict
import json

import arrow
from kafka import KafkaConsumer


class MTATrainTracker(object):

    def __init__(self):
        self.kafka_consumer = KafkaConsumer(
             bootstrap_servers=['localhost:9092'],
             group_id='test_consumer_group',
             auto_offset_reset  = 'smallest',
        )
        self.kafka_topic = 'test'

        # subway line number -> (stop_id, direction) -> next arrival time
        self.arrival_times = defaultdict(lambda: defaultdict(lambda: -1))
        self.stations = {}
        with open('static/mta_stations.csv') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                self.stations[row['GTFS Stop ID']] = row['Stop Name']

    def process_message(self, timestamp, message):
        trip_update = json.loads(message)
        trip_header = trip_update.get('trip')
        if not trip_header:
            return

        route_id = trip_header['routeId']
        trip_id = trip_header['tripId']
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
                    self.save_message(timestamp, stop_id, direction, next_arrival_ts, trip_id)


    def save_message(self, timestamp, stop_id, direction, next_arrival, trip_id):

        csvRow = f"{timestamp},{stop_id},{direction},{next_arrival},{trip_id}\n"
        with open('trip_data_ACE.csv', 'a') as writer:
                writer.write(csvRow)


    def run(self):
        self.kafka_consumer.subscribe([self.kafka_topic])

        while True:
            msg = self.kafka_consumer.poll(1.0)
            if msg is None or not msg.values():
                continue
            # if msg.error() and msg.error().code() != KafkaError._PARTITION_EOF:
            #    raise ValueError('Kafka consumer exception: {}'.format(msg.error()))

            for tp, messages in msg.items():
                for message in messages:
                    self.process_message(message.timestamp, message.value.decode('utf-8'))
o = MTATrainTracker()
o.run()