#!/usr/bin/env python3
"""
Evaluation script for Problem 6: Codebase Archaeology
Checks the analysis report against expected findings.
"""

import json
import re
import sys
from pathlib import Path


def load_expected():
    """Load expected answers."""
    expected_path = Path(__file__).parent / "expected_answers.json"
    with open(expected_path) as f:
        return json.load(f)


def check_dependency_graph(content: str, expected: dict) -> tuple:
    """Check if dependency graph is covered."""
    score = 0
    max_score = 20
    details = []

    # Check for key import relationships
    key_imports = [
        ("main.py", "core.engine"),
        ("main.py", "config.settings"),
        ("core/engine.py", "core.processor"),
        ("core/processor.py", "core.engine"),
    ]

    found = 0
    for file, imports in key_imports:
        if file in content and imports in content:
            found += 1

    if found >= 3:
        score = 15
        details.append(f"✓ Found {found}/4 key dependencies")
    else:
        score = found * 3
        details.append(f"◐ Only found {found}/4 key dependencies")

    # Check for circular import mention
    if "circular" in content.lower():
        score += 5
        details.append("✓ Circular imports identified")
    else:
        details.append("✗ Circular imports not mentioned")

    return score, details


def check_dead_code(content: str, expected: dict) -> tuple:
    """Check dead code analysis."""
    score = 0
    max_score = 20
    details = []

    # Check for dead file identification
    dead_files = ["cache.py", "formatting.py", "old_processor.py", "deprecated.py"]
    files_found = sum(1 for f in dead_files if f in content)

    if files_found >= 3:
        score += 10
        details.append(f"✓ Identified {files_found}/4 dead code files")
    else:
        score += files_found * 2
        details.append(f"◐ Only identified {files_found}/4 dead code files")

    # Check for dead function identification
    dead_funcs = ["unused_init_function", "unused_main_helper", "unused_engine_helper",
                  "deprecated_transform", "validate_database_config"]
    funcs_found = sum(1 for f in dead_funcs if f in content)

    if funcs_found >= 3:
        score += 10
        details.append(f"✓ Identified {funcs_found}/5 key dead functions")
    else:
        score += funcs_found * 2
        details.append(f"◐ Only identified {funcs_found}/5 key dead functions")

    return score, details


def check_duplication(content: str, expected: dict) -> tuple:
    """Check duplication report."""
    score = 0
    max_score = 15
    details = []

    duplicates = [
        ("format_output", "indent"),
        ("parse_response", "None"),
        ("is_valid_email", "regex"),
    ]

    found = 0
    for func, diff_hint in duplicates:
        if func in content:
            found += 1

    if found >= 2:
        score = 10 + (found - 2) * 5
        details.append(f"✓ Found {found}/3 duplicated functions")
    else:
        score = found * 5
        details.append(f"◐ Only found {found}/3 duplicated functions")

    return min(score, max_score), details


def check_configuration(content: str, expected: dict) -> tuple:
    """Check configuration audit."""
    score = 0
    max_score = 15
    details = []

    config_sources = ["DEFAULTS", "yaml", "json", "local_settings", "environment", "env"]
    sources_found = sum(1 for s in config_sources if s.lower() in content.lower())

    if sources_found >= 4:
        score = 10
        details.append(f"✓ Identified multiple config sources")
    else:
        score = sources_found * 2
        details.append(f"◐ Only identified {sources_found} config sources")

    # Check for precedence/priority mention
    if "priority" in content.lower() or "precedence" in content.lower() or "order" in content.lower():
        score += 5
        details.append("✓ Config precedence discussed")
    else:
        details.append("✗ Config precedence not discussed")

    return min(score, max_score), details


def check_bugs(content: str, expected: dict) -> tuple:
    """Check bug identification."""
    score = 0
    max_score = 20
    details = []

    bug_hints = [
        ("deep_merge", "mutate", "copy"),
        ("load_config", "order", "backwards", "priority"),
        ("parse_response", "None", "inconsistent"),
    ]

    found = 0
    for hints in bug_hints:
        if any(h.lower() in content.lower() for h in hints):
            found += 1

    score = found * 7
    if found >= 2:
        details.append(f"✓ Found {found}/3 bugs")
    else:
        details.append(f"◐ Only found {found}/3 bugs")

    return min(score, max_score), details


def check_refactoring(content: str, expected: dict) -> tuple:
    """Check refactoring plan."""
    score = 0
    max_score = 10
    details = []

    # Check for refactoring keywords
    refactor_keywords = ["refactor", "cleanup", "remove", "delete", "consolidate", "merge"]
    found = sum(1 for k in refactor_keywords if k in content.lower())

    if found >= 3:
        score = 7
        details.append("✓ Refactoring plan included")
    else:
        score = found * 2
        details.append("◐ Limited refactoring suggestions")

    # Check for priority/order
    if "priority" in content.lower() or "first" in content.lower() or "order" in content.lower():
        score += 3
        details.append("✓ Priority order suggested")

    return min(score, max_score), details


def evaluate_report(report_path: str) -> dict:
    """Evaluate the analysis report."""
    results = {
        "scores": {},
        "details": [],
        "total_score": 0,
        "max_score": 100
    }

    try:
        with open(report_path) as f:
            content = f.read()
    except Exception as e:
        results["error"] = f"Failed to read report: {e}"
        return results

    expected = load_expected()

    # Run all checks
    checks = [
        ("dependency_graph", check_dependency_graph, 20),
        ("dead_code", check_dead_code, 20),
        ("duplication", check_duplication, 15),
        ("configuration", check_configuration, 15),
        ("bugs", check_bugs, 20),
        ("refactoring", check_refactoring, 10),
    ]

    for name, check_func, max_pts in checks:
        score, details = check_func(content, expected)
        results["scores"][name] = score
        results["details"].extend(details)

    results["total_score"] = sum(results["scores"].values())

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_p6.py <analysis_report.md>")
        sys.exit(1)

    report_path = sys.argv[1]

    print("=" * 60)
    print("Problem 6: Codebase Archaeology - Evaluation")
    print("=" * 60 + "\n")

    results = evaluate_report(report_path)

    if "error" in results:
        print(f"Error: {results['error']}")
        sys.exit(1)

    print("Results:")
    for detail in results["details"]:
        print(f"  {detail}")

    print("\nScore Breakdown:")
    for category, score in results["scores"].items():
        print(f"  {category}: {score}")

    print(f"\nTotal Score: {results['total_score']}/{results['max_score']}")

    # Save results
    results_path = Path(report_path).parent / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
