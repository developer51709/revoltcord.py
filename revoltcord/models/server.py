"""
Server model
Represents a Revolt server (similar to a Discord guild).
"""

class Server:
    def __init__(self, id: str, name: str | None = None, owner_id: str | None = None):
        self.id = id
        self.name = name
        self.owner_id = owner_id

        # Placeholder lists for future expansion
        self.channels = []
        self.members = []

    def __repr__(self):
        return f"<Server id={self.id!r} name={self.name!r}>"
