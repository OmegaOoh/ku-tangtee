"""Module for handle URL /activities."""
from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response, validators, status
from activities import models, serializers
from channels import layers
from asgiref import sync


class JoinView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    
    queryset = models.Attend.objects.all()
    serializer_class = serializers.AttendSerializer
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        return self.list(request, *args, **kwargs)
    
class JoinLeaveView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    
    queryset = models.Attend.objects.all()
    serializer_class = serializers.AttendSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        return response.Response({
            'yes': 'yes'
        })

    def post(self, request: HttpRequest, *args, **kwargs) -> response.Response:
        return self.create(request, *args, **kwargs)
    
    def create(self, request: HttpRequest, *args, **kwargs):
        
        serializer = self.get_serializer(
            data={
                "user": request.user.id,
                "activity": kwargs.get('pk')
            }
        )
        serializer.is_valid(raise_exception=True)
        new_attend = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return response.Response({'message': f'You have successfully joined the activity {new_attend.activity.name}'}, status=status.HTTP_201_CREATED, headers=headers)