#!/usr/bin/env python3
"""
Evaluation script for Problem 3: Kanban Board
Static analysis + optional browser automation (if Playwright available)
"""

import json
import re
import sys
from pathlib import Path


def analyze_html(html_content: str) -> dict:
    """Analyze HTML file for required features."""
    results = {
        "scores": {},
        "details": [],
        "warnings": []
    }

    # Check for external dependencies (should be none)
    external_patterns = [
        r'<script\s+src=[\'"](http|https|//)',
        r'<link\s+.*href=[\'"](http|https|//)',
        r'import\s+.*from\s+[\'"]http',
    ]
    for pattern in external_patterns:
        if re.search(pattern, html_content, re.IGNORECASE):
            results["warnings"].append("⚠ External dependency detected - should be self-contained")

    # Check three columns
    column_patterns = [
        r'todo|to-do|to_do',
        r'in[-_\s]?progress|doing|wip',
        r'done|complete|finished'
    ]
    columns_found = sum(1 for p in column_patterns if re.search(p, html_content, re.IGNORECASE))
    if columns_found >= 3:
        results["scores"]["columns"] = 5
        results["details"].append("✓ Three columns detected")
    else:
        results["scores"]["columns"] = 0
        results["details"].append(f"✗ Only {columns_found}/3 columns detected")

    # Check drag and drop
    drag_events = ['dragstart', 'dragover', 'drop', 'dragend', 'draggable']
    drag_found = sum(1 for e in drag_events if e in html_content.lower())
    if drag_found >= 4:
        results["scores"]["drag_drop"] = 20
        results["details"].append("✓ Drag and drop events implemented")
    elif drag_found >= 2:
        results["scores"]["drag_drop"] = 10
        results["details"].append("◐ Partial drag and drop implementation")
    else:
        results["scores"]["drag_drop"] = 0
        results["details"].append("✗ Drag and drop not detected")

    # Check localStorage
    if 'localStorage' in html_content:
        if 'setItem' in html_content and 'getItem' in html_content:
            results["scores"]["persistence"] = 10
            results["details"].append("✓ LocalStorage persistence implemented")
        else:
            results["scores"]["persistence"] = 5
            results["details"].append("◐ LocalStorage mentioned but incomplete")
    else:
        results["scores"]["persistence"] = 0
        results["details"].append("✗ LocalStorage not detected")

    # Check undo/redo
    undo_patterns = ['undo', 'ctrl+z', 'ctrlz', 'meta+z']
    redo_patterns = ['redo', 'ctrl+y', 'ctrly', 'ctrl+shift+z']
    has_undo = any(p in html_content.lower() for p in undo_patterns)
    has_redo = any(p in html_content.lower() for p in redo_patterns)
    if has_undo and has_redo:
        # Check for history/stack implementation
        if re.search(r'(history|stack|undo.*stack|action.*log)', html_content, re.IGNORECASE):
            results["scores"]["undo_redo"] = 15
            results["details"].append("✓ Undo/Redo with history stack")
        else:
            results["scores"]["undo_redo"] = 10
            results["details"].append("◐ Undo/Redo detected but history unclear")
    elif has_undo:
        results["scores"]["undo_redo"] = 5
        results["details"].append("◐ Only undo detected, no redo")
    else:
        results["scores"]["undo_redo"] = 0
        results["details"].append("✗ Undo/Redo not detected")

    # Check inline editing
    edit_patterns = ['dblclick', 'double-click', 'contenteditable', 'input.*edit', 'edit.*mode']
    if any(p in html_content.lower() for p in edit_patterns):
        results["scores"]["inline_edit"] = 10
        results["details"].append("✓ Inline editing detected")
    else:
        results["scores"]["inline_edit"] = 0
        results["details"].append("✗ Inline editing not detected")

    # Check keyboard navigation
    keyboard_patterns = ['keydown', 'keyup', 'keypress', 'keyboard', 'tabindex']
    if sum(1 for p in keyboard_patterns if p in html_content.lower()) >= 2:
        results["scores"]["keyboard"] = 5
        results["details"].append("✓ Keyboard navigation detected")
    else:
        results["scores"]["keyboard"] = 0
        results["details"].append("✗ Keyboard navigation not detected")

    # Check CSS animations/transitions
    css_patterns = ['transition', 'animation', '@keyframes', 'transform']
    css_found = sum(1 for p in css_patterns if p in html_content.lower())
    if css_found >= 2:
        results["scores"]["animations"] = 10
        results["details"].append("✓ CSS animations/transitions detected")
    elif css_found >= 1:
        results["scores"]["animations"] = 5
        results["details"].append("◐ Some CSS animation detected")
    else:
        results["scores"]["animations"] = 0
        results["details"].append("✗ No CSS animations detected")

    # Check responsive design
    responsive_patterns = ['@media', 'flex', 'grid', 'min-width', 'max-width', 'viewport']
    if sum(1 for p in responsive_patterns if p in html_content.lower()) >= 2:
        results["scores"]["responsive"] = 5
        results["details"].append("✓ Responsive design detected")
    else:
        results["scores"]["responsive"] = 0
        results["details"].append("✗ Responsive design not detected")

    # Check accessibility
    a11y_patterns = ['aria-', 'role=', 'alt=', 'label']
    if sum(1 for p in a11y_patterns if p in html_content.lower()) >= 2:
        results["scores"]["accessibility"] = 5
        results["details"].append("✓ Accessibility features detected")
    else:
        results["scores"]["accessibility"] = 0
        results["details"].append("✗ Accessibility features not detected")

    # Check add functionality
    if re.search(r'add.*card|create.*card|new.*card|appendChild|insertBefore', html_content, re.IGNORECASE):
        results["scores"]["add_cards"] = 10
        results["details"].append("✓ Add card functionality detected")
    else:
        results["scores"]["add_cards"] = 0
        results["details"].append("✗ Add card functionality not detected")

    # Check delete functionality
    if re.search(r'delete|remove.*card|removeChild', html_content, re.IGNORECASE):
        results["scores"]["delete_cards"] = 5
        results["details"].append("✓ Delete card functionality detected")
    else:
        results["scores"]["delete_cards"] = 0
        results["details"].append("✗ Delete card functionality not detected")

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_p3.py <kanban.html>")
        sys.exit(1)

    html_path = Path(sys.argv[1])

    if not html_path.exists():
        print(f"Error: File not found: {html_path}")
        sys.exit(1)

    print("=" * 60)
    print("Problem 3: Kanban Board - Evaluation")
    print("=" * 60)

    html_content = html_path.read_text()

    print(f"\nAnalyzing {html_path.name} ({len(html_content)} bytes)...")

    results = analyze_html(html_content)

    # Print warnings
    if results["warnings"]:
        print("\nWarnings:")
        for warning in results["warnings"]:
            print(f"  {warning}")

    # Print details
    print("\nStatic Analysis Results:")
    for detail in results["details"]:
        print(f"  {detail}")

    # Calculate total
    total = sum(results["scores"].values())
    max_score = 100

    print("\nScore Breakdown:")
    for category, score in results["scores"].items():
        print(f"  {category}: {score}")

    print(f"\nStatic Analysis Score: {total}/{max_score}")

    print("\n" + "=" * 60)
    print("IMPORTANT: This is static analysis only.")
    print("Manual testing is required to verify actual functionality.")
    print("=" * 60)

    print("\nManual Test Checklist:")
    checklist = [
        "Page loads without console errors",
        "Can add cards to each column",
        "Can drag cards between columns",
        "Can delete cards",
        "Double-click to edit works",
        "Ctrl+Z undoes last action",
        "Ctrl+Y redoes undone action",
        "Refresh preserves cards",
        "Works on different screen sizes",
        "Keyboard navigation (Tab, Enter, Arrows)"
    ]
    for item in checklist:
        print(f"  [ ] {item}")

    # Save results
    results_path = html_path.parent / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump({
            "problem": "p3_kanban",
            "static_score": total,
            "max_score": max_score,
            "breakdown": results["scores"],
            "details": results["details"],
            "note": "Manual testing required for full evaluation"
        }, f, indent=2)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
