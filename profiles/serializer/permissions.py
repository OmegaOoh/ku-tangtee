"""Custom permission class."""
from typing import Any
from django.http import HttpRequest
from rest_framework import permissions, generics
from .. import models


class OnlyOwnerCanEdit(permissions.BasePermission):
    """Custom permission to only allow the profile owners to edit it."""

    message = 'Cannot edit other profile.'

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Profile) -> Any:
        """Check such that user is the profile owner.

        :param request: Http request object
        :param view: APIView object
        :param obj: Profile model object
        :return: boolean value that signify that user has permission to perform action or not.
        """
        # GET, HEAD, POST or OPTIONS requests are allowed.
        if request.method != "PUT":
            return True

        # Edit permissions are only allowed to the profile owner.
        return request.user == obj.user
