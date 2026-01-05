"""
Client module
Defines the base Client class responsible for managing the connection
to the Revolt API and gateway, dispatching events, and providing the
Discord.py-style event interface.
"""

from __future__ import annotations
import inspect
import asyncio
from typing import Any, Callable, Coroutine, Dict, Optional

from .http import APIClient
from .gateway import Gateway


class Client:
    def __init__(self, *, token: Optional[str] = None):
        self.token = token
        self.http: Optional[APIClient] = None
        self.gateway: Optional[Gateway] = None

        # Event name -> coroutine function
        self._events: Dict[str, Callable[..., Coroutine[Any, Any, Any]]] = {}

        # Internal loop reference
        self.loop = asyncio.get_event_loop()

    # ------------------------------------------------------------
    # Event Registration
    # ------------------------------------------------------------

    def event(self, func: Callable) -> Callable:
        """
        Decorator to register an event handler.

        Example:
            @client.event
            async def on_ready():
                ...
        """
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Event handler must be a coroutine function")

        self._events[func.__name__] = func
        return func

    async def dispatch(self, event_name: str, *args, **kwargs):
        """
        Dispatch an event to the registered handler.
        """
        handler = self._events.get(event_name)
        if handler:
            try:
                await handler(*args, **kwargs)
            except Exception as exc:
                await self.dispatch("on_error", event_name, exc)

    # ------------------------------------------------------------
    # Lifecycle Management
    # ------------------------------------------------------------

    async def start(self, token: Optional[str] = None):
        """
        Start the client: initialize HTTP, connect to gateway, and begin
        receiving events.
        """
        self.token = token or self.token
        if not self.token:
            raise ValueError("Client.start() requires a bot token")

        # Initialize HTTP client
        self.http = APIClient(self.token)

        # Initialize gateway
        self.gateway = Gateway(self.token, client=self)

        # Connect to gateway
        await self.gateway.connect()

        # Fire ready event
        await self.dispatch("on_ready")

    def run(self, token: Optional[str] = None):
        """
        Synchronous entry point for running the client.
        """
        try:
            self.loop.run_until_complete(self.start(token))
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.run_until_complete(self.close())

    async def close(self):
        """
        Cleanly shut down the client.
        """
        if self.gateway:
            await self.gateway.close()

        if self.http:
            await self.http.close()

        await self.dispatch("on_close")

    # ------------------------------------------------------------
    # Utility Methods
    # ------------------------------------------------------------

    async def fetch_user(self, user_id: str):
        """
        Convenience wrapper for APIClient.fetch_user().
        """
        if not self.http:
            raise RuntimeError("Client.fetch_user() called before client is started")

        return await self.http.fetch_user(user_id)
