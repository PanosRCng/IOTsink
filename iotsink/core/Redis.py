import redis

from .Config import Config
from .Logger import Logger


class Redis:

    # these are public for test purposes
    instance = None


    # constructor is not intended to be called from outside the module, only fo test purposes
    def __init__(self):

        if Redis.instance is not None:
            return

        Redis.instance = self
        self.__setup()


    @staticmethod
    def __get_instance():

        if Redis.instance is None:
            Redis()

        return Redis.instance


    @staticmethod
    def connection(connection_name):
        return Redis.__get_instance().__connection(connection_name)


    def __setup(self):
        self.__conns = {}
        self.__configs = Config.get('redis')


    def __connection(self, connection_name):

        if connection_name not in self.__configs:
            return None

        return self.__get_conn(connection_name)


    def __get_conn(self, connection_name):

        if self.__conn_exists(connection_name):
            return self.__conns[connection_name]

        connection = self.__open_conn(self.__configs[connection_name])

        if connection is None:
            return None

        try:
            connection.ping()
        except Exception as ex:
            Logger.log(__name__, str(ex), type='error')
            return None

        self.__conns[connection_name] = connection

        return self.__conns[connection_name]


    def __conn_exists(self, connection_name):

        if connection_name not in self.__conns:
            return False

        if self.__conns[connection_name] is None:
            return False

        return True


    def __open_conn(self, config):

        connection = None

        try:
            connection = redis.Redis(host=config['host'], port=config['port'], db=config['db'], socket_connect_timeout=config['timeout'])
        except Exception as ex:
            Logger.log(__name__, str(ex), type='error')

        return connection