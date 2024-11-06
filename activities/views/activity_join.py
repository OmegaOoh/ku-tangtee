"""Module for handle URL /activities/join/<activity_id>/."""
from typing import Any
from django.http import HttpRequest
from rest_framework import generics, permissions, mixins, response, status
from activities import models
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
        user_profile = request.user.profile_set.first()

        if not user_profile:
            return response.Response(
                {
                    'message': 'User must have profile page before joining an activity',
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if not user_profile.able_to_join_more:
            return response.Response(
                {
                    'message': "The number of activities you have joined has reached the limit",
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(
            data={
                "user": request.user.id,
                "activity": kwargs.get('pk')
            }
        )
        serializer.is_valid(raise_exception=True)
        new_attend = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            {'message': f'You have successfully joined the activity {new_attend.activity.name}'},
            status=status.HTTP_201_CREATED, headers=headers
        )

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle delete request by destroy attend instance.

        :param request: Http request object
        :return: Http response object
        """
        res = self.destroy(request, *args, **kwargs)
        return res

    def destroy(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Get attend instance and destroy it.

        :param request: Http request object
        :return: Http response object
        """
        tobe_del = self.get_serializer().get_attend(self.kwargs.get('pk'), request.user.id)
        self.perform_destroy(tobe_del)
        return response.Response(
            {'message': f"You've successfully leave {tobe_del.activity.name}"},
            status=status.HTTP_200_OK
        )
