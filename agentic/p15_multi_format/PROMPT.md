# Task: Multi-Format Document Integration

Consolidate quarterly reports from four different document formats into unified outputs.

## Setup

Generate all input files:
```bash
pip install openpyxl python-docx python-pptx reportlab PyMuPDF
python generate_inputs.py
```

## Input Files

You have reports from different departments in different formats:

1. **`sales_report.xlsx`** - Sales team's Excel workbook
   - Summary, Monthly, Products, Regions sheets
   - Revenue, orders, customer metrics

2. **`marketing_deck.pptx`** - Marketing's PowerPoint
   - Campaign performance table
   - Market share metrics
   - Brand awareness data

3. **`finance_summary.pdf`** - Finance's PDF report
   - Income statement
   - Key financial ratios
   - Year-over-year comparisons

4. **`operations_update.docx`** - Operations' Word document
   - KPI table
   - Initiative updates
   - Risk assessments

## Your Task

Extract, consolidate, and produce unified reports.

### Step 1: Extract Data from Each Source

Create `extracted/` directory with JSON for each source:

**`extracted/sales_data.json`:**
```json
{
  "source": "sales_report.xlsx",
  "extracted_at": "ISO timestamp",
  "summary": {
    "total_revenue": 14400000,
    "total_orders": 2680,
    "avg_order_value": 5373
  },
  "monthly": [...],
  "products": [...],
  "regions": [...]
}
```

**`extracted/marketing_data.json`:**
```json
{
  "source": "marketing_deck.pptx",
  "campaigns": [...],
  "market_share": "18%",
  "brand_awareness": "45%"
}
```

**`extracted/finance_data.json`:**
```json
{
  "source": "finance_summary.pdf",
  "income_statement": {...},
  "ratios": {...}
}
```

**`extracted/operations_data.json`:**
```json
{
  "source": "operations_update.docx",
  "kpis": [...],
  "initiatives": [...],
  "risks": [...]
}
```

### Step 2: Consolidate Data

Create `consolidated_data.json`:
```json
{
  "period": "Q4 2024",
  "consolidated_at": "ISO timestamp",
  "sources_used": 4,
  "key_metrics": {
    "revenue": {
      "value": 14400000,
      "sources": {
        "sales": 14400000,
        "finance": 14400000
      },
      "variance": 0
    },
    "net_income": {...},
    "market_share": {...}
  },
  "cross_validation": {
    "revenue_match": true,
    "discrepancies_found": 0
  }
}
```

### Step 3: Identify Discrepancies

Create `discrepancies.md`:

```markdown
# Data Discrepancy Report

## Summary
- Sources analyzed: 4
- Discrepancies found: X

## Revenue Figures
| Source | Revenue | Variance |
|--------|---------|----------|
| Sales Excel | $14.4M | - |
| Finance PDF | $14.4M | 0% |

## Other Discrepancies
[List any data that doesn't match across sources]

## Missing Data
[Data present in one source but missing from others]
```

### Step 4: Create Executive Summary

Create `executive_summary.docx`:

A 2-page Word document with:
- Title: "Q4 2024 Consolidated Executive Summary"
- Key highlights from all departments
- Consolidated metrics table
- Top risks and opportunities
- Recommendations

### Step 5: Create Board Presentation

Create `board_presentation.pptx`:

8 slides:
1. Title: Q4 2024 Board Update
2. Executive Summary (key metrics)
3. Financial Performance (from finance PDF)
4. Sales Performance (from sales Excel)
5. Marketing Results (from marketing deck)
6. Operations Update (from operations doc)
7. Key Risks & Opportunities
8. Q1 2025 Outlook

### Step 6: Create Dashboard

Create `dashboard.xlsx`:

Sheets:
- **Summary**: All key metrics in one view
- **Source Data**: Raw data from each source
- **Charts**: Visualizations
- **Validation**: Cross-source comparison

### Step 7: Create Archive PDF

Create `report_archive.pdf`:

Combined document with:
- Cover page
- Table of contents
- All key data and analysis
- Source citations

## Process

This is a multi-step task requiring iteration:

1. Read each input file
2. Extract structured data
3. Compare and validate across sources
4. Identify discrepancies
5. Create consolidated outputs
6. Generate final deliverables

## Libraries Required

```python
# Reading
from openpyxl import load_workbook
from docx import Document
from pptx import Presentation
import fitz  # PyMuPDF

# Writing
from openpyxl import Workbook
from docx import Document
from pptx import Presentation
from reportlab.platypus import SimpleDocTemplate
```

## Evaluation

Your outputs will be checked for:
- Complete data extraction from all sources
- Accurate consolidation
- Discrepancies correctly identified
- Professional output documents
- Data consistency across outputs
