"""
Gateway module
Handles WebSocket communication with the Revolt gateway.
"""

class Gateway:
    def __init__(self, token: str):
        self.token = token

    async def connect(self):
        """Connect to the Revolt gateway."""
        raise NotImplementedError("Gateway.connect() has not been implemented yet.")
