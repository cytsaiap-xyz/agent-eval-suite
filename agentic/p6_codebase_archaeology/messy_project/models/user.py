"""User model."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """Represents a user in the system."""

    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool = True
    role: str = "user"

    def __post_init__(self):
        """Validate user data after initialization."""
        if not self.username:
            raise ValueError("Username cannot be empty")

        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address")

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary."""
        return cls(
            id=data["id"],
            username=data["username"],
            email=data["email"],
            created_at=datetime.fromisoformat(data["created_at"]),
            is_active=data.get("is_active", True),
            role=data.get("role", "user")
        )


# Dead code - unused user types
class AdminUser(User):
    """Admin user with extra privileges. Never used."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = "admin"

    def can_delete_users(self) -> bool:
        return True


class GuestUser:
    """Guest user - not actually a User subclass. Never used."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.username = "guest"

    def is_authenticated(self) -> bool:
        return False


# Dead function
def create_test_user() -> User:
    """Create a test user. Never called."""
    return User(
        id=0,
        username="testuser",
        email="test@example.com",
        created_at=datetime.now()
    )
