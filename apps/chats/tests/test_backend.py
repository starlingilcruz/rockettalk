from unittest import TestCase
from unittest.mock import patch

from ..store import RedisStore


class TestDjangoRedisCache(TestCase):

    def setUp(self) -> None:
        self.redis_store = RedisStore()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.redis_store.delete_objects("hash1")
        return super().tearDown()

    def test_store_messages_belong_channel(self):
        hash_key = "hash1"
        data = {
            "attribute1": "testing 1",
            "attribute2": "testing 2"
        }
        self.redis_store.store_object(hash_key, data)
        restored_data = self.redis_store.retrieve_objects(hash_key)
        self.assertEqual(restored_data, [data])
