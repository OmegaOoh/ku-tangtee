"""Module for handle URL /profile."""
from typing import Any
from django.http import HttpRequest
from django.db.models import QuerySet
from rest_framework import generics, permissions, mixins, response, status
from profiles import models

from profiles.serializer import model_serializers
from profiles.serializer.permissions import IsOwnerOrReadOnly


class ProfileDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    """Return detail of the profile when GET request and edit profile when PUT request."""

    serializer_class = model_serializers.ProfilesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self) -> QuerySet:
        """Profile view returns a user's profile."""
        return models.Profile.objects.all()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return detail of a profile.

        :param request: Http request object
        :return: Http response object
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle put request by edit a profile.

        :param request: Http request object
        :return: Http response object
        """
        res = self.update(request, partial=True, *args, **kwargs)

        res_dict = res.data

        return response.Response(
            {
                "message": "You have successfully edited your KU Tangtee profile.",
                "id": res_dict.get("id")
            }
        )
