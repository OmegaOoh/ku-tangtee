"""Shotcuts function for testing activities app."""
from django.utils import timezone
from activities import models


def create_activity(activity_name: str, days_delta: int, people: int = 0, max_people: int = None):
    """Return created activity with given parameters."""
    activity = models.Activity.objects.create()
    activity.name = activity_name
    activity.date = timezone.now() + timezone.timedelta(days=days_delta)
    if (max_people is not None):
        activity.max_people = max_people
    activity.people = people
    activity.save()
    return activity
