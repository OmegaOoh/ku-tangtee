"""Module for serializing data before respond a request."""
from typing import Any
from rest_framework import serializers, exceptions
from .. import models


class ProfilesSerializer(serializers.ModelSerializer):
    """Serialized profile."""

    class Meta:
        """Profile serializer META class."""

        model = models.Profile
        fields = ('__all__')
