from time import sleep
from json import dumps
from kafka import KafkaProducer
import binascii


def prod(str):
    print("calling producer")
    producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],api_version=(0,11,5),
    value_serializer=lambda v: binascii.hexlify(v.encode('utf-8')))
    producer.send('topic_test', value=str)
    sleep(0.5)