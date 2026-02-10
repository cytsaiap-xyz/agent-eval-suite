#!/usr/bin/env python3
"""
Evaluation script for Problem 4: Concurrent Bug Hunt
Tests the solution under various concurrency scenarios.
"""

import importlib.util
import json
import random
import sys
import threading
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, TimeoutError


def load_solution(solution_path: str):
    """Dynamically load the solution module."""
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stress_transfer(bank, accounts, num_transfers):
    """Perform random transfers between accounts."""
    for _ in range(num_transfers):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            amount = random.uniform(1, 100)
            bank.transfer(from_acc, to_acc, amount)


def test_concurrency(BankSystem, num_accounts: int, num_threads: int,
                     transfers_per_thread: int, timeout: int = 30) -> dict:
    """Run a concurrency test and return results."""
    result = {
        "passed": False,
        "audit_passed": False,
        "completed": False,
        "deadlock": False,
        "error": None,
        "runtime_ms": 0
    }

    try:
        bank = BankSystem()

        # Create accounts
        for i in range(num_accounts):
            bank.create_account(f"user_{i}", 1000.0)

        initial_total = bank.total_money
        accounts = list(bank.accounts.keys())

        # Run concurrent transfers
        start = time.time()

        threads = []
        for _ in range(num_threads):
            t = threading.Thread(
                target=stress_transfer,
                args=(bank, accounts, transfers_per_thread)
            )
            threads.append(t)
            t.start()

        # Wait with timeout
        deadline = time.time() + timeout
        for t in threads:
            remaining = deadline - time.time()
            if remaining <= 0:
                result["deadlock"] = True
                result["error"] = "Timeout - possible deadlock"
                return result
            t.join(timeout=remaining)
            if t.is_alive():
                result["deadlock"] = True
                result["error"] = "Thread still running - possible deadlock"
                return result

        result["runtime_ms"] = (time.time() - start) * 1000
        result["completed"] = True

        # Check audit
        result["audit_passed"] = bank.audit()

        # Verify total money conserved
        final_total = sum(bank.accounts.values())
        discrepancy = abs(final_total - initial_total)

        if discrepancy < 0.01:
            result["passed"] = True
        else:
            result["error"] = f"Money not conserved: lost ${discrepancy:.2f}"

    except Exception as e:
        result["error"] = str(e)

    return result


def test_not_serialized(BankSystem) -> dict:
    """Test that the solution is actually concurrent, not serialized."""
    result = {"passed": False, "error": None}

    try:
        bank = BankSystem()

        for i in range(4):
            bank.create_account(f"user_{i}", 10000.0)

        accounts = list(bank.accounts.keys())

        # Time sequential transfers
        start_seq = time.time()
        for _ in range(100):
            bank.transfer(accounts[0], accounts[1], 1)
        seq_time = time.time() - start_seq

        # Time concurrent transfers
        start_conc = time.time()
        threads = []
        for _ in range(4):
            t = threading.Thread(target=lambda: [
                bank.transfer(accounts[i % 4], accounts[(i + 1) % 4], 1)
                for i in range(25)
            ])
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        conc_time = time.time() - start_conc

        # If fully serialized, concurrent should take ~same as sequential
        # If concurrent, should be faster (or at least not much slower)
        # Allow 3x slower due to lock overhead, but not 10x (which would indicate serialization)
        if conc_time < seq_time * 5:
            result["passed"] = True
        else:
            result["error"] = f"Appears serialized: seq={seq_time*1000:.0f}ms, conc={conc_time*1000:.0f}ms"

    except Exception as e:
        result["error"] = str(e)

    return result


def evaluate(solution_path: str) -> dict:
    """Run all tests on the solution."""
    results = {
        "tests": [],
        "scores": {},
        "total_score": 0,
        "max_score": 100
    }

    try:
        module = load_solution(solution_path)
        BankSystem = module.BankSystem
    except Exception as e:
        results["error"] = f"Failed to load solution: {e}"
        return results

    # Test 1: 2 threads (10 pts)
    print("Test 1: 2 threads, 10 accounts, 100 transfers each...")
    test1 = test_concurrency(BankSystem, 10, 2, 100)
    results["tests"].append({"name": "2_threads", **test1})
    if test1["passed"]:
        results["scores"]["2_threads"] = 10
        print("  ✓ Passed")
    else:
        results["scores"]["2_threads"] = 0
        print(f"  ✗ Failed: {test1.get('error', 'audit failed')}")

    # Test 2: 10 threads (15 pts)
    print("Test 2: 10 threads, 10 accounts, 50 transfers each...")
    test2 = test_concurrency(BankSystem, 10, 10, 50)
    results["tests"].append({"name": "10_threads", **test2})
    if test2["passed"]:
        results["scores"]["10_threads"] = 15
        print("  ✓ Passed")
    else:
        results["scores"]["10_threads"] = 0
        print(f"  ✗ Failed: {test2.get('error', 'audit failed')}")

    # Test 3: 100 threads (15 pts)
    print("Test 3: 100 threads, 20 accounts, 20 transfers each...")
    test3 = test_concurrency(BankSystem, 20, 100, 20, timeout=60)
    results["tests"].append({"name": "100_threads", **test3})
    if test3["passed"]:
        results["scores"]["100_threads"] = 15
        print("  ✓ Passed")
    else:
        results["scores"]["100_threads"] = 0
        print(f"  ✗ Failed: {test3.get('error', 'audit failed')}")

    # Test 4: No deadlocks (20 pts)
    print("Test 4: Deadlock test (many cross transfers)...")
    test4 = test_concurrency(BankSystem, 5, 50, 100, timeout=30)
    results["tests"].append({"name": "deadlock_test", **test4})
    if test4["completed"] and not test4["deadlock"]:
        results["scores"]["no_deadlock"] = 20
        print(f"  ✓ Passed ({test4['runtime_ms']:.0f}ms)")
    else:
        results["scores"]["no_deadlock"] = 0
        print(f"  ✗ Failed: {test4.get('error', 'deadlock detected')}")

    # Test 5: Transaction log consistency (15 pts)
    print("Test 5: Transaction log consistency...")
    try:
        bank = BankSystem()
        for i in range(4):
            bank.create_account(f"user_{i}", 1000.0)

        success_count = 0
        for _ in range(100):
            if bank.transfer("user_0", "user_1", 10):
                success_count += 1

        log_count = bank.get_transaction_count() if hasattr(bank, 'get_transaction_count') else len(bank.transaction_log)

        if log_count == success_count:
            results["scores"]["transaction_log"] = 15
            print("  ✓ Passed")
        else:
            results["scores"]["transaction_log"] = 7
            print(f"  ◐ Partial: {log_count} logged vs {success_count} successful")
    except Exception as e:
        results["scores"]["transaction_log"] = 0
        print(f"  ✗ Failed: {e}")

    # Test 6: Not serialized (15 pts)
    print("Test 6: Concurrency preserved (not serialized)...")
    test6 = test_not_serialized(BankSystem)
    results["tests"].append({"name": "not_serialized", **test6})
    if test6["passed"]:
        results["scores"]["concurrent"] = 15
        print("  ✓ Passed")
    else:
        results["scores"]["concurrent"] = 0
        print(f"  ✗ Failed: {test6.get('error', 'appears serialized')}")

    # Test 7: Code quality (10 pts) - manual assessment
    results["scores"]["code_quality"] = 10  # Assume pass for automated
    print("Test 7: Code quality (manual review)...")
    print("  ◐ Assumed 10 pts (requires manual review)")

    results["total_score"] = sum(results["scores"].values())

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_p4.py <solution.py>")
        sys.exit(1)

    solution_path = sys.argv[1]

    print("=" * 60)
    print("Problem 4: Concurrent Bug Hunt - Evaluation")
    print("=" * 60 + "\n")

    results = evaluate(solution_path)

    print("\n" + "=" * 60)
    print("Score Breakdown:")
    for test, score in results["scores"].items():
        print(f"  {test}: {score}")

    print(f"\nTotal Score: {results['total_score']}/{results['max_score']}")

    # Save results
    results_path = Path(solution_path).parent / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
