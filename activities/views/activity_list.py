"""Module for handle URL /activities."""
import re
from datetime import timedelta
from activities.views.util import image_loader, image_loader_64
from typing import Any
from django.http import HttpRequest
from django.utils import timezone, dateparse
from django.db.models import Q, QuerySet
from rest_framework import generics, permissions, mixins, response
from activities import models
from channels import layers
from asgiref import sync

from activities.serializer import model_serializers


class ActivityList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    """Return list of available upcoming activity when GET request and create new activity when POST request."""

    queryset = models.Activity.objects.filter(date__gte=timezone.now()).order_by("date")
    serializer_class = model_serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        """Activity index view returns a list of all the activities according to query parameters."""
        queryset = super().get_queryset()

        keyword = self.request.GET.get("keyword")
        if keyword:
            queryset = queryset.filter(Q(name__iregex=rf'{keyword}') | Q(detail__iregex=rf'{keyword}'))

        day = self.__parse_date(self.request.GET.get("day"))
        if day:
            queryset = queryset.filter(date__week_day__in=day)

        try:
            start_date = dateparse.parse_date(self.request.query_params.get("start_date"))
            queryset = queryset.filter(date__gte=start_date)
        except (ValueError, TypeError):
            pass

        try:
            end_date = dateparse.parse_date(self.request.query_params.get("end_date")) + timedelta(days=1)
            queryset = queryset.filter(date__lte=end_date)
        except (ValueError, TypeError):
            pass

        return queryset

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return with list of activity."""
        return self.list(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Create an activity and add user who create it to attend table.

        :param request: Http request object
        :return: Http response object
        """
        image_urls = request.data.pop('images', [])
        res = self.create(request, *args, **kwargs)

        res_dict = res.data

        new_act = models.Activity.objects.get(pk=res_dict.get("id"))

        if image_urls:
            if any("base64" in attachment for attachment in image_urls):
                image_loader_64(image_urls, new_act)
            else:
                image_loader(image_urls, new_act)

        request.user.attend_set.create(
            activity=new_act,
            is_host=True,
            checked_in=True
        )

        # Send message to websocket
        layer = layers.get_channel_layer()
        sync.async_to_sync(layer.group_send)(
            'activity_index', {
                'type': "new_act",
                'activity_id': new_act.id,
            }
        )

        return response.Response(
            {
                "message": f"Your have successfully create activity {res_dict.get('name')}",
                "id": res_dict.get("id")
            }
        )

    def __parse_date(self, date_param: str) -> list[int] | None:

        day_list_format = r'^(?:[1-7](?:,[1-7])*)?$'

        if (not date_param) or (not re.fullmatch(day_list_format, date_param)):
            return None

        split_day = date_param.split(',')

        if len(split_day) > 7:
            return None

        return [int(s.strip()) for s in split_day]
