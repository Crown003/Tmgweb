# api frontend websocket.
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"notification_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    async def send_notification(self, event):
        message = json.loads(event["message"])

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket connected...", event)
        await self.send(
            {
                "type": "websocket.accept",
            }
        )

    async def send_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))
        # for i in range(10):
        #     await self.send(
        #         {
        #             "type": "websocket.send",
        #             "text": str(i),
        #         }
        #     )
        #     await asyncio.sleep(1)

    async def websocket_disconnect(self, event):
        print("Websocket disconnected...")
        raise StopConsumer()
