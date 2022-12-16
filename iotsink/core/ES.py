import os

import elasticsearch

from .Logger import Logger
from .Config import Config



class ES:

    # these are public for test purposes
    instance = None


    # constructor is not intended to be called from outside the module, only fo test purposes
    def __init__(self):

        if ES.instance is not None:
            return

        ES.instance = self
        self.__setup()



    @staticmethod
    def __get_instance():

        if ES.instance is None:
            ES()

        return ES.instance


    @staticmethod
    def connection(connection_name):
        return ES.__get_instance().__connection(connection_name)



    def __setup(self):
        self.__conns = {}
        self.__configs = Config.get('elasticsearch')


    def __connection(self, connection_name):

        if connection_name not in self.__configs:
            return None

        return self.__get_conn(connection_name)


    def __get_conn(self, connection_name):

        pid_conn_name = self.__pid_connection_name(connection_name)

        if self.__conn_exists(pid_conn_name):
            return self.__conns[pid_conn_name]

        connection = self.__open_conn(self.__configs[connection_name])

        if connection is None:
            return None

        self.__conns[pid_conn_name] = connection

        return self.__conns[pid_conn_name]


    def __conn_exists(self, connection_name):

        if connection_name not in self.__conns:
            return False

        if self.__conns[connection_name] is None:
            return False

        return True


    def __open_conn(self, config):

        connection = None

        try:
            url = '{scheme}://{host}:{port}'.format(scheme=config['scheme'], host=config['host'], port=config['port'])
            connection = elasticsearch.Elasticsearch(url)
        except Exception as ex:
            Logger.log(__name__, str(ex), type='error')

        if connection.ping(request_timeout=config['timeout']) is False:
            Logger.log(__name__, 'cloud not ping elasticsearch at {url}'.format(url=url), type='error')
            return None

        return connection


    def __pid_connection_name(self, connection_name):
        return connection_name + '_' + str(os.getpid())

