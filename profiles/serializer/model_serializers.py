"""Module for serializing data before respond a request."""
from rest_framework import serializers
from .. import models
from django.contrib.auth import models as auth_models


class UserSerializer(serializers.ModelSerializer):
    """Serialized Django User Model."""

    class Meta:
        """User serializer META class."""
        user = auth_models.User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfilesSerializer(serializers.ModelSerializer):
    """Serialized Profile model."""
    user = UserSerializer(read_only=True)

    class Meta:
        """Profile serializer META class."""

        model = models.Profile
        fields = ('__all__')
