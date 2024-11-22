"""Module for serializing data before responding to a request."""
from rest_framework import serializers
from .models import Message, Attachment
from typing import Any


class MessageSerializer(serializers.ModelSerializer):
    """Serialized chat message."""

    first_name = serializers.CharField(source='sender.first_name', read_only=True)
    last_name = serializers.CharField(source='sender.last_name', read_only=True)
    user_id = serializers.CharField(source='sender.id', read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        """Message serializer META class."""

        model = Message
        fields = ['id', 'message', 'timestamp', 'first_name', 'last_name', 'user_id', 'activity', 'images']

    def get_images(self, message: Message) -> list[Any]:
        """Return activity images.

        :param obj: Activity model instance.
        :return: List of serialized images.
        """
        act_images = Attachment.objects.filter(message=message)
        images = [img.image.url for img in act_images]
        return images
