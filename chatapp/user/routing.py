from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/message/<int:id>", consumers.ChatManagement.as_asgi()),
    path("ws/status/", consumers.UpdateStatus.as_asgi()),
]