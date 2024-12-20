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


class OnlyHostCanGet(permissions.BasePermission):
    """Custom permission to only allow host of an activity to edit it."""

    message = 'User must be the host to perform this action.'

    def has_object_permission(self, request: HttpRequest, view: generics.GenericAPIView, obj: models.Activity) -> Any:
        """Check such that user has right to get an information or not.

        :param request: Http request object
        :param view: APIView object
        :param obj: Activity model object
        :return: boolean value that signify that user has permission to perform action or not.
        """
        if request.method != "GET":
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
        # Edit permissions are only allowed to activity member and host.
        return obj.is_participated(request.user) or obj.is_hosts(request.user)
