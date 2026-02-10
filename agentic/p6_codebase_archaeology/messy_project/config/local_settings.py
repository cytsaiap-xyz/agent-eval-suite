"""
Local settings override.

These should have HIGH priority but due to bug in settings.py, they don't.
"""

CONFIG = {
    "debug": True,
    "log_level": "DEBUG",
    "database": {
        "host": "dev-db.local",
        "port": 5433,
    },
    "feature_flags": {
        "new_ui": True,
        "beta_api": True
    }
}

# Dead code
UNUSED_SETTING = "this is never read"

SECRET_KEY = "dev-secret-key-12345"  # Should be in env, not here!
