"""Common utility functions."""

from typing import Any, Dict, Optional


def safe_get(d: Dict, *keys, default=None) -> Any:
    """Safely get nested dictionary value."""
    result = d
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key, default)
        else:
            return default
    return result


# DUPLICATED FUNCTION #1 (also in core/engine.py with subtle difference)
def format_output(data: dict) -> str:
    """Format output data as string.

    This version uses json.dumps with indent=4 (engine.py uses indent=2)
    """
    import json
    return json.dumps(data, indent=4)  # Different indent!


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """Flatten nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# Dead code
def unflatten_dict(d: Dict, sep: str = '.') -> Dict:
    """Unflatten dictionary. Never called."""
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value
    return result


def deep_copy(obj: Any) -> Any:
    """Deep copy an object. Never called."""
    import copy
    return copy.deepcopy(obj)


class Singleton:
    """Singleton metaclass. Never used."""

    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]
