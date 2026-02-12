# Task: Process and Analyze an Excel Workbook

Transform a multi-sheet Excel workbook by adding calculations, analysis, and a dashboard using the `/xlsx` skill.

## Setup

First, generate the sample workbook:
```bash
pip install openpyxl
python generate_workbook.py
```

## Skills Available

You have access to the `/xlsx` skill for Excel operations. Use it to:
- Read and modify Excel workbooks
- Add formulas (NOT hardcoded values)
- Create charts and conditional formatting
- Follow financial modeling best practices

**Critical**: The skill emphasizes using Excel formulas instead of hardcoded values. Read this section carefully!

## Input File

`financial_data.xlsx` contains 5 sheets:
- **Sales**: 500+ transaction records
- **Products**: Product catalog with costs
- **Regions**: Region information
- **Targets**: Monthly revenue targets
- **Exchange_Rates**: Currency conversion rates

## Your Task

Modify the workbook and create `analysis_summary.json`.

### 1. Add "Data_Quality" Sheet

Analyze data quality issues:

| Check | Result |
|-------|--------|
| Total Rows (Sales) | [count] |
| Missing Customer_ID | [count] |
| Missing Product_ID | [count] |
| Duplicate Order_IDs | [count] |
| Negative Quantities | [count] |
| Future Dates | [count] |

### 2. Add Calculated Columns to Sales Sheet

Add these columns **with formulas** (as specified in /xlsx skill):

- **Revenue**: `=Quantity * Unit_Price * (1 - Discount_Pct/100)`
- **Revenue_USD**: Revenue converted using Exchange_Rates (VLOOKUP)
- **Quarter**: Derived from Date (e.g., "Q1 2024")
- **Month**: Month name from Date
- **Product_Category**: VLOOKUP from Products sheet
- **Region_Name**: VLOOKUP from Regions sheet

### 3. Create "Pivot_Analysis" Sheet

Build these summary tables:

**Revenue by Region and Quarter:**
| Region | Q1 | Q2 | Q3 | Q4 | Total |
|--------|----|----|----|----|-------|
| North America | ... | ... | ... | ... | ... |

**Top 10 Products by Revenue:**
| Rank | Product | Revenue_USD |
|------|---------|-------------|

**Monthly Trend:**
| Month | Orders | Revenue_USD | Avg_Order |
|-------|--------|-------------|-----------|

### 4. Create "Dashboard" Sheet

A summary dashboard with:

**KPI Section (top):**
- Total Revenue (USD): $X,XXX,XXX
- Total Orders: X,XXX
- Unique Customers: XXX
- Average Order Value: $XXX

**Charts:**
- Bar Chart: Revenue by Region
- Line Chart: Monthly Revenue Trend
- Pie Chart: Revenue by Product Category

**Top Performers Table:**
| Rank | Region | Revenue | vs Target |
|------|--------|---------|-----------|

### 5. Apply Conditional Formatting

As documented in `/xlsx` skill:
- **Target Achievement**: Green (>=100%), Yellow (80-99%), Red (<80%)
- **Revenue columns**: Data bars
- **Top 10%**: Bold green text
- **Bottom 10%**: Red italic text

### 6. Recalculate Formulas

**Critical**: After adding formulas, use the recalculation script as specified in the `/xlsx` skill:
```bash
python scripts/recalc.py financial_data.xlsx
```

Check for formula errors (#REF!, #DIV/0!, etc.) and fix them.

### 7. Create analysis_summary.json

```json
{
  "generated_at": "ISO timestamp",
  "data_overview": {
    "total_rows": 0,
    "date_range": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
    "unique_customers": 0,
    "unique_products": 0
  },
  "revenue_summary": {
    "total_usd": 0.00,
    "by_region": {
      "North America": 0.00,
      "Western Europe": 0.00,
      "APAC": 0.00,
      "Latin America": 0.00,
      "Eastern Europe": 0.00
    },
    "by_quarter": {
      "Q1": 0.00, "Q2": 0.00, "Q3": 0.00, "Q4": 0.00
    }
  },
  "top_performers": {
    "region": "...",
    "product": "...",
    "customer": "..."
  },
  "data_quality": {
    "missing_values": 0,
    "duplicates": 0,
    "anomalies": 0
  }
}
```

## Skill Usage Expectations

This task tests your ability to:
1. **Invoke the /xlsx skill** and understand its requirements
2. **Use formulas NOT hardcoded values** (critical skill requirement)
3. **Apply financial modeling standards** (color coding, number formats)
4. **Create embedded Excel charts**
5. **Use conditional formatting** patterns from the skill
6. **Perform formula verification** using recalc script

## Key Skill Concepts to Apply

From the `/xlsx` skill, pay attention to:
- Formula construction rules
- Color coding standards (blue for inputs, black for formulas)
- Number formatting standards
- Verification checklist
- Common pitfalls (NaN handling, column mapping)

## Evaluation

Your modified workbook will be checked for:
- Proper /xlsx skill invocation
- All new sheets present
- **Formulas used (not hardcoded values)**
- Formulas calculate correctly (no errors)
- Charts render with correct data
- Conditional formatting applied
- Summary JSON matches actual data
