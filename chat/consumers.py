import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['user']
        self.receiver_id = int(self.scope['url_route']['kwargs']['receiver_id'])

        if not self.sender.is_authenticated:
            await self.close()
            return

        # Create a unique room name based on both user IDs
        ids = sorted([self.sender.id, self.receiver_id])
        self.room_group_name = f"chat_{ids[0]}_{ids[1]}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Load and send chat history
        messages = await self.get_chat_history(self.sender.id, self.receiver_id)
        for msg in messages:
            await self.send(text_data=json.dumps({
                "message": msg["content"],
                "sender": msg["sender__username"]
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if message:
            # Save the message
            await self.save_message(self.sender.id, self.receiver_id, message)

            # Broadcast to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": self.sender.username
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        return Message.objects.create(sender=sender, receiver=receiver, content=content)

    @database_sync_to_async
    def get_chat_history(self, sender_id, receiver_id):
        ids = sorted([sender_id, receiver_id])
        return list(Message.objects.filter(
            sender_id__in=ids,
            receiver_id__in=ids
        ).order_by("timestamp").values("content", "sender__username"))
