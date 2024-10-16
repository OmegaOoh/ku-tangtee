from django.db import models
from django.contrib.auth.models import User
from activities.models import Activity


class Message(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=255)  # TODO change to foreign key
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)

    class Meta:
        ordering = ["timestamp"]
