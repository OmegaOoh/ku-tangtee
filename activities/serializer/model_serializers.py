"""Module for serializing data before respond a request."""
from typing import Any
from rest_framework import serializers, exceptions
from .. import models
from . import custom_validator
from auth import serializer


class ParticipantDetailSerializer(serializers.ModelSerializer):
    """Serialize participant detail for combine with activity detail."""

    user = serializer.UserSerializer()

    class Meta:
        """ParticipantSerializer Meta class."""

        model = models.Attend
        fields = ('user', 'is_host', 'checked_in')


class ActivitiesSerializer(serializers.ModelSerializer):
    """Serialized Activity and created activity from validated data."""

    people = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    host = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        """Activity serializer META class."""

        model = models.Activity
        fields = ('__all__')

    def get_fields(self) -> Any:
        """Modify get fields to exclude check-in code."""
        fields = super().get_fields()
        fields.pop("check_in_code")

        return fields

    def create(self, validated_data: dict[str, Any]) -> models.Activity:
        """Override create function to prevent pre-created check-in code.

        :param validated_data: Data that got validated,
        :return: _description_
        """
        # Prevent user to pre-created check-in code.
        validated_data.pop('check_in_allowed', None)
        validated_data.pop('check_in_code', None)

        result: models.Activity = super().create(validated_data)
        return result

    def get_host(self, activity: models.Activity) -> list[Any]:
        """Return list of activity host.

        :param obj: Instance of activity model
        :return: List of activity host id
        """
        act_host = models.Attend.objects.filter(activity=activity, is_host=True)
        host_ids = [attend.user_id for attend in act_host]

        return host_ids

    def get_images(self, activity: models.Activity) -> list[Any]:
        """Return activity images.

        :param obj: Activity model instance.
        :return: List of serialized images.
        """
        act_images = models.Attachment.objects.filter(activity=activity)
        images = [{"id": img.id, "url": img.image.url} for img in act_images]
        return images


class AttendSerializer(serializers.ModelSerializer):
    """Validated data and create attend model instance from it."""

    class Meta:
        """Attend serializer META class."""

        model = models.Attend
        fields = ('__all__')

        validators = [
            custom_validator.CustomMsgUniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['user', 'activity']
            ),
            custom_validator.CanJoinValidator()
        ]

    def get_attend(self, activity_id: int, user_id: int) -> Any:
        """Return attend object specify by activity_id and user_id.

        :param activity_id: Id of activity model instance
        :param user_id: Id of user model instance
        :raises exceptions.APIException: if Attend object with specify id not exist.
        :return: None
        """
        try:
            return models.Attend.objects.get(
                activity__id=activity_id,
                user__id=user_id
            )
        except models.Attend.DoesNotExist:
            raise exceptions.APIException("You've never join this activity")
