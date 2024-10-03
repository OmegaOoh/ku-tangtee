"""Views for activities app, handle html request."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django import urls
from django.utils import timezone
from django import db
from django.contrib import messages
from . import models
from django.views import generic

class IndexView(generic.ListView):
    """View class to show all upcoming activities."""

    model = models.Activity
    template_name = "activities/index.html"
    context_object_name = "activities"

    def get_queryset(self) -> db.models.QuerySet:
        """
        Return Queryset of activities that is not took place yet.

        Queryset is order by date that the activity took place.(ealier to later)
        """
        return models.Activity.objects.filter(date__gte=timezone.now()).order_by("date")


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


def join(request: HttpRequest, activity_id: int) -> HttpResponse:
    """Increase number of people when user join an activity."""
    activity = get_object_or_404(models.Activity, pk=activity_id)
    if activity.can_join():
        activity.people = db.models.F('people') + 1
        activity.save(update_fields=['people'])
        messages.success(request, f"you successfully join {activity.name}")
    else:
        messages.error(request, f"{activity_id} is not joinable")
    return redirect(urls.reverse("activities:detail", args=[activity_id]))
