"""Module for handle URL /activities."""
import re
from datetime import timedelta
from activities.views.util import image_loader, image_loader_64, create_location
from typing import Any
from django.http import HttpRequest
from django.utils import timezone, dateparse
from django.db.models import Q, QuerySet, ExpressionWrapper, F, DateTimeField
from rest_framework import generics, permissions, mixins, response, status
from activities import models
from activities.logger import logger, Action, RequestData, data_to_log

from activities.serializer import model_serializers


class ActivityList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    """Return list of available upcoming activity when GET request and create new activity when POST request."""

    queryset = models.Activity.objects.filter(is_cancelled=False).order_by("date")
    serializer_class = model_serializers.ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        """Activity index view returns a list of all the activities according to query parameters."""
        queryset = super().get_queryset()

        offset = 0
        if (self.request.headers.get('tzoffset')):
            offset = int(self.request.headers.get('tzoffset'))

        usertz = timedelta(minutes=offset)

        queryset = queryset.filter(end_registration_date__gte=timezone.now())

        keyword = self.request.GET.get("keyword")
        if keyword:
            queryset = queryset.filter(Q(name__iregex=rf'{keyword}') | Q(detail__iregex=rf'{keyword}'))

        queryset = queryset.annotate(
            modified_date=ExpressionWrapper(
                F('date') - usertz,
                output_field=DateTimeField()
            )
        )
        day = self.__parse_date(self.request.GET.get("day"))
        if day:
            queryset = queryset.filter(modified_date__week_day__in=day)

        if self.request.query_params.get("start_date"):
            start_date = dateparse.parse_datetime(self.request.query_params.get("start_date"))
            print('start_date', start_date)
            queryset = queryset.filter(modified_date__gte=start_date)

        if self.request.query_params.get("end_date"):
            end_date = dateparse.parse_datetime(self.request.query_params.get("end_date"))
            end_date = end_date.replace(hour=23, minute=59, second=59)
            queryset = queryset.filter(modified_date__lte=end_date)

        return queryset

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle get request by return with list of activity."""
        return self.list(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Create an activity and add user who create it to attend table.

        :param request: Http request object
        :return: Http response object
        """
        res = self.create(request, *args, **kwargs)

        if res.status_code != status.HTTP_201_CREATED:
            return res

        res_dict = res.data
        new_act = models.Activity.objects.get(pk=res_dict.get("id"))

        self.__load_image(request, new_act)
        self.__add_host(request, new_act)

        req_data = RequestData(req_user=request.user, act_id=new_act.id)
        logger.info(data_to_log(Action.CREATE, req_data))

        return response.Response(
            {
                "message": f"Your have successfully create activity {res_dict.get('name')}",
                "id": res_dict.get("id")
            }
        )

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Create activity instance.

        :param request: Http request object
        :return: Http response object
        """
        user_profile = request.user.profile_set.first()
        req_data = RequestData(req_user=request.user, act_id=-1)

        if not user_profile:
            logger.warning(data_to_log(Action.FAIL_CREATE, req_data, 'No profile'))
            return response.Response(
                {
                    'message': 'User must have profile page before create an activity',
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if user_profile.reputation_score < request.data.get('minimum_reputation_score', 0):
            logger.warning(data_to_log(Action.FAIL_CREATE, req_data, 'Owner rep < Min rep'))
            return response.Response(
                {
                    'message': 'Activity Minimum reputation must less then or equal to creator reputation score'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        request.data["owner"] = request.user.id

        location_id = self.__add_location(request)
        request.data["locations"] = location_id
        if request.data.get('locations', False):
            request.data["on_site"] = True

        return super().create(request, *args, **kwargs)

    def __load_image(self, request: HttpRequest, activity: models.Activity) -> None:
        """Load activity attachment."""
        image_urls = request.data.pop('images', [])
        if image_urls:
            if any("base64" in attachment for attachment in image_urls):
                image_loader_64(image_urls, activity)
            else:
                image_loader(image_urls, activity)

    def __add_host(self, request: HttpRequest, activity: models.Activity) -> None:
        """Add creator as a activity host."""
        request.user.attend_set.create(
            activity=activity,
            is_host=True,
            checked_in=True
        )

    def __add_location(self, request: HttpRequest) -> int | None:
        """Create a location object of the activity."""
        coordinate = request.data.pop('location', {'lat': 0, 'lon': 0})
        return create_location(coordinate)

    def __parse_date(self, date_param: str) -> list[int] | None:

        day_list_format = r'^(?:[1-7](?:,[1-7])*)?$'

        if (not date_param) or (not re.fullmatch(day_list_format, date_param)):
            return None

        split_day = date_param.split(',')

        if len(split_day) > 7:
            return None

        return [int(s.strip()) for s in split_day]
