from .BasePlugin import BasePlugin


# test plugin for test purposes


class TestPlugin(BasePlugin):


    def __init__(self, config):
        self._config = config
        self._test_value = 'test_value'



    def load(self):
        
        if self._test_value == self._config['test_value']:
            return True

        return False


    def handle(self, request):

        if request['data']['test_data_value'] == 'test_data_value':
            return True

        return False
