"""
Configuration management.

Loads configuration from multiple sources with confusing precedence.
"""

import json
import os
from pathlib import Path

# Try to import yaml (might not be available)
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# HARDCODED DEFAULTS (Source 1)
DEFAULTS = {
    "debug": False,
    "log_level": "INFO",
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp"
    },
    "api": {
        "base_url": "http://localhost:8000",
        "timeout": 30
    },
    "cache": {
        "enabled": True,
        "ttl": 3600
    }
}

# This will be populated by load_config
_config = None


def load_defaults_yaml():
    """Load from defaults.yaml (Source 2)."""
    yaml_path = Path(__file__).parent / "defaults.yaml"
    if yaml_path.exists() and HAS_YAML:
        with open(yaml_path) as f:
            return yaml.safe_load(f)
    return {}


def load_json_config():
    """Load from config.json in project root (Source 3)."""
    json_path = Path(__file__).parent.parent / "config.json"
    if json_path.exists():
        with open(json_path) as f:
            return json.load(f)
    return {}


def load_local_settings():
    """Load from local_settings.py (Source 4) - HIGHEST PRIORITY."""
    try:
        from . import local_settings
        return getattr(local_settings, 'CONFIG', {})
    except ImportError:
        return {}


def load_env_vars():
    """Load from environment variables (Source 5)."""
    config = {}

    if os.environ.get("DEBUG"):
        config["debug"] = os.environ["DEBUG"].lower() == "true"

    if os.environ.get("LOG_LEVEL"):
        config["log_level"] = os.environ["LOG_LEVEL"]

    if os.environ.get("DATABASE_HOST"):
        config.setdefault("database", {})["host"] = os.environ["DATABASE_HOST"]

    if os.environ.get("API_TIMEOUT"):
        config.setdefault("api", {})["timeout"] = int(os.environ["API_TIMEOUT"])

    return config


def deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries.

    BUG #2: This merge has a subtle bug - it mutates the base dict!
    """
    result = base  # BUG: Should be base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def load_config() -> dict:
    """
    Load configuration from all sources.

    Priority (highest to lowest):
    1. Environment variables
    2. local_settings.py
    3. config.json
    4. defaults.yaml
    5. Hardcoded DEFAULTS

    Note: This is actually implemented BACKWARDS - defaults override specifics!
    """
    global _config

    # BUG #3: The merge order is wrong - lower priority should be base
    # Currently, higher priority configs get overwritten by lower ones
    config = {}
    config = deep_merge(config, load_env_vars())       # Should be last (highest priority)
    config = deep_merge(config, load_local_settings()) # Should be second to last
    config = deep_merge(config, load_json_config())    # Should be third
    config = deep_merge(config, load_defaults_yaml())  # Should be second
    config = deep_merge(config, DEFAULTS)              # Should be first (lowest priority)

    _config = config
    return config


def get_config() -> dict:
    """Get the current configuration."""
    global _config
    if _config is None:
        _config = load_config()
    return _config


# Dead code: unused configuration validators
def validate_database_config(config):
    """Validate database configuration. NEVER CALLED."""
    required = ["host", "port", "name"]
    db_config = config.get("database", {})
    for key in required:
        if key not in db_config:
            raise ValueError(f"Missing database config: {key}")
    return True


def validate_api_config(config):
    """Validate API configuration. NEVER CALLED."""
    if "api" not in config:
        return False
    if "base_url" not in config["api"]:
        return False
    return True
