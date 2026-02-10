# Problem 9: Incremental Debugging Loop

## Difficulty: Very Hard (Agentic)
## Expected Iterations: 15-30
## Discrimination Target: Iterative debugging, root cause analysis, regression prevention

## Task

Debug a Flask application with 7 interconnected bugs. You must iterate:
fix → test → analyze → fix more.

## The Bug-Ridden App

`buggy_app/` contains a small Flask application with:
- User authentication
- Note-taking API
- Session management
- Database operations

## The Bugs

There are exactly 7 bugs hidden across:
- Route handlers (3 bugs)
- Database queries (2 bugs)
- Template/response handling (1 bug)
- Session handling (1 bug)

**Important**: Some bugs mask others. You won't see all failures until earlier bugs are fixed.

## Test Suite

`test_app.py` contains 10 test cases. All must pass.

## Process

```
1. Run: pytest test_app.py -v
2. Observe failures (initially ~5-7 will fail)
3. Pick one failing test
4. Investigate the cause
5. Fix the bug
6. Re-run tests
7. Observe: some tests may now pass, new failures may appear
8. Repeat until all 10 tests pass
```

## Rules

- You MUST run tests after each fix to verify
- Document each bug found and the fix applied
- Do not modify test_app.py
- Keep fixes minimal - don't refactor

## Files

```
buggy_app/
├── __init__.py
├── app.py          # Main Flask app
├── models.py       # Database models
├── auth.py         # Authentication
└── utils.py        # Utility functions
test_app.py         # Test suite (DO NOT MODIFY)
```

## Evaluation

```bash
python evaluate_p9.py
```

## Scoring

| Criterion | Points |
|-----------|--------|
| Test 1 passes | 8 |
| Test 2 passes | 8 |
| Test 3 passes | 8 |
| Test 4 passes | 8 |
| Test 5 passes | 8 |
| Test 6 passes | 10 |
| Test 7 passes | 10 |
| Test 8 passes | 10 |
| Test 9 passes | 10 |
| Test 10 passes | 10 |
| Bug documentation | 10 |
| **Total** | **100** |

## Hints

- Start with the simplest failing test
- Read error messages carefully
- Check for typos in variable names
- Look for off-by-one errors
- Session/state bugs often appear as intermittent failures
- Database bugs might cause cascade failures
