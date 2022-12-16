import pytest
import kafka
from iotsink.core.Config import Config
from iotsink.core.Kafka import Kafka



@pytest.fixture()
def config_test_default(monkeypatch):
    monkeypatch.setattr(Config, "config_path", 'tests/data/test_kafka_config.json')
    monkeypatch.setattr(Config, "env_path", None)
    Kafka()
    yield
    Config.instance = None
    Kafka.instance = None


@pytest.fixture()
def patch_kafka_producer_success(monkeypatch):

    def mock_producer(*args, **kwargs):
        return {}

    monkeypatch.setattr(kafka, 'KafkaProducer', mock_producer)


@pytest.fixture()
def patch_kafka_producer_fail(monkeypatch):

    def mock_producer(*args, **kwargs):
        return None

    monkeypatch.setattr(kafka, 'KafkaProducer', mock_producer)


@pytest.fixture()
def patch_kafka_consumer_success(monkeypatch):

    def mock_consumer(*args, **kwargs):
        return {}

    monkeypatch.setattr(kafka, 'KafkaConsumer', mock_consumer)


@pytest.fixture()
def patch_kafka_consumer_fail(monkeypatch):

    def mock_consumer(*args, **kwargs):
        return None

    monkeypatch.setattr(kafka, 'KafkaConsumer', mock_consumer)


def test_singleton_can_be_instatiated(config_test_default):
    assert Kafka.instance != None


def test_singleton_cannot_be_instantiated_twice(config_test_default):

    instance_1 = Kafka.instance
    Kafka()
    instance_2 = Kafka.instance

    assert instance_1 is instance_2


def test_get_producer_success(config_test_default, patch_kafka_producer_success):
    Config.instance = None
    Kafka.instance = None
    Kafka()
    assert Kafka.producer() is not None


def test_get_producer_fail(config_test_default, patch_kafka_producer_fail):
    Config.instance = None
    Kafka.instance = None
    Kafka()
    assert Kafka.producer() is None


def test_get_consumer_success(config_test_default, patch_kafka_consumer_success):
    Config.instance = None
    Kafka.instance = None
    Kafka()
    assert Kafka.consumer() is not None


def test_get_consumer_fail(config_test_default, patch_kafka_consumer_fail):
    Config.instance = None
    Kafka.instance = None
    Kafka()
    assert Kafka.consumer() is None


