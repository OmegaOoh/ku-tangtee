import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels import exceptions
from asgiref.sync import sync_to_async  # Correct import for sync_to_async
from activities import models as act_models
from . import models as chat_models


class ChatConsumer(AsyncWebsocketConsumer):
    """Consumer app for Chat application."""

    async def connect(self):
        """Connect user to websocket, verify user auth and activity_id."""
        activity_id = self.scope['url_route']['kwargs']['activity_id']
        self.room_group_name = f"activity{activity_id}"
        self.user = self.scope['user']

        # Check the activity
        try:
            self.activity = await sync_to_async(act_models.Activity.objects.get)(pk=activity_id)
        except act_models.Activity.DoesNotExist:
            print("no activity")
            raise exceptions.DenyConnection("There is no activity with this id")

        # Check the user
        if (not self.user.is_authenticated):
            print("not authenticate")
            raise exceptions.DenyConnection("Please Login before moving on.")
        try:
            await sync_to_async(self.activity.attend_set.get)(user=self.user)
        except act_models.Attend.DoesNotExist:
            print("not attend")
            raise exceptions.DenyConnection("You does not attend to this activity.")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Disconnect user from websocket"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        """Handle message receive on server side"""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to the group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "sendMessage",
                "message": message,
            }
        )
        # Verify user and activity
        if self.user != self.scope['user'] or self.activity.id != self.scope['url_route']['kwargs']['activity_id']:
            raise self.disconnect(4000)  # User does not the same.
        new_message = chat_models.Message(message=message, sender=self.user, activity=self.activity)
        await sync_to_async(new_message.save)()

    async def sendMessage(self, event):
        """Sent message to websocket"""
        await self.send(text_data=json.dumps({
            "message": event["message"],
        }))
