# Problem 11: Word Document Analysis & Transformation

## Difficulty: Hard (Agentic)
## Expected Tool Calls: 10-20
## Skills Required: docx reading/writing

## Task

Analyze a complex Word document and produce transformed outputs based on specific requirements.

## Input File

`report_draft.docx` - A 15-page company report with:
- Multiple heading levels (H1-H4)
- Tables with data
- Bullet and numbered lists
- Images with captions
- Headers and footers
- Comments and tracked changes
- Inconsistent formatting

## Required Outputs

### 1. `document_analysis.json`

Extract and structure the document:
```json
{
  "metadata": {
    "title": "...",
    "author": "...",
    "created": "...",
    "modified": "...",
    "word_count": 0,
    "page_count": 0
  },
  "structure": {
    "headings": [
      {"level": 1, "text": "...", "page": 1},
      ...
    ],
    "tables": [
      {"rows": 5, "cols": 3, "page": 2, "has_header": true}
    ],
    "images": [
      {"caption": "...", "page": 3}
    ],
    "lists": {
      "bullet_count": 5,
      "numbered_count": 3
    }
  },
  "issues": {
    "inconsistent_headings": [...],
    "missing_captions": [...],
    "formatting_problems": [...]
  }
}
```

### 2. `table_of_contents.md`

Generate a proper TOC from the document headings:
```markdown
# Table of Contents

1. [Introduction](#introduction)
   1.1 [Background](#background)
   1.2 [Objectives](#objectives)
2. [Methodology](#methodology)
...
```

### 3. `extracted_tables.xlsx`

Export all tables from the document to an Excel file:
- One sheet per table
- Sheet names: "Table_1", "Table_2", etc.
- Preserve formatting where possible

### 4. `cleaned_report.docx`

Create a cleaned version:
- Fix inconsistent heading styles
- Remove tracked changes (accept all)
- Resolve all comments
- Standardize fonts (body: Calibri 11pt, headings: Calibri Bold)
- Add proper page numbers

### 5. `executive_summary.docx`

Extract/generate a 1-page executive summary:
- Pull the abstract/introduction
- Key findings from each major section
- Summary table if applicable

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Metadata extraction accurate | 10 |
| Headings correctly identified | 15 |
| Tables extracted properly | 15 |
| TOC generation accurate | 10 |
| Excel export correct | 15 |
| Cleaned document valid | 15 |
| Executive summary coherent | 10 |
| Issues correctly identified | 10 |
| **Total** | **100** |

## Hints

- Use python-docx library for reading/writing .docx
- Document properties are in core_properties
- Tables have rows and cells accessible via iteration
- Styles can be accessed and modified via paragraph.style
