"""Module for handle URL /activities/<activity_id>."""

from typing import Any
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, mixins, response, status
from activities import models
from activities.serializer.permissions import OnlyHostCanEdit
from activities.serializer import model_serializers


class CheckInView(generics.GenericAPIView, 
                  mixins.UpdateModelMixin):
    
    queryset = models.Activity.objects.filter(date__gte=timezone.now())
    serializer_class = model_serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OnlyHostCanEdit]
    
    
    def __init__(self, **kwargs: Any) -> None:
        self.status_change_method = {
            'open': self.open_check_in,
            'close': self.close_check_in
        }
        super().__init__(**kwargs)
    
    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        status = request.GET.get('status', 'no')
        return self.status_change_method.get(status, self.invalid_status)(request, args, kwargs)
    
    def open_check_in(self, request, *args, **kwargs):
        request.data['check_in_allowed'] = True
        res = super().update(request, partial=True,*args, **kwargs)
        return response.Response({
            'message': 'Activity check-in are open'
        })
    
    def close_check_in(self, request, *args, **kwargs):
        request.data['check_in_allowed'] = False      
        super().update(request, partial=True, *args, **kwargs)
        return response.Response({
            'message': 'Activity check-in are close'
        })
    
    def invalid_status(self, request, *args, **kwargs):
        return response.Response(
            {'message': 'No status provided.'}
        )
    
    
    