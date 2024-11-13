"""Module for serializing data before respond a request."""
from typing import Any
from rest_framework import serializers
from allauth.socialaccount.models import SocialAccount
from .. import models
from django.contrib.auth import models as auth_models


class UserSerializer(serializers.ModelSerializer):
    """Serialized Django User Model."""

    class Meta:
        """User serializer META class."""

        model = auth_models.User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ProfilesSerializer(serializers.ModelSerializer):
    """Serialized Profile model."""

    user = UserSerializer(read_only=True)
    profile_picture_url = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    join_limit = serializers.IntegerField(read_only=True)
    active_activity_count = serializers.IntegerField(read_only=True)

    class Meta:
        """Profile serializer META class."""

        model = models.Profile
        fields = ("__all__")

    def create(self, validated_data: Any) -> Any:
        """Create user profile and popped user id from data.

        :param validated_data: full data to use to create the profile
        """
        user = self.context['request'].user
        profile = models.Profile.objects.create(user_id=user.id, **validated_data)
        return profile

    def get_profile_picture_url(self, obj: Any) -> Any:
        """Get user profile picture to use as serializer fields.

        :param obj: object to get the data from
        :return: profile picture url
        """
        # Call the get_profile_picture method with the user from the profile
        try:
            social_account = SocialAccount.objects.get(user=obj.user)
            return social_account.extra_data.get('picture', '')
        except SocialAccount.DoesNotExist:
            return ''
