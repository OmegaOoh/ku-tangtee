import json
from channels.generic import websocket

class ChatConsumer(websocket.AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = 'activity_chat'
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self , close_code):
        await self.channel.name.group_discard(
            self.roomGroupName ,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
            })

    async def sendMessage(self, request):
        await self.send(text_data=json.dumps({"message": request["message"],
                                              "username": request["username"]}))
