"""Views for activities app, handle html request."""
from django.http import HttpRequest
from allauth.socialaccount.models import SocialAccount
from .settings import OAUTH_PROVIDER
from rest_framework import decorators, response


@decorators.api_view(["GET"])
def profile_picture_view(request: HttpRequest) -> response.Response:  # pragma: no cover
    """Return profile picture url from Google account."""
    user = request.user
    try:
        social_account = SocialAccount.objects.get(user=user, provider=OAUTH_PROVIDER)
        profile_picture_url = social_account.extra_data.get('picture', '')
        return response.Response({"profile_picture_url": profile_picture_url})
    except SocialAccount.DoesNotExist:
        return response.Response({"error": "Google account not found for user"}, status=404)
    
