"""Views for activities app, handle html request."""
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from .settings import OAUTH_PROVIDER


def profile_picture_view(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return profile picture url from Google account."""
    user = request.user
    if request.method == 'GET':
        try:
            social_account = SocialAccount.objects.get(user=user, provider=OAUTH_PROVIDER)
            profile_picture_url = social_account.extra_data.get('picture', '')
            return JsonResponse({"profile_picture_url": profile_picture_url})
        except SocialAccount.DoesNotExist:
            return JsonResponse({"error": "Google account not found for user"}, status=404)
