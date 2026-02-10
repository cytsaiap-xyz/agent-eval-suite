# Task: Analyze and Transform a Word Document

You have a Word document `report_draft.docx` containing a company quarterly report. Analyze it and produce several outputs.

## Setup

First, generate the sample document:
```bash
pip install python-docx
python generate_document.py
```

## Your Task

Analyze `report_draft.docx` and create the following outputs:

### 1. `document_analysis.json`

Extract comprehensive metadata and structure:
```json
{
  "metadata": {
    "title": "...",
    "author": "...",
    "created": "ISO date",
    "modified": "ISO date",
    "word_count": 0,
    "paragraph_count": 0
  },
  "structure": {
    "headings": [
      {"level": 1, "text": "...", "position": 0}
    ],
    "tables": [
      {"index": 0, "rows": 5, "cols": 3, "has_header_row": true}
    ],
    "lists": {
      "bullet_lists": 0,
      "numbered_lists": 0,
      "total_items": 0
    }
  },
  "issues": {
    "heading_level_skips": ["Skipped from H2 to H4 at position X"],
    "inconsistent_styles": ["..."]
  }
}
```

### 2. `table_of_contents.md`

Generate a markdown Table of Contents from the headings:
```markdown
# Table of Contents

1. Executive Summary
2. Introduction
   2.1. Background
   2.2. Objectives
3. Methodology
   3.1. Data Sources
...
```

Numbering should be hierarchical based on heading levels.

### 3. `extracted_tables.xlsx`

Export all tables to Excel:
- One worksheet per table
- Name sheets: "Table_1_DataSources", "Table_2_Financial", etc.
- Include headers
- Preserve cell content exactly

### 4. `section_summaries.json`

For each major section (H1), provide:
```json
{
  "sections": [
    {
      "title": "Executive Summary",
      "word_count": 85,
      "has_table": false,
      "has_list": false,
      "key_points": ["15% revenue increase", "3 new markets", "flagship launch"]
    }
  ]
}
```

### 5. `quality_report.md`

Document quality issues found:
- Heading hierarchy problems (level skips)
- Inconsistent styles
- Missing elements (tables without headers, etc.)
- Recommendations for fixes

## Process

1. Read the document using python-docx
2. Iterate through paragraphs and identify structure
3. Extract tables and their contents
4. Analyze heading hierarchy for issues
5. Generate all output files

## Requirements

- Use `python-docx` for reading .docx
- Use `openpyxl` for writing .xlsx
- Use `json` for JSON output
- Handle edge cases (empty cells, merged cells if any)

## Evaluation

Your outputs will be checked for:
- Accurate metadata extraction
- Complete heading extraction
- Correct table export
- Proper TOC generation
- Quality issue identification
