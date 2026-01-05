"""
User model
Represents a Revolt user.

This model is intentionally lightweight but structured to support
future expansion such as profile data, badges, status, and API-backed
updates.
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http import APIClient


class User:
    def __init__(
        self,
        id: str,
        username: str,
        avatar: Optional[str] = None,
        api: Optional["APIClient"] = None,
    ):
        self.id = id
        self.username = username
        self.avatar = avatar
        self._api = api  # API client injected by the library

    def __repr__(self):
        return f"<User id={self.id!r} username={self.username!r}>"

    async def fetch_profile(self) -> dict:
        """
        Fetch extended profile information for this user.
        Placeholder for future API expansion.
        """
        if not self._api:
            raise RuntimeError("User.fetch_profile() called without an API client")

        # Future: Revolt API endpoint for user profiles
        data = await self._api.fetch_user_profile(self.id)
        return data
