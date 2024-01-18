import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from user.models import ChatGroup, Chat, User
from user.utils import group_name


class ChatManagement(AsyncWebsocketConsumer):

    @sync_to_async
    def save_group_and_chat(self, chat_group_name, message, sender):
        instance, group = ChatGroup.objects.get_or_create(name=chat_group_name)
        sender = User.objects.get(id=int(sender))
        return Chat.objects.create(message=message,group=instance,sender=sender)
    @sync_to_async
    def save_files(self, chat_group_name, files, sender):
        instance, group = ChatGroup.objects.get_or_create(name=chat_group_name)
        sender = User.objects.get(id=int(sender))
        return Chat.objects.create(images=files, group=instance, sender=sender)

    async def connect(self):
        self.room_group_name = group_name(self.scope['user'].id,self.scope["url_route"]["kwargs"]["id"])
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = text_data_json["user"]
        if "message" in text_data_json.keys():
            message = text_data_json["message"]
            await self.save_group_and_chat(self.room_group_name,message,user)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message, "user":user}
            )
        else:
            document_len = text_data_json["document_len"]
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "document_len": document_len, "user": user}
            )

    @sync_to_async
    def get_attachment(self, user, count):
        from .models import Chat
        url_list = []
        images = Chat.objects.filter(sender__id=user).order_by('-id')[:count]
        for img in images:
            url_list.append(img.images.url)
        return url_list

    async def chat_message(self, event):
        user = event["user"]
        if "message" in event.keys():
            message = event["message"]
            if self.scope['user'].id == user:
                user = True
            await self.send(text_data=json.dumps({"message": message, "sender":user}))
        elif event['document_len']:
            document_len = event["document_len"]
            files_url = await self.get_attachment(user, document_len)
            if self.scope['user'].id == user:
                user = True
            await self.send(text_data=json.dumps({"files": files_url, "sender":user}))
            # else:
            #     files = event["files"]
            #     if self.scope['user'].id == user:
            #         user = True
            #     await self.send(text_data=json.dumps({"message": files, "sender": user}))



    # async def send_documents(self, event):
    #     breakpoint()
    #     user = event["user"]
    #     document_len = event["document_len"]
    #     await self.get_attachment(user,document_len)
    #     # await self.send(text_data=json.dumps({"files": files, "sender": user}))


class UpdateStatus(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "checkStatus"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message"}
        )

    async def chat_message(self, event):
        status = event["status"]
        id = event["id"]
        await self.send(text_data=json.dumps({"status": status,"id":id}))


