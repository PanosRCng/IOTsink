from twisted.web.resource import Resource




class CheckResource(Resource):


    isLeaf = True



    def render_GET(self, request):

        return 'OK'.encode('utf-8')

