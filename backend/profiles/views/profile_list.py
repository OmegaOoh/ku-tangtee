"""Module for handle URL /profile."""
from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest
from profiles import models
from profiles.logger import Action, RequestData, data_to_log, logger
from profiles.serializer import model_serializers
from rest_framework import generics, mixins, permissions, response, status


class ProfileList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    """Return detail of the profile when GET request and create new profile when POST request."""

    serializer_class = model_serializers.ProfilesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        """Profile view returns a user's profile."""
        return models.Profile.objects.filter(user__id=self.request.user.id)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return with list of profile."""
        return self.list(request, *args, **kwargs)

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """List user's profile instance.

        :param request: Http request object
        :return: Http response object
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset.first())
        return response.Response({
            "has_profile": models.Profile.has_profile(request.user), 'profile': serializer.data
        })

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle post request by creating a profile.

        :param request: Http request object
        :return: Http response object
        """
        if self.get_queryset().exists():
            req_data = RequestData(req_user=request.user, profile_id=-1)
            logger.warning(data_to_log(Action.FAIL_CREATE, req_data, 'Already exist'))
            return response.Response({"message": "You've already created your profile.",
                                      "id": self.get_queryset().first().id}, status=status.HTTP_403_FORBIDDEN)
        return self.create(request, *args, **kwargs)

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Create new profile instance.

        :param request: Http request object
        :return: Http response object
        """
        data = {"user": request.user.id} | request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        new_profile = serializer.save()
        headers = self.get_success_headers(serializer.data)

        req_data = RequestData(req_user=request.user, profile_id=new_profile.id)
        logger.info(data_to_log(Action.CREATE, req_data))
        return response.Response(
            {'message': "You have successfully created your KU Tangtee profile.", "id": new_profile.id},
            status=status.HTTP_201_CREATED, headers=headers
        )
