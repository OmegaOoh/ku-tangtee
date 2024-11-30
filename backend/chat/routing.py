"""Routing path for websocket."""
from chat.consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path("ws/chat/<int:activity_id>", ChatConsumer.as_asgi()),
]
