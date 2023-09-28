from django.test import TestCase
from django.urls import path
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from channels.routing import URLRouter

from .consumers import ChatConsumer


class ChatConsumerTest(TestCase):
    
    async def connect(self):
        _path = "/testws/testroom/"
        application = URLRouter([
            path("testws/<str:room_id>/", ChatConsumer.as_asgi()),
        ])
        communicator = WebsocketCommunicator(application, _path)
        connected, _ = await communicator.connect()
        assert connected
        return communicator
    
    async def disconnect(self, communicator):
        await communicator.disconnect()

    @database_sync_to_async
    def create_user(self, username, password):
        return get_user_model().objects.create_user(
            username=username, password=password
        )

    async def test_receive_valid_message(self):
        user = await self.create_user("awesome_user", "testpwd")

        payload = {
            "message": "super cool test!!",
            "username": user.username
        }

        communicator = await self.connect()

        await communicator.send_json_to({
            "type": "websocket.connect",
            **payload
        })

        response = await communicator.receive_json_from()

        await self.disconnect(communicator)

        self.assertEqual(response, { "type": "message", **payload })

    async def test_receive_invalid_message(self):
        pass


       