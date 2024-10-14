"""Shortcuts function for testing activities app."""
import io
import sys
import json
import pytz
from datetime import datetime
from django.http import HttpResponse
import django.test
from django.utils import timezone
from activities import models
from django.contrib.auth.models import User
from django import urls
from activities.serializers import ActivitiesSerializer


def create_test_user(username: str = "test_user") -> User:
    """Return a test user."""
    return User.objects.create_user(
        username=username,
        password="password"
    )


def create_activity(
    host: User = None,
    client: django.test.Client = django.test.Client(),
    data: dict = {"name": "test_activity", "detail": "hello"},
    days_delta: int = 1
):
    """Return response and created activity with given parameters."""
    if not host:
        host = create_test_user("host")

    data_with_date = data | {
        "date": (timezone.now() + timezone.timedelta(days=days_delta)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }
    client.force_login(host)
    url = urls.reverse("activities:index")
    res = post_request_json_data(url, client, data_with_date)
    
    response_dict = json.loads(res.content)
    
    act = models.Activity.objects.get(pk=int(response_dict["id"]))
    # try:
    #     act = models.Activity.objects.get(pk=int(response_dict["id"]))
    # except KeyError:
    #     act = None

    return res, act


def activity_to_json(activity: models.Activity, use_can_join: bool = False):
    """Return dict that replicates json that's contain activity data."""
    # formatted_date = activity.date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    # output = {
    #     "id": activity.id,
    #     "name": activity.name,
    #     "detail": activity.detail,
    #     "date": formatted_date,
    #     "max_people": activity.max_people,
    #     "people": activity.people
    # }
    # if use_can_join:
    #     output['can_join'] = activity.can_join()
    # return output
    
    serial = ActivitiesSerializer(activity)
    return serial.data


def time_formatter(date_string: str) -> str:
    """Format time into expected format."""
    received_date = timezone.make_aware(datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ'))
    utc_date = received_date.astimezone(pytz.utc)
    formatted_date = utc_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return formatted_date


def post_request_json_data(path: str, client: django.test.Client, data: dict) -> HttpResponse:
    """Create POST request with provided data and Return response."""
    # Suppress print statement
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    json_data = json.dumps(data)
    response = client.post(path, data=json_data, content_type='application/json')
    
    # Restore original std out
    sys.stdout = stdout

    return response
