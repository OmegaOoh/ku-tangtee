"""Custom decorator for activities app."""

from django.http import HttpRequest, JsonResponse
from typing import Callable, Any, Optional


def login_required(func: Callable[..., None]) -> Callable[..., None]:
    """Return a wrapper function that make function return error Json when user doesn't login."""

    def wrapper(request: HttpRequest, *args: tuple[Any], **kwargs: Optional[str]) -> JsonResponse:
        """If user already login just invoke request handler func."""
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return JsonResponse(
            {
                'error': 'User must authenticated before perform this action'
            },
            status=401
        )

    return wrapper
