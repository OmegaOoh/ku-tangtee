"""Views for activities app, handle html request."""
import json
from typing import Dict, Any
from datetime import datetime
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django import db
from . import models, utils
from django.views import generic
from django.middleware.csrf import get_token
from activities.decorator import login_required
from django.views.decorators.http import require_POST
from django.db.models import F, ExpressionWrapper, IntegerField
from typing import Callable
from rest_framework import mixins
from rest_framework import generics
from . import serializers


# class IndexView(generic.ListView):
#     """View class to show all upcoming activities."""

#     model = models.Activity
#     template_name = "activities/index.html"
#     context_object_name = "activities"

#     def get_queryset(self) -> db.models.QuerySet:
#         """
#         Return Queryset of activities that is not took place yet.

#         Queryset is order by date that the activity took place.(earlier to later)
#         """
#         query = models.Activity.objects.filter(date__gte=timezone.now()).order_by("date")

#         return query

#     def render_to_response(self, context: Dict[str, Any], **response_kwargs: Any) -> JsonResponse:
#         """Send out JSON response to Vue for Activity Index."""
#         activities = list(self.get_queryset().values(
#             "id", "name", "detail", "date", "max_people"
#         ))

#         activities = [act | {"people": get_number_of_people(act["id"])} for act in activities]
#         return JsonResponse(activities, safe=False)


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


# @require_POST
# @login_required
# def create(request: HttpRequest) -> JsonResponse:
#     """Handle request to create an activity."""
#     # Get activity data from POST request
#     data = json.loads(request.body.decode('utf-8'))
#     print(data)
#     name = data.get("name")
#     detail = data.get("detail")
#     date_string = data.get("date")
#     max_people = data.get("max_people")

#     try:

#         # Create new activities with provide name and detail
#         new_act = models.Activity.objects.create(
#             name=name,
#             detail=detail,
#         )

#         # If user has set the date use, set activity date.
#         if date_string:
#             date = timezone.make_aware(datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ"))
#             new_act.date = date

#         # If user has set the max people, set activity max_people.
#         if max_people:
#             new_act.max_people = max_people

#         new_act.save()

#         attend = new_act.attend_set.create(
#             user=request.user,
#             is_host=True
#         )

#         attend.save()

#         # Return successful message
#         # TODO Log warning when logging already setup
#         return JsonResponse(
#             {
#                 "message": f"Your have successfully create activity {new_act.name}",
#                 "id": new_act.id
#             }
#         )

#     except (db.utils.DataError, db.utils.IntegrityError, ValueError, TypeError) as e:

#         # If any error occur, return an error message.
#         return JsonResponse(
#             {
#                 "error": f"Error occur : {e}"
#             },
#             status=400
#         )


def edit_activity(request: HttpRequest, activity_id: int) -> JsonResponse:
    """Handle request to edit an activity."""
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

        # Get activity with provided id
        modified_activity = get_object_or_404(models.Activity, pk=activity_id)

        # If user has set the date use, set activity date.
        if date_string:
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
            # Get the timezone offset
            aware_date = timezone.make_aware(date)
            modified_activity.date = aware_date

        modified_activity.name = name
        modified_activity.detail = detail
        modified_activity.max_people = max_people

        modified_activity.save()

        # Return successful message
        # TODO Log warning when logging already setup
        return JsonResponse(
            {
                "message": f"Your have successfully edit activity {modified_activity.name}",
                "id": modified_activity.id,
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


def get_timezone(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return time zone offset to vue."""
    tzo = utils.get_time_zone_offset()
    return JsonResponse({'offset': tzo})
