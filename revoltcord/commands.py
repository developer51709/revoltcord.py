"""
Commands module
Provides a Discord.py‑style command framework, including the Bot class
and command decorators.
"""

class Bot:
    def __init__(self, command_prefix: str):
        self.command_prefix = command_prefix

    def command(self, name: str = None):
        """Decorator for registering a command."""
        def decorator(func):
            return func
        return decorator

    def run(self, token: str):
        """Start the bot."""
        raise NotImplementedError("Bot.run() has not been implemented yet.")
