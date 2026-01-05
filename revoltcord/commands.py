"""
Commands module
Provides a Discord.py-style command framework for revoltcord.py.

This includes:
- Command class
- Context class
- Bot class with command registration and dispatching
"""

from __future__ import annotations
import inspect
from typing import Any, Callable, Dict, List, Optional, Coroutine

from .client import Client
from .utils.converters import run_converter


# ------------------------------------------------------------
# Context Object
# ------------------------------------------------------------

class Context:
    """
    Represents the context in which a command is invoked.
    """

    def __init__(self, client: Client, message):
        self.client = client
        self.message = message
        self.channel = message.channel
        self.author = message.author

    async def send(self, content: str):
        """
        Send a message back to the same channel.
        """
        return await self.channel.send(content)


# ------------------------------------------------------------
# Command Object
# ------------------------------------------------------------

class Command:
    """
    Represents a registered command.
    """

    def __init__(self, func: Callable, name: Optional[str] = None):
        self.callback = func
        self.name = name or func.__name__
        self.help = func.__doc__ or "No description provided."

        # Extract type annotations for argument conversion
        sig = inspect.signature(func)
        self.params = list(sig.parameters.values())[1:]  # skip 'ctx'

    async def invoke(self, ctx: Context, args: List[str]):
        """
        Invoke the command with converted arguments.
        """
        converted_args = []

        for param, raw in zip(self.params, args):
            annotation = param.annotation

            if annotation is inspect._empty:
                # No type annotation → treat as string
                converted_args.append(raw)
            else:
                # Use converter system
                converted = await run_converter(annotation, raw)
                converted_args.append(converted)

        await self.callback(ctx, *converted_args)


# ------------------------------------------------------------
# Bot Class
# ------------------------------------------------------------

class Bot(Client):
    """
    Bot class that extends Client and adds command handling.
    """

    def __init__(self, command_prefix: str = "!", **kwargs):
        super().__init__(**kwargs)
        self.command_prefix = command_prefix
        self.commands: Dict[str, Command] = {}

        # Register internal event hooks
        self.event(self._on_message_internal)

    # --------------------------------------------------------
    # Command Registration
    # --------------------------------------------------------

    def command(self, name: Optional[str] = None):
        """
        Decorator to register a command.

        Example:
            @bot.command()
            async def ping(ctx):
                await ctx.send("Pong!")
        """
        def decorator(func: Callable):
            cmd = Command(func, name)
            self.commands[cmd.name] = cmd
            return func

        return decorator

    # --------------------------------------------------------
    # Message Handling
    # --------------------------------------------------------

    async def _on_message_internal(self, message):
        """
        Internal handler for on_message events.
        Parses commands and dispatches them.
        """
        content = message.content

        if not content.startswith(self.command_prefix):
            return

        # Remove prefix
        content = content[len(self.command_prefix):]

        # Split into command + args
        parts = content.split()
        if not parts:
            return

        name = parts[0]
        args = parts[1:]

        cmd = self.commands.get(name)
        if not cmd:
            return  # Unknown command

        ctx = Context(self, message)
        await cmd.invoke(ctx, args)
