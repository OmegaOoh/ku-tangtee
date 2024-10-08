"""Views for activities app, handle html request."""
from datetime import datetime
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django import db
from . import models
from django.views import generic
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from typing import Dict, Any
import json


class IndexView(generic.ListView):
    """View class to show all upcoming activities."""

    model = models.Activity
    template_name = "activities/index.html"
    context_object_name = "activities"

    def get_queryset(self) -> db.models.QuerySet:
        """
        Return Queryset of activities that is not took place yet.

        Queryset is order by date that the activity took place.(earlier to later)
        """
        return models.Activity.objects.filter(date__gte=timezone.now()).order_by("date")

    def render_to_response(self, context: Dict[str, Any], **response_kwargs: Any) -> JsonResponse:
        """Send out JSON response to Vue for Activity Index."""
        activities = list(self.get_queryset().values(
            "id", "name", "detail", "date", "max_people", "people"))
        return JsonResponse(activities, safe=False)


class ActivityDetailView(generic.DetailView):
    """View class to show activity information."""

    model = models.Activity
    template_name = "activities/detail.html"

    def get_queryset(self) -> db.models.QuerySet:
        """
        Return Queryset of activities that is not took place yet.

        Queryset is order by date that the activity took place.(ealier to later)
        """
        return models.Activity.objects.filter(date__gte=timezone.now())

    def render_to_response(self, context: Dict[str, Any], **response_kwargs: Any) -> JsonResponse:
        """Send out JSON Response to Vue for Activity Detail."""
        activity = self.get_object()
        data = {
            "id": activity.id,
            "name": activity.name,
            "detail": activity.detail,
            "date": activity.date,
            "max_people": activity.max_people,
            "people": activity.people,
            "can_join": activity.can_join(),
        }
        return JsonResponse(data)


@csrf_exempt
def join(request: HttpRequest, activity_id: int) -> JsonResponse:
    """Increase number of people when user join an activity."""
    activity = get_object_or_404(models.Activity, pk=activity_id)
    if activity.can_join():
        activity.people = db.models.F('people') + 1
        activity.save(update_fields=['people'])
        return JsonResponse({"message": f"You successfully joined {activity.name}"})
    else:
        return JsonResponse({"error": f"{activity.name} is not joinable"}, status=400)
    # return redirect(urls.reverse("activities:detail", args=[activity_id]))
    # Implement redirection in Vue methods


@csrf_exempt
def create(request: HttpRequest) -> JsonResponse:
    """Handle request to create an activity."""
    # Check request type
    if request.method != "POST":
        return JsonResponse({"error": "Forbidden access"}, status=403)
    # Get activity data from POST request
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    name = data.get("name")
    detail = data.get("detail")
    date_string = data.get("date")
    max_people = data.get("max_people")

    try:

        # Create new activities with provide name and detail
        new_act = models.Activity.objects.create(
            name=name,
            detail=detail,
        )

        # If user has set the date use, set activity date.
        if date_string:
            date = timezone.make_aware(datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ"))
            new_act.date = date

        # If user has set the max people, set activity max_people.
        if max_people:
            new_act.max_people = max_people

        new_act.people = 1

        new_act.save()

        # Return successful message
        # TODO Log warning when logging already setup
        return JsonResponse(
            {
                "message": f"Your have successfully create activity {new_act.name}",
                "id": new_act.id
            }
        )

    except (db.utils.DataError, db.utils.IntegrityError, ValueError, TypeError) as e:

        # If any error occur, return an error message.
        return JsonResponse(
            {"error": f"Error occur : {e}"},
            status=400
        )


def csrf_token_view(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return csrf token."""
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
