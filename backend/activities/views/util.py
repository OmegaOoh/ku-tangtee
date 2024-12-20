"""Utility module."""
import base64
import uuid
from typing import Any

import requests
from activities import models
from activities.logger import Action, RequestData, data_to_log, logger
from django.contrib.auth import models as auth_models
from django.core.files.base import ContentFile
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from rest_framework import decorators, response

CHECKIN_CODE_LEN = 6


@decorators.api_view(['get'])
def check_user_status(request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
    """Return user status on give activity.

    :param request: HttpRequest object.
    :return: Json file with a key "is-joined" and boolean value
            which tell does user participant in activity or not
            also with key "is_checked_in" which tell does user
            already checked-in or not
    """
    if not request.user.is_authenticated:
        return response.Response(
            {
                'is_joined': False,
                'is_checked_in': False
            }
        )

    activity = get_object_or_404(models.Activity, id=kwargs.get('id'))

    return response.Response(
        activity.user_status(request.user)
    )


@decorators.api_view(['get'])
def csrf_token_view(request: HttpRequest) -> response.Response:  # pragma: no cover
    """Return csrf token."""
    csrf_token = get_token(request)
    return response.Response({'csrfToken': csrf_token})


@decorators.api_view(['get'])
def get_recent_activity(request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
    """Return recently joined activities.

    :param request: Http request object
    :return: Response object contain activities that recently joined.
    """
    user = get_object_or_404(models.User, id=kwargs.get('id'))
    order_by_date = bool(request.GET.get('byDate', False))
    is_host = bool(request.GET.get('isHost', False))  # pragma: no cover
    records = request.GET.get('records', None)
    if (records):
        records = int(records)
    activities = models.Attend.recently_joined(user, records, is_host, order_by_date)
    recent_activities = [{"name": activity.name,
                          "activity_id": activity.id,
                          "activity_date": activity.date} for activity in activities]
    return response.Response(recent_activities)


def edit_host_access(
        user_ids: list[int],
        act: models.Activity,
        request_user: auth_models.User,
        remove: bool = True) -> response.Response | None:
    """Save is_host value according to the given query into the Attend objects.

    :param user_ids: List of user_ids
    :param act: Activity object to query Attend object
    :param request_user: User object to query Attend object
    :param remove: True if granting host access, False if removing host access
    """
    if request_user != act.owner:
        req_data = RequestData(req_user=request_user, act_id=act.id)
        logger.warning(data_to_log(Action.FAIL_EDIT_HOST, req_data, 'Not owner'))
        return response.Response({'message': "You must be the owner of this activity to perform this action."},
                                 status=403)
    for user_id in user_ids:
        user = get_object_or_404(auth_models.User, id=user_id)

        if not act.is_participated(user) and not act.is_hosts(user):
            return response.Response({'message': f'Cannot find user {user.username} in this activity.'}, status=403)

        attend = get_object_or_404(models.Attend, activity=act, user=user)

        if user == act.owner:
            return response.Response({'message': 'Cannot modify access of your own activity.'}, status=403)

        attend.is_host = not remove

        if not remove:
            attend.checked_in = True
        elif not act.check_in_allowed:
            attend.checked_in = False

        attend.save()

        req_data = RequestData(req_user=request_user, act_id=act.id, target_user=user)
        logger.info(data_to_log(Action.EDIT_HOST, req_data, f'is_host={not remove}'))

    return None


def image_loader(image_urls: list[str], act: models.Activity) -> None:
    """Save images into Attachment objects.

    :param image_urls: List of string contains image urls.
    :param act: Activity object for creating Attachment.
    """
    for url in image_urls[:10]:
        try:
            img_response = requests.get(url)
            img_response.raise_for_status()

            # Extract the image name and create ContentFile for attachment
            file_name = url.split("/")[-1]
            image_content = ContentFile(img_response.content, name=file_name)
            models.Attachment.objects.create(activity=act, image=image_content)
        except requests.exceptions.RequestException as e:  # pragma: no cover
            print(f"Failed to download image from {url}: {e}")


def image_deleter(image_ids: list[int]) -> None:
    """Delete images and Attachment objects.

    :param image_ids: List of ids of Attachment object.
    """
    for attachment_id in image_ids:
        attachment = models.Attachment.objects.filter(pk=attachment_id).first()
        if attachment:
            attachment.image.delete(save=False)
            attachment.delete()


def image_loader_64(image_data_list: list[str], act: models.Activity) -> None:
    """Create attachments and save for a message from base64-encoded images.

    :param image_data_list: List of string contains image urls in base64 format.
    :param act: Activity object for creating Attachment.
    """
    for image_data in image_data_list:
        try:
            # Separate the base64 header if it exists
            if "base64," in image_data:
                image_data = image_data.split("base64,")[1]

            # Decode the base64 string into binary data
            image_content = base64.b64decode(image_data)

            # Generate a unique name for the file, for example by using the message ID
            file_name = f"{act.id}_attachment_{uuid.uuid4()}.jpg"

            # Create ContentFile and save the attachment
            image_file = ContentFile(image_content, name=file_name)
            models.Attachment.objects.create(activity=act, image=image_file)

        except Exception as e:  # pragma: no cover
            print(f"Failed to decode image data: {e}")


def create_location(coor: dict[str, float]) -> int | None:
    """Create Location object and set on_site status.

    :param coor: latitude and longitude of the Location
    """
    latitude, longitude = coor['lat'], coor['lon']

    if latitude and longitude:
        location = models.Locations.objects.create(
            latitude=latitude,
            longitude=longitude
        )
        location.save()

        return int(location.id)

    return None
