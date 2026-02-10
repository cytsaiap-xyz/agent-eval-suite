"""
Authentication Module

Contains 1 bug in session handling.
"""

from functools import wraps
from flask import session, jsonify
from .models import User


def authenticate(username, password):
    """Authenticate user with username and password."""
    if not username or not password:
        return None

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return user

    return None


def require_auth(f):
    """Decorator to require authentication for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # BUG #6: Wrong session key name
        user_id = session.get("userid")  # Should be "user_id"

        if not user_id:
            return jsonify({"error": "Authentication required"}), 401

        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 401

        return f(*args, **kwargs)

    return decorated_function


def get_current_user():
    """Get the currently authenticated user."""
    user_id = session.get("user_id")
    if user_id:
        return User.query.get(user_id)
    return None
