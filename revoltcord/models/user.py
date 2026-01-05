"""
User model
Represents a Revolt user.
"""

class User:
    def __init__(self, id: str, username: str):
        self.id = id
        self.username = username
