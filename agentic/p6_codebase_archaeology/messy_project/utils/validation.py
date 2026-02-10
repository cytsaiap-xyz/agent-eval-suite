"""Validation utilities."""

import re
from typing import Any, Dict, List, Optional


class Validator:
    """Data validator class."""

    def __init__(self):
        self.errors: List[str] = []

    def validate(self, data: Dict[str, Any], rules: Dict[str, Any]) -> bool:
        """Validate data against rules."""
        self.errors = []

        for field, rule in rules.items():
            value = data.get(field)

            if rule.get("required") and value is None:
                self.errors.append(f"{field} is required")
                continue

            if value is not None:
                if "type" in rule and not isinstance(value, rule["type"]):
                    self.errors.append(f"{field} must be {rule['type'].__name__}")

                if "min_length" in rule and len(str(value)) < rule["min_length"]:
                    self.errors.append(f"{field} must be at least {rule['min_length']} characters")

                if "max_length" in rule and len(str(value)) > rule["max_length"]:
                    self.errors.append(f"{field} must be at most {rule['max_length']} characters")

        return len(self.errors) == 0

    def get_errors(self) -> List[str]:
        """Get validation errors."""
        return self.errors.copy()


# DUPLICATED FUNCTION #3 (also in core/utils.py with subtle difference)
def is_valid_email(email: str) -> bool:
    """Check if email is valid.

    This version uses a MORE COMPLETE regex that handles more cases.
    """
    # More comprehensive pattern than core/utils.py
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """Check if phone number is valid."""
    # Remove non-digits
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10


def is_valid_url(url: str) -> bool:
    """Check if URL is valid."""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


# Dead code
def validate_username(username: str) -> bool:
    """Validate username. Never called."""
    if not username:
        return False
    if len(username) < 3 or len(username) > 20:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_]+$', username))


def validate_password(password: str) -> tuple:
    """Validate password strength. Never called."""
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain uppercase letter")

    if not re.search(r'[a-z]', password):
        errors.append("Password must contain lowercase letter")

    if not re.search(r'\d', password):
        errors.append("Password must contain a digit")

    return (len(errors) == 0, errors)


class SchemaValidator:
    """JSON schema validator. Never instantiated."""

    def __init__(self, schema: dict):
        self.schema = schema

    def validate(self, data: dict) -> bool:
        # Simplified validation
        for key, rules in self.schema.items():
            if rules.get("required") and key not in data:
                return False
        return True
