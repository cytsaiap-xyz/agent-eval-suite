#!/usr/bin/env python3
"""Evaluation script for P15: Multi-Format Integration"""

import json
import sys
from pathlib import Path


def evaluate(base_path: str = ".") -> dict:
    base = Path(base_path)
    results = {"scores": {}, "details": [], "total_score": 0, "max_score": 100}

    # Check extracted/ directory
    extracted_dir = base / "extracted"
    if extracted_dir.exists():
        json_files = list(extracted_dir.glob("*.json"))
        if len(json_files) >= 4:
            results["scores"]["extraction"] = 20
            results["details"].append(f"✓ {len(json_files)} extraction files")
        elif len(json_files) > 0:
            results["scores"]["extraction"] = len(json_files) * 4
            results["details"].append(f"◐ Only {len(json_files)} extraction files")
        else:
            results["scores"]["extraction"] = 0
            results["details"].append("✗ No extraction files")
    else:
        results["scores"]["extraction"] = 0
        results["details"].append("✗ extracted/ directory not found")

    # Check consolidated_data.json
    consolidated_path = base / "consolidated_data.json"
    if consolidated_path.exists():
        try:
            with open(consolidated_path) as f:
                data = json.load(f)
            if "key_metrics" in data or "metrics" in data:
                results["scores"]["consolidation"] = 20
                results["details"].append("✓ consolidated_data.json complete")
            else:
                results["scores"]["consolidation"] = 10
                results["details"].append("◐ consolidated_data.json incomplete")
        except:
            results["scores"]["consolidation"] = 0
            results["details"].append("✗ consolidated_data.json invalid")
    else:
        results["scores"]["consolidation"] = 0
        results["details"].append("✗ consolidated_data.json not found")

    # Check discrepancies.md
    disc_path = base / "discrepancies.md"
    if disc_path.exists():
        results["scores"]["discrepancies"] = 10
        results["details"].append("✓ discrepancies.md created")
    else:
        results["scores"]["discrepancies"] = 0
        results["details"].append("✗ discrepancies.md not found")

    # Check executive_summary.docx
    exec_path = base / "executive_summary.docx"
    if exec_path.exists():
        results["scores"]["exec_summary"] = 15
        results["details"].append("✓ executive_summary.docx created")
    else:
        results["scores"]["exec_summary"] = 0
        results["details"].append("✗ executive_summary.docx not found")

    # Check board_presentation.pptx
    board_path = base / "board_presentation.pptx"
    if board_path.exists():
        results["scores"]["board_pptx"] = 15
        results["details"].append("✓ board_presentation.pptx created")
    else:
        results["scores"]["board_pptx"] = 0
        results["details"].append("✗ board_presentation.pptx not found")

    # Check dashboard.xlsx
    dash_path = base / "dashboard.xlsx"
    if dash_path.exists():
        results["scores"]["dashboard"] = 15
        results["details"].append("✓ dashboard.xlsx created")
    else:
        results["scores"]["dashboard"] = 0
        results["details"].append("✗ dashboard.xlsx not found")

    # Check report_archive.pdf
    archive_path = base / "report_archive.pdf"
    if archive_path.exists():
        results["scores"]["archive"] = 5
        results["details"].append("✓ report_archive.pdf created")
    else:
        results["scores"]["archive"] = 0
        results["details"].append("✗ report_archive.pdf not found")

    results["total_score"] = sum(results["scores"].values())
    return results


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    print("=" * 60)
    print("Problem 15: Multi-Format Integration - Evaluation")
    print("=" * 60)

    results = evaluate(base_path)

    for detail in results["details"]:
        print(f"  {detail}")

    print(f"\nTotal Score: {results['total_score']}/{results['max_score']}")

    with open(Path(base_path) / "evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
