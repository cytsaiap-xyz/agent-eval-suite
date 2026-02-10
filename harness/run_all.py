#!/usr/bin/env python3
"""
Run all evaluations in the suite.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


PROBLEMS = {
    "coding": [
        ("p1_data_pipeline", "evaluate_p1.py", "solution.py"),
        ("p2_interpreter", "evaluate_p2.py", "interpreter.py"),
        ("p3_kanban", "evaluate_p3.py", "kanban.html"),
        ("p4_concurrency", "evaluate_p4.py", "solution.py"),
        ("p5_optimization", "evaluate_p5.py", "solution.py"),
    ],
    "agentic": [
        ("p6_codebase_archaeology", "evaluate_p6.py", "analysis_report.md"),
        ("p7_test_generation", "evaluate_p7.py", "test_scheduler.py"),
        ("p8_data_transformation", "evaluate_p8.py", "."),
        ("p9_debug_loop", "evaluate_p9.py", None),
        ("p10_markdown_converter", "evaluate_p10.py", "converter.py"),
        ("p11_docx_analysis", "evaluate_p11.py", "."),
        ("p12_pptx_generation", "evaluate_p12.py", "."),
        ("p13_xlsx_processing", "evaluate_p13.py", "."),
        ("p14_pdf_extraction", "evaluate_p14.py", "."),
        ("p15_multi_format", "evaluate_p15.py", "."),
    ]
}


def run_evaluation(category: str, problem: str, eval_script: str, solution: str) -> dict:
    """Run a single evaluation."""
    base_path = Path(__file__).parent.parent / category / problem

    result = {
        "problem": problem,
        "category": category,
        "score": 0,
        "max_score": 100,
        "status": "not_run",
        "error": None
    }

    eval_path = base_path / eval_script
    if not eval_path.exists():
        result["status"] = "missing_evaluator"
        result["error"] = f"Evaluator not found: {eval_path}"
        return result

    solution_path = base_path / solution if solution else None
    if solution_path and not solution_path.exists():
        result["status"] = "missing_solution"
        result["error"] = f"Solution not found: {solution_path}"
        return result

    try:
        cmd = [sys.executable, str(eval_path)]
        if solution:
            cmd.append(str(solution_path) if solution != "." else str(base_path))

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=base_path
        )

        # Try to find score in output
        import re
        match = re.search(r'Total Score:\s*(\d+)/(\d+)', proc.stdout)
        if match:
            result["score"] = int(match.group(1))
            result["max_score"] = int(match.group(2))
            result["status"] = "completed"
        else:
            result["status"] = "completed_no_score"
            result["output"] = proc.stdout[-500:]  # Last 500 chars

    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["error"] = "Evaluation timed out"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def main():
    print("=" * 70)
    print("AGENT EVALUATION SUITE - Full Run")
    print("=" * 70)
    print(f"Started: {datetime.now().isoformat()}\n")

    all_results = {
        "timestamp": datetime.now().isoformat(),
        "coding": [],
        "agentic": [],
        "totals": {}
    }

    for category, problems in PROBLEMS.items():
        print(f"\n{'='*40}")
        print(f" {category.upper()} PROBLEMS")
        print(f"{'='*40}\n")

        category_total = 0
        category_max = 0

        for problem, eval_script, solution in problems:
            print(f"Evaluating {problem}...")
            result = run_evaluation(category, problem, eval_script, solution)

            if result["status"] == "completed":
                print(f"  Score: {result['score']}/{result['max_score']}")
                category_total += result["score"]
            elif result["status"] == "missing_solution":
                print(f"  Skipped: No solution found")
            else:
                print(f"  Status: {result['status']}")
                if result.get("error"):
                    print(f"  Error: {result['error']}")

            category_max += result["max_score"]
            all_results[category].append(result)

        all_results["totals"][category] = {
            "score": category_total,
            "max": category_max
        }

        print(f"\n{category.upper()} Total: {category_total}/{category_max}")

    # Overall summary
    overall_score = sum(t["score"] for t in all_results["totals"].values())
    overall_max = sum(t["max"] for t in all_results["totals"].values())

    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Coding:  {all_results['totals']['coding']['score']}/{all_results['totals']['coding']['max']}")
    print(f"Agentic: {all_results['totals']['agentic']['score']}/{all_results['totals']['agentic']['max']}")
    print(f"{'='*40}")
    print(f"TOTAL:   {overall_score}/{overall_max}")
    print("=" * 70)

    # Save results
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)

    results_path = results_dir / f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
