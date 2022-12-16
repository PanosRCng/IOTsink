from time import sleep

from .BasePlugin import BasePlugin


# load test plugin for load test purposes


class LoadTestPlugin(BasePlugin):


    def __init__(self, config):
        self._config = config



    def load(self):
        return True


    def handle(self, request):

        source = request['source']
        data = request['data']
        timestamp = request['timestamp']

        return self.__load_test(cpu=data['cpu'], io=data['io'])



    def __load_test(self, cpu, io):

        LoadTestPlugin.__factorial(cpu)
        sleep(io)

        return True


    def __factorial(n):
        if n == 0:
            return 1
        else:
            return n * LoadTestPlugin.__factorial(n-1)

