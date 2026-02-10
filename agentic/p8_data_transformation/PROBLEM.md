# Problem 8: Multi-Stage Data Transformation

## Difficulty: Very Hard (Agentic)
## Expected Tool Calls: 12-25
## Discrimination Target: Multi-format parsing, data joining, validation

## Task

Process 5 data files in different formats and produce a unified order fulfillment report.

## Input Files

1. `users.csv` - Customer information
2. `orders.xml` - Order records
3. `products.json` - Product catalog
4. `inventory.yaml` - Stock levels
5. `pricing.ini` - Price rules and discounts

## Requirements

### Data Processing
1. Parse ALL 5 files (handle malformed entries gracefully)
2. Join data: orders ← users ← products ← inventory ← pricing
3. Calculate final prices with applicable discounts
4. Check stock availability for each order
5. Flag issues: out of stock, price mismatches, orphan records

### Output Files
1. `fulfillment.csv` - Orders ready to fulfill
2. `issues.json` - Problems found during processing
3. `summary.md` - Statistics and report

### Validation
- Row counts must reconcile
- All orders must be either fulfilled or flagged
- No data loss during transformation

## Detailed Requirements

### fulfillment.csv columns:
- order_id
- customer_name
- customer_email
- product_name
- quantity
- unit_price
- discount_percent
- final_price
- in_stock (true/false)
- fulfillment_status (ready/partial/blocked)

### issues.json structure:
```json
{
  "out_of_stock": [...],
  "price_mismatch": [...],
  "missing_customer": [...],
  "missing_product": [...],
  "invalid_data": [...]
}
```

### summary.md sections:
- Total orders processed
- Orders by status (ready/partial/blocked)
- Revenue summary
- Top 5 products by order count
- Issues breakdown

## Evaluation

```bash
python evaluate_p8.py
```

Checks:
- All input files correctly parsed
- Joins performed correctly
- Calculations accurate
- Issues properly flagged
- Output format correct
- Row counts reconcile

## Scoring

| Criterion | Points |
|-----------|--------|
| CSV parsing | 10 |
| XML parsing | 10 |
| JSON parsing | 10 |
| YAML parsing | 10 |
| INI parsing | 5 |
| Data joining correct | 15 |
| Price calculations | 10 |
| Stock validation | 10 |
| Issues properly flagged | 10 |
| Summary statistics | 5 |
| Row count reconciliation | 5 |
| **Total** | **100** |

## Hints

- Use pandas for CSV operations
- xml.etree.ElementTree for XML
- PyYAML for YAML (or parse manually)
- configparser for INI
- Watch for data type mismatches when joining
- Some records are intentionally malformed
