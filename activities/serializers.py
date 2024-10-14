"""Module for serializing data before respond a request."""

from rest_framework import serializers
from . import models


# class HostFields(serializers.SlugRelatedField):
    
#     def __init__(self, slug_field=None, **kwargs):
#         super().__init__(slug_field, **kwargs)
    
#     def get_queryset(self):
#         q = models.Attend.objects.filter(is_host=True)
#         print(q)
#         return q


class ActivitiesSerializer(serializers.ModelSerializer):
    """Serialized activity."""

    
    people = serializers.ReadOnlyField()
    host = serializers.SerializerMethodField()

    class Meta:
        model = models.Activity
        fields = ('__all__')
        
    def get_host(self, obj):
        
        act_host = models.Attend.objects.filter(activity=obj, is_host=True)
        host_ids = [attend.user_id for attend in act_host]  
        
        return host_ids
        