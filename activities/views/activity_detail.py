"""Module for handle URL /activities/<activity_id>."""

from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response, status
from activities import models, serializers
from activities.permissions import IsHostOrReadOnly, IsNotJoinedForPOST, IsFullForPOST


class ActivityDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     generics.GenericAPIView):
    """Return detail of an activity when GET request, and edit the activity when PUT request."""

    queryset = models.Activity.objects.filter(date__gte=timezone.now())
    serializer_class = serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsHostOrReadOnly, IsNotJoinedForPOST, IsFullForPOST]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return detail of an activity."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle put request by edit an activity."""
        activity = self.get_object()
        max_people = request.data.get("max_people")
        current_people = activity.people
        if max_people and current_people >= max_people:
            return response.Response(
                {"message": "Number of participants exceed the capacity.",
                 "id": activity.id
                 },
            )
        res = self.update(request, *args, **kwargs)
        res_dict = res.data
        return response.Response(
            {
                "message": f"You have successfully edited the activity {res_dict.get('name')}",
                "id": res_dict.get("id")
            }
        )

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle post request by joining an activity."""
        res = self.retrieve(request, *args, **kwargs)

        res_dict = res.data

        request.user.attend_set.create(
            activity=models.Activity.objects.get(pk=res_dict.get("id")),
            is_host=False
        )

        return response.Response(
            {
                "message": f"You have successfully joined the activity {res_dict.get('name')}",
                "id": res_dict.get("id")
            }
        )
