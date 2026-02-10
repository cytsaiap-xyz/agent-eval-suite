"""
Core utility functions.
"""

import re
from typing import Any, Dict


def validate_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate input data."""
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary")

    return data


def transform_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform data for processing."""
    result = {}

    for key, value in data.items():
        # Convert keys to lowercase
        new_key = key.lower()

        # Transform values
        if isinstance(value, str):
            result[new_key] = value.strip()
        elif isinstance(value, (int, float)):
            result[new_key] = value
        else:
            result[new_key] = str(value)

    return result


def sanitize_string(s: str) -> str:
    """Sanitize a string by removing special characters."""
    # Remove HTML tags
    s = re.sub(r'<[^>]+>', '', s)

    # Remove multiple whitespace
    s = re.sub(r'\s+', ' ', s)

    return s.strip()


# Dead code below
def deprecated_transform(data):
    """Old transform function - replaced by transform_data."""
    return data


def unused_helper():
    """Nobody calls this."""
    return 42


# DUPLICATED FUNCTION #3 (also in utils/validation.py with subtle difference)
def is_valid_email(email: str) -> bool:
    """Check if email is valid.

    This version uses a SIMPLE regex that misses edge cases.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


# More dead code
class TransformationPipeline:
    """Pipeline for transformations. Never instantiated."""

    def __init__(self):
        self.steps = []

    def add_step(self, func):
        self.steps.append(func)

    def run(self, data):
        result = data
        for step in self.steps:
            result = step(result)
        return result
