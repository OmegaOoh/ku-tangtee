"""Module contains websocket consumers implementation."""
import json
import requests
from django.core.files.base import ContentFile
from typing import Any, Dict
from channels.generic.websocket import AsyncWebsocketConsumer
from channels import exceptions
from asgiref import sync
from activities import models as act_models
from . import models as chat_models


class ChatConsumer(AsyncWebsocketConsumer):
    """Consumer app for Chat application."""

    async def connect(self) -> None:
        """Attempt to connect the websocket to the activity.

        :raises exceptions.DenyConnection: Websocket does not connect
        """
        activity_id = self.scope['url_route']['kwargs']['activity_id']
        self.room_group_name = f"activity{activity_id}"
        self.user = self.scope['user']

        # Check the activity
        try:
            self.activity = await sync.sync_to_async(act_models.Activity.objects.get)(pk=activity_id)
        except act_models.Activity.DoesNotExist:
            print("no activity")
            raise exceptions.DenyConnection("There is no activity with this id")

        # Check the user
        if (not self.user.is_authenticated):
            print("not authenticate")
            raise exceptions.DenyConnection("Please Login before moving on.")
        try:
            await sync.sync_to_async(self.activity.attend_set.get)(user=self.user)
        except act_models.Attend.DoesNotExist:
            print("not attend")
            raise exceptions.DenyConnection("You does not attend to this activity.")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        """Disconnect user from the websocket.

        :param close_code: number that indicates the reason of disconnection
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data: bytes) -> None:
        """Handle message receive on server side.

        :param text_data: message data that the sender sends
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        image_urls = text_data_json.get("images", [])

        # Verify user and activity
        if self.user != self.scope['user'] or self.activity.id != self.scope['url_route']['kwargs']['activity_id']:
            await self.disconnect(4000)  # User does not the same.
            return
        new_message = chat_models.Message(message=message, sender=self.user, activity=self.activity)
        await sync.sync_to_async(new_message.save)()

        attachment_urls = []
        # Limit images per message to be 5
        for url in image_urls[:5]:
            try:
                img_response = requests.get(url)
                img_response.raise_for_status()

                file_name = url.split("/")[-1]
                image_content = ContentFile(img_response.content, name=file_name)
                attachment = await sync.sync_to_async(chat_models.Attachment.objects.create)(message=new_message, image=image_content)
                attachment_urls.append(attachment.image.url)
            except requests.exceptions.RequestException as e:
                print(f"Failed to download image from {url}: {e}")

        # Send message to the group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "sendMessage",
                "message": message,
                'user_id': self.scope['user'].id,
                'images': attachment_urls,
            }
        )

    async def sendMessage(self, event: Dict[str, Any]) -> None:
        """Send message to the websocket.

        :param event: the data you want to send to the websocket
        """
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "user_id": event['user_id'],
            "images": event['images'],
        }))
