"""Module for handle URL /profile."""
from typing import Any
from django.http import HttpRequest
from django.db.models import QuerySet
from rest_framework import generics, permissions, mixins, response, status
from profiles import models

from profiles.serializer import model_serializers


class ProfileList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):

    serializer_class = model_serializers.ProfilesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        """Profile view returns a user's profile."""
        return models.Profile.objects.filter(user__id=self.request.user.id)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return with list of activity."""
        return self.list(request, *args, **kwargs)

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data + [{
                "has_profile": models.Profile.has_profile(request.user)}])

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle post request by creating a profile.

        :param request: Http request object
        :return: Http response object
        """
        if self.get_queryset().exists():
            return response.Response({"message": "You've already created your profile.", "id": self.get_queryset().first().id}, status=status.HTTP_403_FORBIDDEN)
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
        return response.Response(
            {'message': f"You have successfully created your KU Tangtee profile.", "id": new_profile.id},
            status=status.HTTP_201_CREATED, headers=headers
        )
