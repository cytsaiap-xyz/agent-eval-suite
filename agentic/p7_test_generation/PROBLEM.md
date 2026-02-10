# Problem 7: Test Generation with Coverage

## Difficulty: Very Hard (Agentic)
## Expected Iterations: 10-20
## Discrimination Target: Iterative refinement, coverage analysis, edge case discovery

## Task

Create comprehensive tests for the `scheduler.py` module and achieve high coverage through iteration.

## The Module

`scheduler.py` - A complex event scheduling system with:
- Recurring events (daily, weekly, monthly)
- Timezone handling
- Conflict detection
- Event overlap merging
- Priority queues
- Snooze/dismiss logic

## Requirements

1. **Line Coverage**: Achieve >90%
2. **Branch Coverage**: Achieve >80%
3. **Tests Must Pass**: All tests green
4. **Edge Cases Required**:
   - DST transitions
   - Leap year handling
   - Overlapping events
   - Invalid inputs
   - Boundary conditions

## Process

This problem requires ITERATION:

```
1. Write initial tests
2. Run: pytest test_scheduler.py --cov=scheduler --cov-report=term-missing
3. Analyze uncovered lines
4. Add tests for uncovered code
5. Run again
6. Repeat until coverage targets met
```

## Provided Files

- `scheduler.py` - The module to test (300+ lines)
- `pytest.ini` - Pytest configuration
- `run_coverage.sh` - Script to run coverage

## Evaluation

```bash
python evaluate_p7.py test_scheduler.py
```

Checks:
- All tests pass
- Line coverage >= 90%
- Branch coverage >= 80%
- Key edge cases covered

## Scoring

| Criterion | Points |
|-----------|--------|
| Tests pass (no failures) | 20 |
| Line coverage >= 70% | 10 |
| Line coverage >= 80% | 10 |
| Line coverage >= 90% | 10 |
| Branch coverage >= 60% | 10 |
| Branch coverage >= 80% | 10 |
| DST edge cases | 10 |
| Leap year edge cases | 5 |
| Overlap handling tests | 10 |
| Invalid input tests | 5 |
| **Total** | **100** |

## Hints

- Start with happy path tests
- Use `pytest-cov` for coverage reports
- The `--cov-report=term-missing` shows uncovered lines
- Create fixtures for common setup
- Test both valid and invalid inputs
- Remember timezone edge cases
