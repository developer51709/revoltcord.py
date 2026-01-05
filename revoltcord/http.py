"""
HTTP module
Provides a wrapper around the Revolt REST API.
"""

class APIClient:
    def __init__(self, token: str):
        self.token = token

    async def send_message(self, channel_id: str, content: str):
        raise NotImplementedError("send_message() has not been implemented yet.")

    async def edit_message(self, message_id: str, content: str):
        raise NotImplementedError("edit_message() has not been implemented yet.")

    async def delete_message(self, message_id: str):
        raise NotImplementedError("delete_message() has not been implemented yet.")
