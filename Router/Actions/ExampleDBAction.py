from datetime import datetime

from Router.Actions.DBAction import DBAction





class ExampleDBAction(DBAction):


    def __init__(self, config):
        super().__init__(config)



    def execute(self, request):
        return self._dbpools['example_db'].runInteraction(self.__insert_measurement, request)




    def __insert_measurement(self, adapi_transaction, request):

        data = [
            request['client'],
            request['msg']['Temperature'],
            request['msg']['Humidity'],
            datetime.utcfromtimestamp(request['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        ]

        adapi_transaction.execute("INSERT INTO measurements (client, temperature, humidity, created_at) VALUES (%s, %s, %s, %s)", data)

        adapi_transaction.execute("SELECT LAST_INSERT_ID() as inserted_id")
        result = adapi_transaction.fetchone()

        return result['inserted_id']






