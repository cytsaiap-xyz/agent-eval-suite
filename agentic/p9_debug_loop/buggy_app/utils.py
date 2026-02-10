"""
Utility Functions

Contains 1 bug in validation.
"""

MAX_CONTENT_LENGTH = 10000  # Maximum note content length


def validate_note_content(content):
    """
    Validate note content.

    Returns (is_valid, error_message)
    """
    if content is None:
        return True, None

    if not isinstance(content, str):
        return False, "Content must be a string"

    # BUG #7: Wrong comparison (< instead of >)
    # Should reject content that EXCEEDS max length
    if len(content) < MAX_CONTENT_LENGTH:  # Should be: len(content) > MAX_CONTENT_LENGTH
        return False, f"Content exceeds maximum length of {MAX_CONTENT_LENGTH} characters"

    return True, None


def sanitize_input(text):
    """Sanitize text input."""
    if not text:
        return ""

    # Remove leading/trailing whitespace
    text = text.strip()

    # Basic HTML escape (not comprehensive - just for demo)
    text = text.replace("<", "&lt;").replace(">", "&gt;")

    return text


def generate_slug(title):
    """Generate URL-friendly slug from title."""
    if not title:
        return ""

    # Convert to lowercase
    slug = title.lower()

    # Replace spaces with hyphens
    slug = slug.replace(" ", "-")

    # Remove non-alphanumeric characters (except hyphens)
    slug = "".join(c for c in slug if c.isalnum() or c == "-")

    # Remove consecutive hyphens
    while "--" in slug:
        slug = slug.replace("--", "-")

    return slug.strip("-")
