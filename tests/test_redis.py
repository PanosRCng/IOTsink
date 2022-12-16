import pytest
import redis
from iotsink.core.Config import Config
from iotsink.core.Redis import Redis



@pytest.fixture()
def config_test_default(monkeypatch):
    monkeypatch.setattr(Config, "config_path", 'tests/data/test_redis_config.json')
    monkeypatch.setattr(Config, "env_path", None)
    Redis()
    yield
    Config.instance = None
    Redis.instance = None


@pytest.fixture()
def patch_redis_connection_success(monkeypatch):

    class MockRedis:
        def ping(self):
            return 'PONG'

    def mock_connect(*args, **kwargs):
        return MockRedis()

    monkeypatch.setattr(redis, 'Redis', mock_connect)


@pytest.fixture()
def patch_redis_connection_fail(monkeypatch):

    def mock_connect(*args, **kwargs):
        return None

    monkeypatch.setattr(redis, 'Redis', mock_connect)



def test_singleton_can_be_instatiated(config_test_default):
    assert Redis.instance != None


def test_singleton_cannot_be_instantiated_twice(config_test_default):

    instance_1 = Redis.instance
    Redis()
    instance_2 = Redis.instance

    assert instance_1 is instance_2


def test_get_connection_success(config_test_default, patch_redis_connection_success):
    Redis.instance = None
    Redis()
    assert Redis.connection('test_connection') is not None


def test_get_connection_fail(patch_redis_connection_fail):
    Redis.instance = None
    Redis()
    assert Redis.connection('test_connection') is None


def test_get_nonexistent_connection(config_test_default):
    assert Redis.connection('nonexistent_connection') is None


def test_get_already_opened_connection(config_test_default, patch_redis_connection_success):
    connection_1 = Redis.connection('test_connection')
    Redis()
    connection_2 = Redis.connection('test_connection')

    assert connection_1 is connection_2
