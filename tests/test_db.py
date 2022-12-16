import pytest
import pymysql
from iotsink.core.Config import Config
from iotsink.core.DB import DB



@pytest.fixture()
def config_test_default(monkeypatch):
    monkeypatch.setattr(Config, "config_path", 'tests/data/test_db_config.json')
    monkeypatch.setattr(Config, "env_path", None)
    DB()
    yield
    Config.instance = None
    DB.instance = None


@pytest.fixture()
def patch_pymysql_connection_success(monkeypatch):

    def mock_connect(*args, **kwargs):
        return {}

    monkeypatch.setattr(pymysql, 'connect', mock_connect)


@pytest.fixture()
def patch_pymysql_connection_fail(monkeypatch):

    def mock_connect(*args, **kwargs):
        return None

    monkeypatch.setattr(pymysql, 'connect', mock_connect)



def test_singleton_can_be_instatiated(config_test_default):
    assert DB.instance != None


def test_singleton_cannot_be_instantiated_twice(config_test_default):

    instance_1 = DB.instance
    DB()
    instance_2 = DB.instance

    assert instance_1 is instance_2


def test_get_connection_success(config_test_default, patch_pymysql_connection_success):
    DB.instance = None
    DB()
    assert DB.connection('test_connection') is not None


def test_get_connection_fail(patch_pymysql_connection_fail):
    DB.instance = None
    DB()
    assert DB.connection('test_connection') is None


def test_get_nonexistent_connection(config_test_default):
    assert DB.connection('nonexistent_connection') is None


def test_get_already_opened_connection(config_test_default, patch_pymysql_connection_success):
    connection_1 = DB.connection('test_connection')
    DB()
    connection_2 = DB.connection('test_connection')

    assert connection_1 is connection_2
