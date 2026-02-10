# Task: Extract and Analyze a PDF Document

Extract structured data from a multi-page PDF annual report.

## Setup

First, generate the sample PDF:
```bash
pip install reportlab
python generate_pdf.py
```

## Input File

`annual_report.pdf` - A company annual report containing:
- Letter to Shareholders
- Financial tables
- Business segment breakdowns
- Regional performance data
- Balance sheet

## Your Task

Extract and structure all content from the PDF.

### 1. Extract Full Text → `extracted_text.md`

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

### 2. Extract Tables → `extracted_tables/`

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

### 3. Document Structure → `document_structure.json`

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

### 4. Financial Summary → `financial_summary.json`

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

### 5. Search Index → `search_index.json`

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

## Libraries

```bash
pip install PyMuPDF  # or pdfplumber, pypdf2
```

## Example Code

```python
import fitz  # PyMuPDF

# Open PDF
doc = fitz.open("annual_report.pdf")

# Extract text from page
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    print(f"Page {page_num + 1}:")
    print(text)

# Find tables (basic approach)
for page_num in range(len(doc)):
    page = doc[page_num]
    tables = page.find_tables()
    for table in tables:
        print(table.extract())
```

## Evaluation

Your outputs will be checked for:
- Complete text extraction
- Accurate table parsing
- Correct financial figures
- Proper document structure
- Working search index
