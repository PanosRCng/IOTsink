import json
import importlib

from .core.Logger import Logger



class Handler:

    # these are public for test purposes
    instance = None
    handler_config_path = 'iotsink/handler.json'
    plugins_config_path = 'iotsink/plugins.json'


    # constructor is not intended to be called from outside the module, only fo test purposes
    def __init__(self):

        if Handler.instance is not None:
            return

        Handler.instance = self
        self.__handle_map = {}


    @staticmethod
    def __get_instance():

        if Handler.instance is None:
            Handler()

        return Handler.instance


    @staticmethod
    def load():
        try:
            Handler.__get_instance().__load()
            Logger.log(__name__, 'Handler loaded successfully')
            return True
        except Exception as ex:
            Logger.log(__name__, str(ex), 'error')
            Logger.log(__name__, 'cloud not load Handler', 'error')
            return False


    @staticmethod
    def handle(request):
        return Handler.__get_instance().__handle(request)



    def __load(self):

        with open(Handler.handler_config_path) as file:
            self.__handler_config = json.load(file)

        with open(Handler.plugins_config_path) as file:
            self.__plugins_config = json.load(file)

        loaded_plugins = self.__load_plugins()

        self.__set_plugin_handlers(loaded_plugins)
    

    def __load_plugins(self):

        mentioned_plugins = []

        for msg_type in self.__handler_config:
            mentioned_plugins += self.__handler_config[msg_type]
        
        mentioned_plugins = list(set(mentioned_plugins))

        Logger.log(__name__, "active plugins: <{active_plugins}>".format(active_plugins=', '.join(mentioned_plugins)))

        loaded_plugins = {}

        for plugin_name in mentioned_plugins:

            if plugin_name not in self.__plugins_config:
                Logger.log(__name__, "plugin <{plugin}> mentioned to handler.json, but is not specified to plugins.json".format(plugin=plugin_name), type='error')
                continue

            try:
                loaded_plugins[plugin_name] = self.__load_plugin(plugin_name, self.__plugins_config[plugin_name]['config'])
                Logger.log(__name__, 'successfully loaded plugin <{plugin_name}>'.format(plugin_name=plugin_name))
            except Exception as ex:
                raise ValueError(str(ex))

        return loaded_plugins


    def __load_plugin(self, plugin, config):

        PluginModule = importlib.import_module('iotsink.plugins.' + plugin)
        PluginClass = getattr(PluginModule, plugin)

        pluginInstance = PluginClass(config)

        if not pluginInstance.load():
            raise ValueError('cloud not load plugin <{plugin_name}>'.format(plugin_name=plugin)) 

        return pluginInstance


    def __set_plugin_handlers(self, loaded_plugins):

        for msg_type, plugins in self.__handler_config.items():
            
            self.__handle_map[msg_type] = []

            for plugin_name in plugins:

                if plugin_name in loaded_plugins:
                    self.__handle_map[msg_type].append(loaded_plugins[plugin_name])

        Logger.log(__name__, 'message types: <{msg_types}>'.format(msg_types=', '.join(list(self.__handle_map.keys()))))

        for msg_type, plugins in self.__handle_map.items():
            if len(plugins) > 0:
                Logger.log(__name__, 'message type <{msg_type}> has: <{plugins}> plugin handlers'.format(msg_type=msg_type, plugins=', '.join(([str(plugin) for plugin in plugins]))))



    def __handle(self, request):
        
        if request['type'] not in self.__handle_map:
            Logger.log(__name__, 'type <{type}> does not have a plugin map'.format(type=request['type']), type='error')
            return False
        
        for plugin in self.__handle_map[request['type']]:

            if plugin.handle(request) is False:
                Logger.log(__name__, 'plugin {plugin} failed to handle request {request}'.format(plugin=str(plugin), request=request) ,type='error')



