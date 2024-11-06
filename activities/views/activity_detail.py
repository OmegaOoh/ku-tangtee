"""Module for handle URL /activities/<activity_id>."""
from activities.views.util import image_loader, image_deleter, image_loader_64, edit_host_access
from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response
from activities import models
from activities.serializer.permissions import OnlyHostCanEdit
from activities.serializer import model_serializers


class ActivityDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     generics.GenericAPIView):
    """Return detail of an activity when GET request, and edit the activity when PUT request."""

    queryset = models.Activity.objects.all()
    serializer_class = model_serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OnlyHostCanEdit]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return detail of an activity.

        :param request: Http request object
        :return: Http response object
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle put request by edit an activity.

        :param request: Http request object
        :return: Http response object
        """
        activity = self.get_object()
        max_people = request.data.get("max_people")
        current_people = activity.people
        if max_people and current_people > max_people:
            return response.Response(
                {"message": "Number of participants exceed the capacity.",
                 "id": activity.id
                 },
            )
        res = self.update(request, partial=True, *args, **kwargs)
        res_dict = res.data

        grant_host_user_ids = request.data.get("grant_host", [])
        if grant_host_user_ids:
            res = edit_host_access(grant_host_user_ids, activity, request.user, remove=False)
            if res:
                return res

        remove_host_user_ids = request.data.get("remove_host", [])
        if remove_host_user_ids:
            res = edit_host_access(remove_host_user_ids, activity, request.user, remove=True)
            if res:
                return res

        attachment_ids_to_remove = request.data.get("remove_attachments", [])

        if attachment_ids_to_remove:
            image_deleter(attachment_ids_to_remove)

        attachment_to_add = request.data.get("new_images", [])
        if attachment_to_add:
            if any("base64" in attachment for attachment in attachment_to_add):
                image_loader_64(attachment_to_add, activity)
            else:
                image_loader(attachment_to_add, activity)

        activity.refresh_from_db()

        return response.Response(
            {
                "message": f"You have successfully edited the activity {res_dict.get('name')}",
                "id": res_dict.get("id")
            }
        )
