
from django.urls import path
from django.conf import settings

from .consumers import ChatConsumer
from .store import RedisStore

protocol = settings.WEBSOCKET_PROTOCOL

websocket_urlpatterns = [
    path(f"{protocol}/<str:room_id>/", ChatConsumer.use_store(RedisStore).as_asgi()),
]
