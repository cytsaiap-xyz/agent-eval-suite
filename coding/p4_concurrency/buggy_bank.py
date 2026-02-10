#!/usr/bin/env python3
"""
Buggy Bank System - Contains multiple race conditions
Your task: Fix all bugs while maintaining concurrency

DO NOT just add a global lock - the system must remain concurrent.
"""

import threading
import time
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    timestamp: datetime
    from_account: str
    to_account: str
    amount: float
    success: bool


class BankSystem:
    """
    A banking system with INTENTIONAL bugs.

    Bugs present:
    1. Race condition on account balances
    2. Race condition on total_money tracker
    3. Race condition on transaction log
    4. Check-then-act race in transfer
    5. Non-atomic operations

    Your task: Fix these while keeping the system concurrent.
    """

    def __init__(self):
        self.accounts: Dict[str, float] = {}
        self.transaction_log: List[Transaction] = []
        self.total_money: float = 0.0
        self._creation_count = 0

    def create_account(self, name: str, initial_balance: float) -> bool:
        """Create a new account with initial balance."""
        if name in self.accounts:
            return False

        # BUG: Race condition - check and insert not atomic
        self.accounts[name] = initial_balance

        # BUG: Race condition on total_money
        self.total_money += initial_balance
        self._creation_count += 1

        return True

    def get_balance(self, name: str) -> Optional[float]:
        """Get account balance."""
        return self.accounts.get(name)

    def transfer(self, from_account: str, to_account: str, amount: float) -> bool:
        """Transfer money between accounts."""
        # Check accounts exist
        if from_account not in self.accounts or to_account not in self.accounts:
            return False

        if from_account == to_account:
            return False

        if amount <= 0:
            return False

        # BUG: Check-then-act race condition
        # Another thread could modify balance between check and deduction
        if self.accounts[from_account] >= amount:
            # BUG: Simulated processing delay makes race more likely
            time.sleep(0.0001)

            # BUG: Not atomic - read, modify, write
            self.accounts[from_account] -= amount

            time.sleep(0.0001)

            # BUG: Same problem
            self.accounts[to_account] += amount

            # BUG: Race condition on list append
            # While append itself is atomic, the Transaction object creation
            # and timing could cause inconsistencies
            self.transaction_log.append(Transaction(
                timestamp=datetime.now(),
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                success=True
            ))

            return True

        return False

    def deposit(self, account: str, amount: float) -> bool:
        """Deposit money into account."""
        if account not in self.accounts:
            return False

        if amount <= 0:
            return False

        # BUG: Race condition
        self.accounts[account] += amount
        self.total_money += amount

        return True

    def withdraw(self, account: str, amount: float) -> bool:
        """Withdraw money from account."""
        if account not in self.accounts:
            return False

        if amount <= 0:
            return False

        # BUG: Check-then-act
        if self.accounts[account] >= amount:
            time.sleep(0.0001)
            self.accounts[account] -= amount
            self.total_money -= amount
            return True

        return False

    def audit(self) -> bool:
        """
        Verify that total money in system matches expected amount.
        Returns True if money is conserved, False if there's a discrepancy.
        """
        actual_total = sum(self.accounts.values())
        discrepancy = abs(actual_total - self.total_money)

        if discrepancy > 0.01:  # Allow tiny floating point errors
            print(f"AUDIT FAILED: Expected {self.total_money}, found {actual_total}")
            print(f"Discrepancy: {discrepancy}")
            return False

        return True

    def get_transaction_count(self) -> int:
        """Get number of successful transactions."""
        return len([t for t in self.transaction_log if t.success])

    def get_total_transferred(self) -> float:
        """Get total amount successfully transferred."""
        return sum(t.amount for t in self.transaction_log if t.success)


def stress_test(bank: BankSystem, num_transfers: int):
    """Perform random transfers."""
    accounts = list(bank.accounts.keys())
    if len(accounts) < 2:
        return

    for _ in range(num_transfers):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            amount = random.uniform(1, 50)
            bank.transfer(from_acc, to_acc, amount)


def main():
    """Demo the bugs."""
    print("Creating bank system...")
    bank = BankSystem()

    # Create accounts
    print("Creating 10 accounts with $1000 each...")
    for i in range(10):
        bank.create_account(f"user_{i}", 1000.0)

    print(f"Initial total: ${bank.total_money}")
    print(f"Initial audit: {bank.audit()}")

    # Run concurrent transfers
    print("\nRunning 100 threads with 50 transfers each...")
    threads = []
    for _ in range(100):
        t = threading.Thread(target=stress_test, args=(bank, 50))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\nFinal audit: {bank.audit()}")
    print(f"Expected total: ${bank.total_money}")
    print(f"Actual total: ${sum(bank.accounts.values())}")
    print(f"Transactions logged: {bank.get_transaction_count()}")

    if not bank.audit():
        print("\n*** BUGS DETECTED - MONEY NOT CONSERVED ***")
    else:
        print("\n*** ALL GOOD - This shouldn't happen with bugs! ***")


if __name__ == "__main__":
    main()
