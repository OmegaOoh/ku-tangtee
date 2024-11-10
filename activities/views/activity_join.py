"""Module for handle URL /activities/join/<activity_id>/."""
from typing import Any
from django.http import HttpRequest
from rest_framework import generics, permissions, mixins, response, status
from activities import models, logger
from activities.serializer import model_serializers


class JoinLeaveView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """API view class for handle URL activities/join/<activies_id>."""

    queryset = models.Attend.objects.all()
    serializer_class = model_serializers.AttendSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle post request by create new attend instance.

        :param request: Http request object
        :return: Http response object
        """
        return self.create(request, *args, **kwargs)

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Create new attend instance.

        :param request: Http request object
        :return: Http response object
        """
        serializer = self.get_serializer(
            data={
                "user": request.user.id,
                "activity": kwargs.get('pk')
            }
        )
        serializer.is_valid(raise_exception=True)
        new_attend = serializer.save()
        headers = self.get_success_headers(serializer.data)

        act = new_attend.activity
        logger.info(req_user=request.user, action='JOIN', activity_id=act.id)
        return response.Response(
            {'message': f'You have successfully joined the activity {act.name}'},
            status=status.HTTP_201_CREATED, headers=headers
        )

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle delete request by destroy attend instance.

        :param request: Http request object
        :return: Http response object
        """
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Get attend instance and destroy it.

        :param request: Http request object
        :return: Http response object
        """
        tobe_del = self.get_serializer().get_attend(self.kwargs.get('pk'), request.user.id)
        self.perform_destroy(tobe_del)
        act = tobe_del.activity
        logger.info(req_user=request.user, action='LEAVE', activity_id=act.id)
        return response.Response(
            {'message': f"You've successfully leave {act.name}"},
            status=status.HTTP_200_OK
        )
