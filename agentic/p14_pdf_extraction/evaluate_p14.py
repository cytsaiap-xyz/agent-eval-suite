#!/usr/bin/env python3
"""Evaluation script for P14: PDF Extraction"""

import json
import sys
from pathlib import Path


def evaluate(base_path: str = ".") -> dict:
    base = Path(base_path)
    results = {"scores": {}, "details": [], "total_score": 0, "max_score": 100}

    # Check extracted_text.md
    text_path = base / "extracted_text.md"
    if text_path.exists():
        content = text_path.read_text()
        if len(content) > 1000:
            results["scores"]["text_extraction"] = 20
            results["details"].append(f"✓ extracted_text.md ({len(content)} chars)")
        else:
            results["scores"]["text_extraction"] = 10
            results["details"].append("◐ extracted_text.md too short")
    else:
        results["scores"]["text_extraction"] = 0
        results["details"].append("✗ extracted_text.md not found")

    # Check extracted_tables directory
    tables_dir = base / "extracted_tables"
    if tables_dir.exists() and tables_dir.is_dir():
        csv_files = list(tables_dir.glob("*.csv"))
        if len(csv_files) >= 3:
            results["scores"]["table_extraction"] = 25
            results["details"].append(f"✓ {len(csv_files)} tables extracted")
        elif len(csv_files) > 0:
            results["scores"]["table_extraction"] = len(csv_files) * 5
            results["details"].append(f"◐ Only {len(csv_files)} tables extracted")
        else:
            results["scores"]["table_extraction"] = 0
            results["details"].append("✗ No CSV files in extracted_tables/")
    else:
        results["scores"]["table_extraction"] = 0
        results["details"].append("✗ extracted_tables/ directory not found")

    # Check document_structure.json
    structure_path = base / "document_structure.json"
    if structure_path.exists():
        try:
            with open(structure_path) as f:
                data = json.load(f)
            if "sections" in data or "pages" in data:
                results["scores"]["structure"] = 15
                results["details"].append("✓ document_structure.json complete")
            else:
                results["scores"]["structure"] = 5
                results["details"].append("◐ document_structure.json incomplete")
        except:
            results["scores"]["structure"] = 0
            results["details"].append("✗ document_structure.json invalid")
    else:
        results["scores"]["structure"] = 0
        results["details"].append("✗ document_structure.json not found")

    # Check financial_summary.json
    fin_path = base / "financial_summary.json"
    if fin_path.exists():
        try:
            with open(fin_path) as f:
                data = json.load(f)
            if "revenue" in str(data).lower() or "income" in str(data).lower():
                results["scores"]["financial"] = 25
                results["details"].append("✓ financial_summary.json with data")
            else:
                results["scores"]["financial"] = 10
                results["details"].append("◐ financial_summary.json lacks data")
        except:
            results["scores"]["financial"] = 0
            results["details"].append("✗ financial_summary.json invalid")
    else:
        results["scores"]["financial"] = 0
        results["details"].append("✗ financial_summary.json not found")

    # Check search_index.json
    index_path = base / "search_index.json"
    if index_path.exists():
        results["scores"]["search_index"] = 15
        results["details"].append("✓ search_index.json created")
    else:
        results["scores"]["search_index"] = 0
        results["details"].append("✗ search_index.json not found")

    results["total_score"] = sum(results["scores"].values())
    return results


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    print("=" * 60)
    print("Problem 14: PDF Extraction - Evaluation")
    print("=" * 60)

    results = evaluate(base_path)

    for detail in results["details"]:
        print(f"  {detail}")

    print(f"\nTotal Score: {results['total_score']}/{results['max_score']}")

    with open(Path(base_path) / "evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
