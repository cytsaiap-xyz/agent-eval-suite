#!/usr/bin/env python3
"""
Test runner for Markdown converter.
Shows which tests pass/fail with diffs.
"""

import importlib.util
import sys
from pathlib import Path
from difflib import unified_diff


def load_converter(path: str):
    """Load the converter module."""
    spec = importlib.util.spec_from_file_location("converter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_tests(converter_path: str = "converter.py") -> dict:
    """Run all tests and return results."""
    results = {
        "passed": [],
        "failed": [],
        "errors": [],
        "total": 0
    }

    try:
        converter = load_converter(converter_path)
        convert = converter.markdown_to_html
    except Exception as e:
        print(f"Error loading converter: {e}")
        return results

    test_dir = Path(__file__).parent / "test_cases"
    md_files = sorted(test_dir.glob("*.md"))

    results["total"] = len(md_files)

    for md_file in md_files:
        test_name = md_file.stem
        html_file = md_file.with_suffix(".html")

        if not html_file.exists():
            results["errors"].append(f"{test_name}: Expected HTML file not found")
            continue

        try:
            md_content = md_file.read_text()
            expected = html_file.read_text()

            actual = convert(md_content)

            # Normalize whitespace for comparison
            actual_norm = actual.strip()
            expected_norm = expected.strip()

            if actual_norm == expected_norm:
                results["passed"].append(test_name)
                print(f"✓ {test_name}")
            else:
                results["failed"].append(test_name)
                print(f"✗ {test_name}")

                # Show diff
                diff = list(unified_diff(
                    expected_norm.split('\n'),
                    actual_norm.split('\n'),
                    fromfile='expected',
                    tofile='actual',
                    lineterm=''
                ))
                if diff:
                    print("  Diff:")
                    for line in diff[:10]:  # Limit diff output
                        print(f"    {line}")
                    if len(diff) > 10:
                        print(f"    ... ({len(diff) - 10} more lines)")

        except Exception as e:
            results["errors"].append(f"{test_name}: {str(e)}")
            print(f"✗ {test_name}: Error - {e}")

    return results


def main():
    converter_path = sys.argv[1] if len(sys.argv) > 1 else "converter.py"

    print("=" * 60)
    print("Markdown Converter - Test Runner")
    print("=" * 60 + "\n")

    results = run_tests(converter_path)

    print("\n" + "=" * 60)
    print(f"Results: {len(results['passed'])}/{results['total']} passed")

    if results['failed']:
        print(f"\nFailed tests: {', '.join(results['failed'][:5])}")
        if len(results['failed']) > 5:
            print(f"  ... and {len(results['failed']) - 5} more")

    if results['errors']:
        print(f"\nErrors: {len(results['errors'])}")
        for error in results['errors'][:3]:
            print(f"  {error}")


if __name__ == "__main__":
    main()
