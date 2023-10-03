
from django.urls import path

from .views import chat_view, get_messages


urlpatterns = [
    path("", chat_view, name="chat-page"),
    path("messages/<str:channel>", chat_view, name="chat-page"),
    path("api/messages/<str:channel>", get_messages)
]
