"""Module for handle URL /activities."""
from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response
from activities import models, serializers


class ActivityList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    """Return list of available upcoming activity when GET request and create new activity when POST request."""

    queryset = models.Activity.objects.filter(date__gte=timezone.now()).order_by("date")
    serializer_class = serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return with list of activity."""
        return self.list(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Create an activity and add user who create it to attend table."""
        res = self.create(request, *args, **kwargs)

        res_dict = res.data

        request.user.attend_set.create(
            activity=models.Activity.objects.get(pk=res_dict.get("id")),
            is_host=True
        )

        return response.Response(
            {
                "message": f"Your have successfully create activity {res_dict.get('name')}",
                "id": res_dict.get("id")
            }
        )