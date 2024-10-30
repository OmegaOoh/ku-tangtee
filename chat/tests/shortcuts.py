"""Shortcut module contains many functions for convenient."""
import requests
from chat import models
from django.core.files.base import ContentFile


def image_loader(image_urls: list[str], new_msg: models.Message):
    """Create attachments and save for message."""
    for url in image_urls[:5]:
        try:
            img_response = requests.get(url)
            img_response.raise_for_status()

            # Extract the image name and create ContentFile for attachment
            file_name = url.split("/")[-1]
            image_content = ContentFile(img_response.content, name=file_name)
            models.Attachment.objects.create(message=new_msg, image=image_content)
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image from {url}: {e}")
