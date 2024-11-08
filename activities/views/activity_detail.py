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
        if 'search-participants' in request.path:
            return self.search_participants(request)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle put request by edit an activity.

        :param request: Http request object
        :return: Http response object
        """
        return self.update(request, *args, **kwargs)

    def update(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Update an activity with new information provided.

        :param request: Http request object
        :return: Http response object
        """
        # Checking number of people join
        check_max_error = self.__check_max_people(request)
        if check_max_error:
            return check_max_error

        # Update activity information
        res = super().update(request, *args, **kwargs)
        res_dict = res.data

        # Deal with attachment.
        self.__add_remove_attachment(request)
        # Deal with participants
        self.__grant_host_remove_host(request)
        # Kick attendee
        self.__kick_attendee(request)

        return response.Response(
            {
                "message": f"You have successfully edited the activity {res_dict.get('name')}",
                "id": res_dict.get("id")
            }
        )

    def __check_max_people(self, request: HttpRequest) -> response.Response | None:
        """Check max people.

        :param request: HttpRequest object
        """
        activity = self.get_object()
        max_people = request.data.get("max_people")
        current_people = activity.people
        if max_people and current_people > max_people:
            return response.Response(
                {
                    "message": "Number of participants exceed the capacity.",
                    "id": activity.id
                },
            )
        return None

    def __add_remove_attachment(self, request: HttpRequest) -> None:
        """Add or remove images from activity.

        :param request: HttpRequest object
        """
        activity = self.get_object()
        attachment_ids_to_remove = request.data.get("remove_attachments", [])

        if attachment_ids_to_remove:
            image_deleter(attachment_ids_to_remove)

        attachment_to_add = request.data.get("new_images", [])
        if attachment_to_add:
            if any("base64" in attachment for attachment in attachment_to_add):
                image_loader_64(attachment_to_add, activity)
            else:
                image_loader(attachment_to_add, activity)

    def __grant_host_remove_host(self, request: HttpRequest) -> Any:
        """Grant host and remove host from activity.

        :param request: HttpRequest object
        """
        activity = self.get_object()
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

    def __kick_attendee(self, request: HttpRequest) -> None:
        """Handle kick attendee from activity.

        :param request: HttpRequest object
        """
        activity = self.get_object()

        attendee_ids_to_remove = request.data.get("attendee_to_remove", [])
        attendee_to_remove = activity.attend_set.filter(user__id__in=attendee_ids_to_remove, is_host=False)

        print(attendee_ids_to_remove)
        attendee_to_remove.delete()
        return

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

        serializer = model_serializers.ParticipantDetailSerializer(participants, many=True)
        return response.Response(serializer.data)
