"""Utility module."""

from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from activities import models, participant_profile_picture
from rest_framework import decorators, response
from rest_framework.permissions import IsAuthenticated


@decorators.api_view(['get'])
def csrf_token_view(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return csrf token."""
    csrf_token = get_token(request)
    return response.Response({'csrfToken': csrf_token})


@decorators.api_view(['get'])
def get_participant_detail(request: HttpRequest, activity_id: int) -> JsonResponse:  # pragma: no cover
    """Return list of participant with detail and profile picture."""
    activity = models.Activity.objects.get(id=activity_id)
    attendees = activity.attend_set.all()
    participants_detail = []
    for attendance in attendees:
        details = participant_profile_picture.retrieve_profile_picture(attendance.user)
        participants_detail.append(details)
    return response.Response(participants_detail)


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
