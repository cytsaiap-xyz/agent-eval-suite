# Problem 4: Concurrent Bug Hunt

## Difficulty: Very Hard
## Expected Time: 45-60 minutes
## Discrimination Target: Race conditions, deadlock prevention, fine-grained locking

## Task

Fix all race conditions in the buggy bank system while maintaining concurrency.

## The Bug-Ridden Code

See `buggy_bank.py` - a banking system with multiple race conditions.

## Requirements

1. **Fix all race conditions** - money should be conserved
2. **Maintain concurrency** - don't just wrap everything in one big lock
3. **Prevent deadlocks** - transfers between accounts shouldn't deadlock
4. **Transaction log consistency** - log should match final state
5. **Bonus: Performance** - minimize lock contention

## Rules

- You MUST keep the system concurrent (multiple threads)
- You CANNOT use a single global lock that serializes everything
- The `audit()` method must always return True after all threads complete
- The transaction log must be consistent with actual transfers

## Test Cases

```bash
python evaluate_p4.py solution.py
```

The evaluator runs your solution many times with various thread counts and transfer patterns.

## Specific Bugs to Find

1. **Race on account balance** - read-modify-write not atomic
2. **Race on total_money** - multiple accounts created concurrently
3. **Race on transaction_log** - list.append is not thread-safe for consistency
4. **Check-then-act bug** - balance check and deduction not atomic
5. **Missing remaining transfers** - some transfers can be lost

## Expected Behavior After Fix

```python
bank = BankSystem()

# Create accounts
for i in range(10):
    bank.create_account(f"user_{i}", 1000.0)

# Run 1000 concurrent random transfers
threads = []
for _ in range(100):
    t = threading.Thread(target=random_transfers, args=(bank, 10))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

assert bank.audit() == True  # Total money unchanged
assert len(bank.transaction_log) == actual_transfer_count
```

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Audit passes with 2 threads | 10 |
| Audit passes with 10 threads | 15 |
| Audit passes with 100 threads | 15 |
| No deadlocks (completes in time) | 20 |
| Transaction log consistent | 15 |
| Code still concurrent (not serialized) | 15 |
| Clean, readable solution | 10 |
| **Total** | **100** |

## Hints

- Consider lock ordering to prevent deadlocks
- `threading.Lock` for mutual exclusion
- `threading.RLock` if you need reentrant locking
- Think about which operations need to be atomic
- Consider using `with lock:` context manager
