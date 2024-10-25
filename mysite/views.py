"""Views for activities app, handle html request."""
from django.http import HttpRequest
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from rest_framework import decorators, response


@decorators.api_view(["GET"])
def profile_picture_view(request: HttpRequest) -> response.Response:  # pragma: no cover
    """Return profile picture url from Google account.

    :param request: Http request object
    :return: Response object contain user profile picture or error message.
    """
    user = request.user
    try:
        social_account = SocialAccount.objects.get(user=user)
        profile_picture_url = social_account.extra_data.get('picture', '')
        return response.Response({"profile_picture_url": profile_picture_url, "user_id": user.id})
    except SocialAccount.DoesNotExist:
        return response.Response({"error": "Google account not found for user"}, status=404)

@decorators.api_view(["GET"])
def get_user_data(user_id: int) -> response.Response:  # pragma: no cover
    """Return user data from Google account.

    :param user_id: User id to indicate the user
    :return: Response object contain single user data or error message.
    """
    user = User.object.get(id=user_id)
    try:
        social_account = SocialAccount.objects.get(user=user)
        profile_picture_url = social_account.extra_data.get('picture', '')
        return response.Response({"profile_picture_url": profile_picture_url,
                                   "id": user.id,
                                   "first_name":user.first_name,
                                   "last_name":user.last_name})
    except SocialAccount.DoesNotExist:
        return response.Response({"error": "Google account not found for user"}, status=404)
