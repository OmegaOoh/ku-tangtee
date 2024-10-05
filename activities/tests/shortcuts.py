"""Shotcuts function for testing activities app."""
import json
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

def activity_to_json(activity: models.Activity, use_can_join: bool = False):
    """Return dict that replicates json thats contain activity data"""
    formatted_date = activity.date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    output = {
            "id": activity.id,
            "name": activity.name,
            "detail": activity.detail,
            "date": formatted_date,
            "max_people": activity.max_people,
            "people": activity.people
    }
    if (use_can_join):
        output['can_join'] = activity.can_join()
    return output
