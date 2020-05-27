from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints

from Router.TwistedWebServer.Resources.RouteResource import RouteResource
from Router.TwistedWebServer.Resources.CheckResource import CheckResource




class Server:


    def __init__(self, port=8080):
        self.__port = port



    def run(self):

        root = Resource()
        root.putChild('check'.encode('utf-8'), CheckResource())
        root.putChild('route'.encode('utf-8'), RouteResource())

        factory = Site(root)
        endpoint = endpoints.TCP4ServerEndpoint(reactor, self.__port)
        endpoint.listen(factory)
        reactor.run()


