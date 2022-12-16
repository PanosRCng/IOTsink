from datetime import datetime
import json

from iotsink.core.Logger import Logger
from .ElasticsearchPlugin import ElasticsearchPlugin



class ExampleElasticsearchPlugin(ElasticsearchPlugin):

    def __init__(self, config):
        super().__init__(config)


    def load(self):
        
        if super(ExampleElasticsearchPlugin, self).load() is False:
            return False

        self.__create_index()

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
            self._connections['dev'].index(index='events', body={"event": event})
        except Exception as ex:
            Logger.log(__name__, str(ex), type='error')
            return False

        return True


    def __create_index(self):

        index_settings = {
            "settings":
            {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": 
            {
            "properties": 
            {
                "event": 
                {
                    "type": "object",
                    "enabled": False
                }
            }
            }
        }

        try:
            self._connections['dev'].indices.create(index='events', body=index_settings)
        except Exception as ex:
            Logger.log(__name__, str(ex), type='warning')
