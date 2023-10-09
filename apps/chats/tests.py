from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from django.urls import path
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from channels.routing import URLRouter

from .consumers import ChatConsumer
from .store import RedisStore
from .utils import uuid


class ChatConsumerTest(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.communicator = await self.connect()
        self.user = await self.create_user(str(uuid(128)), "testpwd")

    async def asyncTearDown(self):
        await self.communicator.disconnect()

    async def connect(self, store=None):
        if store:
            consumer = ChatConsumer.use_store(store)
        else:
            consumer = ChatConsumer

        _path = "/testws/testroom/"
        application = URLRouter([
            path("testws/<str:room_id>/", consumer.as_asgi()),
        ])
        communicator = WebsocketCommunicator(application, _path)
        connected, _ = await communicator.connect()
        assert connected
        return communicator

    @database_sync_to_async
    def create_user(self, username, password):
        return get_user_model().objects.create_user(
            username=username, password=password
        )

    async def __send_websocket_message(self, payload={}):

        await self.communicator.send_json_to({
            "type": "websocket.connect",
            "message": "super cool test!",
            "username": self.user.username,
            **payload
        })

        return await self.communicator.receive_json_from()

    async def test_receive_valid_message(self):
        payload = {
            "message": "testing 1",
            "username": self.user.username
        }

        response = await self.__send_websocket_message(payload)

        self.assertEqual(response, {"type": "message", **payload})

    @patch("apps.chats.consumers.ChatConsumer.clean_and_validate_input")
    async def test_should_validate_input_stream(self, mock_validator):

        payload = {
            "message": "testing 2",
            "username": self.user.username
        }

        await self.__send_websocket_message(payload)

        mock_validator.assert_called_once()
        # validates right before broadcasting
        mock_validator.assert_called_with({
            "type": "send_message",
            **payload
        })

    @patch("apps.chats.consumers.ChatConsumer.save_message")
    async def test_should_not_store_message_in_cache(self, mock_save_message):
        """ Since the cache api is not provided, should not intent to cache message """
        await self.__send_websocket_message()
        mock_save_message.assert_not_called()

    @patch("apps.chats.consumers.ChatConsumer.save_message")
    @patch("apps.chats.store.RedisStore.store_object")
    async def test_should_store_message_in_cache(self, mock_redis_store, mock_save_message):
        await self.communicator.disconnect()

        self.communicator = await self.connect(store=RedisStore)

        payload = {
            "message": "test 4",
            "username": self.user.username
        }

        await self.communicator.send_json_to({
            "type": "websocket.connect",
            **payload
        })

        await self.communicator.receive_json_from()
        mock_save_message.assert_called_once_with(
            "chat_testroom", {"type": "message", **payload}
        )