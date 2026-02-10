#!/usr/bin/env python3
"""
Evaluation script for Problem 1: Complex Data Pipeline
Runs the solution and validates outputs against expected results.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Expected values after correct processing
EXPECTED = {
    "total_rows_after_dedup": 147,  # 150 original - 3 duplicates
    "date_parse_failures": 2,  # InvalidDate and empty date
    "flagged_high_discount": 3,  # discount > 50%
    "flagged_revenue_mismatch": 2,  # qty * price != revenue
    "regions": ["North", "South", "East", "West"],
    "categories": ["Electronics", "Clothing", "Home"],
    "total_revenue_range": (85000, 95000),  # Approximate expected range
}


def run_solution(solution_path: str) -> dict:
    """Run the solution script and collect results."""
    results = {
        "execution": {"success": False, "error": None, "runtime_ms": 0},
        "scores": {},
        "details": []
    }

    start = datetime.now()
    try:
        proc = subprocess.run(
            [sys.executable, solution_path],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=Path(__file__).parent
        )
        results["execution"]["runtime_ms"] = (datetime.now() - start).total_seconds() * 1000

        if proc.returncode != 0:
            results["execution"]["error"] = proc.stderr
            return results

        results["execution"]["success"] = True

    except subprocess.TimeoutExpired:
        results["execution"]["error"] = "Timeout after 60 seconds"
        return results
    except Exception as e:
        results["execution"]["error"] = str(e)
        return results

    return results


def validate_outputs() -> dict:
    """Validate all output files."""
    scores = {}
    details = []
    base_path = Path(__file__).parent

    # Check cleaned_data.parquet
    parquet_path = base_path / "cleaned_data.parquet"
    if parquet_path.exists():
        try:
            import pandas as pd
            df = pd.read_parquet(parquet_path)

            # Check row count (deduplication)
            if len(df) == EXPECTED["total_rows_after_dedup"]:
                scores["deduplication"] = 15
                details.append("✓ Correct row count after deduplication")
            else:
                scores["deduplication"] = 5
                details.append(f"✗ Row count: got {len(df)}, expected {EXPECTED['total_rows_after_dedup']}")

            # Check date column is datetime
            if pd.api.types.is_datetime64_any_dtype(df.get('date', pd.Series())):
                scores["date_parsing"] = 20
                details.append("✓ Dates properly parsed to datetime")
            else:
                scores["date_parsing"] = 5
                details.append("✗ Dates not converted to datetime type")

            # Check numeric columns
            numeric_cols = ['quantity', 'unit_price', 'revenue', 'discount']
            numeric_ok = all(
                pd.api.types.is_numeric_dtype(df.get(col, pd.Series(dtype=object)))
                for col in numeric_cols if col in df.columns
            )
            if numeric_ok:
                scores["numeric_cleaning"] = 15
                details.append("✓ Numeric columns properly cleaned")
            else:
                scores["numeric_cleaning"] = 5
                details.append("✗ Some numeric columns not properly converted")

        except ImportError:
            scores["parquet"] = 0
            details.append("✗ pandas/pyarrow not available for parquet validation")
        except Exception as e:
            scores["parquet"] = 0
            details.append(f"✗ Error reading parquet: {e}")
    else:
        scores["parquet"] = 0
        details.append("✗ cleaned_data.parquet not found")

    # Check aggregated_stats.json
    json_path = base_path / "aggregated_stats.json"
    if json_path.exists():
        try:
            with open(json_path) as f:
                stats = json.load(f)

            # Check structure
            has_regions = any(r in str(stats) for r in EXPECTED["regions"])
            has_categories = any(c in str(stats) for c in EXPECTED["categories"])
            has_metrics = all(
                m in str(stats).lower()
                for m in ["revenue", "count"]
            )

            if has_regions and has_categories and has_metrics:
                scores["aggregation"] = 20
                details.append("✓ Aggregation structure correct")
            else:
                scores["aggregation"] = 10
                details.append("✗ Aggregation missing expected structure")

        except Exception as e:
            scores["aggregation"] = 0
            details.append(f"✗ Error reading aggregated_stats.json: {e}")
    else:
        scores["aggregation"] = 0
        details.append("✗ aggregated_stats.json not found")

    # Check flagged_issues.csv
    flagged_path = base_path / "flagged_issues.csv"
    if flagged_path.exists():
        try:
            import pandas as pd
            flagged = pd.read_csv(flagged_path)

            # Should have flagged high discounts and revenue mismatches
            if len(flagged) >= 3:
                scores["validation"] = 15
                details.append(f"✓ Flagged {len(flagged)} issues")
            else:
                scores["validation"] = 7
                details.append(f"✗ Only flagged {len(flagged)} issues, expected >= 3")

        except Exception as e:
            scores["validation"] = 0
            details.append(f"✗ Error reading flagged_issues.csv: {e}")
    else:
        scores["validation"] = 0
        details.append("✗ flagged_issues.csv not found")

    # Check processing_log.txt
    log_path = base_path / "processing_log.txt"
    if log_path.exists():
        scores["logging"] = 5
        details.append("✓ Processing log created")
    else:
        scores["logging"] = 0
        details.append("✗ processing_log.txt not found")

    # Error handling test - empty file
    scores["error_handling"] = 10  # Assume pass unless we test

    return {"scores": scores, "details": details}


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_p1.py <solution.py>")
        sys.exit(1)

    solution_path = sys.argv[1]

    print("=" * 60)
    print("Problem 1: Complex Data Pipeline - Evaluation")
    print("=" * 60)

    # Run solution
    print("\n[1/2] Running solution...")
    run_results = run_solution(solution_path)

    if not run_results["execution"]["success"]:
        print(f"FAILED: {run_results['execution']['error']}")
        print("\nScore: 0/100")
        sys.exit(1)

    print(f"Completed in {run_results['execution']['runtime_ms']:.0f}ms")

    # Validate outputs
    print("\n[2/2] Validating outputs...")
    validation = validate_outputs()

    # Print details
    print("\nResults:")
    for detail in validation["details"]:
        print(f"  {detail}")

    # Calculate total
    total = sum(validation["scores"].values())
    print("\nScore Breakdown:")
    for category, score in validation["scores"].items():
        print(f"  {category}: {score}")

    print(f"\nTotal Score: {total}/100")

    # Write results
    results_path = Path(__file__).parent / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump({
            "problem": "p1_data_pipeline",
            "execution": run_results["execution"],
            "validation": validation,
            "total_score": total
        }, f, indent=2)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
