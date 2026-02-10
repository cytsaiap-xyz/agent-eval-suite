"""
Test Suite for Buggy App

DO NOT MODIFY THIS FILE.
Your task is to fix the bugs in buggy_app/ to make all tests pass.
"""

import pytest
from buggy_app import create_app
from buggy_app.models import db, User, Note


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def auth_client(app, client):
    """Create authenticated test client."""
    # Register a user
    client.post("/register", json={
        "username": "testuser",
        "password": "testpass123"
    })

    # Login
    client.post("/login", json={
        "username": "testuser",
        "password": "testpass123"
    })

    return client


class TestHealthCheck:
    """Test 1: Health check endpoint."""

    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json["status"] == "ok"


class TestUserRegistration:
    """Test 2-3: User registration."""

    def test_register_new_user(self, client):
        """Test 2: Can register a new user."""
        response = client.post("/register", json={
            "username": "newuser",
            "password": "password123"
        })

        assert response.status_code == 201
        assert "user_id" in response.json

    def test_register_duplicate_user(self, client):
        """Test 3: Cannot register duplicate username."""
        # First registration
        client.post("/register", json={
            "username": "duplicate",
            "password": "password123"
        })

        # Second registration should fail
        response = client.post("/register", json={
            "username": "duplicate",
            "password": "password456"
        })

        assert response.status_code == 409
        assert "already exists" in response.json.get("error", "").lower()


class TestUserLogin:
    """Test 4-5: User login."""

    def test_login_valid_credentials(self, client):
        """Test 4: Can login with valid credentials."""
        # Register first
        client.post("/register", json={
            "username": "loginuser",
            "password": "mypassword"
        })

        # Login
        response = client.post("/login", json={
            "username": "loginuser",
            "password": "mypassword"
        })

        assert response.status_code == 200
        assert "successful" in response.json.get("message", "").lower()

    def test_login_invalid_credentials(self, client):
        """Test 5: Cannot login with invalid credentials."""
        response = client.post("/login", json={
            "username": "nonexistent",
            "password": "wrongpass"
        })

        assert response.status_code == 401


class TestNotes:
    """Test 6-10: Note operations."""

    def test_create_note(self, auth_client):
        """Test 6: Can create a note when authenticated."""
        response = auth_client.post("/notes", json={
            "title": "My Note",
            "content": "This is the content"
        })

        assert response.status_code == 201
        assert "note_id" in response.json

    def test_get_notes(self, auth_client):
        """Test 7: Can get list of notes."""
        # Create a note first
        auth_client.post("/notes", json={
            "title": "Test Note",
            "content": "Test content"
        })

        response = auth_client.get("/notes")

        assert response.status_code == 200
        assert "notes" in response.json
        assert len(response.json["notes"]) >= 1

    def test_get_specific_note(self, auth_client):
        """Test 8: Can get a specific note by ID."""
        # Create a note
        create_response = auth_client.post("/notes", json={
            "title": "Specific Note",
            "content": "Specific content"
        })
        note_id = create_response.json["note_id"]

        # Get the note
        response = auth_client.get(f"/notes/{note_id}")

        assert response.status_code == 200
        assert response.json["title"] == "Specific Note"

    def test_update_note(self, auth_client):
        """Test 9: Can update a note."""
        # Create a note
        create_response = auth_client.post("/notes", json={
            "title": "Original Title",
            "content": "Original content"
        })
        note_id = create_response.json["note_id"]

        # Update the note
        response = auth_client.put(f"/notes/{note_id}", json={
            "title": "Updated Title"
        })

        assert response.status_code == 200

        # Verify update
        get_response = auth_client.get(f"/notes/{note_id}")
        assert get_response.json["title"] == "Updated Title"

    def test_delete_note(self, auth_client):
        """Test 10: Can delete a note."""
        # Create a note
        create_response = auth_client.post("/notes", json={
            "title": "To Be Deleted",
            "content": "This will be deleted"
        })
        note_id = create_response.json["note_id"]

        # Delete the note
        response = auth_client.delete(f"/notes/{note_id}")
        assert response.status_code == 200

        # Verify deletion
        get_response = auth_client.get(f"/notes/{note_id}")
        assert get_response.status_code == 404
