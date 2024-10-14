"""Module for serializing data before respond a request."""

from rest_framework import serializers
from . import models


class ActivitiesSerializer(serializers.ModelSerializer):
    """Serialized activity."""

    people = serializers.IntegerField()

    class Meta:
        model = models.Activity
        fields = ('__all__')
