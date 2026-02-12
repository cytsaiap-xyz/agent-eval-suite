# Task: Multi-Format Document Integration

Consolidate quarterly reports from four different document formats into unified outputs. This task requires using **all four document skills** together.

## Setup

Generate all input files:
```bash
pip install openpyxl python-docx python-pptx reportlab PyMuPDF
python generate_inputs.py
```

## Skills Available

You have access to **all document processing skills**:

| Skill | Use For |
|-------|---------|
| `/xlsx` | Reading sales_report.xlsx, creating dashboard.xlsx |
| `/pptx` | Reading marketing_deck.pptx, creating board_presentation.pptx |
| `/pdf` | Reading finance_summary.pdf, creating report_archive.pdf |
| `/docx` | Reading operations_update.docx, creating executive_summary.docx |

**This task tests your ability to combine multiple skills effectively.**

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

Extract, consolidate, and produce unified reports using appropriate skills for each format.

### Step 1: Extract Data from Each Source

Use the appropriate skill for each file format:

**Use `/xlsx` skill for `extracted/sales_data.json`:**
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

**Use `/pptx` skill for `extracted/marketing_data.json`:**
```json
{
  "source": "marketing_deck.pptx",
  "campaigns": [...],
  "market_share": "18%",
  "brand_awareness": "45%"
}
```

**Use `/pdf` skill for `extracted/finance_data.json`:**
```json
{
  "source": "finance_summary.pdf",
  "income_statement": {...},
  "ratios": {...}
}
```

**Use `/docx` skill for `extracted/operations_data.json`:**
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

### Step 4: Create Executive Summary (Use /docx)

Create `executive_summary.docx`:

A 2-page Word document with:
- Title: "Q4 2024 Consolidated Executive Summary"
- Key highlights from all departments
- Consolidated metrics table
- Top risks and opportunities
- Recommendations

Follow `/docx` skill guidance for:
- Document structure
- Table formatting
- Professional styling

### Step 5: Create Board Presentation (Use /pptx)

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

Follow `/pptx` skill guidance for:
- Design principles
- Color palette selection
- Chart creation
- QA verification

### Step 6: Create Dashboard (Use /xlsx)

Create `dashboard.xlsx`:

Sheets:
- **Summary**: All key metrics in one view
- **Source Data**: Raw data from each source
- **Charts**: Visualizations
- **Validation**: Cross-source comparison

Follow `/xlsx` skill guidance for:
- Formula usage (not hardcoded values)
- Conditional formatting
- Chart creation

### Step 7: Create Archive PDF (Use /pdf)

Create `report_archive.pdf`:

Combined document with:
- Cover page
- Table of contents
- All key data and analysis
- Source citations

Follow `/pdf` skill guidance for:
- PDF creation with reportlab
- Multi-page document structure

## Skill Usage Expectations

This task tests your ability to:
1. **Use all four skills** appropriately for each format
2. **Switch between skills** as needed during the workflow
3. **Apply skill-specific patterns** (formulas for xlsx, design for pptx, etc.)
4. **Maintain consistency** across outputs created with different skills
5. **Cross-validate data** extracted using different skills

## Process

This is a multi-step task requiring iteration and multiple skill invocations:

1. **Invoke /xlsx** -> Read Excel, extract sales data
2. **Invoke /pptx** -> Read PowerPoint, extract marketing data
3. **Invoke /pdf** -> Read PDF, extract finance data
4. **Invoke /docx** -> Read Word, extract operations data
5. Compare and validate across sources
6. **Invoke /docx** -> Create executive summary
7. **Invoke /pptx** -> Create board presentation
8. **Invoke /xlsx** -> Create dashboard
9. **Invoke /pdf** -> Create archive PDF

## Evaluation

Your outputs will be checked for:
- **All four skills properly invoked** (critical)
- Complete data extraction from all sources
- Accurate consolidation
- Discrepancies correctly identified
- Professional output documents
- Data consistency across outputs
- Evidence of skill-specific patterns used
