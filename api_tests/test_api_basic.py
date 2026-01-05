"""
Basic API behavior tests for revoltcord.py.

These tests use mock objects to simulate Revolt API responses.
They ensure that the REST wrapper behaves correctly with valid inputs.
"""

import pytest

# Import your API client once implemented
# from revoltcord.http import APIClient


class MockAPIClient:
    """A mock API client used for early testing."""

    def send_message(self, channel_id, content):
        return {
            "id": "msg123",
            "channel": channel_id,
            "content": content,
            "success": True,
        }

    def fetch_user(self, user_id):
        return {
            "id": user_id,
            "username": "TestUser",
            "avatar": None,
        }

    def edit_message(self, message_id, content):
        return {
            "id": message_id,
            "content": content,
            "edited": True,
        }


@pytest.fixture
def api():
    """Provides a mock API client for testing."""
    return MockAPIClient()


def test_send_message(api):
    """Test sending a basic message."""
    response = api.send_message("channel123", "hello world")

    assert response["success"] is True
    assert response["channel"] == "channel123"
    assert response["content"] == "hello world"


def test_fetch_user(api):
    """Test fetching a user."""
    response = api.fetch_user("user123")

    assert response["id"] == "user123"
    assert response["username"] == "TestUser"
    assert response["avatar"] is None


def test_edit_message(api):
    """Test editing a message."""
    response = api.edit_message("msg123", "updated text")

    assert response["id"] == "msg123"
    assert response["content"] == "updated text"
    assert response["edited"] is True
