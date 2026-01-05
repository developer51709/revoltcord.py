"""
Channel model
Represents a Revolt channel.
"""

class Channel:
    def __init__(self, id: str):
        self.id = id

    async def send(self, content: str):
        raise NotImplementedError("Channel.send() has not been implemented yet.")
