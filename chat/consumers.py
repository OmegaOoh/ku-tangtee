import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels import exceptions
from asgiref.sync import sync_to_async  # Correct import for sync_to_async
from activities import models as act_models
from . import models as chat_models


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        activity_id = self.scope['url_route']['kwargs']['activity_id']
        self.room_group_name = f"activity{activity_id}"  # Set room group name based on activity ID

        try:
            # Fetch the activity object asynchronously
            self.activity = await sync_to_async(act_models.Activity.objects.get)(pk=activity_id)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )
            await self.accept()  # Accept the WebSocket connection
        except act_models.Activity.DoesNotExist:
            # There is no activity with this id
            raise exceptions.DenyConnection("There is no activity with this id")

    async def disconnect(self, close_code):
        # Leave the room group on disconnect
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        # Send message to the group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "sendMessage",
                "message": message,
                "username": username,
            }
        )

        # Save the new message asynchronously
        new_message = chat_models.Message(message=message, sender=username, activity=self.activity)
        await sync_to_async(new_message.save)()

    async def sendMessage(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"]
        }))
