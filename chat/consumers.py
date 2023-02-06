import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        print("scope ==", self.scope)
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("text_data_json ==", text_data_json)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        print("event==", event)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat{self.room_name}'

#         # join room group
#         await self.channel_layer.group_add(self.room_group_name, self.room_name)

#         await self.accept()

#     async def disconnect(self, close_code):

#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     # receive message from group

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # send message to room group
#         await self.channel_layer.group_send(self.room_group_name, {"type": "caht_message", "message": message})

#     # receive message from room group

#     async def chat_message(self, event):
#         message = event['message']

#         # send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))
# # class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat{self.room_name}'

#         # join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )

#         self.accept()

#     def disconnect(self):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     # receive messages from websocket
#     def receive(self, text_data):
#         tex_data_json = json.loads(text_data)
#         print(tex_data_json)
#         message = tex_data_json['message']
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )
#         # self.send(text_data=json.dumps({'message': message + ' fuck you'}))

#     # receive message from caht group
#     def chat_message(self, event):
#         message = event['message']

#         # send message to websocket
#         self.send(text_data=json.dumps({"message": message}))
