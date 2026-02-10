# Task: Process and Analyze an Excel Workbook

Transform a multi-sheet Excel workbook by adding calculations, analysis, and a dashboard.

## Setup

First, generate the sample workbook:
```bash
pip install openpyxl
python generate_workbook.py
```

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

Add these columns (with formulas, not hardcoded values):

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
| ... | | | | | |

**Top 10 Products by Revenue:**
| Rank | Product | Revenue_USD |
|------|---------|-------------|
| 1 | ... | ... |

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

- **Target Achievement**: Green (>=100%), Yellow (80-99%), Red (<80%)
- **Revenue columns**: Data bars
- **Top 10%**: Bold green text
- **Bottom 10%**: Red italic text

### 6. Create analysis_summary.json

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

## Technical Requirements

- Use `openpyxl` for Excel operations
- Formulas should use cell references (not hardcoded values)
- Charts must be embedded Excel charts
- Preserve original data (add new sheets/columns, don't delete)

## Example Code Patterns

```python
from openpyxl import load_workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule

wb = load_workbook("financial_data.xlsx")
ws = wb["Sales"]

# Add formula
ws["J2"] = "=F2*G2*(1-I2/100)"

# Add VLOOKUP
ws["K2"] = '=VLOOKUP(H2,Exchange_Rates!A:B,2,FALSE)*J2'

# Add chart
chart = BarChart()
chart.add_data(Reference(ws, min_col=11, min_row=1, max_row=100))
ws_dashboard.add_chart(chart, "A10")

# Conditional formatting
rule = DataBarRule(start_type='min', end_type='max', color="638EC6")
ws.conditional_formatting.add("J2:J500", rule)

wb.save("financial_data.xlsx")
```

## Evaluation

Your modified workbook will be checked for:
- All new sheets present
- Formulas calculate correctly
- Charts render with correct data
- Conditional formatting applied
- Summary JSON matches actual data
