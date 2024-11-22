"""Module for handle URL /activities/<activity_id>."""
from activities.views.util import image_loader, image_deleter, image_loader_64, edit_host_access
from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response
from django.db.models import Q
from activities import models
from activities.serializer.permissions import OnlyHostCanEdit
from activities.serializer import model_serializers
from django.db import transaction
from auth import serializer
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet


class ParticipantList(mixins.ListModelMixin,
                      generics.GenericAPIView):
    """Return detail of an activity when GET request, and edit the activity when PUT request."""

    queryset = models.Activity.objects.all()
    serializer_class = model_serializers.ParticipantDetailSerializer

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return detail of an activity.

        :param request: Http request object
        :return: Http response object
        """
        if 'search-participants' in request.path:
            return self.search_participants(request)
        return self.list(request, *args, **kwargs)

    def get_object(self) -> Any:
        """Override GenericAPIView get_object by get an object directly from queryset class variable.

        :raises TypeError: When queryset is not of type QuerySet.
        :return: None if lookup field are not provided or not exist and return and Activity instance if exist.
        """
        queryset = self.queryset

        if not isinstance(queryset, QuerySet):
            raise TypeError('queryset must be of type Queryset')

        field_val = self.kwargs.get(self.lookup_field, None)

        if not isinstance(field_val, int):
            field_val = None

        filter_kwargs = {self.lookup_field: field_val}

        return generics.get_object_or_404(queryset, **filter_kwargs)

    def get_queryset(self) -> QuerySet:
        """Override get_queryset by return list of activity Attend instance.

        :return: List of activity attend instance
        """
        activity = self.get_object()
        return activity.attend_set.all()

    def search_participants(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Search for participants by keyword.

        :param request: Http request object
        :return: Http response object
        """
        activity = self.get_object()
        keyword = request.GET.get("keyword", "")
        if keyword:
            participants = activity.attend_set.filter(
                Q(user__username__iregex=rf"{keyword}") |
                Q(user__first_name__iregex=rf"{keyword}") |
                Q(user__last_name__iregex=rf"{keyword}")
            )
        else:
            participants = activity.attend_set.all()

        page = self.paginate_queryset(participants)
        if page is not None:
            par_serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(par_serializer.data)

        par_serializer = self.get_serializer(participants, many=True)
        return response.Response(par_serializer.data)
