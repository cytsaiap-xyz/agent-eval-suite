#!/usr/bin/env python3
"""
Evaluation script for Problem 5: Performance Optimization
Tests correctness and performance of anagram grouping.
"""

import importlib.util
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path


def load_solution(solution_path: str):
    """Load the solution module."""
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reference_anagram_groups(words: list) -> dict:
    """Fast reference implementation for validation."""
    groups = defaultdict(list)
    for word in words:
        key = tuple(sorted(word.lower()))
        groups[key].append(word)
    return {k: sorted(v) for k, v in groups.items()}


def validate_groups(solution_groups: list, reference: dict) -> tuple:
    """Validate solution against reference. Returns (correct, error_msg)."""
    # Convert solution to comparable format
    solution_dict = {}
    for group in solution_groups:
        if group:
            key = tuple(sorted(group[0].lower()))
            solution_dict[key] = sorted(group)

    # Check all reference groups exist
    missing = []
    incorrect = []

    for key, ref_group in reference.items():
        if len(ref_group) <= 1:
            continue  # Skip singletons

        if key not in solution_dict:
            missing.append(ref_group[:3])
        elif sorted(solution_dict[key]) != sorted(ref_group):
            incorrect.append((ref_group[:3], solution_dict.get(key, [])[:3]))

    if missing or incorrect:
        return False, f"Missing: {len(missing)}, Incorrect: {len(incorrect)}"

    return True, None


def test_correctness(module, words_file: str, name: str) -> dict:
    """Test correctness on a word file."""
    result = {"passed": False, "error": None, "time_ms": 0}

    try:
        with open(words_file) as f:
            words = [line.strip() for line in f if line.strip()]

        # Get reference
        reference = reference_anagram_groups(words)

        # Run solution
        start = time.time()
        if hasattr(module, 'find_anagram_groups'):
            solution_groups = module.find_anagram_groups(words)
        elif hasattr(module, 'main'):
            # Might be a script - run as subprocess
            proc = subprocess.run(
                [sys.executable, module.__file__, words_file],
                capture_output=True, text=True, timeout=300
            )
            # Parse output - expect JSON or similar
            result["error"] = "main() function not supported, use find_anagram_groups()"
            return result
        else:
            result["error"] = "No find_anagram_groups function found"
            return result

        result["time_ms"] = (time.time() - start) * 1000

        # Validate
        correct, error = validate_groups(solution_groups, reference)
        result["passed"] = correct
        if error:
            result["error"] = error

    except Exception as e:
        result["error"] = str(e)

    return result


def test_performance(module, words_file: str, target_ms: int) -> dict:
    """Test performance on a word file."""
    result = {"passed": False, "time_ms": 0, "target_ms": target_ms}

    try:
        with open(words_file) as f:
            words = [line.strip() for line in f if line.strip()]

        start = time.time()
        module.find_anagram_groups(words)
        result["time_ms"] = (time.time() - start) * 1000

        result["passed"] = result["time_ms"] <= target_ms

    except Exception as e:
        result["error"] = str(e)

    return result


def test_unicode(module) -> dict:
    """Test Unicode handling."""
    result = {"passed": False, "error": None}

    test_words = [
        "café", "face",  # Should be grouped if accent ignored
        "naïve", "avine",
        "résumé", "resume",
        "über", "beru",
    ]

    try:
        groups = module.find_anagram_groups(test_words)

        # Check that we get reasonable groups
        # (exact behavior depends on normalization strategy)
        if len(groups) >= 1:
            result["passed"] = True
        else:
            result["error"] = "No groups found"

    except Exception as e:
        result["error"] = str(e)

    return result


def test_case_insensitive(module) -> dict:
    """Test case insensitivity."""
    result = {"passed": False, "error": None}

    test_words = ["Listen", "SILENT", "enlist", "TiNsEl"]

    try:
        groups = module.find_anagram_groups(test_words)

        # All should be in one group
        if len(groups) == 1 and len(groups[0]) == 4:
            result["passed"] = True
        else:
            result["error"] = f"Expected 1 group of 4, got {len(groups)} groups"

    except Exception as e:
        result["error"] = str(e)

    return result


def evaluate(solution_path: str) -> dict:
    """Run all evaluations."""
    results = {
        "tests": {},
        "scores": {},
        "total_score": 0,
        "max_score": 100
    }

    base_path = Path(__file__).parent

    try:
        module = load_solution(solution_path)
    except Exception as e:
        results["error"] = f"Failed to load solution: {e}"
        return results

    # Test 1: Correctness on 10K (15 pts)
    print("Test 1: Correctness on 10K words...")
    test1 = test_correctness(module, base_path / "words_10k.txt", "10k")
    results["tests"]["correctness_10k"] = test1
    if test1["passed"]:
        results["scores"]["correctness_10k"] = 15
        print(f"  ✓ Passed ({test1['time_ms']:.0f}ms)")
    else:
        results["scores"]["correctness_10k"] = 0
        print(f"  ✗ Failed: {test1.get('error')}")

    # Test 2: Correctness on 100K (15 pts)
    print("Test 2: Correctness on 100K words...")
    test2 = test_correctness(module, base_path / "words_100k.txt", "100k")
    results["tests"]["correctness_100k"] = test2
    if test2["passed"]:
        results["scores"]["correctness_100k"] = 15
        print(f"  ✓ Passed ({test2['time_ms']:.0f}ms)")
    else:
        results["scores"]["correctness_100k"] = 0
        print(f"  ✗ Failed: {test2.get('error')}")

    # Test 3: 1M in < 5 seconds (15 pts)
    print("Test 3: 1M words in < 5 seconds...")
    test3 = test_performance(module, base_path / "words_1m.txt", 5000)
    results["tests"]["perf_5s"] = test3
    if test3["passed"]:
        results["scores"]["perf_5s"] = 15
        print(f"  ✓ Passed ({test3['time_ms']:.0f}ms)")
    else:
        results["scores"]["perf_5s"] = 0
        print(f"  ✗ Failed ({test3['time_ms']:.0f}ms > 5000ms)")

    # Test 4: 1M in < 1 second (15 pts)
    print("Test 4: 1M words in < 1 second...")
    test4 = test_performance(module, base_path / "words_1m.txt", 1000)
    results["tests"]["perf_1s"] = test4
    if test4["passed"]:
        results["scores"]["perf_1s"] = 15
        print(f"  ✓ Passed ({test4['time_ms']:.0f}ms)")
    else:
        results["scores"]["perf_1s"] = 0
        print(f"  ✗ Failed ({test4['time_ms']:.0f}ms > 1000ms)")

    # Test 5: Unicode (10 pts)
    print("Test 5: Unicode handling...")
    test5 = test_unicode(module)
    results["tests"]["unicode"] = test5
    if test5["passed"]:
        results["scores"]["unicode"] = 10
        print("  ✓ Passed")
    else:
        results["scores"]["unicode"] = 0
        print(f"  ✗ Failed: {test5.get('error')}")

    # Test 6: Case insensitive (10 pts)
    print("Test 6: Case insensitivity...")
    test6 = test_case_insensitive(module)
    results["tests"]["case_insensitive"] = test6
    if test6["passed"]:
        results["scores"]["case_insensitive"] = 10
        print("  ✓ Passed")
    else:
        results["scores"]["case_insensitive"] = 0
        print(f"  ✗ Failed: {test6.get('error')}")

    # Test 7: Top 10 groups (10 pts) - requires statistics output
    print("Test 7: Statistics output...")
    if hasattr(module, 'get_statistics'):
        results["scores"]["statistics"] = 10
        print("  ✓ get_statistics() function found")
    else:
        results["scores"]["statistics"] = 5
        print("  ◐ No get_statistics() function (partial credit)")

    # Test 8: Memory efficiency (10 pts) - hard to test, give benefit of doubt
    print("Test 8: Memory efficiency...")
    results["scores"]["memory"] = 10
    print("  ◐ Assumed pass (requires manual review)")

    results["total_score"] = sum(results["scores"].values())

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_p5.py <solution.py>")
        sys.exit(1)

    solution_path = sys.argv[1]

    print("=" * 60)
    print("Problem 5: Performance Optimization - Evaluation")
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
