#!/usr/bin/env python3
"""
Evaluation script for Problem 9: Incremental Debugging Loop
Runs tests and scores based on passing tests.
"""

import json
import subprocess
import sys
import re
from pathlib import Path


TEST_POINTS = {
    "test_health_returns_ok": 8,
    "test_register_new_user": 8,
    "test_register_duplicate_user": 8,
    "test_login_valid_credentials": 8,
    "test_login_invalid_credentials": 8,
    "test_create_note": 10,
    "test_get_notes": 10,
    "test_get_specific_note": 10,
    "test_update_note": 10,
    "test_delete_note": 10,
}


def run_tests() -> dict:
    """Run pytest and parse results."""
    result = {
        "passed": [],
        "failed": [],
        "error": None,
        "raw_output": ""
    }

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "test_app.py", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=Path(__file__).parent
        )

        result["raw_output"] = proc.stdout + proc.stderr

        # Parse passed tests
        passed_matches = re.findall(r'(test_\w+)\s+PASSED', result["raw_output"])
        result["passed"] = passed_matches

        # Parse failed tests
        failed_matches = re.findall(r'(test_\w+)\s+FAILED', result["raw_output"])
        result["failed"] = failed_matches

    except subprocess.TimeoutExpired:
        result["error"] = "Tests timed out"
    except Exception as e:
        result["error"] = str(e)

    return result


def check_bug_documentation(base_path: Path) -> dict:
    """Check if bugs were documented."""
    result = {"score": 0, "details": []}

    doc_files = ["bug_report.md", "bugs.md", "fixes.md", "BUGS.md", "bug_documentation.md"]
    doc_found = None

    for doc_file in doc_files:
        doc_path = base_path / doc_file
        if doc_path.exists():
            doc_found = doc_path
            break

    if doc_found:
        content = doc_found.read_text().lower()

        # Check for bug descriptions
        bug_keywords = ["bug", "fix", "issue", "error", "wrong", "incorrect"]
        if sum(1 for k in bug_keywords if k in content) >= 3:
            result["score"] = 10
            result["details"].append("✓ Bug documentation found")
        else:
            result["score"] = 5
            result["details"].append("◐ Bug documentation incomplete")
    else:
        result["details"].append("✗ No bug documentation file found")

    return result


def evaluate() -> dict:
    """Run full evaluation."""
    results = {
        "scores": {},
        "details": [],
        "passed_tests": [],
        "failed_tests": [],
        "total_score": 0,
        "max_score": 100
    }

    base_path = Path(__file__).parent

    # Run tests
    print("Running tests...")
    test_results = run_tests()

    if test_results["error"]:
        results["details"].append(f"✗ Error running tests: {test_results['error']}")
        return results

    results["passed_tests"] = test_results["passed"]
    results["failed_tests"] = test_results["failed"]

    # Score each test
    for test_name, points in TEST_POINTS.items():
        if test_name in test_results["passed"]:
            results["scores"][test_name] = points
            results["details"].append(f"✓ {test_name}: {points} pts")
        else:
            results["scores"][test_name] = 0
            results["details"].append(f"✗ {test_name}: 0 pts")

    # Check documentation
    print("Checking bug documentation...")
    doc_check = check_bug_documentation(base_path)
    results["scores"]["documentation"] = doc_check["score"]
    results["details"].extend(doc_check["details"])

    results["total_score"] = sum(results["scores"].values())

    # Summary
    results["details"].append("")
    results["details"].append(f"Tests passed: {len(test_results['passed'])}/10")
    results["details"].append(f"Tests failed: {len(test_results['failed'])}")

    return results


def main():
    print("=" * 60)
    print("Problem 9: Debugging Loop - Evaluation")
    print("=" * 60 + "\n")

    results = evaluate()

    print("Results:")
    for detail in results["details"]:
        print(f"  {detail}")

    print("\nScore Breakdown:")
    for category, score in results["scores"].items():
        print(f"  {category}: {score}")

    print(f"\nTotal Score: {results['total_score']}/{results['max_score']}")

    # Save results
    results_path = Path(__file__).parent / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
