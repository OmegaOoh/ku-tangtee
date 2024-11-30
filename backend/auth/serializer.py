"""Module contain serializer class relate to User model."""
from typing import Any

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from profiles.models import Profile
from profiles.serializer.model_serializers import ProfilesSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serialized User data."""

    user_profile = serializers.SerializerMethodField()

    class Meta:
        """User serailizer Meta class."""

        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'user_profile')

    def get_user_profile(self, user: User) -> Any:
        """Get user profile."""
        try:
            profile = Profile.objects.get(user=user)
            return ProfilesSerializer(instance=profile).data
        except Profile.DoesNotExist:
            return ""
