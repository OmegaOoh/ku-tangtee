"""Module for serializing data before respond a request."""
from typing import Any
from rest_framework import serializers, exceptions
from .. import models
from . import custom_validator
from auth import serializer


class ParticipantSerializer(serializers.ModelSerializer):
    """Serialize participant detail."""

    participant = serializer.UserSerializer(source='user')

    class Meta:
        """ParticipantSerializer Meta class."""

        model = models.Attend
        fields = ('participant', 'is_host')


class ActivitiesSerializer(serializers.ModelSerializer):
    """Serialized activity."""

    people = serializers.ReadOnlyField()
    can_join = serializers.ReadOnlyField()
    host = serializers.SerializerMethodField()
    participant = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        """Activity serializer META class."""

        model = models.Activity
        fields = ('__all__')

    def get_host(self, activity: models.Activity) -> list[Any]:
        """Return list of activity host.

        :param obj: Instance of activity model
        :return: List of activity host id
        """
        act_host = models.Attend.objects.filter(activity=activity, is_host=True)
        host_ids = [attend.user_id for attend in act_host]

        return host_ids

    def get_participant(self, activity: models.Activity) -> list[Any]:
        """Return list of serialized activity participant.

        :param obj: Activity model instance.
        :return: List of serialized participant detail
        """
        attend = activity.attend_set.all()
        participants = ParticipantSerializer(attend, many=True).data
        result = []

        for participant in participants:
            participant['participant']['is_host'] = participant.get('is_host')
            result.append(participant['participant'])

        return result
    
    def get_images(self, activity: models.Activity) -> list[Any]:
        """Return activity images.

        :param obj: Activity model instance.
        :return: List of serialized images.
        """
        act_images = models.Attachment.objects.filter(activity=activity)
        images = [img.image.url for img in act_images]
        return images


class AttendSerializer(serializers.ModelSerializer):
    """Serialized Attend."""

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
