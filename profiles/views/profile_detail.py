"""Module for handle URL /profile."""
from typing import Any
from django.http import HttpRequest
from django.db.models import QuerySet
from rest_framework import generics, permissions, mixins, response, status
from profiles import models

from profiles.serializer import model_serializers


class ProfileDetail(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    """Return detail of the profile when GET request and create new profile when POST request."""

    serializer_class = model_serializers.ProfilesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        """Profile view returns a user's profile."""
        return models.Profile.objects.filter(user__id=self.request.user.id)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return detail of a profile.

        :param request: Http request object
        :return: Http response object
        """
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

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle put request by edit a profile.

        :param request: Http request object
        :return: Http response object
        """
        res = self.update(request, *args, **kwargs)

        res_dict = res.data

        return response.Response(
            {
                "message": f"You have successfully edited your KU Tangtee profile",
                "id": res_dict.get("id")
            }
        )

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle post request by creating a profile.

        :param request: Http request object
        :return: Http response object
        """
        return self.create(request, *args, **kwargs)

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Create new profile instance.

        :param request: Http request object
        :return: Http response object
        """
        serializer = self.get_serializer(
            data={
                "user": request.user.id
            }
        )
        serializer.is_valid(raise_exception=True)
        new_profile = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            {'message': f"You have successfully created your KU Tangtee profile" , "id": new_profile.id},
            status=status.HTTP_201_CREATED, headers=headers
        )
