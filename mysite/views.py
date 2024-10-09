"""Views for activities app, handle html request."""
from django.http import HttpRequest, JsonResponse


def is_authen(request: HttpRequest) -> JsonResponse:
    """Return Json which inform that user is login right now."""
    print(request.user.is_authenticated)
    return JsonResponse({"is_authen": request.user.is_authenticated})
