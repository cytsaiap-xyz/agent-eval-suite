# Task: Multi-Format Data Transformation Pipeline

Process 5 data files in different formats and produce a unified order fulfillment report.

## Your Task

Read all input files, join the data, and produce three output files.

## Input Files

You have 5 files in different formats:

1. **`users.csv`** - Customer information
   - user_id, name, email, tier, signup_date
   - Some emails may be invalid

2. **`orders.xml`** - Order records
   - Order ID, user ID, date, items (product_id, quantity)
   - Some orders reference non-existent users
   - Some orders have missing data

3. **`products.json`** - Product catalog
   - id, name, category, base_price, weight_kg
   - Some products may be discontinued

4. **`inventory.yaml`** - Current stock levels
   - Product ID → quantity, warehouse, reorder_point
   - Some products may be out of stock (quantity: 0)

5. **`pricing.ini`** - Pricing rules
   - Tier discounts (bronze/silver/gold/platinum)
   - Category discounts
   - Bulk order discounts
   - Active promotions

## Required Outputs

### 1. `fulfillment.csv`

One row per order item with columns:
- order_id
- customer_name
- customer_email
- product_name
- quantity
- unit_price (from products.json)
- discount_percent (calculated from pricing rules)
- final_price (unit_price × quantity × (1 - discount))
- in_stock (true/false based on inventory)
- fulfillment_status: "ready" | "partial" | "blocked"

### 2. `issues.json`

Document all problems found:
```json
{
  "out_of_stock": [
    {"order_id": "...", "product_id": "...", "requested": 10, "available": 0}
  ],
  "missing_customer": [
    {"order_id": "...", "user_id": "..."}
  ],
  "missing_product": [
    {"order_id": "...", "product_id": "..."}
  ],
  "invalid_data": [
    {"file": "...", "issue": "..."}
  ]
}
```

### 3. `summary.md`

A markdown report with:
- Total orders processed
- Orders by status (ready/partial/blocked)
- Total revenue (sum of final_price for fulfillable orders)
- Top 5 products by order count
- Issues breakdown by category

## Discount Calculation

Apply discounts in this order:
1. Customer tier discount (from pricing.ini [tier_discounts])
2. Product category discount (from pricing.ini [category_discounts])
3. Bulk discount if quantity >= min_quantity (from pricing.ini [bulk_discounts])
4. Product-specific promotions (from pricing.ini [promotions])

Discounts are additive (not compounded).

## Data Joining

```
orders → users (via user_id)
orders.items → products (via product_id)
products → inventory (via product_id)
products → pricing (via category and promotions)
users → pricing (via tier)
```

## Handling Issues

- **Missing user**: Log to issues.json, still process order but mark customer_name as "Unknown"
- **Missing product**: Log to issues.json, skip that order item
- **Out of stock**: Include in fulfillment.csv with in_stock=false, fulfillment_status="blocked"
- **Partial stock**: If requested > available, status="partial"
- **Malformed data**: Log to issues.json invalid_data, continue processing

## Validation

Your row counts should reconcile:
- Total order items = fulfillment.csv rows + skipped (missing product)
- All orders appear either in fulfillment.csv or issues.json

## Example Commands

You can use Python with standard libraries plus:
- pandas for CSV
- xml.etree.ElementTree for XML
- json for JSON
- PyYAML or manual parsing for YAML
- configparser for INI
