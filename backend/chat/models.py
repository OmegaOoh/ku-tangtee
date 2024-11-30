"""Database Schema for Chat application."""
from activities.models import Activity
from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    """Message model for chat application."""

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.RESTRICT)

    class Meta:
        """Meta class for Message models."""

        ordering = ["timestamp"]


class Attachment(models.Model):
    """Image attachment for chat."""

    image = models.ImageField('Chat', upload_to="chat/", height_field=None, width_field=None, max_length=None)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
