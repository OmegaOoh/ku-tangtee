"""Module contains websocket consumers implementation."""
import json
from typing import Any, Dict
from channels.generic.websocket import AsyncWebsocketConsumer
from channels import exceptions
from asgiref import sync
from . import models


class IndexPageConsumer(AsyncWebsocketConsumer):
    """Consumer app for Index Page websocket."""

    async def connect(self) -> None:
        """Connect user to websocket."""
        self.room_group_name = "activity_index"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        """Disconnect user from websocket."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data: bytes) -> None:
        """Handle new activity receive on server side."""
        text_data_json = json.loads(text_data)
        activity_id = text_data_json["activity_id"]
        # Validate Activity ids
        if activity_id is not None:
            if not models.Activity.objects.get(pk=activity_id):
                return  # Activity does not valid
        # Send message to the group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "new_act",
            }
        )

    async def new_act(self, event: Dict[str, Any]) -> None:
        """Sent new activity status to websocket."""
        await self.send(text_data=json.dumps({
            "type": "new_act",
            "activity_id": event["activity_id"],
        }))
