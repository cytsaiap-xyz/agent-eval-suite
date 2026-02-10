"""
Data processor module.
"""

from typing import Any, Dict, List

# This import creates a circular dependency with engine
from .engine import Engine
from .utils import sanitize_string


class DataProcessor:
    """Processes data using the engine."""

    def __init__(self, engine: 'Engine'):
        self.engine = engine
        self._history: List[Dict] = []

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data and return result."""
        # Sanitize input strings
        processed = {}
        for key, value in data.items():
            if isinstance(value, str):
                processed[key] = sanitize_string(value)
            else:
                processed[key] = value

        # Store in history
        self._history.append(processed)

        # Use engine's process method
        return self.engine.process(processed)

    def get_history(self) -> List[Dict]:
        """Get processing history."""
        return self._history.copy()

    def clear_history(self):
        """Clear processing history."""
        self._history = []


# DUPLICATED FUNCTION #2 (also in services/api.py with subtle difference)
def parse_response(response: dict) -> dict:
    """Parse API response.

    This version returns None for missing 'data' key.
    """
    if "error" in response:
        raise ValueError(response["error"])

    return response.get("data")  # Returns None if missing


# Dead code - processing strategies never used
class ProcessingStrategy:
    """Abstract processing strategy."""

    def execute(self, data):
        raise NotImplementedError


class FastStrategy(ProcessingStrategy):
    """Fast but less accurate."""

    def execute(self, data):
        return data


class AccurateStrategy(ProcessingStrategy):
    """Accurate but slower."""

    def execute(self, data):
        import time
        time.sleep(0.1)
        return data


# These strategies are never instantiated or used
STRATEGIES = {
    "fast": FastStrategy,
    "accurate": AccurateStrategy,
}


def get_strategy(name: str) -> ProcessingStrategy:
    """Get strategy by name. NEVER CALLED."""
    return STRATEGIES.get(name, FastStrategy)()
