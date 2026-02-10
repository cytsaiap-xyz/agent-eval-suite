#!/usr/bin/env python3
"""
Main entry point for the messy project.
"""

import os
import sys

from config.settings import get_config
from core.engine import Engine
from core.processor import DataProcessor
from services.api import APIClient
from services.database import DatabaseConnection
from models.user import User

# BUG #1: This import will fail if models.helpers imports from here
# from models.helpers import format_user  # Commented out but someone might uncomment

# Dead import - module imported but never used
from utils.validation import Validator


def main():
    """Main entry point."""
    config = get_config()

    # Initialize engine
    engine = Engine(config)

    # Create processor
    processor = DataProcessor(engine)

    # Setup database
    db = DatabaseConnection(config.get("database", {}))

    # Setup API client
    api = APIClient(config.get("api", {}))

    # Process some data
    result = processor.process({"input": "test data"})

    print(f"Processing complete: {result}")

    return 0


def unused_main_helper():
    """DEAD CODE: This helper is never called."""
    print("This will never print")
    return {"status": "unused"}


def another_dead_function(x, y):
    """
    Another piece of dead code.

    Args:
        x: Never passed
        y: Never passed
    """
    return x + y


# Dead code - unreachable
if False:
    print("This is unreachable code")
    secret_value = "should not be seen"


# More dead code hidden in a condition that's always false
DEBUG_MODE = False
if DEBUG_MODE:
    def debug_helper():
        """Only defined when DEBUG_MODE is True."""
        pass


if __name__ == "__main__":
    sys.exit(main())
