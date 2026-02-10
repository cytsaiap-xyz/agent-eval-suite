# Problem 15: Multi-Format Document Integration

## Difficulty: Very Hard (Agentic)
## Expected Tool Calls: 20-35
## Skills Required: docx, pptx, xlsx, pdf - all combined

## Task

Integrate data from multiple document formats to produce a unified report package.

## Scenario

You are consolidating quarterly reports from different departments, each submitted in their preferred format:
- Sales team: Excel spreadsheet
- Marketing: PowerPoint presentation
- Finance: PDF report
- Operations: Word document

## Input Files

1. `sales_report.xlsx` - Sales data with multiple sheets
2. `marketing_deck.pptx` - Marketing presentation with charts
3. `finance_summary.pdf` - Financial statements
4. `operations_update.docx` - Operations narrative

## Requirements

### 1. Data Extraction

Extract key data from each source:

**From Excel:**
- Monthly revenue figures
- Product performance metrics
- Regional breakdowns

**From PowerPoint:**
- Campaign performance data
- Market share figures
- Key messaging points

**From PDF:**
- Financial statement figures
- Key ratios
- Audit notes

**From Word:**
- KPI summaries
- Initiative updates
- Risk assessments

### 2. Data Consolidation

Create `consolidated_data.json`:
```json
{
  "period": "Q4 2024",
  "sources": ["sales_report.xlsx", "marketing_deck.pptx", ...],
  "revenue": {
    "total": 14400000,
    "by_source": {
      "sales_excel": 14400000,
      "finance_pdf": 14400000
    },
    "discrepancy": 0
  },
  "metrics": {
    "from_sales": {...},
    "from_marketing": {...},
    "from_finance": {...},
    "from_operations": {...}
  }
}
```

### 3. Discrepancy Report

Create `discrepancies.md` identifying:
- Revenue figures that don't match between sources
- Metric calculations that differ
- Missing data in any source
- Data quality issues

### 4. Executive Summary

Create `executive_summary.docx`:
- 2-page Word document
- Consolidated highlights from all sources
- Key metrics table
- Recommendations section

### 5. Board Presentation

Create `board_presentation.pptx`:
- 8-slide deck
- Data pulled from all sources
- Charts comparing metrics across sources
- Professional formatting

### 6. Data Dashboard

Create `dashboard.xlsx`:
- Summary sheet with all key metrics
- Charts consolidating data
- Source reference sheet
- Conditional formatting for discrepancies

### 7. Archive Package

Create `report_archive.pdf`:
- Combine all key information into single PDF
- Include table of contents
- Page numbers
- Source citations

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Excel data extraction | 10 |
| PowerPoint data extraction | 10 |
| PDF data extraction | 10 |
| Word data extraction | 10 |
| Data consolidation accurate | 15 |
| Discrepancies identified | 10 |
| Executive summary quality | 10 |
| Board presentation quality | 10 |
| Dashboard completeness | 10 |
| Archive PDF generated | 5 |
| **Total** | **100** |

## Hints

- Start by extracting all data into JSON
- Compare figures across sources for validation
- Use consistent formatting in outputs
- Handle missing data gracefully
- Document all assumptions
