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

    try:
        response_dict = json.loads(res.content)
        # print(response_dict)
        act = models.Activity.objects.get(pk=int(response_dict["id"]))
    except KeyError:
        act = None

    return res, act


def activity_to_json(activity: models.Activity, use_can_join: bool = False):
    """Return dict that replicates json that's contain activity data."""
    serial = ActivitiesSerializer(activity)
    return serial.data


def time_formatter(date_string: str) -> str:
    """Format time into expected format."""
    utc_date = pytz.utc.localize(datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ'))
    local_date = utc_date.astimezone()
    formatted_date = local_date.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
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


def put_request_json_data(path: str, client: django.test.Client, data: dict) -> HttpResponse:
    """Create PUT request with provided data and Return response."""
    # Suppress print statement
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    json_data = json.dumps(data)
    response = client.put(path, data=json_data, content_type='application/json')

    # Restore original std out
    sys.stdout = stdout

    return response


def client_join_activity(client: django.test.Client, user: User, activity: models.Activity) -> None:
    """Client join specific activity with provided user."""
    client.force_login(user)
    client.post(urls.reverse("activities:detail", args=[activity.id]))
    activity.refresh_from_db()
