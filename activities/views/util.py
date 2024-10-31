"""Utility module."""
import requests
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


def image_loader(image_urls: list[str], new_act: models.Activity):
    """Saving attachments for activity"""
    for url in image_urls[:10]:
        try:
            img_response = requests.get(url)
            img_response.raise_for_status()

            # Extract the image name and create ContentFile for attachment
            file_name = url.split("/")[-1]
            image_content = ContentFile(img_response.content, name=file_name)
            models.Attachment.objects.create(activity=new_act, image=image_content)
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image from {url}: {e}")


def image_deleter(image_ids: list[int]):
    """Delete attachments for all given ids."""
    for attachment_id in image_ids:
        attachment = models.Attachment.objects.filter(pk=attachment_id).first()
        if attachment:
            attachment.image.delete(save=False)
            attachment.delete()
