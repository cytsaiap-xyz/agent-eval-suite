# Problem 10: Self-Correcting Markdown Converter

## Difficulty: Very Hard (Agentic)
## Expected Iterations: 10-25
## Discrimination Target: Code generation, test-driven iteration, edge case handling

## Task

Implement a Markdown to HTML converter and iterate until 48/50 test cases pass.

## Features to Support

### Basic (Required)
1. Headers (h1-h6): `# Header`
2. Bold: `**bold**`
3. Italic: `*italic*`
4. Links: `[text](url)`
5. Images: `![alt](url)`
6. Inline code: `` `code` ``

### Intermediate (Required)
7. Unordered lists: `- item`
8. Ordered lists: `1. item`
9. Nested lists (2 levels)
10. Code blocks: ``` ```code``` ```
11. Blockquotes: `> quote`
12. Horizontal rules: `---`

### Advanced (Required)
13. Tables
14. Strikethrough: `~~text~~`
15. Nested blockquotes
16. Code blocks with language hints

## Process

```
1. Implement the converter: converter.py
2. Run: python run_tests.py
3. See which tests fail
4. Fix your implementation
5. Run tests again
6. Repeat until >= 48/50 pass
```

## Interface

Your `converter.py` must provide:

```python
def markdown_to_html(markdown: str) -> str:
    """Convert Markdown string to HTML string."""
    ...
```

## Test Structure

```
test_cases/
├── 01_simple_paragraph.md
├── 01_simple_paragraph.html  (expected output)
├── 02_headers.md
├── 02_headers.html
...
├── 50_complex_document.md
└── 50_complex_document.html
```

## Evaluation

```bash
python evaluate_p10.py converter.py
```

## Scoring

| Tests Passing | Points |
|--------------|--------|
| < 20 | 0 |
| 20-29 | 20 |
| 30-39 | 40 |
| 40-47 | 60 |
| 48-49 | 80 |
| 50 | 100 |

Plus partial credit for individual feature coverage.

## Hints

- Start simple: paragraphs, then headers
- Use regex for inline patterns
- Handle edge cases: empty input, whitespace
- Lists are tricky - track indentation
- Tables need proper alignment handling
- Test frequently - small iterations
- The diff output shows exactly what's wrong

## Allowed

- Standard library only (re, html, etc.)
- No external markdown libraries (that defeats the purpose!)
