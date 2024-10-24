"""Utility module."""

from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from activities import models, participant_profile_picture
from rest_framework import decorators, response


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
