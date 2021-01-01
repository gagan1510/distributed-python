import os
import sys
from datetime import datetime

import logging
from pythonjsonlogger import jsonlogger

import inspect

def print_caller_info():
    try:
        # Get the full stack
        stack = inspect.stack()

        # Get one level up from current
        previous_stack_frame = stack[-1]

        # Get the module object of the caller
        calling_module = inspect.getmodule(previous_stack_frame[0])
        return str(calling_module.__file__)
    except Exception as e:
        return ""

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            index_suffix = datetime.utcnow().strftime('%Y_%m_%d')
            log_record['timestamp'] = now
            log_record['env'] = os.environ.get('ENV')             
            log_record['index'] = "logs_cliff_"+index_suffix
            caller = {}
            caller['filepath'] = print_caller_info()
            caller['filename'] = log_record['filename']
            caller['function'] = log_record['funcName']
            log_record['caller'] = caller


        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

from kafka import KafkaProducer
import json

class MyKafka(object):
    def __init__(self, kafka_brokers, json=False):
        self.json = json
        if not json:
            self.producer = KafkaProducer(
                bootstrap_servers=kafka_brokers
            )
        else:
            self.producer = KafkaProducer(
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                bootstrap_servers=kafka_brokers
            )
    def send(self, data, topic):
        if self.json:
            result = self.producer.send(topic, key=b'log', value=data)
        else:
            result = self.producer.send(topic, bytes(data, 'utf-8'))
        # print("kafka send result: {}".format(result.get()))

from logging import StreamHandler

class KafkaHandler(StreamHandler):
    def __init__(self, broker, topic):
        StreamHandler.__init__(self)
        self.broker = broker
        self.topic = topic
        # Kafka Broker Configuration
        self.kafka_broker = MyKafka(broker)
    def emit(self, record):
        msg = self.format(record)
        # if type(msg) == type(""):
        #     print("string: "+msg)
        # if type(msg) == type({}):
        #     print("doc: "+json.dumps(msg))
        self.kafka_broker.send(msg, self.topic)

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    # pass
    formatter = CustomJsonFormatter('(timestamp) (filename) (funcName) (level) (name) (message)')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    # logger.addHandler(sh)

    return logger


def create_log_directory():
    """
    create log directory if not exists

    """
    final_path = "data/logs/{}".format(str(ENV))

    if not os.path.exists('data'):
        os.mkdir('data')

    if not os.path.exists('data/logs'):
        os.mkdir('data/logs')

    if not os.path.exists(final_path):
        os.mkdir(final_path)