"""Module for serializing data before respond a request."""
from typing import Any
from rest_framework import serializers, validators, exceptions, status
from . import models


class ForbiddenValidationError(exceptions.APIException):
    """Custom error inherit from ValidationError but different error code."""

    status_code = status.HTTP_403_FORBIDDEN


class CanJoinValidator:
    """Validate activity joinability."""

    def __call__(
        self,
        attrs: dict[str, models.Activity],
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Raise an error if actican't join."""
        act: models.Activity = attrs['activity']

        if act:
            if not act.can_join():
                message = f'The activity {act.name} is full.'
                raise ForbiddenValidationError(message)

        return None


class CustomMsgUniqueTogetherValidator(validators.UniqueTogetherValidator):
    """Custom validator class base from UniqueTogetherValidator."""

    status_code = status.HTTP_403_FORBIDDEN

    def __call__(self, attrs: dict[str, Any], serializer: serializers.Serializer) -> Any:
        """Make object callable."""
        try:
            return super().__call__(attrs, serializer)
        except validators.ValidationError:
            raise ForbiddenValidationError(
                {
                    "message": f"You've already joined the activity {attrs['activity'].name}."
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
            CanJoinValidator()
        ]

    def get_attend(self, activity_id: int, user_id: int) -> Any:
        """Return attend object specify by activity_id and user_id."""
        try:
            return models.Attend.objects.get(
                activity__id=activity_id,
                user__id=user_id
            )
        except models.Attend.DoesNotExist:
            raise exceptions.APIException("You've never join this activity")
