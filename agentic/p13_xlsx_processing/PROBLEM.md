# Problem 13: Excel Spreadsheet Processing & Analysis

## Difficulty: Hard (Agentic)
## Expected Tool Calls: 15-25
## Skills Required: xlsx reading/writing, formulas, charts

## Task

Process a complex Excel workbook with multiple sheets, add calculations, create charts, and generate a summary dashboard.

## Input File

`financial_data.xlsx` - A workbook with 5 sheets:
1. Sales - Transaction-level sales data
2. Products - Product catalog
3. Regions - Regional information
4. Targets - Monthly targets
5. Exchange_Rates - Currency conversion rates

## Requirements

### 1. Data Validation & Cleaning

Create a new sheet "Data_Quality" with:
- Count of missing values per column
- Count of duplicate rows
- List of data anomalies (negative quantities, future dates, etc.)
- Summary statistics for numeric columns

### 2. Calculated Columns

Add to "Sales" sheet:
- `Revenue_USD` - Revenue converted to USD using exchange rates
- `Margin` - Calculated from product cost data
- `Quarter` - Derived from date
- `Target_Achievement` - Actual vs target percentage

### 3. Pivot Analysis

Create new sheet "Pivot_Analysis" with:
- Revenue by Region and Quarter (pivot table style)
- Top 10 products by revenue
- Monthly trend summary
- Customer segment breakdown

### 4. Dashboard Sheet

Create "Dashboard" sheet with:
- KPI cards (Total Revenue, Total Orders, Avg Order Value, YoY Growth)
- Bar chart: Revenue by Region
- Line chart: Monthly Revenue Trend
- Pie chart: Revenue by Product Category
- Table: Top 5 performing regions

### 5. Conditional Formatting

Apply to appropriate sheets:
- Red/Yellow/Green for target achievement
- Data bars for revenue columns
- Highlight top/bottom 10% performers

### 6. Output Summary

Create `analysis_summary.json`:
```json
{
  "total_revenue_usd": 0,
  "total_orders": 0,
  "unique_customers": 0,
  "date_range": {"start": "...", "end": "..."},
  "top_region": "...",
  "top_product": "...",
  "data_quality_issues": 0,
  "yoy_growth": 0.0
}
```

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Data quality sheet complete | 10 |
| Calculated columns correct | 15 |
| Pivot analysis accurate | 15 |
| Dashboard complete | 20 |
| Charts render correctly | 15 |
| Conditional formatting applied | 10 |
| Summary JSON accurate | 10 |
| Formulas use proper references | 5 |
| **Total** | **100** |

## Hints

- Use openpyxl for Excel operations
- Formula strings start with '='
- Charts need data ranges as references
- Conditional formatting uses rules
- Named ranges can simplify formulas
