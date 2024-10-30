"""Module for serializing data before respond a request."""
from typing import Any
from rest_framework import serializers, exceptions
from .. import models


class ProfilesSerializer(serializers.ModelSerializer):
    """Serialized profile."""

    faculty = serializers.ReadOnlyField()
    major = serializers.ReadOnlyField()

    class Meta:
        """Profile serializer META class."""

        model = models.Profile
        fields = ('__all__')

    def get_profile(self, user_id: int) -> Any:
        """Return attend object specify by user_id.

        :param user_id: ID of user model instance
        :raises exceptions.APIException: if Profile object with specify id not exist.
        :return: None
        """
        try:
            return models.Profile.objects.get(
                user__id=user_id
            )
        except models.Profile.DoesNotExist:
            raise exceptions.APIException("You've never created your profile")
