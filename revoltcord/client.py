"""
Client module
Defines the base Client class responsible for managing the connection
to the Revolt API and gateway.
"""

class Client:
    def __init__(self):
        pass

    def run(self, token: str):
        """Start the client using the provided bot token."""
        raise NotImplementedError("Client.run() has not been implemented yet.")
