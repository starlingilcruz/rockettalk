import redis
import os
import json
import logging

from .utils import uuid

logger = logging.getLogger(__name__)


class StoreConnector:

    @classmethod
    def use_store(cls, store_cls):
        """Set the class to be used for storing messages."""

        assert hasattr(
            store_cls, 'store_object'), "Store class has missing store_object()"
        assert hasattr(
            store_cls, 'retrieve_objects'), "Store class has missing retrieve_objects()"

        return type(cls.__name__, (cls, ), {"store": store_cls()})


class RedisStore:

    def __init__(self) -> None:
        self.redis = redis.StrictRedis(
            host=os.environ.get("REDIS_HOST"),
            port=os.environ.get("REDIS_PORT"),
            db=0
        )

    def store_object(self, hashname, obj):
        try:
            logger.info('Storing %s in cache', str((hashname, obj)))
            return self.redis.hset(hashname, uuid(128), json.dumps(obj))
        except Exception as ex:
            logger.Error(f"Unable to store object in cache: {ex}")

    def retrieve_objects(self, hashname) -> list:
        try:
            logger.info('Fetching objects from %s hash', str((hashname)))
            return [
                json.loads(v) for v in self.redis.hgetall(hashname).values()
            ]
        except Exception as ex:
            logger.Error(f"Unable to retrieve objects from cache: {ex}")
        return []
