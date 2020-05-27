import json
from datetime import datetime, timezone

from twisted.logger import Logger
from twisted.web.resource import Resource

from Router.Routes import Routes





class RouteResource(Resource):


    def __init__(self):
        self.__routes = Routes.load()
        self.__logger = Logger()

    isLeaf = True



    def render_POST(self, request):

        content = request.content.read().decode('utf-8')

        request = json.loads(content)
        request['timestamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()

        deferred = self.__routes[request['client']].execute(request)

        deferred.addCallback(self.action_result)
        deferred.addErrback(self.action_error)

        return ''.encode('utf-8')





    def action_result(self, result):
        pass


    def action_error(self, failure):
        self.__logger.error('action failed')