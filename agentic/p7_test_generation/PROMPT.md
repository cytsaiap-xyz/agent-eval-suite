# Task: Achieve High Test Coverage Through Iteration

Write comprehensive tests for `scheduler.py` and iteratively improve them until you achieve high coverage.

## Your Task

Create `test_scheduler.py` with tests that achieve:
- **Line coverage: ≥ 90%**
- **Branch coverage: ≥ 80%**

## The Module

`scheduler.py` is a 300+ line event scheduling system with:
- Event creation with start/end times
- Recurring events (daily, weekly, monthly, yearly)
- Timezone handling
- Conflict detection between events
- Event overlap merging
- Priority queues
- Snooze and dismiss functionality
- Free slot finding

## Process

This task requires iteration:

```
1. Write initial tests
2. Run: pytest test_scheduler.py --cov=scheduler --cov-report=term-missing
3. Look at uncovered lines in the report
4. Add tests targeting those lines
5. Run coverage again
6. Repeat until targets are met
```

## Coverage Commands

```bash
# Run with coverage report showing missing lines
pytest test_scheduler.py --cov=scheduler --cov-report=term-missing

# Run with branch coverage
pytest test_scheduler.py --cov=scheduler --cov-branch --cov-report=term-missing

# Generate HTML report for detailed view
pytest test_scheduler.py --cov=scheduler --cov-report=html
```

## Required Test Categories

Your tests must cover:

### Basic Functionality
- Create events with valid parameters
- Add and remove events from scheduler
- Get events by ID
- Get events in a time range

### Edge Cases
- **DST transitions**: Events spanning daylight saving time changes
- **Leap years**: February 29th handling
- **Month boundaries**: Jan 31 + 1 month = Feb 28?
- **Year boundaries**: Recurring events across years

### Validation
- Invalid event (end before start)
- Duplicate event IDs
- Events with negative duration

### Advanced Features
- Recurring event next occurrence calculation
- Conflict detection between overlapping events
- Merging overlapping events
- Finding free time slots
- Snooze and dismiss functionality

### Priority and Filtering
- Get events by priority level
- Get events by tag
- Get upcoming events

## Example Test Structure

```python
import pytest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from scheduler import Scheduler, Event, EventPriority, RecurrenceType

@pytest.fixture
def scheduler():
    return Scheduler()

@pytest.fixture
def sample_event():
    return Event(
        id="test-1",
        title="Test Event",
        start=datetime(2024, 1, 15, 10, 0, tzinfo=ZoneInfo("UTC")),
        end=datetime(2024, 1, 15, 11, 0, tzinfo=ZoneInfo("UTC"))
    )

class TestEventCreation:
    def test_create_valid_event(self):
        ...

    def test_event_end_before_start_raises(self):
        ...

class TestRecurrence:
    def test_daily_recurrence(self):
        ...

    def test_monthly_recurrence_end_of_month(self):
        # Jan 31 + 1 month should be Feb 28 (or 29 in leap year)
        ...
```

## Tips

- Start with simple happy-path tests
- Use pytest fixtures for common setup
- The `--cov-report=term-missing` output shows exactly which lines need coverage
- Branch coverage requires testing both True and False paths of conditionals
- Don't forget to test error conditions (exceptions)
