"""
Server model
Represents a Revolt server (similar to a Discord guild).

This model is structured to support future features such as:
- channel caching
- member caching
- role management
- server settings
- API-backed updates
"""

from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .channel import Channel
    from .user import User
    from ..http import APIClient


class Server:
    def __init__(
        self,
        id: str,
        name: Optional[str] = None,
        owner_id: Optional[str] = None,
        api: Optional["APIClient"] = None,
    ):
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self._api = api

        # Caches (populated by gateway or API)
        self.channels: List["Channel"] = []
        self.members: List["User"] = []

    def __repr__(self):
        return f"<Server id={self.id!r} name={self.name!r}>"

    def get_channel(self, channel_id: str) -> Optional["Channel"]:
        """
        Return a channel from the server's cache.
        """
        for channel in self.channels:
            if channel.id == channel_id:
                return channel
        return None

    def get_member(self, user_id: str) -> Optional["User"]:
        """
        Return a member from the server's cache.
        """
        for member in self.members:
            if member.id == user_id:
                return member
        return None

    async def fetch_channels(self) -> List["Channel"]:
        """
        Fetch all channels for this server from the API.
        """
        if not self._api:
            raise RuntimeError("Server.fetch_channels() called without an API client")

        data = await self._api.fetch_server_channels(self.id)
        return data

    async def fetch_members(self) -> List["User"]:
        """
        Fetch all members for this server from the API.
        """
        if not self._api:
            raise RuntimeError("Server.fetch_members() called without an API client")

        data = await self._api.fetch_server_members(self.id)
        return data
