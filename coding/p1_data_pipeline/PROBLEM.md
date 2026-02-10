# Problem 1: Complex Data Pipeline

## Difficulty: Hard
## Expected Time: 30-45 minutes
## Discrimination Target: Date parsing, edge cases, aggregation logic

## Task

Process the messy `sales_data.csv` file and produce clean outputs.

## Input File
- `sales_data.csv` - 1000 rows of sales data with intentional messiness

## Requirements

1. **Date Normalization**: Handle multiple formats:
   - MM/DD/YYYY, YYYY-MM-DD, DD-Mon-YY, Unix timestamps
   - Invalid dates should be logged, not crash

2. **Numeric Cleaning**:
   - Remove $, commas from currency
   - Handle "N/A", "NULL", "", "-" as missing
   - Percentages like "15%" → 0.15

3. **Deduplication**:
   - Rows with same (order_id) are duplicates
   - Keep the row with latest timestamp
   - If same timestamp, keep higher revenue

4. **Aggregation**:
   - Group by region and product_category
   - Calculate: total_revenue, avg_order_value, order_count
   - Running total within each region (sorted by date)

5. **Validation**:
   - Flag rows where discount > 50% (suspicious)
   - Flag rows where quantity * unit_price != revenue (within 1% tolerance)

## Output Files

1. `cleaned_data.parquet` - All valid, deduplicated rows
2. `aggregated_stats.json` - Grouped statistics
3. `flagged_issues.csv` - Problematic rows with reason
4. `processing_log.txt` - Parsing errors and decisions made

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| All date formats parsed correctly | 20 |
| Numeric cleaning handles all edge cases | 15 |
| Deduplication logic correct | 15 |
| Aggregations mathematically correct | 20 |
| Validation flags accurate | 15 |
| Code handles file not found, empty file | 10 |
| Clean, readable code | 5 |
| **Total** | **100** |

## Test Command
```bash
python evaluate_p1.py solution.py
```
