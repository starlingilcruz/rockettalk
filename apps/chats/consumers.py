from channels.generic.websocket import AsyncJsonWebsocketConsumer
import logging

from .forms import ChatMessageForm
from .store import StoreConnector
from .utils import channel_fmt

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncJsonWebsocketConsumer, StoreConnector):

    async def connect(self):
        try:
            self.group_id = self.scope['url_route']['kwargs']['room_id']

            if not self.group_id:
                # default room which every member is commom
                self.group_id = channel_fmt('global-room')

            self.group_name = channel_fmt(self.group_id)

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
            logger.info("WebSocket connection established")

        except Exception as e:
            logger.error(f"Error during websocket connection: {e}")

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            logger.info("WebSocket connection closed")

        except Exception as e:
            logger.error(f"Error during websocket disconnection: {e}")

    async def receive_json(self, content=None):
        try:
            # Broadcast message to a room group
            await self.channel_layer.group_send(
                self.group_name, {
                    "type": "send_message",
                    "message": content["message"],
                    "username": content["username"],
                })
            logger.debug(f"Received message: {content}")

        except KeyError as e:
            logger.error(f"KeyError in received data: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in received method: {e}")

    async def send_message(self, event, reason="message"):
        try:
            form = ChatMessageForm(event)
            form.is_valid()  # TODO handle invalid form

            content = {
                "type": reason,
                "message": form.cleaned_data['message'],
                "username": form.cleaned_data['username']
            }
            await self.send_json(content=content)

            logger.debug(f"Message sent: {event}")

            if self.store:
                await self.save_message(self.group_name, content)

        except Exception as e:
            logger.error(f"Error sending message: {e}")

    async def save_message(self, channel_name, content):
        if not self.store:
            raise Exception("Error: no store provided")
        
        return self.store.store_object(
            hashname=channel_name, obj=content
        )