from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer

class ChatMessageList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        activity_id = self.kwargs['activity_id']
        return Message.objects.filter(activity_id=activity_id).order_by('timestamp')
