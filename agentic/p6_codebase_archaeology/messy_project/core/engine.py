"""
Main processing engine.
"""

from typing import Any, Dict, Optional

# Circular import - but works due to late binding
from .utils import validate_input, transform_data


class Engine:
    """Main processing engine."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._initialized = False
        self._cache = {}

    def initialize(self):
        """Initialize the engine."""
        if self._initialized:
            return

        # Late import to avoid circular dependency
        from .processor import DataProcessor

        self._processor = DataProcessor(self)
        self._initialized = True

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data."""
        if not self._initialized:
            self.initialize()

        validated = validate_input(data)
        transformed = transform_data(validated)

        return {
            "status": "success",
            "result": transformed
        }

    def get_cached(self, key: str) -> Optional[Any]:
        """Get cached value."""
        return self._cache.get(key)

    def set_cached(self, key: str, value: Any):
        """Set cached value."""
        self._cache[key] = value


# DUPLICATED FUNCTION #1 (also in utils/common.py with subtle difference)
def format_output(data: dict) -> str:
    """Format output data as string.

    Note: This version uses json.dumps with indent=2
    """
    import json
    return json.dumps(data, indent=2)


# Dead code
def unused_engine_helper():
    """Never called."""
    return "dead"


class DeprecatedEngine:
    """Old engine class - nobody uses this anymore."""

    def __init__(self):
        self.name = "deprecated"

    def run(self):
        """Does nothing useful."""
        pass
