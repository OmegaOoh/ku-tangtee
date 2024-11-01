"""Module for serializing data before respond a request."""
from rest_framework import serializers
from .. import models


class ProfilesSerializer(serializers.ModelSerializer):
    """Serialized Profile model."""

    class Meta:
        """Profile serializer META class."""

        model = models.Profile
        fields = ('__all__')
