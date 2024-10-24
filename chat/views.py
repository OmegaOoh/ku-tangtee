"""View modules for Chat message."""
from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from django.db.models import QuerySet


class ChatMessageList(generics.ListAPIView):
    """Class view for ChatMessage."""

    serializer_class = MessageSerializer

    def get_queryset(self) -> QuerySet[Message]:
        """Query chat messages using activity id.

        :return: all the messages that exist in the activity
        """
        activity_id = self.kwargs['activity_id']
        return Message.objects.filter(activity_id=activity_id).order_by('timestamp')
