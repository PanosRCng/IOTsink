import json
from datetime import datetime

from iotsink.core.Logger import Logger
from .BasePlugin import BasePlugin
from iotsink.core.Kafka import Kafka

class ExampleKafkaPlugin(BasePlugin):


    def __init__(self, config):
        self._config = config
        self._producer = None


    def load(self):

        producer = Kafka.producer()

        if producer is None:
            return False

        return True


    def handle(self, request):

        source = request['source']
        data = request['data']
        timestamp = request['timestamp']

        return self.__sink_event(source, data, timestamp)



    def __sink_event(self, source, data, timestamp):

        event = {
            'source' : source,
            'event': list(data.keys())[0],
            'timestamp': datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            future = Kafka.producer().send(self._config['topic'], event)
            future.add_callback(self.__kafka_success, event)
            future.add_errback(self.__kafka_failure, event)
        except Exception as ex:
            Logger.log(__name__, str(ex), type='error')
            return False

        return True


    def __kafka_success(self, value, response):
        pass


    def __kafka_failure(self, value, exception):
        Logger.log(__name__, 'failed to to send {value}, {exception}'.format(value=value, exception=exception))