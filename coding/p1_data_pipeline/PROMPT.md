# Task: Data Pipeline Processing

You are given a messy CSV file `sales_data.csv` containing sales records with various data quality issues.

## Your Task

Create a Python script `solution.py` that processes this data and produces clean outputs.

## Input File

`sales_data.csv` - Contains sales data with these columns:
- order_id, date, region, product_category, quantity, unit_price, revenue, discount, customer_id, timestamp

## Data Quality Issues to Handle

1. **Date formats are inconsistent**: MM/DD/YYYY, YYYY-MM-DD, DD-Mon-YY, and Unix timestamps
2. **Numeric fields have formatting issues**: Currency symbols ($), commas, "N/A", "NULL", empty strings
3. **Duplicate rows**: Same order_id appears multiple times - keep the one with the latest timestamp
4. **Invalid data**: Some rows have invalid dates or negative quantities

## Required Outputs

1. **`cleaned_data.parquet`** - Cleaned, deduplicated data with:
   - All dates as datetime type
   - All numeric fields as proper numbers
   - Duplicates removed (keep latest by timestamp)

2. **`aggregated_stats.json`** - Statistics grouped by region and product_category:
   - total_revenue
   - avg_order_value
   - order_count

3. **`flagged_issues.csv`** - Rows with problems:
   - Discount > 50% (suspicious)
   - quantity * unit_price doesn't match revenue (within 1% tolerance)

4. **`processing_log.txt`** - Log of parsing errors and decisions

## Requirements

- Handle all edge cases gracefully (don't crash on bad data)
- Use pandas for data processing
- Output parquet requires pyarrow or fastparquet

## Run Your Solution

```bash
python solution.py
```

The solution should read `sales_data.csv` from the current directory and write outputs to the current directory.
