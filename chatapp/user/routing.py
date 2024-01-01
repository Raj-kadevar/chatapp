from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/message/<int:id>", consumers.ChatMessage.as_asgi()),
]