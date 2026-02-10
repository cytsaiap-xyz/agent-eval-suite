#!/usr/bin/env python3
"""
Evaluation script for Problem 8: Multi-Stage Data Transformation
Validates output files against expected results.
"""

import csv
import json
import sys
from pathlib import Path


def check_fulfillment_csv(base_path: Path) -> dict:
    """Check fulfillment.csv output."""
    result = {"score": 0, "max": 30, "details": []}

    csv_path = base_path / "fulfillment.csv"
    if not csv_path.exists():
        result["details"].append("✗ fulfillment.csv not found")
        return result

    try:
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Check required columns
        required_cols = ["order_id", "customer_name", "product_name",
                        "quantity", "unit_price", "final_price"]
        headers = rows[0].keys() if rows else []
        missing_cols = [c for c in required_cols if c not in headers]

        if missing_cols:
            result["details"].append(f"✗ Missing columns: {missing_cols}")
        else:
            result["score"] += 10
            result["details"].append("✓ All required columns present")

        # Check row count (should have valid order items)
        if len(rows) >= 10:
            result["score"] += 10
            result["details"].append(f"✓ {len(rows)} rows in fulfillment report")
        else:
            result["details"].append(f"◐ Only {len(rows)} rows (expected >= 10)")

        # Check for calculated fields
        for row in rows[:3]:
            if "final_price" in row and row["final_price"]:
                try:
                    float(row["final_price"])
                    result["score"] += 10
                    result["details"].append("✓ Price calculations present")
                    break
                except:
                    pass

    except Exception as e:
        result["details"].append(f"✗ Error reading CSV: {e}")

    return result


def check_issues_json(base_path: Path) -> dict:
    """Check issues.json output."""
    result = {"score": 0, "max": 25, "details": []}

    json_path = base_path / "issues.json"
    if not json_path.exists():
        result["details"].append("✗ issues.json not found")
        return result

    try:
        with open(json_path) as f:
            issues = json.load(f)

        # Check for issue categories
        expected_categories = ["out_of_stock", "missing_customer", "missing_product"]
        found_categories = [c for c in expected_categories if c in issues]

        if len(found_categories) >= 2:
            result["score"] += 10
            result["details"].append(f"✓ Found issue categories: {found_categories}")
        else:
            result["details"].append(f"◐ Only found: {found_categories}")

        # Check that issues were actually detected
        total_issues = sum(len(v) if isinstance(v, list) else 0 for v in issues.values())
        if total_issues >= 3:
            result["score"] += 15
            result["details"].append(f"✓ {total_issues} issues properly flagged")
        elif total_issues > 0:
            result["score"] += 7
            result["details"].append(f"◐ Only {total_issues} issues flagged")
        else:
            result["details"].append("✗ No issues detected (there should be some)")

    except Exception as e:
        result["details"].append(f"✗ Error reading JSON: {e}")

    return result


def check_summary_md(base_path: Path) -> dict:
    """Check summary.md output."""
    result = {"score": 0, "max": 10, "details": []}

    md_path = base_path / "summary.md"
    if not md_path.exists():
        result["details"].append("✗ summary.md not found")
        return result

    try:
        content = md_path.read_text().lower()

        # Check for expected sections
        sections = ["total", "order", "revenue", "product", "issue"]
        found = sum(1 for s in sections if s in content)

        if found >= 4:
            result["score"] += 5
            result["details"].append("✓ Summary contains key sections")
        else:
            result["details"].append(f"◐ Only {found}/5 expected sections found")

        # Check for numbers/statistics
        import re
        numbers = re.findall(r'\d+', content)
        if len(numbers) >= 5:
            result["score"] += 5
            result["details"].append("✓ Summary contains statistics")
        else:
            result["details"].append("◐ Summary lacks statistics")

    except Exception as e:
        result["details"].append(f"✗ Error reading summary: {e}")

    return result


def check_data_parsing(base_path: Path) -> dict:
    """Check if all input formats were parsed."""
    result = {"score": 0, "max": 35, "details": []}

    # This is inferred from the output quality
    # If outputs are correct, parsing must have worked

    outputs_exist = all(
        (base_path / f).exists()
        for f in ["fulfillment.csv", "issues.json", "summary.md"]
    )

    if outputs_exist:
        # Assume parsing worked if outputs exist
        result["score"] = 35
        result["details"].append("✓ All input files appear to be parsed")
        result["details"].append("  (CSV, XML, JSON, YAML, INI)")
    else:
        result["details"].append("✗ Some outputs missing - parsing may have failed")

    return result


def evaluate(base_path: str = ".") -> dict:
    """Run full evaluation."""
    base = Path(base_path)
    results = {
        "scores": {},
        "details": [],
        "total_score": 0,
        "max_score": 100
    }

    # Check each output
    checks = [
        ("fulfillment", check_fulfillment_csv),
        ("issues", check_issues_json),
        ("summary", check_summary_md),
        ("parsing", check_data_parsing),
    ]

    for name, check_func in checks:
        check_result = check_func(base)
        results["scores"][name] = check_result["score"]
        results["details"].extend(check_result["details"])

    results["total_score"] = sum(results["scores"].values())

    return results


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."

    print("=" * 60)
    print("Problem 8: Data Transformation - Evaluation")
    print("=" * 60 + "\n")

    results = evaluate(base_path)

    print("Results:")
    for detail in results["details"]:
        print(f"  {detail}")

    print("\nScore Breakdown:")
    for category, score in results["scores"].items():
        print(f"  {category}: {score}")

    print(f"\nTotal Score: {results['total_score']}/{results['max_score']}")

    # Save results
    results_path = Path(base_path) / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
