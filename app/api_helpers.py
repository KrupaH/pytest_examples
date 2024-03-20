import requests
import logging
import redis


class Settings:
    api_url = "https://randomuser.me/api/"
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379


def make_request():
    """Method to make get JSON details of a single user from an API"""
    try:
        response = requests.get(Settings.api_url, timeout=5)
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        logging.error("Invalid response format; unable to parse json")
        return None
    except requests.exceptions.Timeout as e:
        logging.error(f"{Settings.api_url} timed out: {e}")
        raise RuntimeError(f"Timeout: {e}") from e


def save_to_redis(key, value):
    """Method to save the given key and value to redis"""
    client = redis.StrictRedis(host=Settings.REDIS_HOST,
                               port=Settings.REDIS_PORT)
    client.set(key, value)


def get_from_redis(key):
    """Method to get the given key from redis"""
    client = redis.StrictRedis(host=Settings.REDIS_HOST,
                               port=Settings.REDIS_PORT)
    return client.get(key)