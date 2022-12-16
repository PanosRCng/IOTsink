from .BasePlugin import BasePlugin
from iotsink.core.DB import DB


class DBPlugin(BasePlugin):


    def __init__(self, config):
        self._config = config
        self._connections = {}



    def load(self):
        
        for database_name in self._config['databases']:

            conn = DB.connection(database_name)

            if conn is None:
                return False

            self._connections[database_name] = conn

            return True


    def handle(self, request):
        pass
