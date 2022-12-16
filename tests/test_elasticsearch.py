import pytest
import elasticsearch
from iotsink.core.Config import Config
from iotsink.core.ES import ES



@pytest.fixture()
def config_test_default(monkeypatch):
    monkeypatch.setattr(Config, "config_path", 'tests/data/test_elasticsearch_config.json')
    monkeypatch.setattr(Config, "env_path", None)
    ES()
    yield
    Config.instance = None
    ES.instance = None


@pytest.fixture()
def patch_elasticsearch_connection_success(monkeypatch):

    class MockElasticsearch:
        def ping(self, request_timeout=1):
            return True

    def mock_connect(*args, **kwargs):
        return MockElasticsearch()

    monkeypatch.setattr(elasticsearch, 'Elasticsearch', mock_connect)


@pytest.fixture()
def patch_elasticsearch_connection_fail(monkeypatch):

    def mock_connect(*args, **kwargs):
        return None

    monkeypatch.setattr(elasticsearch, 'Elasticsearch', mock_connect)



def test_singleton_can_be_instatiated(config_test_default):
    assert ES.instance != None


def test_singleton_cannot_be_instantiated_twice(config_test_default):

    instance_1 = ES.instance
    ES()
    instance_2 = ES.instance

    assert instance_1 is instance_2


def test_get_connection_success(config_test_default, patch_elasticsearch_connection_success):
    ES.instance = None
    ES()

    assert ES.connection('test_connection') is not None


def test_get_connection_fail(patch_elasticsearch_connection_fail):
    ES.instance = None
    ES()
    assert ES.connection('test_connection') is None


def test_get_nonexistent_connection(config_test_default):
    assert ES.connection('nonexistent_connection') is None


def test_get_already_opened_connection(config_test_default, patch_elasticsearch_connection_success):
    connection_1 = ES.connection('test_connection')
    ES()
    connection_2 = ES.connection('test_connection')

    assert connection_1 is connection_2
