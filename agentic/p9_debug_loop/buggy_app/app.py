"""
Main Flask Application

Contains 3 bugs in route handlers.
"""

from flask import Flask, jsonify, request, session
from .models import db, User, Note
from .auth import authenticate, require_auth
from .utils import validate_note_content


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)

    # Initialize database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Routes

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/register", methods=["POST"])
    def register():
        """Register a new user."""
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        # BUG #1: Wrong comparison operator
        # Should check if user EXISTS, not if it doesn't
        existing = User.query.filter_by(username=username).first()
        if existing is None:  # BUG: Should be "if existing is not None"
            # Create user (this logic is correct)
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "User created", "user_id": user.id}), 201

        # This message is misleading due to bug
        return jsonify({"error": "Username already exists"}), 409

    @app.route("/login", methods=["POST"])
    def login():
        """Login user."""
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username, password)

        if user:
            session["user_id"] = user.id
            # BUG #2: Returning wrong status code
            return jsonify({"message": "Login successful"}), 201  # Should be 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    @app.route("/logout", methods=["POST"])
    @require_auth
    def logout():
        """Logout user."""
        session.pop("user_id", None)
        return jsonify({"message": "Logged out"}), 200

    @app.route("/notes", methods=["GET"])
    @require_auth
    def get_notes():
        """Get all notes for current user."""
        user_id = session.get("user_id")
        notes = Note.query.filter_by(user_id=user_id).all()

        return jsonify({
            "notes": [{"id": n.id, "title": n.title, "content": n.content} for n in notes]
        })

    @app.route("/notes", methods=["POST"])
    @require_auth
    def create_note():
        """Create a new note."""
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        title = data.get("title")
        content = data.get("content")

        if not title:
            return jsonify({"error": "Title required"}), 400

        # Validate content
        is_valid, error = validate_note_content(content)
        if not is_valid:
            return jsonify({"error": error}), 400

        user_id = session.get("user_id")

        # BUG #3: Wrong variable name (user_id vs userid)
        note = Note(title=title, content=content or "", userid=user_id)  # Should be user_id=user_id
        db.session.add(note)
        db.session.commit()

        return jsonify({
            "message": "Note created",
            "note_id": note.id
        }), 201

    @app.route("/notes/<int:note_id>", methods=["GET"])
    @require_auth
    def get_note(note_id):
        """Get a specific note."""
        user_id = session.get("user_id")
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()

        if not note:
            return jsonify({"error": "Note not found"}), 404

        return jsonify({
            "id": note.id,
            "title": note.title,
            "content": note.content
        })

    @app.route("/notes/<int:note_id>", methods=["PUT"])
    @require_auth
    def update_note(note_id):
        """Update a note."""
        user_id = session.get("user_id")
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()

        if not note:
            return jsonify({"error": "Note not found"}), 404

        data = request.get_json()
        if data.get("title"):
            note.title = data["title"]
        if data.get("content") is not None:
            note.content = data["content"]

        db.session.commit()

        return jsonify({"message": "Note updated"})

    @app.route("/notes/<int:note_id>", methods=["DELETE"])
    @require_auth
    def delete_note(note_id):
        """Delete a note."""
        user_id = session.get("user_id")
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()

        if not note:
            return jsonify({"error": "Note not found"}), 404

        db.session.delete(note)
        db.session.commit()

        return jsonify({"message": "Note deleted"})

    return app
