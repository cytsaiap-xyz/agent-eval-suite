#!/usr/bin/env python3
"""
Evaluation script for Problem 7: Test Generation with Coverage
Runs tests and checks coverage metrics.
"""

import json
import subprocess
import sys
from pathlib import Path


def run_tests(test_file: str) -> dict:
    """Run pytest and collect results."""
    result = {
        "passed": False,
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "error": None
    }

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=Path(test_file).parent
        )

        output = proc.stdout + proc.stderr

        # Parse results
        if "passed" in output:
            import re
            match = re.search(r'(\d+) passed', output)
            if match:
                result["tests_passed"] = int(match.group(1))

            match = re.search(r'(\d+) failed', output)
            if match:
                result["tests_failed"] = int(match.group(1))

            result["tests_run"] = result["tests_passed"] + result["tests_failed"]
            result["passed"] = result["tests_failed"] == 0 and result["tests_passed"] > 0

    except subprocess.TimeoutExpired:
        result["error"] = "Tests timed out"
    except Exception as e:
        result["error"] = str(e)

    return result


def run_coverage(test_file: str) -> dict:
    """Run coverage and get metrics."""
    result = {
        "line_coverage": 0,
        "branch_coverage": 0,
        "uncovered_lines": [],
        "error": None
    }

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", test_file,
             "--cov=scheduler", "--cov-report=term-missing", "--cov-branch"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=Path(test_file).parent
        )

        output = proc.stdout + proc.stderr

        # Parse coverage percentage
        import re

        # Look for line like: scheduler.py    300    30    90%
        match = re.search(r'scheduler(?:\.py)?\s+\d+\s+\d+\s+(\d+)%', output)
        if match:
            result["line_coverage"] = int(match.group(1))

        # Look for branch coverage
        match = re.search(r'scheduler(?:\.py)?\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)%', output)
        if match:
            result["branch_coverage"] = int(match.group(1))
        else:
            # Estimate branch coverage as slightly less than line coverage
            result["branch_coverage"] = max(0, result["line_coverage"] - 10)

        # Find uncovered lines
        match = re.search(r'Missing[^\n]*\n[^\n]*scheduler[^\n]*\s+([\d,\-\s]+)', output)
        if match:
            result["uncovered_lines"] = match.group(1).strip()

    except Exception as e:
        result["error"] = str(e)

    return result


def check_edge_cases(test_file: str) -> dict:
    """Check if specific edge cases are tested."""
    result = {
        "dst": False,
        "leap_year": False,
        "overlap": False,
        "invalid_input": False
    }

    try:
        with open(test_file) as f:
            content = f.read().lower()

        # Check for DST tests
        dst_keywords = ["dst", "daylight", "timezone", "zoneinfo", "utc"]
        result["dst"] = sum(1 for k in dst_keywords if k in content) >= 2

        # Check for leap year tests
        leap_keywords = ["leap", "feb", "february", "29", "2024"]
        result["leap_year"] = sum(1 for k in leap_keywords if k in content) >= 2

        # Check for overlap tests
        overlap_keywords = ["overlap", "conflict", "merge"]
        result["overlap"] = sum(1 for k in overlap_keywords if k in content) >= 2

        # Check for invalid input tests
        invalid_keywords = ["invalid", "error", "raise", "exception", "valueerror"]
        result["invalid_input"] = sum(1 for k in invalid_keywords if k in content) >= 2

    except Exception as e:
        pass

    return result


def evaluate(test_file: str) -> dict:
    """Run full evaluation."""
    results = {
        "scores": {},
        "details": [],
        "total_score": 0,
        "max_score": 100
    }

    # Run tests
    print("Running tests...")
    test_results = run_tests(test_file)

    if test_results["passed"]:
        results["scores"]["tests_pass"] = 20
        results["details"].append(f"✓ All {test_results['tests_passed']} tests passed")
    elif test_results["tests_passed"] > 0:
        results["scores"]["tests_pass"] = 10
        results["details"].append(f"◐ {test_results['tests_passed']}/{test_results['tests_run']} tests passed")
    else:
        results["scores"]["tests_pass"] = 0
        results["details"].append(f"✗ Tests failed: {test_results.get('error', 'No tests passed')}")

    # Run coverage
    print("Running coverage analysis...")
    coverage = run_coverage(test_file)

    # Line coverage scoring
    if coverage["line_coverage"] >= 90:
        results["scores"]["line_90"] = 10
        results["scores"]["line_80"] = 10
        results["scores"]["line_70"] = 10
        results["details"].append(f"✓ Line coverage: {coverage['line_coverage']}% (>= 90%)")
    elif coverage["line_coverage"] >= 80:
        results["scores"]["line_90"] = 0
        results["scores"]["line_80"] = 10
        results["scores"]["line_70"] = 10
        results["details"].append(f"◐ Line coverage: {coverage['line_coverage']}% (>= 80%)")
    elif coverage["line_coverage"] >= 70:
        results["scores"]["line_90"] = 0
        results["scores"]["line_80"] = 0
        results["scores"]["line_70"] = 10
        results["details"].append(f"◐ Line coverage: {coverage['line_coverage']}% (>= 70%)")
    else:
        results["scores"]["line_90"] = 0
        results["scores"]["line_80"] = 0
        results["scores"]["line_70"] = 0
        results["details"].append(f"✗ Line coverage: {coverage['line_coverage']}% (< 70%)")

    # Branch coverage scoring
    if coverage["branch_coverage"] >= 80:
        results["scores"]["branch_80"] = 10
        results["scores"]["branch_60"] = 10
        results["details"].append(f"✓ Branch coverage: {coverage['branch_coverage']}% (>= 80%)")
    elif coverage["branch_coverage"] >= 60:
        results["scores"]["branch_80"] = 0
        results["scores"]["branch_60"] = 10
        results["details"].append(f"◐ Branch coverage: {coverage['branch_coverage']}% (>= 60%)")
    else:
        results["scores"]["branch_80"] = 0
        results["scores"]["branch_60"] = 0
        results["details"].append(f"✗ Branch coverage: {coverage['branch_coverage']}% (< 60%)")

    # Edge case coverage
    print("Checking edge case coverage...")
    edge_cases = check_edge_cases(test_file)

    if edge_cases["dst"]:
        results["scores"]["dst"] = 10
        results["details"].append("✓ DST/timezone edge cases tested")
    else:
        results["scores"]["dst"] = 0
        results["details"].append("✗ DST/timezone edge cases not tested")

    if edge_cases["leap_year"]:
        results["scores"]["leap_year"] = 5
        results["details"].append("✓ Leap year edge cases tested")
    else:
        results["scores"]["leap_year"] = 0
        results["details"].append("✗ Leap year edge cases not tested")

    if edge_cases["overlap"]:
        results["scores"]["overlap"] = 10
        results["details"].append("✓ Overlap handling tested")
    else:
        results["scores"]["overlap"] = 0
        results["details"].append("✗ Overlap handling not tested")

    if edge_cases["invalid_input"]:
        results["scores"]["invalid_input"] = 5
        results["details"].append("✓ Invalid input handling tested")
    else:
        results["scores"]["invalid_input"] = 0
        results["details"].append("✗ Invalid input handling not tested")

    results["total_score"] = sum(results["scores"].values())
    results["coverage"] = coverage
    results["test_results"] = test_results

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_p7.py <test_scheduler.py>")
        sys.exit(1)

    test_file = sys.argv[1]

    print("=" * 60)
    print("Problem 7: Test Generation - Evaluation")
    print("=" * 60 + "\n")

    results = evaluate(test_file)

    print("\nResults:")
    for detail in results["details"]:
        print(f"  {detail}")

    print("\nScore Breakdown:")
    for category, score in results["scores"].items():
        print(f"  {category}: {score}")

    print(f"\nTotal Score: {results['total_score']}/{results['max_score']}")

    # Save results
    results_path = Path(test_file).parent / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
