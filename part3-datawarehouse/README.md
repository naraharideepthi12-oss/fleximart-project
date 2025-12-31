# Part 3: Data Warehouse & OLAP Analytics

## Overview

Part 3 implements a complete data warehouse using the star schema design pattern, enabling advanced analytical queries and business intelligence reporting.

**Components:**

- Star Schema Design Documentation
- Star Schema Implementation
- OLAP Analytics Queries

---

## Files

### `star_schema_design.md`

Comprehensive schema documentation explaining:

**FACT TABLE: fact_sales** (Sales transactions)

- Measures: quantity_sold, unit_price, discount_amount, total_amount
- Foreign Keys: date_key, product_key, customer_key
- Surrogate Key: sale_key (PK)

**DIMENSION TABLES:**

1. **dim_date** (Time dimension)

   - date_key (PK), full_date, day, month, quarter, year
   - Enables temporal analysis

2. **dim_product** (Product dimension)

   - product_key (PK), product_id, name, category, price
   - Supports product-based analytics

3. **dim_customer** (Customer dimension)
   - customer_key (PK), customer_id, name, email, region, segment
   - Enables customer-based reporting

---

## Database Setup

### `warehouse_schema.sql`

DDL statements creating:

- 4 tables (1 fact, 3 dimensions)
- Primary and foreign key constraints
- Indexes on dimension keys for performance
- Appropriate data types for measures and attributes

### `warehouse_data.sql`

Sample data including:

- 30 date records (temporal coverage)
- 15 products across categories
- 12 customers across regions
- 40+ sales transactions

---

## Analytics Implementation

### `analytics_queries.sql`

Advanced OLAP queries demonstrating:

**Query 1: Sales by Category Over Time**

```sql
SELECT dim_product.category, dim_date.quarter,
       SUM(fact_sales.total_amount) as total_sales
FROM fact_sales
JOIN dim_product ON fact_sales.product_key = dim_product.product_key
JOIN dim_date ON fact_sales.date_key = dim_date.date_key
GROUP BY dim_product.category, dim_date.quarter
ORDER BY dim_date.quarter, total_sales DESC;
```

**Query 2: Customer Segmentation Analysis**

```sql
SELECT dim_customer.segment,
       COUNT(DISTINCT dim_customer.customer_key) as customer_count,
       SUM(fact_sales.total_amount) as segment_revenue
FROM fact_sales
JOIN dim_customer ON fact_sales.customer_key = dim_customer.customer_key
GROUP BY dim_customer.segment
ORDER BY segment_revenue DESC;
```

**Query 3: Product Performance Metrics**

```sql
SELECT dim_product.name, dim_product.category,
       SUM(fact_sales.quantity_sold) as total_qty,
       AVG(fact_sales.total_amount) as avg_sale,
       COUNT(*) as transaction_count
FROM fact_sales
JOIN dim_product ON fact_sales.product_key = dim_product.product_key
GROUP BY dim_product.product_key, dim_product.name, dim_product.category
HAVING COUNT(*) > 1
ORDER BY total_qty DESC;
```

---

## Running the Setup

```bash
# Create databases and load schema
mysql -u root -p < warehouse_schema.sql
mysql -u root -p fleximart_dw < warehouse_data.sql

# Run analytics queries
mysql -u root -p fleximart_dw < analytics_queries.sql
```

---

## Star Schema Advantages

✅ **Simplified Queries** - No complex joins, straightforward dimension access
✅ **Fast Aggregations** - Fact table pre-aggregated, minimal computation
✅ **Scalable** - Dimensions grow slowly, facts scale horizontally
✅ **Intuitive** - Business users understand dimension-based queries
✅ **OLAP-Ready** - Optimized for read-heavy analytical workloads

---

## Key Metrics

**Measures Tracked:**

- Sales amount (total, discounted)
- Quantities sold
- Unit pricing

**Dimensions for Analysis:**

- Time (temporal trends)
- Product (category, performance)
- Customer (segments, regions)

---

## Performance Optimization

- Indexes on foreign keys for join performance
- Surrogate keys (integers) for efficient lookups
- Dimension table denormalization for query simplicity
- Appropriate data types for storage efficiency
