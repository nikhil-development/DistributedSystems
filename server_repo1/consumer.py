from kafka import KafkaConsumer
from json import loads
from time import sleep
import binascii
consumer = KafkaConsumer(
    'topic_test',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
     value_deserializer=lambda v: binascii.unhexlify(v).decode('utf-8')
)
for event in consumer:
    event_data = event.value
    # Do whatever you want
    print(event_data)
    sleep(2)