"""
Old processor - DEPRECATED

This entire module is dead code. It was replaced by core/processor.py
but never removed from the codebase.
"""

from typing import Any, Dict, List
import warnings


def deprecated(func):
    """Decorator to mark functions as deprecated."""
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is deprecated",
            DeprecationWarning,
            stacklevel=2
        )
        return func(*args, **kwargs)
    return wrapper


class OldProcessor:
    """
    Original data processor.

    This class was replaced by core.processor.DataProcessor
    but remains in the codebase.
    """

    def __init__(self):
        self.data = []

    @deprecated
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data using old algorithm."""
        return {"processed": True, "data": data}

    @deprecated
    def batch_process(self, items: List[Dict]) -> List[Dict]:
        """Process multiple items."""
        return [self.process(item) for item in items]


@deprecated
def old_transform(data: dict) -> dict:
    """Old transformation function."""
    return {k.upper(): v for k, v in data.items()}


@deprecated
def old_validate(data: dict) -> bool:
    """Old validation function."""
    return bool(data)


# Constants that are never used
OLD_VERSION = "0.9.0"
LEGACY_MODE = True
DEPRECATED_FEATURES = ["old_transform", "old_validate", "OldProcessor"]
