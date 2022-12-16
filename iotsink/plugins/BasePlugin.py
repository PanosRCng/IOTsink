from abc import ABC, abstractmethod



class BasePlugin(ABC):

    def __str__(self):
        return str(self.__class__.__name__)


    @abstractmethod
    def load(self):
        pass


    @abstractmethod
    def handle(self, request):
        pass
