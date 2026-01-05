"""
Message model
Represents a message sent in a Revolt channel.
"""

class Message:
    def __init__(self, id: str, content: str, author, channel):
        self.id = id
        self.content = content
        self.author = author
        self.channel = channel

    async def edit(self, content: str):
        raise NotImplementedError("Message.edit() has not been implemented yet.")

    async def delete(self):
        raise NotImplementedError("Message.delete() has not been implemented yet.")
