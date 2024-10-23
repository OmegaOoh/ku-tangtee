"""Module for serializing data before responding to a request."""
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    """Serialized chat message."""
    first_name = serializers.CharField(source='sender.first_name', read_only=True)
    last_name = serializers.CharField(source='sender.last_name', read_only=True)

    class Meta:
        """Message serializer META class."""
        model = Message
        fields = ['id', 'message', 'timestamp', 'first_name', 'last_name', 'activity']
