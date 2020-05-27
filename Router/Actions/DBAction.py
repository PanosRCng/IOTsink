from twisted.enterprise import adbapi
import pymysql

from Router.Actions.Action import Action
from Router.Config import Config





class DBAction(Action):


    def __init__(self, config):

        self._dbpools = {}

        for database_name in config['databases']:

            db_config = Config.get('databases')[database_name]

            self._dbpools[database_name] = adbapi.ConnectionPool("pymysql",
                                                                  host=db_config['host'],
                                                                  user=db_config['user'],
                                                                  password=db_config['password'],
                                                                  db=db_config['db'],
                                                                  charset=db_config['charset'],
                                                                  autocommit=True,
                                                                  cursorclass=pymysql.cursors.DictCursor)



    def execute(self, request):
        pass






