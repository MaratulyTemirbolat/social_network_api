import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from typing import (
    Optional,
    Dict,
    Any,
)

from chats.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    """ChatConsumer."""

    async def connect(self) -> None:
        """Get in touch with chat."""
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = 'chat_%s' % self.chat_id

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code: int) -> None:
        """Disconnect."""
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None) -> None:
        """receive."""
        data: Dict[str, Any] = json.loads(text_data)
        message: Optional[str] = data.get('message', None)
        username: Optional[str] = data.get('username', None)
        chat_id: Optional[int] = data.get('chat_id', None)
        user_id: Optional[int] = data.get('user_id', None)

        if message and user_id and chat_id:
            await self.save_message(
                chat_id=chat_id,
                user_id=user_id,
                message=message
            )

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chat_id': chat_id,
                'user_id': user_id
            }
        )

    async def chat_message(self, event) -> None:
        """chat_message."""
        message: str = event['message']
        username: str = event['username']
        chat_id: int = event['chat_id']
        user_id: int = event['user_id']

        await self.send(text_data=json.dumps(
            {
                'message': message,
                'username': username,
                'chat': chat_id,
                'user_id': user_id
            }
        ))

    @sync_to_async
    def save_message(
        self,
        chat_id: int,
        user_id: int,
        message: str
    ) -> None:
        """Save message in db."""
        Message.objects.create(
            content=message,
            chat_id=chat_id,
            owner_id=user_id
        )
