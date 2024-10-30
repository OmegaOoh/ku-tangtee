"""Utility module."""

from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from activities import models
from rest_framework import decorators, response
from rest_framework.permissions import IsAuthenticated
import random
import string

CHECKIN_CODE_LEN = 6

@decorators.api_view(['get'])
def csrf_token_view(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return csrf token."""
    csrf_token = get_token(request)
    return response.Response({'csrfToken': csrf_token})


@decorators.api_view(['get'])
@decorators.permission_classes([IsAuthenticated])
def get_recent_activity(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return recently joined activities.

    :param request: Http request object
    :return: Response object contain activities that recently joined.
    """
    user = request.user
    activities = models.Attend.recently_joined(user)
    recent_activities = [{"name": activity.name, "activity_id": activity.id} for activity in activities]
    return response.Response(recent_activities)


def get_checkin_code():
    # choose from all lowercase letter
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(CHECKIN_CODE_LEN))
    return result_str

