"""Custom permission class."""
from typing import Any
from django.http import HttpRequest
from rest_framework import permissions, generics
from . import models


class IsHostOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow host of an activity to edit it."""

    message = 'User must be the host to perform this action.'

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Activity) -> Any:
        """Return boolean value that signify that user has permission to perform action or not."""
        # GET, HEAD, POST or OPTIONS requests are allowed.
        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return True

        # Edit permissions are only allowed to the host.
        return request.user == obj.host()


class IsNotJoinedForPOST(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    message = "You've already joined the activity."

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Activity) -> bool:
        """Return boolean value that signify that user has permission to perform action or not."""
        # Join permissions are only allowed to the user who haven't joined.
        if request.method == "POST":
            return not obj.attend_set.filter(user=request.user).exists()

        # Other method are allowed.
        return True


class IsFullForPOST(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    message = "This activity is full."

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Activity) -> bool:
        """Return boolean value that signify that user has permission to perform action or not."""
        # Join permissions are only allowed when the activity isn't full.
        if request.method == "POST":
            return not obj.max_people or obj.people < obj.max_people

        # Other method are allowed.
        return True
