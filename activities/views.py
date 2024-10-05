"""Views for activities app, handle html request."""
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django import urls
from django.utils import timezone
from django import db
from django.contrib import messages
from . import models
from django.views import generic
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt


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

    def render_to_response(self, context, **response_kwargs) -> JsonResponse:
        """Send out JSON response to Vue"""
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

    def render_to_response(self, context, **response_kwargs) -> JsonResponse:
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


def csrf_token_view(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return csrf token"""
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
