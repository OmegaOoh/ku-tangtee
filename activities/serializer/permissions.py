"""Custom permission class."""
from typing import Any
from django.http import HttpRequest
from rest_framework import permissions, generics
from .. import models


class IsHostOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow host of an activity to edit it."""

    message = 'User must be the host to perform this action.'

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Activity) -> Any:
        """Check such that user has right to edit activity or not.

        :param request: Http request object
        :param view: APIView object
        :param obj: Activity model object
        :return: boolean value that signify that user has permission to perform action or not.
        """
        # GET, HEAD, POST or OPTIONS requests are allowed.
        if request.method != "PUT":
            return True

        # Edit permissions are only allowed to the host.
        return request.user == obj.host()
