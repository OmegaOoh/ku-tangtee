"""Routing path for websocket."""
from django.urls import path
from .consumers import IndexPageConsumer

websocket_urlpatterns = [
    path("ws/index/", IndexPageConsumer.as_asgi()),
]
