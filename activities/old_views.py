"""Views for activities app, handle html request."""
import json
from typing import Any
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from activities.decorator import login_required
from django.views.decorators.http import require_POST
from . import models


@require_POST
@login_required
def join(request: HttpRequest, activity_id: int) -> JsonResponse:
    """Add record to attend table and return success message when action success."""
    activity = get_object_or_404(models.Activity, pk=activity_id)

    if activity.attend_set.filter(user=request.user, activity=activity).exists():
        return JsonResponse({"error": f"You've already joined {activity.name}"}, status=400)

    if activity.can_join():
        attend = activity.attend_set.create(
            user=request.user,
        )
        attend.save()
        return JsonResponse({"message": f"You successfully joined {activity.name}"})
    else:
        return JsonResponse({"error": f"{activity.name} is not joinable"}, status=400)

    # Implement redirection in Vue methods
