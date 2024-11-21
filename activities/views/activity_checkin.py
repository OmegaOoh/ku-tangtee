"""Module for handle URL /activities/<activity_id>."""

from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response
from activities import models
from activities.logger import logger, Action, RequestData, data_to_log
from activities.serializer.permissions import OnlyHostCanEdit, OnlyHostCanGet, MustBeMember
from activities.serializer import model_serializers
from . import util


class CheckInView(
    generics.GenericAPIView,
    mixins.UpdateModelMixin
):
    """Handle PUT req by open/close for check-in and handle POST by check user in."""

    queryset = models.Activity.objects.filter(end_date__gte=timezone.now())
    serializer_class = model_serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OnlyHostCanEdit, OnlyHostCanGet, MustBeMember]

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
            {
                'check_in_code': activity.check_in_code,
                'check_in_allowed': activity.check_in_allowed
            }
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

        req_data = RequestData(req_user=request.user, act_id=activity.id)

        if not activity.check_in_allowed:
            return response.Response(
                {'message': 'Check-in are not allow at the moment'},
                status=403
            )

        if not activity.verified_check_in_code(code):
            logger.warning(data_to_log(Action.FAIL_CHECKIN, req_data, 'Invalid code'))
            return response.Response(
                {'message': 'Check-in code invalid'},
                status=403
            )

        attend = activity.attend_set.get(user=request.user)

        if attend.checked_in:
            logger.warning(data_to_log(Action.FAIL_CHECKIN, req_data, "Already check-in"))
            return response.Response(
                {'message': f"You've already check-in to this {activity.name}"},
                status=403
            )

        attend.checked_in = True
        attend.save()

        user_profile = request.user.profile_set.first()
        user_profile.increase_reputation()

        logger.info(data_to_log(Action.CHECKIN, req_data))
        return response.Response(
            {'message': f"You've successfully check-in to {activity.name}"}
        )

    def open_check_in(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Set check-in code and open for check in.

        :param request: Http request object
        :return: Http response object
        """
        activity = self.get_object()
        req_data = RequestData(req_user=request.user, act_id=activity.id)

        if not activity.is_checkin_period():
            logger.warning(data_to_log(Action.FAIL_OPEN_CHECKIN, req_data, 'Not in Check-in period'))
            return response.Response(
                {'message': 'Check-in period is in between Start date and End date of the activity.'},
                status=403
            )

        request.data.update(
            {
                'check_in_allowed': True,
            }
        )
        super().update(request, partial=True, *args, **kwargs)

        activity.refresh_from_db()
        activity.update_check_in_code()
        activity.refresh_from_db()

        logger.info(data_to_log(Action.OPEN_CHECKIN, req_data))
        return response.Response({
            'message': 'Activity check-in are open',
            'check_in_allowed': activity.check_in_allowed
        })

    def close_check_in(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Close for check-in.

        :param request: Http request object
        :return: Http response object
        """
        activity = self.get_object()
        request.data['check_in_allowed'] = False
        super().update(request, partial=True, *args, **kwargs)
        req_data = RequestData(req_user=request.user, act_id=activity.id)
        logger.info(data_to_log(Action.CLOSE_CHECKIN, req_data))
        return response.Response({
            'message': 'Activity check-in are close',
            'check_in_allowed': activity.check_in_allowed
        })

    def invalid_status(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Return error message when query param is invalid.

        :param request: Http request object
        :return: Http response object
        """
        return response.Response(
            {'message': 'No status provided.'}
        )
