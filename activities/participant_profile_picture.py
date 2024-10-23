"""Module for handle participant detail."""
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from typing import Dict


def retrive_profile_picture(user: User) -> Dict[str, str]:  # pragma: no cover
    """Return profile picture url from Google account and also return his name."""
    try:
        social_account = SocialAccount.objects.get(user=user)
        profile_picture_url = social_account.extra_data.get('picture', '')
        return {"profile_picture_url": profile_picture_url,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "id": user.id}
    except SocialAccount.DoesNotExist:
        return {"error": "Google account not found for user"}
