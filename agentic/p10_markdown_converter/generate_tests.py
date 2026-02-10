#!/usr/bin/env python3
"""
Generate test cases for the Markdown converter.
Creates 50 test cases of varying difficulty.
"""

from pathlib import Path

TEST_CASES = [
    # Basic (1-10)
    ("01_simple_paragraph", "Hello world.", "<p>Hello world.</p>"),
    ("02_multiple_paragraphs", "First paragraph.\n\nSecond paragraph.", "<p>First paragraph.</p>\n<p>Second paragraph.</p>"),
    ("03_h1_header", "# Hello", "<h1>Hello</h1>"),
    ("04_h2_header", "## Subheading", "<h2>Subheading</h2>"),
    ("05_h3_to_h6", "### H3\n#### H4\n##### H5\n###### H6", "<h3>H3</h3>\n<h4>H4</h4>\n<h5>H5</h5>\n<h6>H6</h6>"),
    ("06_bold_text", "This is **bold** text.", "<p>This is <strong>bold</strong> text.</p>"),
    ("07_italic_text", "This is *italic* text.", "<p>This is <em>italic</em> text.</p>"),
    ("08_bold_and_italic", "This is ***bold and italic***.", "<p>This is <strong><em>bold and italic</em></strong>.</p>"),
    ("09_inline_code", "Use `print()` function.", "<p>Use <code>print()</code> function.</p>"),
    ("10_simple_link", "Visit [Google](https://google.com).", "<p>Visit <a href=\"https://google.com\">Google</a>.</p>"),

    # Links and Images (11-15)
    ("11_multiple_links", "[One](1.com) and [Two](2.com)", "<p><a href=\"1.com\">One</a> and <a href=\"2.com\">Two</a></p>"),
    ("12_simple_image", "![Alt text](image.png)", "<p><img src=\"image.png\" alt=\"Alt text\"></p>"),
    ("13_image_in_paragraph", "Here is an image: ![cat](cat.jpg) in text.", "<p>Here is an image: <img src=\"cat.jpg\" alt=\"cat\"> in text.</p>"),
    ("14_link_with_title", "[Link](url.com \"Title\")", "<p><a href=\"url.com\" title=\"Title\">Link</a></p>"),
    ("15_empty_alt_image", "![](logo.png)", "<p><img src=\"logo.png\" alt=\"\"></p>"),

    # Lists (16-25)
    ("16_unordered_list", "- Item 1\n- Item 2\n- Item 3", "<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n<li>Item 3</li>\n</ul>"),
    ("17_ordered_list", "1. First\n2. Second\n3. Third", "<ol>\n<li>First</li>\n<li>Second</li>\n<li>Third</li>\n</ol>"),
    ("18_unordered_asterisk", "* Item A\n* Item B", "<ul>\n<li>Item A</li>\n<li>Item B</li>\n</ul>"),
    ("19_nested_unordered", "- Parent\n  - Child\n  - Child 2\n- Parent 2", "<ul>\n<li>Parent\n<ul>\n<li>Child</li>\n<li>Child 2</li>\n</ul>\n</li>\n<li>Parent 2</li>\n</ul>"),
    ("20_nested_ordered", "1. First\n   1. Sub first\n   2. Sub second\n2. Second", "<ol>\n<li>First\n<ol>\n<li>Sub first</li>\n<li>Sub second</li>\n</ol>\n</li>\n<li>Second</li>\n</ol>"),
    ("21_mixed_list", "- Unordered\n  1. Ordered inside\n  2. Another", "<ul>\n<li>Unordered\n<ol>\n<li>Ordered inside</li>\n<li>Another</li>\n</ol>\n</li>\n</ul>"),
    ("22_list_with_formatting", "- **Bold item**\n- *Italic item*", "<ul>\n<li><strong>Bold item</strong></li>\n<li><em>Italic item</em></li>\n</ul>"),
    ("23_long_list", "- A\n- B\n- C\n- D\n- E", "<ul>\n<li>A</li>\n<li>B</li>\n<li>C</li>\n<li>D</li>\n<li>E</li>\n</ul>"),
    ("24_list_with_code", "- Use `git add`\n- Then `git commit`", "<ul>\n<li>Use <code>git add</code></li>\n<li>Then <code>git commit</code></li>\n</ul>"),
    ("25_list_after_paragraph", "Some text.\n\n- List item\n- Another", "<p>Some text.</p>\n<ul>\n<li>List item</li>\n<li>Another</li>\n</ul>"),

    # Code blocks (26-30)
    ("26_code_block", "```\ncode here\n```", "<pre><code>code here</code></pre>"),
    ("27_code_block_language", "```python\nprint('hi')\n```", "<pre><code class=\"language-python\">print('hi')</code></pre>"),
    ("28_code_block_multiline", "```\nline 1\nline 2\nline 3\n```", "<pre><code>line 1\nline 2\nline 3</code></pre>"),
    ("29_code_block_js", "```javascript\nconst x = 1;\n```", "<pre><code class=\"language-javascript\">const x = 1;</code></pre>"),
    ("30_indented_code", "    function foo() {\n        return 1;\n    }", "<pre><code>function foo() {\n    return 1;\n}</code></pre>"),

    # Blockquotes (31-35)
    ("31_simple_blockquote", "> This is a quote", "<blockquote>\n<p>This is a quote</p>\n</blockquote>"),
    ("32_multiline_blockquote", "> Line one\n> Line two", "<blockquote>\n<p>Line one\nLine two</p>\n</blockquote>"),
    ("33_nested_blockquote", "> Outer\n>> Inner", "<blockquote>\n<p>Outer</p>\n<blockquote>\n<p>Inner</p>\n</blockquote>\n</blockquote>"),
    ("34_blockquote_with_formatting", "> **Bold** and *italic*", "<blockquote>\n<p><strong>Bold</strong> and <em>italic</em></p>\n</blockquote>"),
    ("35_blockquote_with_code", "> Use `command`", "<blockquote>\n<p>Use <code>command</code></p>\n</blockquote>"),

    # Horizontal rules and misc (36-40)
    ("36_horizontal_rule", "Above\n\n---\n\nBelow", "<p>Above</p>\n<hr>\n<p>Below</p>"),
    ("37_hr_asterisks", "***", "<hr>"),
    ("38_hr_underscores", "___", "<hr>"),
    ("39_strikethrough", "This is ~~deleted~~ text.", "<p>This is <del>deleted</del> text.</p>"),
    ("40_escape_html", "Use <div> tags", "<p>Use &lt;div&gt; tags</p>"),

    # Tables (41-45)
    ("41_simple_table", "| A | B |\n|---|---|\n| 1 | 2 |", "<table>\n<thead>\n<tr><th>A</th><th>B</th></tr>\n</thead>\n<tbody>\n<tr><td>1</td><td>2</td></tr>\n</tbody>\n</table>"),
    ("42_table_alignment", "| Left | Center | Right |\n|:-----|:------:|------:|\n| L | C | R |", "<table>\n<thead>\n<tr><th style=\"text-align:left\">Left</th><th style=\"text-align:center\">Center</th><th style=\"text-align:right\">Right</th></tr>\n</thead>\n<tbody>\n<tr><td style=\"text-align:left\">L</td><td style=\"text-align:center\">C</td><td style=\"text-align:right\">R</td></tr>\n</tbody>\n</table>"),
    ("43_table_multirow", "| H1 | H2 |\n|---|---|\n| A | B |\n| C | D |", "<table>\n<thead>\n<tr><th>H1</th><th>H2</th></tr>\n</thead>\n<tbody>\n<tr><td>A</td><td>B</td></tr>\n<tr><td>C</td><td>D</td></tr>\n</tbody>\n</table>"),
    ("44_table_with_formatting", "| **Bold** | *Italic* |\n|---|---|\n| `code` | text |", "<table>\n<thead>\n<tr><th><strong>Bold</strong></th><th><em>Italic</em></th></tr>\n</thead>\n<tbody>\n<tr><td><code>code</code></td><td>text</td></tr>\n</tbody>\n</table>"),
    ("45_table_with_links", "| [Link](url) |\n|---|\n| data |", "<table>\n<thead>\n<tr><th><a href=\"url\">Link</a></th></tr>\n</thead>\n<tbody>\n<tr><td>data</td></tr>\n</tbody>\n</table>"),

    # Complex documents (46-50)
    ("46_mixed_content", "# Title\n\nParagraph with **bold**.\n\n- List item\n\n> Quote", "<h1>Title</h1>\n<p>Paragraph with <strong>bold</strong>.</p>\n<ul>\n<li>List item</li>\n</ul>\n<blockquote>\n<p>Quote</p>\n</blockquote>"),
    ("47_document_structure", "# Heading\n\nIntro paragraph.\n\n## Section\n\nContent here.\n\n### Subsection\n\nMore content.", "<h1>Heading</h1>\n<p>Intro paragraph.</p>\n<h2>Section</h2>\n<p>Content here.</p>\n<h3>Subsection</h3>\n<p>More content.</p>"),
    ("48_code_and_text", "Run this:\n\n```bash\necho hello\n```\n\nThat's it.", "<p>Run this:</p>\n<pre><code class=\"language-bash\">echo hello</code></pre>\n<p>That's it.</p>"),
    ("49_complex_list", "- Item 1\n  - Sub A\n  - Sub B\n- Item 2\n\nParagraph.\n\n1. One\n2. Two", "<ul>\n<li>Item 1\n<ul>\n<li>Sub A</li>\n<li>Sub B</li>\n</ul>\n</li>\n<li>Item 2</li>\n</ul>\n<p>Paragraph.</p>\n<ol>\n<li>One</li>\n<li>Two</li>\n</ol>"),
    ("50_full_document", "# Title\n\nIntro with [link](url) and **bold**.\n\n## Features\n\n- Feature 1\n- Feature 2\n\n```python\ndef main():\n    pass\n```\n\n> Note: Important!\n\n| Col A | Col B |\n|-------|-------|\n| 1     | 2     |", "<h1>Title</h1>\n<p>Intro with <a href=\"url\">link</a> and <strong>bold</strong>.</p>\n<h2>Features</h2>\n<ul>\n<li>Feature 1</li>\n<li>Feature 2</li>\n</ul>\n<pre><code class=\"language-python\">def main():\n    pass</code></pre>\n<blockquote>\n<p>Note: Important!</p>\n</blockquote>\n<table>\n<thead>\n<tr><th>Col A</th><th>Col B</th></tr>\n</thead>\n<tbody>\n<tr><td>1</td><td>2</td></tr>\n</tbody>\n</table>"),
]


def main():
    test_dir = Path(__file__).parent / "test_cases"
    test_dir.mkdir(exist_ok=True)

    for name, md, html in TEST_CASES:
        md_path = test_dir / f"{name}.md"
        html_path = test_dir / f"{name}.html"

        md_path.write_text(md)
        html_path.write_text(html)

    print(f"Generated {len(TEST_CASES)} test cases in {test_dir}")


if __name__ == "__main__":
    main()
