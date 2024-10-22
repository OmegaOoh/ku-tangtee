"""Module for serializing data before respond a request."""
from typing import Any
from rest_framework import serializers, validators, exceptions
from . import models


def can_join_validator(attrs: dict, *args: Any, **kwargs: Any) -> serializers.ValidationError | None:
    """Validate activity joinability."""
    act = attrs.get('activity')

    if not act.can_join():
        message = f'The activity {act.name} is full.'
        raise serializers.ValidationError(message)


class CustomMsgUniqueTogetherValidator(validators.UniqueTogetherValidator):
    """Custom validator class base from UniqueTogetherValidator."""

    def __call__(self, attrs: dict, serializer: serializers.Serializer):
        """Make object callable."""
        try:
            return super().__call__(attrs, serializer)
        except validators.ValidationError:
            raise validators.ValidationError(
                {
                    "message": f"You've already joined the activity {attrs.get('activity').name}."
                },
                code='unique'
            )


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
    """Serialized Attend."""

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

    def get_attend(self, activity_id, user_id) -> models.Attend:
        """Return attend object specify by activity_id and user_id."""
        try:
            return models.Attend.objects.get(
                activity__id=activity_id,
                user__id=user_id
            )
        except models.Attend.DoesNotExist:
            raise exceptions.APIException("You've never join this activity")
