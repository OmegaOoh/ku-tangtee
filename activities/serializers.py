"""Module for serializing data before respond a request."""
from typing import Any

from rest_framework import serializers, validators
from . import models

def can_join_validator(attrs, *args, **kwargs) -> serializers.ValidationError | None:
    act = attrs.get('activity')

    if not act.can_join():
        message = f'The activity {act.name} is full.'
        raise serializers.ValidationError(message)
   
    
class CustomMsgUniqueTogetherValidator(validators.UniqueTogetherValidator):
    
    def __call__(self, attrs, serializer):
        self.enforce_required_fields(attrs, serializer)
        queryset = self.queryset
        queryset = self.filter_queryset(attrs, queryset, serializer)
        queryset = self.exclude_current_instance(attrs, queryset, serializer.instance)

        # Ignore validation if any field is None
        if serializer.instance is None:
            checked_values = [
                value for field, value in attrs.items() if field in self.fields
            ]
        else:
            # Ignore validation if all field values are unchanged
            checked_values = [
                value
                for field, value in attrs.items()
                if field in self.fields and value != getattr(serializer.instance, field)
            ]

        if checked_values and None not in checked_values and validators.qs_exists(queryset):
            raise validators.ValidationError({"message": f"You've already joined the activity {attrs.get('activity').name}."}, code='unique')


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
            CustomMsgUniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['user', 'activity']
            ),
            can_join_validator
        ]

