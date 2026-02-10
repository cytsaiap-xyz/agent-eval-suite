"""API client service."""

from typing import Any, Dict, Optional
import json


class APIClient:
    """Client for external API calls."""

    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get("base_url", "http://localhost:8000")
        self.timeout = config.get("timeout", 30)
        self.api_key = config.get("api_key")
        self._session = None

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def get(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request."""
        # Simulated - no actual HTTP in offline mode
        return {"status": "ok", "data": {}}

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request."""
        return {"status": "ok", "data": data}


# DUPLICATED FUNCTION #2 (also in core/processor.py with subtle difference)
def parse_response(response: dict) -> dict:
    """Parse API response.

    This version returns EMPTY DICT for missing 'data' key (different from processor.py).
    """
    if "error" in response:
        raise ValueError(response["error"])

    return response.get("data", {})  # Returns {} if missing (processor.py returns None)


# Dead code
class MockAPIClient:
    """Mock API client for testing. Never used."""

    def __init__(self):
        self.calls = []

    def get(self, endpoint: str) -> dict:
        self.calls.append(("GET", endpoint))
        return {"mock": True}

    def post(self, endpoint: str, data: dict) -> dict:
        self.calls.append(("POST", endpoint, data))
        return {"mock": True}


def create_test_client() -> APIClient:
    """Create test API client. Never called."""
    return APIClient({"base_url": "http://test.local"})


# More dead code
API_ENDPOINTS = {
    "users": "/api/v1/users",
    "data": "/api/v1/data",
    "auth": "/api/v1/auth",
}


def get_endpoint(name: str) -> str:
    """Get endpoint URL. Never called."""
    return API_ENDPOINTS.get(name, "/api/v1/unknown")
