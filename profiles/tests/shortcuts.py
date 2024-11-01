"""Shortcuts function for testing activities app."""
import io
import sys
import json
from django.http import HttpResponse
import django.test

from profiles import models
from django.contrib.auth.models import User
from django import urls


def create_test_user(username: str = "test_user") -> User:
    """Return a test user."""
    return User.objects.create_user(
        username=username,
        password="password"
    )


def create_profile(
    user: User = None,
    client: django.test.Client = django.test.Client(),
    data: dict = {"faculty": "Faculty", "major": "Major"},
    log_in: bool = True,
):
    """Return response and created profile with given parameters."""
    if not user:
        user = create_test_user("user")

    if log_in:
        client.force_login(user)

    url = urls.reverse("profiles:index")
    res = post_request_json_data(url, client, data)

    try:
        response_dict = json.loads(res.content)
        profile = models.Profile.objects.get(pk=int(response_dict["id"]))
    except KeyError:
        profile = None

    return res, profile


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
