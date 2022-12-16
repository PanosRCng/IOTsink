import kafka
import ujson

from .Logger import Logger
from .Config import Config


class Kafka:

    # these are public for test purposes
    instance = None


    # constructor is not intended to be called from outside the module, only fo test purposes
    def __init__(self):

        if Kafka.instance is not None:
            return

        Kafka.instance = self
        self.__setup()


    @staticmethod
    def __get_instance():

        if Kafka.instance is None:
            Kafka()

        return Kafka.instance


    @staticmethod
    def producer():
        return Kafka.__get_instance().__open_producer()


    @staticmethod
    def consumer():
        return Kafka.__get_instance().__open_consumer()


    def __setup(self):
        self.__config = Config.get('kafka')
        self.__config['bootstrap_servers'] = eval(self.__config['bootstrap_servers'])



    def __open_producer(self):

        producer = None

        try:
            
            producer = kafka.KafkaProducer(bootstrap_servers=self.__config['bootstrap_servers'],
                                     retries=self.__config['producer_retries'],
                                     acks=self.__config['producer_acks'],
                                     linger_ms=self.__config['producer_batch_linger_ms'],
                                     buffer_memory=self.__config['producer_buffer_bytes'],
                                     max_request_size=self.__config['producer_max_request_size'],
                                     value_serializer=lambda m: ujson.dumps(m).encode('utf-8'))
                                     
        except Exception as ex:
            Logger.log(__name__, str(ex), type='error')

        return producer


    def __open_consumer(self):

        producer = None

        try:

            producer = kafka.KafkaConsumer(self.__config['topic'],
                                     group_id=self.__config['group_id'],
                                     bootstrap_servers=self.__config['bootstrap_servers'],
                                     value_deserializer=lambda m: m.decode('utf-8'),
                                     consumer_timeout_ms=self.__config['consumer_timeout'],
                                     auto_offset_reset=self.__config['consumer_auto_offset_reset'],
                                     auto_commit_interval_ms=self.__config['consumer_auto_commit_interval_ms'],
                                     enable_auto_commit=self.__config['consumer_enable_auto_commit'],
                                     max_partition_fetch_bytes=self.__config['consumer_max_partition_fetch_bytes'])
                                           
        except Exception as ex:
            Logger.log(__name__, str(ex), type='error')

        return producer