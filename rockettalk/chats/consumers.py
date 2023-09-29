from channels.generic.websocket import AsyncJsonWebsocketConsumer
import logging

from .forms import ChatMessageForm

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        try:
            self.group_id = self.scope['url_route']['kwargs']['room_id']

            if not self.group_id:
                # default room which every member is commom
                self.group_id = 'global-room'

            self.group_name = f'chat_{self.group_id}'

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

            logger.debug(f"Send message: {event}")
            await self.send_json(
                content={
                    "type": reason,
                    "message": form.cleaned_data['message'],
                    "username": form.cleaned_data['username']
                }
            )

        except Exception as e:
            logger.error(f"Error sending message: {e}")

    async def save_message(self, room_id, message):
        return True

    async def retrieve_messages(self, room_id):
        return []
