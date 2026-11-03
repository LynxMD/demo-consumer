"""Tests for the demo consumer server. The tests mock all outbound HTTP calls."""

from unittest import mock

import pytest

import server


@pytest.fixture
def client():
    server.app.config.update(TESTING=True)
    return server.app.test_client()


def test_index_returns_hello_world(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "<p>Hello, World!</p>"


def test_health_calls_the_server_from_config_json(client, tmp_path, monkeypatch):
    (tmp_path / "config.json").write_text('{"server": "http://10.0.0.5:5000/data"}')
    monkeypatch.chdir(tmp_path)

    with mock.patch.object(server.requests, "get") as get:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "OK"
    get.assert_called_once_with("http://10.0.0.5:5000/data")


def test_health_fails_when_the_server_is_unreachable(client, tmp_path, monkeypatch):
    (tmp_path / "config.json").write_text('{"server": "http://10.0.0.5:5000/data"}')
    monkeypatch.chdir(tmp_path)
    server.app.config.update(TESTING=False, PROPAGATE_EXCEPTIONS=False)

    error = server.requests.ConnectionError("down")
    with mock.patch.object(server.requests, "get", side_effect=error):
        response = client.get("/health")

    assert response.status_code == 500
