"""Module for handle URL /activities."""
from activities.views.util import image_loader
from typing import Any
from django.http import HttpRequest
from django.utils import timezone
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
        queryset = models.Activity.objects.filter(date__gte=timezone.now()).order_by("date")

        keyword = self.request.GET.get("keyword")
        if keyword:
            queryset = queryset.filter(Q(name__iregex=rf'{keyword}') | Q(detail__iregex=rf'{keyword}'))

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

        image_loader(image_urls, new_act)

        request.user.attend_set.create(
            activity=new_act,
            is_host=True
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
