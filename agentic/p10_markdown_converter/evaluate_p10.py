#!/usr/bin/env python3
"""
Evaluation script for Problem 10: Markdown Converter
Runs tests and scores based on passing tests.
"""

import importlib.util
import json
import sys
from pathlib import Path


def load_converter(path: str):
    """Load the converter module."""
    spec = importlib.util.spec_from_file_location("converter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_tests(converter_path: str) -> dict:
    """Run all tests."""
    results = {
        "passed": [],
        "failed": [],
        "total": 0
    }

    try:
        converter = load_converter(converter_path)
        convert = converter.markdown_to_html
    except Exception as e:
        results["error"] = f"Failed to load converter: {e}"
        return results

    test_dir = Path(__file__).parent / "test_cases"
    md_files = sorted(test_dir.glob("*.md"))
    results["total"] = len(md_files)

    for md_file in md_files:
        test_name = md_file.stem
        html_file = md_file.with_suffix(".html")

        if not html_file.exists():
            continue

        try:
            md_content = md_file.read_text()
            expected = html_file.read_text().strip()
            actual = convert(md_content).strip()

            if actual == expected:
                results["passed"].append(test_name)
            else:
                results["failed"].append(test_name)

        except Exception as e:
            results["failed"].append(f"{test_name}: {e}")

    return results


def calculate_score(passed: int, total: int) -> int:
    """Calculate score based on tests passing."""
    if passed >= 50:
        return 100
    elif passed >= 48:
        return 80
    elif passed >= 40:
        return 60
    elif passed >= 30:
        return 40
    elif passed >= 20:
        return 20
    else:
        return 0


def evaluate(converter_path: str) -> dict:
    """Run full evaluation."""
    results = {
        "scores": {},
        "details": [],
        "total_score": 0,
        "max_score": 100
    }

    # Run tests
    print("Running tests...")
    test_results = run_tests(converter_path)

    if "error" in test_results:
        results["details"].append(f"✗ {test_results['error']}")
        return results

    passed = len(test_results["passed"])
    total = test_results["total"]

    results["passed_tests"] = test_results["passed"]
    results["failed_tests"] = test_results["failed"]

    # Calculate main score
    main_score = calculate_score(passed, total)
    results["scores"]["tests"] = main_score
    results["details"].append(f"Tests passed: {passed}/{total}")

    # Feature coverage (partial credit)
    feature_tests = {
        "headers": ["03_h1_header", "04_h2_header", "05_h3_to_h6"],
        "emphasis": ["06_bold_text", "07_italic_text", "08_bold_and_italic"],
        "links": ["10_simple_link", "11_multiple_links", "14_link_with_title"],
        "images": ["12_simple_image", "13_image_in_paragraph"],
        "lists": ["16_unordered_list", "17_ordered_list", "19_nested_unordered"],
        "code": ["09_inline_code", "26_code_block", "27_code_block_language"],
        "blockquotes": ["31_simple_blockquote", "32_multiline_blockquote"],
        "tables": ["41_simple_table", "42_table_alignment"],
    }

    for feature, tests in feature_tests.items():
        passed_feature = sum(1 for t in tests if t in test_results["passed"])
        if passed_feature == len(tests):
            results["details"].append(f"  ✓ {feature}: all tests passed")
        elif passed_feature > 0:
            results["details"].append(f"  ◐ {feature}: {passed_feature}/{len(tests)} passed")
        else:
            results["details"].append(f"  ✗ {feature}: no tests passed")

    results["total_score"] = main_score

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_p10.py <converter.py>")
        sys.exit(1)

    converter_path = sys.argv[1]

    print("=" * 60)
    print("Problem 10: Markdown Converter - Evaluation")
    print("=" * 60 + "\n")

    results = evaluate(converter_path)

    print("\nResults:")
    for detail in results["details"]:
        print(f"  {detail}")

    print(f"\nTotal Score: {results['total_score']}/{results['max_score']}")

    # Save results
    results_path = Path(converter_path).parent / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
