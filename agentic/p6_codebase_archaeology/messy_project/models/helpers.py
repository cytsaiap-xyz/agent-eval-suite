"""Model helpers.

WARNING: This file has circular import issues!
"""

from typing import Dict, Any

# This circular import WILL FAIL if uncommented and main.py imports from here
# from main import unused_main_helper

from .user import User


def format_user(user: User) -> str:
    """Format user for display."""
    return f"{user.username} <{user.email}>"


def format_user_dict(user_dict: Dict[str, Any]) -> str:
    """Format user dictionary for display."""
    return f"{user_dict.get('username', 'Unknown')} <{user_dict.get('email', 'N/A')}>"


# Dead code
def validate_user_data(data: dict) -> bool:
    """Validate user data. Never called."""
    required = ["username", "email"]
    return all(key in data for key in required)


def merge_user_data(base: dict, updates: dict) -> dict:
    """Merge user data. Never called."""
    result = base.copy()
    result.update(updates)
    return result


# This creates a circular dependency with services.database
# Uncommenting this would break imports
# from services.database import get_user_by_id

def get_user_display_name(user_id: int) -> str:
    """Get user display name by ID.

    Note: This has a potential circular import if it tries to use database.
    Currently stubbed out.
    """
    # Would be: user = get_user_by_id(user_id)
    return f"User#{user_id}"
