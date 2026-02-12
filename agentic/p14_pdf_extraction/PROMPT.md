# Task: Extract and Analyze a PDF Document

Extract structured data from a multi-page PDF annual report using the `/pdf` skill.

## Setup

First, generate the sample PDF:
```bash
pip install reportlab
python generate_pdf.py
```

## Skills Available

You have access to the `/pdf` skill for PDF operations. Use it to:
- Extract text from PDF pages
- Parse tables from PDF documents
- Understand document structure
- Handle different PDF content types

The skill provides guidance on:
- pypdf for basic operations
- pdfplumber for text and table extraction
- reportlab for creating PDFs

## Input File

`annual_report.pdf` - A company annual report containing:
- Letter to Shareholders
- Financial tables
- Business segment breakdowns
- Regional performance data
- Balance sheet

## Your Task

Extract and structure all content from the PDF.

### 1. Extract Full Text -> `extracted_text.md`

Create a markdown file with:
- All text content organized by page
- Section headings preserved with proper markdown formatting
- Clear page separators

```markdown
# Annual Report 2024

## Page 1 - Cover

TechCorp Industries
Annual Report 2024
...

## Page 2 - Letter to Shareholders

Dear Shareholders,
...
```

### 2. Extract Tables -> `extracted_tables/`

Create one CSV file per table found:

```
extracted_tables/
├── table_1_financial_highlights.csv
├── table_2_revenue_segments.csv
├── table_3_regional_performance.csv
└── table_4_balance_sheet.csv
```

Each CSV should have:
- Proper headers
- All data rows
- Correct alignment

Also create `table_metadata.json`:
```json
{
  "tables": [
    {
      "id": "table_1",
      "filename": "table_1_financial_highlights.csv",
      "page": 3,
      "title": "Financial Highlights",
      "rows": 6,
      "columns": 4
    }
  ]
}
```

### 3. Document Structure -> `document_structure.json`

Map the document organization:
```json
{
  "title": "TechCorp Industries Annual Report 2024",
  "total_pages": 8,
  "sections": [
    {
      "title": "Cover Page",
      "start_page": 1,
      "end_page": 1
    },
    {
      "title": "Letter to Shareholders",
      "start_page": 2,
      "end_page": 2
    },
    {
      "title": "Financial Highlights",
      "start_page": 3,
      "end_page": 3
    }
  ],
  "tables_found": 4,
  "images_found": 0
}
```

### 4. Financial Summary -> `financial_summary.json`

Extract key financial figures:
```json
{
  "fiscal_year": "2024",
  "currency": "USD",
  "income_statement": {
    "revenue": 14400000,
    "gross_profit": 6300000,
    "operating_income": 2800000,
    "net_income": 2000000,
    "eps": 1.00
  },
  "balance_sheet": {
    "total_assets": 13000000,
    "total_liabilities": 4700000,
    "shareholders_equity": 8300000,
    "cash": 4200000
  },
  "key_metrics": {
    "revenue_growth_pct": 15.2,
    "gross_margin_pct": 43.75,
    "net_margin_pct": 13.89
  },
  "segments": [
    {"name": "Electronics", "revenue": 8200000, "pct_total": 57},
    {"name": "Accessories", "revenue": 4100000, "pct_total": 28},
    {"name": "Tools", "revenue": 1500000, "pct_total": 10},
    {"name": "Services", "revenue": 600000, "pct_total": 5}
  ],
  "regions": [
    {"name": "North America", "revenue": 7200000},
    {"name": "Western Europe", "revenue": 4300000},
    {"name": "APAC", "revenue": 2900000}
  ]
}
```

### 5. Search Index -> `search_index.json`

Create an index for text search:
```json
{
  "document": "annual_report.pdf",
  "indexed_at": "ISO timestamp",
  "pages": [
    {
      "page": 1,
      "word_count": 25,
      "top_terms": ["techcorp", "annual", "report", "2024"]
    }
  ],
  "term_frequency": {
    "revenue": {"count": 15, "pages": [3, 4, 5]},
    "growth": {"count": 12, "pages": [2, 3, 4]},
    "profit": {"count": 8, "pages": [3, 6]}
  },
  "total_words": 2500
}
```

## Skill Usage Expectations

This task tests your ability to:
1. **Invoke the /pdf skill** and understand PDF processing options
2. **Choose appropriate tools** (pypdf vs pdfplumber) based on task
3. **Extract tables accurately** using skill-recommended approaches
4. **Parse financial data** from unstructured PDF content
5. **Handle multi-page documents** systematically

## Key Skill Concepts to Apply

From the `/pdf` skill, pay attention to:
- pdfplumber for table extraction (`page.extract_tables()`)
- Text extraction with layout preservation
- Quick reference table for tool selection
- Advanced table extraction patterns

## Process

1. Use `/pdf` skill to learn extraction approaches
2. Read the PDF and extract text page by page
3. Identify and extract all tables
4. Parse financial figures from table data
5. Build document structure map
6. Create search index from extracted text

## Evaluation

Your outputs will be checked for:
- Proper /pdf skill invocation
- Complete text extraction
- Accurate table parsing
- Correct financial figures
- Proper document structure
- Working search index
