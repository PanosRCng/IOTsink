import pymysql

from .Config import Config
from .Logger import Logger


class DB:

    # these are public for test purposes
    instance = None


    # constructor is not intended to be called from outside the module, only fo test purposes
    def __init__(self):

        if DB.instance is not None:
            return

        DB.instance = self
        self.__setup()


    @staticmethod
    def __get_instance():

        if DB.instance is None:
            DB()

        return DB.instance


    @staticmethod
    def connection(connection_name):
        return DB.__get_instance().__connection(connection_name)


    def __setup(self):
        self.__conns = {}
        self.__configs = Config.get('databases')


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
            connection = pymysql.connect(host=config['host'],
                                         port=config['port'],
                                         user=config['user'],
                                         password=config['password'],
                                         db=config['db'],
                                         charset=config['charset'],
                                         autocommit=True,
                                         cursorclass=pymysql.cursors.DictCursor)
        except Exception as ex:
            Logger.log(__name__, str(ex), 'error')

        return connection