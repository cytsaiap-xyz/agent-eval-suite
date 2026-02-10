# Task: Build a Markdown to HTML Converter

Implement a Markdown to HTML converter and iterate until at least 48 out of 50 test cases pass.

## Your Task

Create `converter.py` with a `markdown_to_html()` function that converts Markdown to HTML.

## Function Signature

```python
def markdown_to_html(markdown: str) -> str:
    """
    Convert a Markdown string to HTML.

    Args:
        markdown: The Markdown text to convert

    Returns:
        The converted HTML string
    """
    ...
```

## Features to Support

### Basic (Tests 1-15)
- Paragraphs (text separated by blank lines)
- Headers: `# H1` through `###### H6`
- Bold: `**text**`
- Italic: `*text*`
- Bold+Italic: `***text***`
- Inline code: `` `code` ``
- Links: `[text](url)` and `[text](url "title")`
- Images: `![alt](src)`

### Lists (Tests 16-25)
- Unordered lists: `- item` or `* item`
- Ordered lists: `1. item`
- Nested lists (2 levels deep)
- Lists with inline formatting

### Code Blocks (Tests 26-30)
- Fenced code blocks: ``` ```code``` ```
- Code blocks with language: ``` ```python ```
- Indented code blocks (4 spaces)

### Blockquotes (Tests 31-35)
- Simple blockquotes: `> quote`
- Multi-line blockquotes
- Nested blockquotes: `>> nested`
- Blockquotes with formatting

### Other (Tests 36-40)
- Horizontal rules: `---`, `***`, `___`
- Strikethrough: `~~text~~`
- HTML escaping: `<` → `&lt;`

### Tables (Tests 41-45)
- Basic tables with `|` separators
- Header row with `|---|` separator
- Column alignment: `:---`, `:---:`, `---:`

### Complex Documents (Tests 46-50)
- Mixed content (headers, lists, code, quotes)
- Multiple features combined

## Process

This task requires iteration:

```
1. Implement basic features
2. Run: python run_tests.py converter.py
3. See which tests fail and why (diff shown)
4. Fix your implementation
5. Run tests again
6. Repeat until ≥48/50 pass
```

## Test Cases

The `test_cases/` directory contains 50 pairs of files:
- `XX_name.md` - Input Markdown
- `XX_name.html` - Expected HTML output

## Running Tests

```bash
# Run all tests
python run_tests.py converter.py

# The test runner shows:
# - ✓ for passing tests
# - ✗ for failing tests with diff
```

## Example

Input (`01_simple_paragraph.md`):
```
Hello world.
```

Expected output (`01_simple_paragraph.html`):
```html
<p>Hello world.</p>
```

## Constraints

- Use only Python standard library
- No external Markdown libraries (that defeats the purpose!)
- Allowed imports: `re`, `html`, etc.

## Tips

- Start with the simplest features (paragraphs, headers)
- Use regular expressions for inline patterns
- Handle block-level elements (lists, code blocks) before inline
- Test frequently - the diff output shows exactly what's wrong
- Edge cases matter: empty input, whitespace, nested structures

## Scoring

| Tests Passing | Score |
|--------------|-------|
| 48-50 | Full credit |
| 40-47 | Good |
| 30-39 | Partial |
| 20-29 | Basic |
| <20 | Needs work |
