# Task: Fix Race Conditions in Banking System

You are given `buggy_bank.py` - a multi-threaded banking system with several race conditions. Fix all the bugs while keeping the system concurrent.

## Your Task

Create `solution.py` with a fixed version of the `BankSystem` class.

## The Problem

The current implementation has these race conditions:
1. Account balance updates are not atomic
2. Total money tracking has race conditions
3. Transaction log can become inconsistent
4. Check-then-act pattern in transfers is not atomic
5. Multiple accounts can be modified without proper synchronization

## Requirements

### Must Fix
- The `audit()` method must always return `True` after all threads complete
- Money must be conserved (total money in system never changes)
- Transaction log must accurately reflect all successful transfers

### Must Maintain
- System must remain **concurrent** (multiple transfers can happen in parallel)
- **Do NOT** use a single global lock that serializes everything
- Use fine-grained locking for better performance

### Must Avoid
- Deadlocks - the system must always complete (no hanging)
- Lost updates - all transfers must be properly recorded

## Testing

Run the stress test:
```bash
python solution.py
```

The test creates 10 accounts with $1000 each, runs 100 threads doing 50 random transfers each, then audits. The audit must pass.

## Hints

- Consider lock ordering to prevent deadlocks (always lock lower account ID first)
- Use `threading.Lock()` for mutual exclusion
- The `with lock:` context manager ensures proper release
- Think about which operations need to be atomic together
- Consider using per-account locks instead of global locks

## Example Structure

```python
class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.transaction_log = []
        self.total_money = 0.0
        # Add your synchronization primitives here

    def create_account(self, name: str, initial: float) -> bool:
        # Thread-safe account creation
        ...

    def transfer(self, from_acc: str, to_acc: str, amount: float) -> bool:
        # Thread-safe transfer with deadlock prevention
        ...

    def audit(self) -> bool:
        # Verify total money is conserved
        ...
```

## Evaluation Criteria

- Audit passes with 2, 10, and 100 concurrent threads
- No deadlocks (completes within timeout)
- Transaction log is consistent
- System is actually concurrent (not fully serialized)
