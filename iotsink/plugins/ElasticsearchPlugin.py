from .BasePlugin import BasePlugin
from iotsink.core.ES import ES


class ElasticsearchPlugin(BasePlugin):


    def __init__(self, config):
        self._config = config
        self._connections = {}



    def load(self):
        
        for es_conn in self._config['connections']:

            conn = ES.connection(es_conn)

            if conn is None:
                return False

            self._connections[es_conn] = conn

            return True


    def handle(self, request):
        pass
