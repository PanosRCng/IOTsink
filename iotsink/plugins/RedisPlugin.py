from .BasePlugin import BasePlugin
from iotsink.core.Redis import Redis


class RedisPlugin(BasePlugin):


    def __init__(self, config):
        self._config = config
        self._connections = {}



    def load(self):
        
        for redis_conn in self._config['connections']:

            conn = Redis.connection(redis_conn)

            if conn is None:
                return False

            self._connections[redis_conn] = conn

            return True


    def handle(self, request):
        pass
