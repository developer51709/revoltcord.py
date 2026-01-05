"""
Server model
Represents a Revolt server (equivalent to a Discord guild).
"""

class Server:
    def __init__(self, id: str, name: str = None):
        self.id = id
        self.name = name
