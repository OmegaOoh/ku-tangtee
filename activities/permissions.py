"""Custom permission class."""

from typing import Any
from django.http import HttpRequest
from rest_framework import permissions, generics
from . import models


class IsHostOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Activity) -> bool:
        """Return boolean value that signify that user has permission to perform action or not."""
        # GET, HEAD or OPTIONS requests are allowed.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Edit permissions are only allowed to the host.
        return request.user == obj.host()
