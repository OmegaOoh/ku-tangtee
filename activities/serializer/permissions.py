"""Custom permission class."""
from typing import Any
from django.http import HttpRequest
from rest_framework import permissions, generics
from .. import models


class OnlyHostCanEdit(permissions.BasePermission):
    """Custom permission to only allow host of an activity to edit it."""

    message = 'User must be the host to perform this action.'

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Activity) -> Any:
        """Check such that user has right to edit activity or not.

        :param request: Http request object
        :param view: APIView object
        :param obj: Activity model object
        :return: boolean value that signify that user has permission to perform action or not.
        """
        if request.method != "PUT":
            return True

        # Edit permissions are only allowed to the host.
        return request.user in obj.host()


class MustBeMember(permissions.BasePermission):
    """Custom permission to only allow host of an activity to edit it."""

    message = 'You must be member of this activity before perform this action.'

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Activity) -> Any:
        """Check such that user has right to edit activity or not.

        :param request: Http request object
        :param view: APIView object
        :param obj: Activity model object
        :return: boolean value that signify that user has permission to perform action or not.
        """
        # Edit permissions are only allowed to activity member.
        return obj.is_participated(request.user)


class MustBeOwner(permissions.BasePermission):
    """Custom permission to only allow owner of an activity to perform action."""

    message = 'You must be the owner of this activity to perform this action.'

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Activity) -> Any:
        """Check such that user is activity owner or not.

        :param request: Http request object
        :param view: APIView object
        :param obj: Activity model object
        :return: boolean value that signify that user has permission to perform action or not.
        """
        # Only allowed to activity owner.
        return request.user == obj.owner
