"""
User model
Represents a Revolt user.
"""

class User:
    def __init__(self, id: str, username: str, avatar: str | None = None):
        self.id = id
        self.username = username
        self.avatar = avatar

    def __repr__(self):
        return f"<User id={self.id!r} username={self.username!r}>"
