"""Module for serializing data before respond a request."""
from typing import Any

from rest_framework import serializers, validators
from . import models


class ActivitiesSerializer(serializers.ModelSerializer):
    """Serialized activity."""

    people = serializers.ReadOnlyField()
    can_join = serializers.ReadOnlyField()
    host = serializers.SerializerMethodField()

    class Meta:
        """Activity serializer META class."""

        model = models.Activity
        fields = ('__all__')

    def get_host(self, obj: models.Activity) -> list[Any]:
        """Return list of activity host."""
        act_host = models.Attend.objects.filter(activity=obj, is_host=True)
        host_ids = [attend.user_id for attend in act_host]

        return host_ids


class AttendSerializer(serializers.ModelSerializer):
    """Serialized Attend"""
    
    class Meta:
        """Attend serializer META class."""
        
        model = models.Attend
        fields = ('__all__')
        
        validators = [
            validators.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['user', 'activity']
            )
        ]