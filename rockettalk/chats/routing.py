
from django.urls import path

from .consumers import ChatConsumer
from .store import RedisStore


websocket_urlpatterns = [
    path("ws/<str:room_id>/", ChatConsumer.use_store(RedisStore).as_asgi()),
]
