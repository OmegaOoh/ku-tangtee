"""Permission module for chat."""
from typing import Any

from activities.models import Activity
from django.http import HttpRequest
from rest_framework import generics, permissions


class IsUserInActivity(permissions.BasePermission):
    """Custom permission to only allow users who are part of the activity to view chat messages."""

    message = 'You must be activity participant in order to view chat.'

    def has_permission(self, request: HttpRequest, view: generics.GenericAPIView) -> Any:
        """Check such that user has right to view the messages.

        :param request: Http request object
        :param view: APIView object
        :param obj: Activity model object
        :return: boolean value that signify that user has permission to perform action or not.
        """
        activity_id = view.kwargs.get('activity_id')
        try:
            activity = Activity.objects.get(id=activity_id)
            return activity.attend_set.filter(user=request.user).exists()
        except Activity.DoesNotExist:
            return False
