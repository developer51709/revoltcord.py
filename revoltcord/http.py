"""
HTTP module
Provides an asynchronous wrapper around the Revolt REST API.

This client is intentionally lightweight and designed to be extended
as revoltcord.py grows. It handles:
- Authorization
- JSON requests
- Error handling
- Basic REST endpoints (send/edit/delete message, fetch user, etc.)
"""

from __future__ import annotations
import aiohttp
from typing import Any, Dict, Optional


class HTTPException(Exception):
    """Base exception for HTTP-related errors."""
    pass


class NotFound(HTTPException):
    """Raised when a requested resource does not exist."""
    pass


class Forbidden(HTTPException):
    """Raised when the bot does not have permission to perform an action."""
    pass


class APIClient:
    BASE_URL = "https://api.revolt.chat"  # Can be overridden for self-hosted instances

    def __init__(self, token: str, session: Optional[aiohttp.ClientSession] = None):
        self.token = token
        self._session = session
        self._owns_session = session is None

    # -------------------------
    # Session Management
    # -------------------------

    async def _ensure_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def close(self):
        if self._session and self._owns_session:
            await self._session.close()

    # -------------------------
    # Core Request Handler
    # -------------------------

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        json: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Low-level HTTP request handler.
        """
        await self._ensure_session()

        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "x-bot-token": self.token,
            "Content-Type": "application/json",
        }

        async with self._session.request(method, url, headers=headers, json=json) as resp:
            if resp.status == 204:
                return None

            data = await resp.json()

            # Error handling
            if resp.status == 404:
                raise NotFound(data.get("message", "Resource not found"))
            if resp.status == 403:
                raise Forbidden(data.get("message", "Forbidden"))
            if resp.status >= 400:
                raise HTTPException(f"HTTP {resp.status}: {data}")

            return data

    # -------------------------
    # Message Endpoints
    # -------------------------

    async def send_message(self, channel_id: str, content: str) -> Dict[str, Any]:
        """
        Send a message to a channel.
        """
        payload = {"content": content}
        return await self.request("POST", f"/channels/{channel_id}/messages", json=payload)

    async def edit_message(self, message_id: str, content: str) -> Dict[str, Any]:
        """
        Edit an existing message.
        """
        payload = {"content": content}
        return await self.request("PATCH", f"/messages/{message_id}", json=payload)

    async def delete_message(self, message_id: str) -> None:
        """
        Delete a message.
        """
        await self.request("DELETE", f"/messages/{message_id}")

    # -------------------------
    # User Endpoints
    # -------------------------

    async def fetch_user(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch a user by ID.
        """
        return await self.request("GET", f"/users/{user_id}")

    async def fetch_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch extended profile information for a user.
        """
        return await self.request("GET", f"/users/{user_id}/profile")

    # -------------------------
    # Server Endpoints
    # -------------------------

    async def fetch_server_channels(self, server_id: str) -> Any:
        """
        Fetch all channels in a server.
        """
        return await self.request("GET", f"/servers/{server_id}/channels")

    async def fetch_server_members(self, server_id: str) -> Any:
        """
        Fetch all members in a server.
        """
        return await self.request("GET", f"/servers/{server_id}/members")
