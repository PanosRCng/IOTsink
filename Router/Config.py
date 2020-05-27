import os
import json



class Config:

    __instance = None


    def __init__(self):

        if Config.__instance is not None:
            return

        Config.__instance = self
        self.__setup()


    @staticmethod
    def __get_instance():

        if Config.__instance is None:
            Config()

        return Config.__instance


    @staticmethod
    def get(key):
        return Config.__get_instance().__get(key)


    def __setup(self):
        self.__configs = self.__load()




    def __load(self):

        config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../config.json")

        with open(config_path) as file:
            contents = json.load(file)

            return contents


    def __get(self, key):

        if key in self.__configs:
            return self.__configs[key]

        return None

