# Task: Debug a Flask Application Iteratively

The `buggy_app/` directory contains a Flask application with 7 hidden bugs. Fix them one by one until all 10 tests pass.

## Your Task

Fix the bugs in `buggy_app/` to make all tests in `test_app.py` pass.

**Important**: Do NOT modify `test_app.py` - only fix the application code.

## The Application

A simple note-taking API with:
- User registration and login
- Session-based authentication
- CRUD operations for notes

### Files to Fix

```
buggy_app/
├── __init__.py      # Package init
├── app.py           # Flask routes (3 bugs)
├── models.py        # Database models (2 bugs)
├── auth.py          # Authentication (1 bug)
└── utils.py         # Utility functions (1 bug)
```

## Process

This task requires iteration:

```
1. Run tests: pytest test_app.py -v
2. See which tests fail
3. Pick one failing test to investigate
4. Find and fix the bug causing it
5. Run tests again
6. Some tests may now pass, new failures may appear
7. Repeat until all 10 tests pass
```

**Important**: Some bugs mask others. You won't see all failures at first. After fixing early bugs, later tests may start failing for different reasons.

## Running Tests

```bash
# Run all tests with verbose output
pytest test_app.py -v

# Run a specific test
pytest test_app.py::TestUserLogin::test_login_valid_credentials -v

# Show more details on failures
pytest test_app.py -v --tb=long
```

## The 10 Tests

1. `test_health_returns_ok` - Health check endpoint
2. `test_register_new_user` - Can register a new user
3. `test_register_duplicate_user` - Cannot register duplicate username
4. `test_login_valid_credentials` - Can login with correct password
5. `test_login_invalid_credentials` - Cannot login with wrong password
6. `test_create_note` - Can create a note when logged in
7. `test_get_notes` - Can retrieve list of notes
8. `test_get_specific_note` - Can get a note by ID
9. `test_update_note` - Can update a note
10. `test_delete_note` - Can delete a note

## Hints for Bug Hunting

- Read error messages carefully - they often point to the exact issue
- Check for typos in variable/column names
- Look for incorrect comparison operators
- Check function argument order
- Look for mismatched key names (e.g., "user_id" vs "userid")
- Consider what happens when conditions are inverted

## Documentation (Optional)

Create `bug_report.md` documenting each bug you found:
- Which file and function
- What was wrong
- How you fixed it

## Requirements

- Flask and Flask-SQLAlchemy must be installed
- Run tests from the problem directory

```bash
pip install flask flask-sqlalchemy werkzeug pytest
```
