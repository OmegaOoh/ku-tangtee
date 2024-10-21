"""Module for handle URL /activities/<activity_id>."""

from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response, status
from activities import models, serializers
from activities.permissions import IsHostOrReadOnly


class ActivityDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     generics.GenericAPIView):
    """Return detail of an activity when GET request, and edit the activity when PUT request."""

    queryset = models.Activity.objects.filter(date__gte=timezone.now())
    serializer_class = serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsHostOrReadOnly]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return detail of an activity."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle put request by edit an activity."""
        activity = self.get_object()
        max_people = request.data.get("max_people")
        current_people = activity.people
        if max_people and current_people > max_people:
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

        activity = models.Activity.objects.get(pk=res_dict.get("id"))

        if not activity.can_join():
            return response.Response(
                {"message": f"The activity {res_dict.get('name')} is full.",
                 "id": activity.id
                 }, status=401
            )

        if activity.attend_set.filter(user=request.user).exists():
            return response.Response(
                {"message": f"You've already joined the activity {res_dict.get('name')}.",
                 "id": activity.id
                 }, status=401
            )

        request.user.attend_set.create(
            activity=activity,
            is_host=False
        )

        return response.Response(
            {
                "message": f"You have successfully joined the activity {res_dict.get('name')}",
                "id": res_dict.get("id")
            }
        )
        