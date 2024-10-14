"""Views for activities app, handle html request."""
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

def is_authen(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return Json which inform that user is login right now."""
    print(request.user.is_authenticated)
    return JsonResponse({"is_authen": request.user.is_authenticated})


def profile_picture_view(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return profile picture url from Google account."""
    user = request.user
    if request.method == 'GET':
        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
            profile_picture_url = social_account.extra_data.get('picture', '')
            return JsonResponse({"profile_picture_url": profile_picture_url})
        except SocialAccount.DoesNotExist:
            return JsonResponse({"error": "Google account not found for user"}, status=404)
