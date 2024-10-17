"""Module for serializing data before respond a request."""
from typing import Any

from rest_framework import serializers
from . import models


class ActivitiesSerializer(serializers.ModelSerializer):
    """Serialized activity."""

    people = serializers.ReadOnlyField()
    host = serializers.SerializerMethodField()

    class Meta:
        model = models.Activity
        fields = ('__all__')

    def get_host(self, obj: models.Activity) -> list[Any]:

        act_host = models.Attend.objects.filter(activity=obj, is_host=True)
        host_ids = [attend.user_id for attend in act_host]

        return host_ids
