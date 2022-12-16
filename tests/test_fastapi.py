import pytest
from fastapi.testclient import TestClient

from iotsink.core.Config import Config
from iotsink.iotsink import app

client = TestClient(app)



@pytest.fixture()
def config_default(monkeypatch):
    monkeypatch.setattr(Config, "env_path", None)
    Config()
    yield
    Config.instance = None



def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "iotsink service"}


def test_nonexistent_route():
    response = client.get("/nonexistent_route")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}




