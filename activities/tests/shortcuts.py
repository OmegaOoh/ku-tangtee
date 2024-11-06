"""Shortcuts function for testing activities app."""
import io
import sys
import json
from datetime import datetime, timedelta
from django.http import HttpResponse
import django.test
from django.utils import timezone
from activities import models
from django.contrib.auth.models import User
from django import urls
from activities.serializer.model_serializers import ActivitiesSerializer
from profiles.tests.shortcuts import create_profile


def create_test_user(username: str = "test_user", with_profile=True, rep_score=0) -> User:
    """Return a test user."""
    
    new_user = User.objects.create_user(
        username=username,
        password="password",
    )
    
    if with_profile:
        create_profile(user=new_user, rep_score=rep_score)

    return new_user

def create_activity(
    host: User = None,
    client: django.test.Client = django.test.Client(),
    data: dict = {"name": "test_activity", "detail": "hello"},
    days_delta: int = 1
):
    """Return response and created activity with given parameters."""
    if not host:
        host = create_test_user("host")
    new_date = (timezone.now() + timezone.timedelta(days=days_delta)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    data_with_date = data.copy()
    if "date" not in data_with_date:
        data_with_date["date"] = new_date

    if "end_date" not in data_with_date:
        data_with_date["end_date"] = new_date

    if "end_registration_date" not in data_with_date:
        data_with_date["end_registration_date"] = new_date

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
    utc_date = timezone.make_aware(datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ'))
    formatted_date = utc_date.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
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
    client.post(urls.reverse("activities:join", args=[activity.id]))
    activity.refresh_from_db()


def convert_day_num(day_num: int) -> int:
    """Convert day num from python format (0 = Monday. 6 = Sunday) to MySQL format (1 = Sunday, 7 = Saturday).

    :param day_num: Day num in Python format
    :return: Day num in MySQL format
    """
    if day_num == 6:
        return 1

    return day_num + 2


def date_from_now(day_delta: int = 0):
    """Return the date after the next day_delta days in string format.

    :param day_delta: Days from now
    :return: Date after day_delta days
    """
    return (timezone.now() + timedelta(days=day_delta)).strftime("%Y-%m-%d")
