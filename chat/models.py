from django.db import models
from django.contrib.auth.models import User
from activities.models import Activity


class Message(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.RESTRICT)

    class Meta:
        ordering = ["timestamp"]
