#!/usr/bin/env python3
"""
Slow Anagram Grouping - O(n²) reference implementation
This is INTENTIONALLY slow. Your task is to optimize it.
"""

import sys
from typing import List


def find_anagram_groups(words: List[str]) -> List[List[str]]:
    """
    Group words that are anagrams of each other.

    Current complexity: O(n²) - compares every pair
    Target complexity: O(n * k log k) where k is word length

    This implementation is correct but way too slow for large inputs.
    """
    groups = []
    used = set()

    for i, w1 in enumerate(words):
        if i in used:
            continue

        # Normalize for comparison
        w1_lower = w1.lower()
        w1_sorted = sorted(w1_lower)

        group = [w1]

        for j, w2 in enumerate(words[i + 1:], i + 1):
            if j in used:
                continue

            w2_lower = w2.lower()

            # O(k log k) comparison for each pair = O(n² * k log k) total!
            if sorted(w2_lower) == w1_sorted:
                group.append(w2)
                used.add(j)

        groups.append(group)

    return groups


def main():
    if len(sys.argv) < 2:
        print("Usage: python slow_anagrams.py <words.txt>")
        sys.exit(1)

    input_file = sys.argv[1]

    print(f"Reading {input_file}...")
    with open(input_file) as f:
        words = [line.strip() for line in f if line.strip()]

    print(f"Processing {len(words)} words...")
    print("WARNING: This is O(n²) and will be very slow!")

    import time
    start = time.time()
    groups = find_anagram_groups(words)
    elapsed = time.time() - start

    print(f"Found {len(groups)} groups in {elapsed:.2f} seconds")

    # Find largest groups
    groups.sort(key=len, reverse=True)
    print("\nTop 5 largest anagram groups:")
    for i, group in enumerate(groups[:5]):
        print(f"  {i + 1}. ({len(group)} words): {group[:5]}{'...' if len(group) > 5 else ''}")


if __name__ == "__main__":
    main()
