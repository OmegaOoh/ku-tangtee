"""Module contain serializer class relate to User model."""
from rest_framework import serializers
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


class UserSerializer(serializers.ModelSerializer):
    """Serialized User data."""

    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        """User serailizer Meta class."""

        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture_url')

    def get_profile_picture_url(self, user: User) -> str:
        """Get profile picture from provided user.

        :param obj: User model instance
        :return: String of user profile URL or empty string if user doesn't have social account.
        """
        try:
            social_account = SocialAccount.objects.get(user=user)
            profile_picture_url: str = social_account.extra_data.get('picture', '')
            return profile_picture_url
        except SocialAccount.DoesNotExist:
            return ""
