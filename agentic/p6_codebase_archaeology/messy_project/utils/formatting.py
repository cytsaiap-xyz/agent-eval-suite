"""Formatting utilities - ENTIRE FILE IS DEAD CODE (never imported)."""

from datetime import datetime
from typing import Any


def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    """Format datetime as string."""
    return dt.strftime(fmt)


def format_datetime(dt: datetime) -> str:
    """Format datetime with time."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage."""
    return f"{value * 100:.{decimals}f}%"


def format_bytes(size: int) -> str:
    """Format bytes as human readable."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def truncate(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def pluralize(word: str, count: int) -> str:
    """Simple pluralization."""
    if count == 1:
        return word
    return word + "s"


def snake_to_camel(text: str) -> str:
    """Convert snake_case to camelCase."""
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def camel_to_snake(text: str) -> str:
    """Convert camelCase to snake_case."""
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
