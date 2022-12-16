import pytest
from iotsink.Handler import Handler



@pytest.fixture()
def config_test_default(monkeypatch):
    monkeypatch.setattr(Handler, "handler_config_path", 'tests/data/test_handler_config.json')
    monkeypatch.setattr(Handler, "plugins_config_path", 'tests/data/test_plugins_config.json')

    Handler()
    yield
    Handler.instance = None


@pytest.fixture()
def config_test_plugin_load_fail(monkeypatch):
    monkeypatch.setattr(Handler, "handler_config_path", 'tests/data/test_handler_config.json')
    monkeypatch.setattr(Handler, "plugins_config_path", 'tests/data/test_plugins_config_load_fail.json')

    Handler()
    yield
    Handler.instance = None




def test_singleton_can_be_instatiated(config_test_default):
    assert Handler.instance != None


def test_singleton_cannot_be_instantiated_twice(config_test_default):

    instance_1 = Handler.instance
    Handler()
    instance_2 = Handler.instance

    assert instance_1 is instance_2


def test_load_plugin_success(config_test_default):

    Handler.instance = None
    Handler()

    assert Handler.load() is True


def test_load_plugin_fail(config_test_plugin_load_fail):

    Handler.instance = None
    Handler()

    assert Handler.load() is False



def test_handle(config_test_default):

    Handler.instance = None
    Handler()

    Handler.load()

    request = {
        'type' : 'test_type',
        'source': 'test_source',
        'data': {"test_data_value": "test_data_value"}
    }

    Handler.handle(request)


def test_handle_plugin_fail(config_test_default):

    Handler.instance = None
    Handler()

    Handler.load()

    request = {
        'type' : 'test_type',
        'source': 'test_source',
        'data': {"test_data_value": "test_data_value_wrong"}
    }

    Handler.handle(request)