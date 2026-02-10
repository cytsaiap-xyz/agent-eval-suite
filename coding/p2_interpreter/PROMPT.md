# Task: Build a Calculator Language Interpreter

Create an interpreter for a simple calculator language that supports variables, functions, recursion, and conditionals.

## Your Task

Create `interpreter.py` that can execute programs written in this calculator language.

## Language Specification

### Variables
```
let x = 5
let y = x * 2 + 3
```

### Functions (single expression body)
```
fn square(n) = n * n
fn add(a, b) = a + b
```

### Recursive Functions
```
fn factorial(n) = if n <= 1 then 1 else n * factorial(n - 1)
fn fib(n) = if n <= 1 then n else fib(n-1) + fib(n-2)
```

### Conditionals
```
if x > 5 then x * 2 else x + 10
```

### Print
```
print factorial(5)
print x + y
```

### Comments
```
# This is a comment
```

### Operators (precedence low to high)
1. Comparison: ==, !=, <, >, <=, >=
2. Addition: +, -
3. Multiplication: *, /, %
4. Unary: -
5. Function call: f(x)
6. Parentheses: (expr)

## Usage

```bash
python interpreter.py program.calc
```

Your interpreter should:
1. Read the file specified as command line argument
2. Execute the program
3. Print output for each `print` statement (one value per line)

## Test Program

See `test_program.calc` for a complete test. Expected output:
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

## Error Handling

Your interpreter should handle these errors gracefully with clear messages:
- Undefined variable
- Undefined function
- Division by zero
- Syntax errors (report line number if possible)
- Wrong number of arguments

## Requirements

- Implement a proper lexer and parser (not just eval())
- Support recursive function calls
- Functions should capture their defining scope (closures)
- Use only Python standard library
