"""
TODO
- Create a ApiView class to handle activity detail request and edit activity request.
- Wire this class view to URL /activities/<activity_id> where
    - If request is GET return activity detail that has id equal to activity_id.
    - If request is PUT update activity according to request content where it's id equal to activity_id.
    - Edit activity is limit to host of an activity therefore, we need permission class to enforce it.
    - Fix _test_detail.py and test_edit_activity.py after create a ApiView class 
- Refer to this docs
    Class base API view https://www.django-rest-framework.org/tutorial/3-class-based-views/
    Permission class https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
"""
from typing import Any

from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response, status
from activities import models
from activities import serializers
from activities import models
from activities.models import Activity
from activities.permissions import IsHostOrReadOnly
from activities.serializers import ActivitiesSerializer


class ActivityDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    """
    Return detail of an activity when GET request,
    and edit the activity when PUT request
    """

    queryset = models.Activity.objects.filter(date__gte=timezone.now())
    serializer_class = serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsHostOrReadOnly]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Edit an activity"""
        res = self.update(request, *args, **kwargs)

        res_dict = res.data

        return response.Response(
            {
                "message": f"Your have edited activity {res_dict.get('name')}",
                "id": res_dict.get("id")
            }
        )
