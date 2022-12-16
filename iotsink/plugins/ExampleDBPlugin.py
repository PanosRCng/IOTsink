from datetime import datetime

from iotsink.core.Logger import Logger
from .DBPlugin import DBPlugin



class ExampleDBPlugin(DBPlugin):

    def __init__(self, config):
        super().__init__(config)


    def handle(self, request):

        source = request['source']
        data = request['data']
        timestamp = request['timestamp']

        inserted_id = self.__sink_info(source, data, timestamp)

        if inserted_id is None:
            return False
        
        return True



    def __sink_info(self, source, data, timestamp):

        inserted_id = None

        try:

            info = [
                source,
                data['Temperature'],
                data['Humidity'],
                data['Light'],
                datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            ]

            with self._connections['dev_db'].cursor() as cursor:

                sql = "INSERT INTO measurements (client, temperature, humidity, light, created_at) VALUES (%s, %s, %s, %s, %s)"

                cursor.execute(sql, info)
                inserted_id = cursor.lastrowid

        except Exception as ex:
            Logger.log(__name__, str(ex), type='error')

        return inserted_id

