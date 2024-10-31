"""Shortcut module contains many functions for convenient."""
import requests
import base64
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


def image_loader_64(image_data_list: list[str], new_msg: models.Message):
    """Create attachments and save for a message from base64-encoded images."""
    for image_data in image_data_list[:5]:
        try:
            # Separate the base64 header if it exists
            if "base64," in image_data:
                image_data = image_data.split("base64,")[1]
 
            # Decode the base64 string into binary data
            image_content = base64.b64decode(image_data)

            # Generate a unique name for the file, for example by using the message ID
            file_name = f"{new_msg.id}_attachment_{len(image_data_list)}.jpg"  # Adjust extension if needed

            # Create ContentFile and save the attachment
            image_file = ContentFile(image_content, name=file_name)
            models.Attachment.objects.create(message=new_msg, image=image_file)

        except (base64.binascii.Error, ValueError) as e:
            print(f"Failed to decode image data: {e}")
