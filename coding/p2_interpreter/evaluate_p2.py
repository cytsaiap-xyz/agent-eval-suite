#!/usr/bin/env python3
"""
Evaluation script for Problem 2: Calculator Interpreter
Tests various features and edge cases.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path


TESTS = [
    # (description, code, expected_outputs, points, category)

    # Basic arithmetic (10 pts)
    ("simple addition", "print 2 + 3", ["5"], 2, "arithmetic"),
    ("operator precedence", "print 2 + 3 * 4", ["14"], 2, "arithmetic"),
    ("parentheses", "print (2 + 3) * 4", ["20"], 2, "arithmetic"),
    ("subtraction and negation", "print 10 - 3\nprint -5 + 10", ["7", "5"], 2, "arithmetic"),
    ("division and modulo", "print 10 / 2\nprint 10 % 3", ["5", "1"], 2, "arithmetic"),

    # Variables (10 pts)
    ("variable declaration", "let x = 5\nprint x", ["5"], 3, "variables"),
    ("variable expression", "let x = 5\nlet y = x + 3\nprint y", ["8"], 3, "variables"),
    ("multiple variables", "let a = 1\nlet b = 2\nlet c = 3\nprint a + b + c", ["6"], 4, "variables"),

    # Functions (15 pts)
    ("simple function", "fn double(x) = x * 2\nprint double(5)", ["10"], 3, "functions"),
    ("two params", "fn add(a, b) = a + b\nprint add(3, 4)", ["7"], 3, "functions"),
    ("nested calls", "fn f(x) = x + 1\nfn g(x) = x * 2\nprint g(f(3))", ["8"], 3, "functions"),
    ("function with vars", "let base = 10\nfn addBase(x) = x + base\nprint addBase(5)", ["15"], 3, "functions"),
    ("composed", "fn sq(x) = x * x\nfn dbl(x) = x * 2\nprint dbl(sq(3))", ["18"], 3, "functions"),

    # Recursion (10 pts)
    ("factorial base", "fn fact(n) = if n <= 1 then 1 else n * fact(n - 1)\nprint fact(1)", ["1"], 2, "recursion"),
    ("factorial 5", "fn fact(n) = if n <= 1 then 1 else n * fact(n - 1)\nprint fact(5)", ["120"], 3, "recursion"),
    ("factorial 10", "fn fact(n) = if n <= 1 then 1 else n * fact(n - 1)\nprint fact(10)", ["3628800"], 2, "recursion"),
    ("fibonacci", "fn fib(n) = if n <= 1 then n else fib(n-1) + fib(n-2)\nprint fib(10)", ["55"], 3, "recursion"),

    # Conditionals (10 pts)
    ("if true branch", "print if 5 > 3 then 1 else 0", ["1"], 2, "conditionals"),
    ("if false branch", "print if 3 > 5 then 1 else 0", ["0"], 2, "conditionals"),
    ("if equality", "print if 5 == 5 then 100 else 0", ["100"], 2, "conditionals"),
    ("nested if", "let x = 5\nprint if x > 3 then if x > 10 then 2 else 1 else 0", ["1"], 2, "conditionals"),
    ("if with expressions", "let a = 10\nlet b = 20\nprint if a < b then a + b else a - b", ["30"], 2, "conditionals"),

    # Closures (5 pts)
    ("closure capture", "let x = 10\nfn addX(y) = x + y\nlet x = 20\nprint addX(5)", ["15"], 5, "closures"),

    # Full program test (15 pts)
    ("full program", """
let x = 10
let y = 3
print x + y * 2
print (x + y) * 2
fn double(n) = n * 2
fn square(n) = n * n
print double(5)
print square(4)
print double(square(3))
fn factorial(n) = if n <= 1 then 1 else n * factorial(n - 1)
print factorial(5)
print factorial(10)
fn fib(n) = if n <= 1 then n else fib(n-1) + fib(n-2)
print fib(10)
fn add(a, b) = a + b
fn mult(a, b) = a * b
print add(3, 4)
print mult(add(2, 3), 4)
let base = 100
fn addBase(n) = n + base
print addBase(50)
let a = 5
let b = 10
print if a < b then 1 else 0
print if a > b then 1 else 0
""", ["16", "26", "10", "16", "18", "120", "3628800", "55", "7", "20", "150", "1", "0"], 15, "full_program"),
]

ERROR_TESTS = [
    # (description, code, should_contain, points, category)
    ("undefined variable", "print undefined_var", ["undefined", "error"], 3, "errors"),
    ("undefined function", "print notFunc(5)", ["undefined", "error"], 3, "errors"),
    ("division by zero", "print 10 / 0", ["division", "zero", "error"], 3, "errors"),
    ("syntax error", "let x = = 5", ["syntax", "error"], 3, "errors"),
    ("wrong arg count", "fn add(a, b) = a + b\nprint add(1)", ["argument", "error"], 3, "errors"),
]


def run_test(interpreter_path: str, code: str, timeout: int = 5) -> tuple:
    """Run interpreter with given code, return (stdout, stderr, returncode)."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.calc', delete=False) as f:
        f.write(code)
        f.flush()
        temp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, interpreter_path, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT", -1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def evaluate_interpreter(interpreter_path: str) -> dict:
    """Run all tests and return results."""
    results = {
        "tests_passed": 0,
        "tests_total": len(TESTS) + len(ERROR_TESTS),
        "scores": {},
        "details": [],
        "by_category": {}
    }

    total_score = 0
    max_score = sum(t[3] for t in TESTS) + sum(t[3] for t in ERROR_TESTS)

    # Run feature tests
    for desc, code, expected, points, category in TESTS:
        stdout, stderr, returncode = run_test(interpreter_path, code)

        # Parse output lines
        output_lines = [l.strip() for l in stdout.split('\n') if l.strip()]

        # Check if output matches expected
        # Allow for floating point representation differences
        def normalize(val):
            try:
                f = float(val)
                if f == int(f):
                    return str(int(f))
                return str(f)
            except:
                return val

        output_normalized = [normalize(l) for l in output_lines]
        expected_normalized = [normalize(e) for e in expected]

        passed = output_normalized == expected_normalized

        if passed:
            total_score += points
            results["tests_passed"] += 1
            results["details"].append(f"✓ {desc} ({points} pts)")
        else:
            results["details"].append(
                f"✗ {desc} (0/{points} pts) - got {output_lines}, expected {expected}"
            )

        # Track by category
        if category not in results["by_category"]:
            results["by_category"][category] = {"earned": 0, "possible": 0}
        results["by_category"][category]["possible"] += points
        if passed:
            results["by_category"][category]["earned"] += points

    # Run error tests
    for desc, code, should_contain_any, points, category in ERROR_TESTS:
        stdout, stderr, returncode = run_test(interpreter_path, code)

        combined_output = (stdout + stderr).lower()

        # Check if any expected substring is in output
        has_error_msg = any(s in combined_output for s in should_contain_any)

        # Should not crash silently - should have some output
        passed = has_error_msg or returncode != 0

        if passed:
            total_score += points
            results["tests_passed"] += 1
            results["details"].append(f"✓ {desc} - error handled ({points} pts)")
        else:
            results["details"].append(
                f"✗ {desc} (0/{points} pts) - no error message/handling"
            )

        if category not in results["by_category"]:
            results["by_category"][category] = {"earned": 0, "possible": 0}
        results["by_category"][category]["possible"] += points
        if passed:
            results["by_category"][category]["earned"] += points

    results["total_score"] = total_score
    results["max_score"] = max_score

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_p2.py <interpreter.py>")
        sys.exit(1)

    interpreter_path = sys.argv[1]

    print("=" * 60)
    print("Problem 2: Calculator Interpreter - Evaluation")
    print("=" * 60)

    results = evaluate_interpreter(interpreter_path)

    print("\nCategory Breakdown:")
    for category, scores in results["by_category"].items():
        print(f"  {category}: {scores['earned']}/{scores['possible']}")

    print("\nDetailed Results:")
    for detail in results["details"]:
        print(f"  {detail}")

    print(f"\nTests Passed: {results['tests_passed']}/{results['tests_total']}")
    print(f"Total Score: {results['total_score']}/{results['max_score']}")

    # Save results
    results_path = Path(__file__).parent / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()
