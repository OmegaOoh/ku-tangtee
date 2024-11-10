"""Module for handle URL /activities/<activity_id>."""

from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response
from activities import models, logger
from activities.serializer.permissions import OnlyHostCanEdit
from activities.serializer import model_serializers
from . import util
from profiles.models import Profile


class CheckInView(
    generics.GenericAPIView,
    mixins.UpdateModelMixin
):
    """Handle PUT req by open/close for check-in and handle POST by check user in."""

    queryset = models.Activity.objects.filter(date__gte=timezone.now())
    serializer_class = model_serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OnlyHostCanEdit]

    def __init__(self, **kwargs: Any) -> None:
        """Set up function for handling open/close checkin."""
        self.status_change_method = {
            'open': self.open_check_in,
            'close': self.close_check_in
        }
        super().__init__(**kwargs)

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
        act = self.get_object()

        if not act.is_participated(request.user):
            logger.warning(req_user=request.user, action='FAIL to CHECK-IN to', activity_id=act.id, reason='Not member')
            return response.Response(
                {'message': "You're not member of this activity"},
                status=403
            )

        if not act.check_in_allowed:
            logger.warning(req_user=request.user, action='FAIL to CHECK-IN to', activity_id=act.id, reason='Check-in not allow')
            return response.Response(
                {'message': 'Check-in are not allow at the moment'},
                status=403
            )

        if not act.verified_check_in_code(code):
            logger.warning(req_user=request.user, action='FAIL to CHECK-IN to', activity_id=act.id, reason='Invalid code')
            return response.Response(
                {'message': 'Check-in code invalid'},
                status=403
            )

        attend = act.attend_set.get(user=request.user)
        attend.checked_in = True
        attend.save()

        user_profile = request.user.profile_set.first()
        user_profile.increase_reputation()

        logger.info(req_user=request.user, action='CHECK-IN to', activity_id=act.id)
        return response.Response(
            {'message': f"You've successfully check-in to {act.name}"}
        )

    def open_check_in(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Set check-in code and open for check in.

        :param request: Http request object
        :return: Http response object
        """
        act = self.get_object()
        if act.is_checkin_period():
            request.data.update(
                {
                    'check_in_allowed': True,
                    'check_in_code': util.get_checkin_code()
                }
            )
            super().update(request, partial=True, *args, **kwargs)

            logger.info(req_user=request.user, action='OPEN CHECK-IN for', activity_id=act.id)
            return response.Response({
                'message': 'Activity check-in are open',
                'check_in_code': request.data.get('check_in_code')
            })

        logger.warning(req_user=request.user, action='FAIL to OPEN CHECK-IN for', activity_id=act.id,
                       reason='Not in Check-in period')
        return response.Response({'message': 'Check-in period is in between Start date and End date of the activity.'},
                                 status=403)

    def close_check_in(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Close for check-in.

        :param request: Http request object
        :return: Http response object
        """
        act = self.get_object()
        request.data['check_in_allowed'] = False
        super().update(request, partial=True, *args, **kwargs)
        logger.info(req_user=request.user, action='CLOSE CHECK-IN for', activity_id=act.id)
        return response.Response({
            'message': 'Activity check-in are close'
        })

    def invalid_status(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Return error message when query param is invalid.

        :param request: Http request object
        :return: Http response object
        """
        return response.Response(
            {'message': 'No status provided.'}
        )
