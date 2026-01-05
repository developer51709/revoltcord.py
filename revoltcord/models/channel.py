"""
Channel model
Represents a Revolt channel.

This model is intentionally lightweight and does not perform HTTP requests
directly. All network operations should be delegated to the API client.
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message
    from ..http import APIClient


class Channel:
    def __init__(
        self,
        id: str,
        name: Optional[str] = None,
        server_id: Optional[str] = None,
        channel_type: Optional[str] = None,
        api: Optional["APIClient"] = None,
    ):
        self.id = id
        self.name = name
        self.server_id = server_id
        self.type = channel_type
        self._api = api  # API client injected by the library

    def __repr__(self):
        return f"<Channel id={self.id!r} name={self.name!r}>"

    async def send(self, content: str) -> "Message":
        """
        Send a message to this channel.
        """
        if not self._api:
            raise RuntimeError("Channel.send() called without an API client")

        data = await self._api.send_message(self.id, content)
        return Message(
            id=data["id"],
            content=data["content"],
            author=data.get("author"),
            channel=self,
            api=self._api,
        )
