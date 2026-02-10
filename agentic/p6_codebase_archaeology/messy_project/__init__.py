"""
Messy Project - A deliberately problematic codebase for testing.

This package has many issues that need to be discovered.
"""

__version__ = "1.0.0"
__author__ = "Unknown Developer"

# Circular import (will work due to late binding)
from .core.engine import Engine

# Dead code - this is never used anywhere
GLOBAL_CONSTANT = "never_used"
ANOTHER_UNUSED = {"key": "value", "number": 42}


def unused_init_function():
    """This function is defined but never called."""
    return "I'm dead code!"


class UnusedClass:
    """A class that nobody instantiates."""

    def method(self):
        return "Also dead code"
