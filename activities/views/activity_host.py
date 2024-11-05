"""Module for handle URL activities/host/<str:action>/<int:activity_id>/<int:user_id>/."""
from typing import Any
from django.http import HttpRequest
from rest_framework import generics, permissions, mixins, response, status
from rest_framework.generics import get_object_or_404
from django.contrib.auth import models as auth_models
from activities.serializer.permissions import MustBeOwner, MustBeMember, OnlyHostCanEdit

from activities import models
from activities.serializer import model_serializers


class GrantRemoveHostView(
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    """API view class for handle URL activities/host/<str:action>/<int:activity_id>/<int:user_id>/."""

    queryset = models.Attend.objects.all()
    serializer_class = model_serializers.AttendSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, MustBeOwner]

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle put request by edit host access according to the arguments.

        :param request: Http request object
        :return: Http response object
        """
        new_kwargs = kwargs.copy()
        action = new_kwargs.pop('action', None)
        user_id = new_kwargs.pop('user_id', None)
        activity_id = new_kwargs.pop('pk', None)

        activity = get_object_or_404(models.Activity, pk=activity_id)
        user = get_object_or_404(auth_models.User, id=user_id)

        if request.user != activity.owner:
            return response.Response({'message': "You must be the owner of this activity to perform this action."}, status=403)

        if user == activity.owner:
            return response.Response({'message': 'Cannot modify access of your own activity.'}, status=403)

        if not activity.is_participated(user) and not activity.is_hosts(user):
            return response.Response({'message': f'Cannot find user {user.username} in this activity.'}, status=403)

        attend = get_object_or_404(models.Attend, activity=activity, user=user)

        if action == "grant":
            attend.is_host = True
            action_text = "granted"

        if action == "remove":
            attend.is_host = False
            action_text = "removed"

        attend.save()

        return response.Response(
            {
                "message": f"You have successfully {action_text} host access "
                           f"to user {user.username} for activity {activity.name}.",
                "id": attend.id,
            }
        )
