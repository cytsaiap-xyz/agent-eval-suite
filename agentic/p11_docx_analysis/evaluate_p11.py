#!/usr/bin/env python3
"""Evaluation script for P11: Word Document Analysis"""

import json
import sys
from pathlib import Path


def evaluate(base_path: str = ".") -> dict:
    base = Path(base_path)
    results = {"scores": {}, "details": [], "total_score": 0, "max_score": 100}

    # Check document_analysis.json
    analysis_path = base / "document_analysis.json"
    if analysis_path.exists():
        try:
            with open(analysis_path) as f:
                data = json.load(f)
            if "metadata" in data and "structure" in data:
                results["scores"]["analysis"] = 25
                results["details"].append("✓ document_analysis.json complete")
            else:
                results["scores"]["analysis"] = 10
                results["details"].append("◐ document_analysis.json incomplete")
        except:
            results["scores"]["analysis"] = 0
            results["details"].append("✗ document_analysis.json invalid")
    else:
        results["scores"]["analysis"] = 0
        results["details"].append("✗ document_analysis.json not found")

    # Check table_of_contents.md
    toc_path = base / "table_of_contents.md"
    if toc_path.exists():
        content = toc_path.read_text()
        if "Table of Contents" in content or "# " in content:
            results["scores"]["toc"] = 15
            results["details"].append("✓ table_of_contents.md created")
        else:
            results["scores"]["toc"] = 5
            results["details"].append("◐ table_of_contents.md incomplete")
    else:
        results["scores"]["toc"] = 0
        results["details"].append("✗ table_of_contents.md not found")

    # Check extracted_tables.xlsx
    xlsx_path = base / "extracted_tables.xlsx"
    if xlsx_path.exists():
        results["scores"]["tables"] = 20
        results["details"].append("✓ extracted_tables.xlsx created")
    else:
        results["scores"]["tables"] = 0
        results["details"].append("✗ extracted_tables.xlsx not found")

    # Check section_summaries.json
    summaries_path = base / "section_summaries.json"
    if summaries_path.exists():
        results["scores"]["summaries"] = 20
        results["details"].append("✓ section_summaries.json created")
    else:
        results["scores"]["summaries"] = 0
        results["details"].append("✗ section_summaries.json not found")

    # Check quality_report.md
    quality_path = base / "quality_report.md"
    if quality_path.exists():
        results["scores"]["quality"] = 20
        results["details"].append("✓ quality_report.md created")
    else:
        results["scores"]["quality"] = 0
        results["details"].append("✗ quality_report.md not found")

    results["total_score"] = sum(results["scores"].values())
    return results


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    print("=" * 60)
    print("Problem 11: DOCX Analysis - Evaluation")
    print("=" * 60)

    results = evaluate(base_path)

    for detail in results["details"]:
        print(f"  {detail}")

    print(f"\nTotal Score: {results['total_score']}/{results['max_score']}")

    with open(Path(base_path) / "evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
