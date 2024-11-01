"""Utility module."""
import requests
import base64
from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from django.core.files.base import ContentFile
from activities import models
from rest_framework import decorators, response
from rest_framework.permissions import IsAuthenticated


@decorators.api_view(['get'])
def csrf_token_view(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return csrf token."""
    csrf_token = get_token(request)
    return response.Response({'csrfToken': csrf_token})


@decorators.api_view(['get'])
@decorators.permission_classes([IsAuthenticated])
def get_recent_activity(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return recently joined activities.

    :param request: Http request object
    :return: Response object contain activities that recently joined.
    """
    user = request.user
    activities = models.Attend.recently_joined(user)
    recent_activities = [{"name": activity.name, "activity_id": activity.id} for activity in activities]
    return response.Response(recent_activities)


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
        except requests.exceptions.RequestException as e:
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
            file_name = f"{act.id}_attachment_{len(image_data_list)}.jpg"

            # Create ContentFile and save the attachment
            image_file = ContentFile(image_content, name=file_name)
            models.Attachment.objects.create(activity=act, image=image_file)

        except Exception as e:
            print(f"Failed to decode image data: {e}")
