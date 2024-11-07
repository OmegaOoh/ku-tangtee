"""Module for handle URL /activities/<activity_id>."""

from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response
from activities import models
from activities.serializer.permissions import OnlyHostCanEdit, OnlyHostCanGet
from activities.serializer import model_serializers
from . import util


class CheckInView(
    generics.GenericAPIView,
    mixins.UpdateModelMixin
):
    """Handle PUT req by open/close for check-in and handle POST by check user in."""

    queryset = models.Activity.objects.filter(date__gte=timezone.now())
    serializer_class = model_serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OnlyHostCanEdit, OnlyHostCanGet]

    def __init__(self, **kwargs: Any) -> None:
        """Set up function for handling open/close checkin."""
        self.status_change_method = {
            'open': self.open_check_in,
            'close': self.close_check_in
        }
        super().__init__(**kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return activity check-in code or error message is check-in are not allow.

        :param request: Http request object
        :return: Http response object
        """
        activity = self.get_object()

        if not activity.check_in_allowed:
            return response.Response(
                {'message': 'Check-in are not allow at the moment'},
                status=403
            )

        return response.Response(
            {"check_in_code": activity.check_in_code}
        )

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle put request by call method associated to query param.

        :param request: Http request object
        :return: Http response object
        """
        status = request.GET.get('status', 'no')
        res: response.Response = self.status_change_method.get(status, self.invalid_status)(request, args, kwargs)
        return res

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle POST request by check-in user.

        :param request: Http request object
        :return: Http response object
        """
        code = request.data.get('check_in_code', 'no')
        activity = self.get_object()

        if not activity.is_participated(request.user):
            return response.Response(
                {'message': "You're not member of this activity"},
                status=403
            )

        if not activity.check_in_allowed:
            return response.Response(
                {'message': 'Check-in are not allow at the moment'},
                status=403
            )

        if not activity.verified_check_in_code(code):
            return response.Response(
                {'message': 'Check-in code invalid'},
                status=403
            )

        attend = activity.attend_set.get(user=request.user)
        attend.checked_in = True
        attend.save()

        return response.Response(
            {'message': f"You've successfully check-in to {activity.name}"}
        )

    def open_check_in(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Set check-in code and open for check in.

        :param request: Http request object
        :return: Http response object
        """
        request.data.update(
            {
                'check_in_allowed': True,
                'check_in_code': util.get_checkin_code()
            }
        )
        super().update(request, partial=True, *args, **kwargs)
        return response.Response({
            'message': 'Activity check-in are open',
            'check_in_code': request.data.get('check_in_code')
        })

    def close_check_in(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Close for check-in.

        :param request: Http request object
        :return: Http response object
        """
        request.data['check_in_allowed'] = False
        super().update(request, partial=True, *args, **kwargs)
        return response.Response({
            'message': 'Activity check-in are close'
        })

    def invalid_status(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Return error message when query param is invalid..

        :param request: Http request object
        :return: Http response object
        """
        return response.Response(
            {'message': 'No status provided.'}
        )
