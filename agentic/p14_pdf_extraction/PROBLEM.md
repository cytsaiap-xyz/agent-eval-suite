# Problem 14: PDF Document Extraction & Analysis

## Difficulty: Hard (Agentic)
## Expected Tool Calls: 10-20
## Skills Required: /pdf skill

## Skill Usage

This problem tests the agent's ability to:
1. **Invoke the /pdf skill** for PDF processing
2. **Choose appropriate tools** (pypdf vs pdfplumber) based on skill guidance
3. **Extract tables accurately** using skill-recommended approaches
4. **Parse financial data** following skill patterns
5. **Handle multi-page documents** systematically

## Task

Extract structured data from a multi-page PDF document containing financial reports, tables, and mixed content.

## Input File

`annual_report.pdf` - A 20-page company annual report containing:
- Text paragraphs
- Financial tables
- Charts (as images)
- Headers and footers
- Page numbers
- Multi-column layouts in some sections

## Requirements

### 1. Text Extraction

Create `extracted_text.md` with:
- Full text content organized by page
- Proper paragraph separation
- Section headings identified and formatted

### 2. Table Extraction

Create `extracted_tables/` directory with:
- `table_1.csv`, `table_2.csv`, etc.
- One CSV per table found in the PDF
- Headers preserved
- Data aligned correctly

Also create `table_metadata.json`:
```json
{
  "tables": [
    {
      "id": "table_1",
      "page": 5,
      "title": "Revenue Summary",
      "rows": 10,
      "columns": 4,
      "has_header": true
    }
  ]
}
```

### 3. Document Structure

Create `document_structure.json`:
```json
{
  "title": "...",
  "total_pages": 20,
  "sections": [
    {
      "title": "Letter to Shareholders",
      "start_page": 1,
      "end_page": 2
    }
  ],
  "table_of_contents": [...],
  "figures": [
    {"page": 5, "caption": "Revenue Growth Chart"}
  ]
}
```

### 4. Financial Data Summary

Create `financial_summary.json` extracting key numbers:
```json
{
  "fiscal_year": "2024",
  "revenue": {"value": 14400000, "currency": "USD"},
  "net_income": {"value": 2000000, "currency": "USD"},
  "total_assets": {...},
  "employees": 450,
  "key_metrics": {
    "revenue_growth": "15%",
    "profit_margin": "13.9%",
    "eps": "$1.00"
  }
}
```

### 5. Search Index

Create `search_index.json` for full-text search:
```json
{
  "pages": [
    {
      "page": 1,
      "keywords": ["revenue", "growth", "shareholders"],
      "summary": "First 100 chars..."
    }
  ],
  "term_frequency": {
    "revenue": 45,
    "growth": 32,
    "profit": 28
  }
}
```

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Text extraction accuracy | 20 |
| Table extraction accuracy | 25 |
| Document structure correct | 15 |
| Financial data extraction | 20 |
| Search index complete | 10 |
| Handles multi-column | 10 |
| **Total** | **100** |

## Hints

- **Invoke /pdf skill first** to understand extraction options
- The skill provides a Quick Reference table for tool selection
- Use pdfplumber for table extraction (`page.extract_tables()`)
- Follow skill patterns for text extraction with layout preservation

## Skill Evaluation

Points are awarded for:
- Properly invoking /pdf skill before starting
- Using skill-recommended tools for each task
- Following skill patterns for table extraction
- Applying skill approaches for document structure analysis
