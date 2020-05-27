import os
import json
import importlib


class Routes:


    @staticmethod
    def load():

        routes = {}

        config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "routes.json")

        with open(config_path) as file:

            for route_entry in json.load(file):

                ActionModule = importlib.import_module('Router.Actions.' + route_entry['action']['module'])
                ActionClass = getattr(ActionModule, route_entry['action']['module'])

                routes[route_entry['source']] = ActionClass(route_entry['action']['config'])

        return routes



