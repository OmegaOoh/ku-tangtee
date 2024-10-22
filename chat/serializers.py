from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'activity', 'sender', 'message', 'timestamp']  # Specify the fields to serialize
