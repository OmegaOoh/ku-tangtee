"""Utility module."""

from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from activities import models
from django.contrib.auth import models as auth_models
from rest_framework import decorators, response
from rest_framework.permissions import IsAuthenticated
import random
import string

CHECKIN_CODE_LEN = 6


@decorators.api_view(['get'])
def csrf_token_view(request: HttpRequest) -> response.Response:  # pragma: no cover
    """Return csrf token."""
    csrf_token = get_token(request)
    return response.Response({'csrfToken': csrf_token})


@decorators.api_view(['get'])
def get_recent_activity(request: HttpRequest, *args, **kwargs) -> response.Response:  # pragma: no cover
    """Return recently joined activities.

    :param request: Http request object
    :return: Response object contain activities that recently joined.
    """
    user = get_object_or_404(models.User, id=kwargs.get('id'))
    order_by_date = bool(request.GET.get('byDate', False))
    records = request.GET.get('records', None)
    if (records):
        records = int()
    activities = models.Attend.recently_joined(user, records, order_by_date)
    recent_activities = [{"name": activity.name,
                          "activity_id": activity.id,
                          "activity_date": activity.date} for activity in activities]
    return response.Response(recent_activities)


def get_checkin_code() -> str:
    """Random 6 capital character.

    :return: string of random 6 character.
    """
    # choose from all lowercase letter
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(CHECKIN_CODE_LEN))
    return result_str
