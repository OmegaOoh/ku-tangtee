"""Shortcuts function for testing profile app."""
import io
import sys
import json
from django.http import HttpResponse
import django.test
from typing import Tuple
from profiles import models
from django.contrib.auth.models import User
from django import urls


def create_test_user(username: str = "test_user") -> User:
    """Return a test user.

    :param username: username for user
    :return: User object
    """
    return User.objects.create_user(
        username=username,
        password="password"
    )


def create_profile(
    user: User = None,
    client: django.test.Client = django.test.Client(),
    data: dict = {"faculty": "Faculty", "ku_generation": "80"},
    log_in: bool = True,
    rep_score: int = 0
) -> Tuple[HttpResponse, models.Profile]:
    """Return response and created profile with given parameters.

    :param user: User object
    :param client: django client for testing
    :param data: dictionary of data for creating profile
    :param log_in: force login immediately or not
    :return: User object
    """
    if not user:
        user = create_test_user("user")

    if log_in:
        client.force_login(user)

    data['reputation_score'] = rep_score

    url = urls.reverse("profiles:index")
    res = post_request_json_data(url, client, data)

    try:
        response_dict = json.loads(res.content)
        profile = models.Profile.objects.get(pk=int(response_dict["id"]))
    except KeyError:
        profile = None

    client.logout()
    return res, profile


def post_request_json_data(path: str, client: django.test.Client, data: dict) -> HttpResponse:
    """Create POST request with provided data and Return response.

    :param path: url path you want to use
    :param client: django client for testing
    :param data: dictionary of data for sending post request
    :return: HttpResponse
    """
    # Suppress print statement
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    json_data = json.dumps(data)
    response = client.post(path, data=json_data, content_type='application/json')

    # Restore original std out
    sys.stdout = stdout

    return response


def put_request_json_data(path: str, client: django.test.Client, data: dict) -> HttpResponse:
    """Create PUT request with provided data and Return response.

    :param path: url path you want to use
    :param client: django client for testing
    :param data: dictionary of data for sending put request
    :return: HttpResponse
    """
    # Suppress print statement
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    json_data = json.dumps(data)
    response = client.put(path, data=json_data, content_type='application/json')

    # Restore original std out
    sys.stdout = stdout

    return response
