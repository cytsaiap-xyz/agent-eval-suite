# Problem 2: Calculator Language Interpreter

## Difficulty: Very Hard
## Expected Time: 60-90 minutes
## Discrimination Target: Multi-phase compilation, recursion, scoping

## Task

Implement a complete interpreter for a simple calculator language.

## Language Specification

### Syntax
```
# Variables
let x = 5
let y = x * 2 + 3

# Functions (single expression body)
fn square(n) = n * n
fn add(a, b) = a + b

# Recursive functions
fn factorial(n) = if n <= 1 then 1 else n * factorial(n - 1)
fn fib(n) = if n <= 1 then n else fib(n-1) + fib(n-2)

# Conditionals
if x > 5 then x * 2 else x + 10

# Print
print factorial(5)
print x + y

# Comments
# This is a comment
```

### Operators (precedence low to high)
1. Comparison: ==, !=, <, >, <=, >=
2. Addition: +, -
3. Multiplication: *, /, %
4. Unary: -
5. Function call: f(x)
6. Parentheses: (expr)

### Types
- Numbers only (integers and floats)
- Booleans only for conditionals (true = non-zero)

## Requirements

### Core Features (60 points)
1. **Lexer** (10 pts): Tokenize input correctly
2. **Parser** (15 pts): Build AST with correct precedence
3. **Variables** (10 pts): Declaration and lookup
4. **Arithmetic** (10 pts): All operators working
5. **Functions** (15 pts): Definition and calling

### Advanced Features (25 points)
6. **Recursion** (10 pts): Recursive function calls
7. **Conditionals** (10 pts): if-then-else expressions
8. **Closures** (5 pts): Functions capture outer scope

### Error Handling (15 points)
9. **Undefined variable** (3 pts): Clear error message
10. **Undefined function** (3 pts): Clear error message
11. **Division by zero** (3 pts): Handle gracefully
12. **Syntax errors** (3 pts): Report line number
13. **Type errors** (3 pts): e.g., calling non-function

## Test Cases

Your interpreter should be run as:
```bash
python interpreter.py program.calc
```

And output the results of all `print` statements.

## Input File: test_program.calc
```
# Basic arithmetic
let x = 10
let y = 3
print x + y * 2
print (x + y) * 2

# Functions
fn double(n) = n * 2
fn square(n) = n * n
print double(5)
print square(4)

# Composed functions
print double(square(3))

# Recursion
fn factorial(n) = if n <= 1 then 1 else n * factorial(n - 1)
print factorial(5)
print factorial(10)

# Fibonacci
fn fib(n) = if n <= 1 then n else fib(n-1) + fib(n-2)
print fib(10)

# Multiple parameters
fn add(a, b) = a + b
fn mult(a, b) = a * b
print add(3, 4)
print mult(add(2, 3), 4)

# Nested scope
let base = 100
fn addBase(n) = n + base
print addBase(50)

# Comparison
let a = 5
let b = 10
print if a < b then 1 else 0
print if a > b then 1 else 0
```

## Expected Output
```
16
26
10
16
18
120
3628800
55
7
20
150
1
0
```

## Evaluation
```bash
python evaluate_p2.py interpreter.py
```
