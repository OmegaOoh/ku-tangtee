"""URL configuration for chat app."""
from django.urls import path
from .views import ChatMessageList

urlpatterns = [
    path('<int:activity_id>/', ChatMessageList.as_view(), name='chat_message_list'),
]
