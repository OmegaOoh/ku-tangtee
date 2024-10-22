from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='sender.first_name', read_only=True)
    last_name = serializers.CharField(source='sender.last_name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'message', 'timestamp', 'first_name', 'last_name', 'activity']
