"""Module for handle URL /activities."""
from typing import Any
from django.http import HttpRequest
from rest_framework import generics, permissions, mixins, response, status
from activities import models, serializers


class JoinLeaveView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """API view class for handle URL activities/join/<activies_id>."""

    queryset = models.Attend.objects.all()
    serializer_class = serializers.AttendSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle post request by create new attend instance."""
        return self.create(request, *args, **kwargs)

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Create new attend instance."""
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

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any):
        """Handle delete request by destroy attend instance."""
        res = self.destroy(request, *args, **kwargs)
        return res

    def destroy(self, request, *args, **kwargs) -> response.Response:
        """Get attend instance and destroy it."""
        tobe_del = self.get_serializer().get_attend(self.kwargs.get('pk'), request.user.id)
        self.perform_destroy(tobe_del)
        return response.Response(
            {'message': f"You've successfully leave {tobe_del.activity.name}"},
            status=status.HTTP_200_OK
        )
