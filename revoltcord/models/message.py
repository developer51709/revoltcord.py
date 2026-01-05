"""
Message model
Represents a message sent in a Revolt channel.

This model is designed to be compatible with Discord.py's Message object
while remaining lightweight and API-agnostic.
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .channel import Channel
    from ..http import APIClient


class Message:
    def __init__(
        self,
        id: str,
        content: str,
        author,
        channel: "Channel",
        api: Optional["APIClient"] = None,
        timestamp: Optional[str] = None,
        edited_timestamp: Optional[str] = None,
    ):
        self.id = id
        self.content = content
        self.author = author
        self.channel = channel
        self.timestamp = timestamp
        self.edited_timestamp = edited_timestamp
        self._api = api

    def __repr__(self):
        return f"<Message id={self.id!r} author={self.author!r}>"

    async def edit(self, content: str) -> "Message":
        """
        Edit this message.
        """
        if not self._api:
            raise RuntimeError("Message.edit() called without an API client")

        data = await self._api.edit_message(self.id, content)
        self.content = data["content"]
        self.edited_timestamp = data.get("edited_timestamp")
        return self

    async def delete(self) -> None:
        """
        Delete this message.
        """
        if not self._api:
            raise RuntimeError("Message.delete() called without an API client")

        await self._api.delete_message(self.id)
