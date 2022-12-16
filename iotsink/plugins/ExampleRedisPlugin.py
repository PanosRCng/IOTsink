from datetime import datetime
import json

from iotsink.core.Logger import Logger
from .RedisPlugin import RedisPlugin



class ExampleRedisPlugin(RedisPlugin):

    def __init__(self, config):
        super().__init__(config)


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

        key = '{source}:{timestamp}'.format(source=source, timestamp=event['timestamp'])

        try:
            return self._connections['dev'].set(key, json.dumps(event), ex=self._config['expire_seconds'])
        except Exception as ex:
            Logger.log(__name__, str(ex), type='error')

        return False

