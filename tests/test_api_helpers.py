import pytest
import requests
import logging
from testcontainers.redis import RedisContainer

from app.api_helpers import make_request, save_to_redis, get_from_redis, Settings


class TestMakeRequest:
    """Tests related to make_request() method in api_helpers"""

    @staticmethod
    def test_make_request():
        # test basic success case
        resp = make_request()
        assert resp["results"]

    @staticmethod
    def test_invalid_json(monkeypatch, caplog):
        """Test case for if api gives non-json response"""
        # patch to api which does not give json response
        monkeypatch.setattr(Settings, "api_url", "https://randomuser.me/")
        resp = make_request()
        assert resp is None

        errs = [i.message for i in caplog.records if i.levelno == logging.ERROR]
        assert "Invalid response format; unable to parse json" in errs
        caplog.clear()

    @staticmethod
    def test_api_timeout(monkeypatch, caplog):
        """Test case for if api times out"""

        # mock function to simulate timeout from requests.get
        def mock_get_timeout(*args, **kwargs):
            raise requests.exceptions.Timeout("simulated timeout")

        monkeypatch.setattr(requests, "get", mock_get_timeout)

        # this will use the above mock_get_timeout instead of requests.get
        with pytest.raises(RuntimeError) as e:
            resp = make_request()
            assert resp is None
        e.match("Timeout: simulated timeout")

        # verify that appropriate logs are present
        errs = [i.message for i in caplog.records if i.levelno == logging.ERROR]
        assert f"{Settings.api_url} timed out: simulated timeout" in errs

        caplog.clear()


class TestRedisOperations:
    """Tests related to redis operations done in api_helpers"""

    @staticmethod
    def test_save_to_redis(monkeypatch):
        """Method to test saving to redis with a testcontainer"""
        with RedisContainer() as redis_container:
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(redis_container.port)

            # patch host and port configs to the testcontainer host and port
            monkeypatch.setattr(Settings, "REDIS_HOST", host)
            monkeypatch.setattr(Settings, "REDIS_PORT", port)

            # test save_to_redis method
            save_to_redis("test_key", "test_value")

            # verify that data is saved in this redis instance
            client = redis_container.get_client()
            assert client.get("test_key") == b"test_value"

    @staticmethod
    def test_get_from_redis(monkeypatch):
        """Method to test saving to redis with a testcontainer"""
        with RedisContainer() as redis_container:
            # patch host and port configs to the testcontainer host and port
            host = redis_container.get_container_host_ip()
            port = redis_container.get_exposed_port(redis_container.port)

            # patch host and port configs to the testcontainer host and port
            monkeypatch.setattr(Settings, "REDIS_HOST", host)
            monkeypatch.setattr(Settings, "REDIS_PORT", port)

            client = redis_container.get_client()
            client.set("test_key", "test_value")

            # test save_to_redis method
            assert get_from_redis("test_key") == b"test_value"

            assert get_from_redis("key_does_not_exist") is None
