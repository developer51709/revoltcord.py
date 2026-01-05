"""
Gateway module
Handles WebSocket communication with the Revolt gateway.

This implementation is intentionally lightweight and designed to be
extended as revoltcord.py grows. It provides:
- WebSocket connection management
- Event listening loop
- Basic reconnection logic
- Dispatching events to the Client
"""

from __future__ import annotations
import aiohttp
import asyncio
import json
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client


class Gateway:
    GATEWAY_URL = "wss://ws.revolt.chat"  # Default Revolt gateway

    def __init__(self, token: str, client: "Client"):
        self.token = token
        self.client = client
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._closed = False

    # ------------------------------------------------------------
    # Connection Management
    # ------------------------------------------------------------

    async def connect(self):
        """
        Connect to the Revolt WebSocket gateway.
        """
        self.session = aiohttp.ClientSession()

        try:
            self.ws = await self.session.ws_connect(
                self.GATEWAY_URL,
                headers={"x-bot-token": self.token},
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to connect to gateway: {exc}")

        # Start listener loop
        asyncio.create_task(self.listen())

    async def close(self):
        """
        Close the WebSocket and session.
        """
        self._closed = True

        if self.ws:
            await self.ws.close()

        if self.session:
            await self.session.close()

    # ------------------------------------------------------------
    # Listener Loop
    # ------------------------------------------------------------

    async def listen(self):
        """
        Main WebSocket event loop.
        """
        while not self._closed:
            try:
                msg = await self.ws.receive()

                if msg.type == aiohttp.WSMsgType.TEXT:
                    await self.handle_payload(msg.data)

                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

            except Exception as exc:
                # Attempt reconnect
                await self.client.dispatch("on_error", "gateway", exc)
                await asyncio.sleep(3)
                await self.reconnect()

    # ------------------------------------------------------------
    # Reconnection Logic
    # ------------------------------------------------------------

    async def reconnect(self):
        """
        Attempt to reconnect to the gateway.
        """
        await self.close()
        await asyncio.sleep(1)
        await self.connect()

    # ------------------------------------------------------------
    # Payload Handling
    # ------------------------------------------------------------

    async def handle_payload(self, raw: str):
        """
        Parse and dispatch a gateway event.
        """
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return

        event_type = data.get("type")
        if not event_type:
            return

        # Dispatch generic event
        await self.client.dispatch(f"on_{event_type.lower()}", data)

        # Special-case message events
        if event_type == "Message":
            await self.handle_message_event(data)

    async def handle_message_event(self, data: dict):
        """
        Convert a raw message payload into a Message model and dispatch it.
        """
        from .models.message import Message
        from .models.channel import Channel
        from .models.user import User

        # Build model objects
        author = User(
            id=data["author"],
            username=data.get("username", "Unknown"),
            api=self.client.http,
        )

        channel = Channel(
            id=data["channel"],
            name=None,
            server_id=None,
            api=self.client.http,
        )

        message = Message(
            id=data["_id"],
            content=data.get("content", ""),
            author=author,
            channel=channel,
            api=self.client.http,
        )

        await self.client.dispatch("on_message", message)
