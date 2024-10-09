"""Custom decorator for activities app."""

from django.http import HttpRequest, JsonResponse
from typing import Callable


def login_required(func: Callable) -> Callable:
    """Return a wrapper function that make function return error Json when user doesn't login."""

    def wrapper(request: HttpRequest) -> JsonResponse:
        """If user already login just invoke request handler func."""
        if request.user.is_authenticated:
            return func
        return JsonResponse(
            {
                'error': 'User must authenticated before perform this action'
            },
            status=401
        )

    return wrapper
