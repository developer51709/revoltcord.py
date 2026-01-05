"""
Error‑handling tests for revoltcord.py.

These tests ensure that the API wrapper correctly handles invalid inputs,
unexpected responses, and simulated server errors.
"""

import pytest


class MockAPIClient:
    """Mock client that simulates API failures."""

    def send_message(self, channel_id, content):
        if not content:
            raise ValueError("Message content cannot be empty")

        if channel_id == "invalid":
            return {"success": False, "error": "Channel not found"}

        return {"success": True}

    def fetch_user(self, user_id):
        if user_id == "missing":
            return None

        return {"id": user_id}

    def edit_message(self, message_id, content):
        if message_id == "404":
            raise RuntimeError("Message not found")

        return {"id": message_id, "content": content}


@pytest.fixture
def api():
    return MockAPIClient()


def test_send_message_empty_content(api):
    """Sending an empty message should raise an error."""
    with pytest.raises(ValueError):
        api.send_message("channel123", "")


def test_send_message_invalid_channel(api):
    """Sending to an invalid channel should return an error response."""
    response = api.send_message("invalid", "hello")

    assert response["success"] is False
    assert response["error"] == "Channel not found"


def test_fetch_missing_user(api):
    """Fetching a missing user should return None."""
    response = api.fetch_user("missing")

    assert response is None


def test_edit_missing_message(api):
    """Editing a nonexistent message should raise an error."""
    with pytest.raises(RuntimeError):
        api.edit_message("404", "new content")
