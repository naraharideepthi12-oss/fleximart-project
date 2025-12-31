# Star Schema Design Documentation - FlexiMart Data Warehouse

## Section 1: Schema Overview (4 marks)

### FACT TABLE: fact_sales

**Purpose:** Central fact table containing all sales transactions at the lowest granularity

**Grain:** One row per product per order line item (transaction-level detail)

**Business Process:** Sales transactions capturing every item sold

**Measures (Numeric Facts):**

- `quantity_sold` (INT): Number of units sold in this transaction
- `unit_price` (DECIMAL(10,2)): Price per unit at the time of sale
- `discount_amount` (DECIMAL(10,2)): Discount applied to this line item (default 0)
- `total_amount` (DECIMAL(10,2)): Final amount = (quantity_sold × unit_price) - discount_amount

**Foreign Keys (Dimension References):**

- `date_key` (INT) → References dim_date table
- `product_key` (INT) → References dim_product table
- `customer_key` (INT) → References dim_customer table

**Primary Key:** sale_key (surrogate key, AUTO_INCREMENT)

---

### DIMENSION TABLE: dim_date

**Purpose:** Time dimension enabling temporal analysis of sales

**Type:** Conformed dimension (shared across all fact tables)

**Grain:** One row per calendar date

**Attributes:**

- `date_key` (INT, PRIMARY KEY): Surrogate key in format YYYYMMDD (e.g., 20240115 for 2024-01-15)
- `full_date` (DATE): Actual calendar date
- `day_of_week` (VARCHAR(10)): Day name (Monday, Tuesday, etc.)
- `day_of_month` (INT): Day number (1-31)
- `month` (INT): Month number (1-12)
- `month_name` (VARCHAR(10)): Month name (January, February, etc.)
- `quarter` (VARCHAR(2)): Quarter designation (Q1, Q2, Q3, Q4)
- `year` (INT): Year (2023, 2024, etc.)
- `is_weekend` (BOOLEAN): True if Saturday or Sunday, False otherwise

**Purpose of Each Attribute:**

- Enables year-over-year, quarterly, and monthly comparisons
- Supports drill-down from year → quarter → month → day
- `is_weekend` flag enables special promotions/sales analysis on weekends vs. weekdays

---

### DIMENSION TABLE: dim_product

**Purpose:** Product information dimension for product analysis

**Grain:** One row per unique product

**Attributes:**

- `product_key` (INT, PRIMARY KEY, AUTO_INCREMENT): Surrogate key
- `product_id` (VARCHAR(20)): Original product ID from source system
- `product_name` (VARCHAR(100)): Full product name
- `category` (VARCHAR(50)): Product category (Electronics, Fashion, Groceries)
- `subcategory` (VARCHAR(50)): Product subcategory for detailed analysis
- `unit_price` (DECIMAL(10,2)): Current product price

**Purpose:** Enables analysis by product, category, and subcategory

---

### DIMENSION TABLE: dim_customer

**Purpose:** Customer information dimension for customer segmentation analysis

**Grain:** One row per unique customer

**Attributes:**

- `customer_key` (INT, PRIMARY KEY, AUTO_INCREMENT): Surrogate key
- `customer_id` (VARCHAR(20)): Original customer ID from source system
- `customer_name` (VARCHAR(100)): Full customer name
- `city` (VARCHAR(50)): Customer's city
- `state` (VARCHAR(50)): Customer's state
- `customer_segment` (VARCHAR(20)): Segment classification (Premium, Regular, Occasional)

**Purpose:** Enables customer segmentation, geographic analysis, and customer lifetime value calculations

---

## Section 2: Design Decisions (3 marks - 150 words)

### Why Transaction Line-Item Level Granularity?

This design captures facts at the order line-item level (one fact row per product per order) rather than the order level. This provides maximum flexibility:

**Benefits:**

- **Flexibility:** Can aggregate to any level - item, order, customer, product, date
- **Accuracy:** Eliminates need to recalculate totals; maintains precision
- **Detail Preservation:** Retains product-specific information (e.g., unit_price at time of sale differs from current price)
- **Analytics:** Supports detailed analysis like "which products drive revenue" and "seasonal patterns per product"

### Why Surrogate Keys Instead of Natural Keys?

**Advantages of Surrogate Keys (date_key: YYYYMMDD, product_key: AUTO_INCREMENT):**

1. **Decoupling:** Dimension table changes don't require updating fact table foreign keys
2. **Performance:** Smaller integer keys (4 bytes) vs. varchar keys (10-20 bytes) = faster joins
3. **Stability:** If product ID format changes in source, warehouse remains unaffected
4. **Compression:** Significantly reduces storage and improves query performance
5. **Slowly Changing Dimensions:** Easier to implement SCD Type 2 (versioning) with surrogate keys

### How This Design Supports Drill-Down and Roll-Up

**Drill-Down Example (Year → Quarter → Month → Day):**

```
Year 2024 Total: ₹5,000,000
  ↓
Q1 2024 Total: ₹1,200,000
  ↓
January 2024 Total: ₹400,000
  ↓
2024-01-15 Total: ₹50,000
```

**SQL Implementation:**
The date dimension attributes (year, quarter, month_name, day_of_week) enable GROUP BY at any level without complex date calculations.

**Roll-Up Example (Product Detail → Category → Company Total):**

```
MacBook Pro Sales: ₹2,000,000
  ↑
Electronics Category: ₹8,500,000
  ↑
Company Total: ₹9,200,000
```

The dimension tables enable natural hierarchical aggregation through simple GROUP BY operations.

---

## Section 3: Sample Data Flow (3 marks)

### Example: How One Transaction Flows from Source to Data Warehouse

**SOURCE DATA (OLTP System):**

```
Order #T022
Customer: C002 (Priya Patel)
Order Date: 2024-03-01
Transaction:
  - Product: P001 (Samsung Galaxy S21)
  - Quantity: 1
  - Unit Price: 45,999.00
  - Discount: 0
  - Subtotal: 45,999.00
Order Status: Completed
```

**TRANSFORMATION PROCESS:**

**Step 1: Dimension Lookup & Key Generation**

```
Customer Lookup:
  C002 → Matches dim_customer record → customer_key = 2

Product Lookup:
  P001 → Matches dim_product record → product_key = 1

Date Lookup:
  2024-03-01 → Matches dim_date record → date_key = 20240301
```

**Step 2: Fact Table Record Creation**

```
INSERT INTO fact_sales VALUES (
  sale_key: AUTO_GENERATED,
  date_key: 20240301,
  product_key: 1,
  customer_key: 2,
  quantity_sold: 1,
  unit_price: 45999.00,
  discount_amount: 0.00,
  total_amount: 45999.00
)
```

**RESULTING DATA WAREHOUSE RECORDS:**

**dim_date Record:**

```
date_key: 20240301
full_date: 2024-03-01
day_of_week: Friday
day_of_month: 1
month: 3
month_name: March
quarter: Q1
year: 2024
is_weekend: FALSE
```

**dim_product Record:**

```
product_key: 1
product_id: P001
product_name: Samsung Galaxy S21
category: Electronics
subcategory: Smartphones
unit_price: 45999.00
```

**dim_customer Record:**

```
customer_key: 2
customer_id: C002
customer_name: Priya Patel
city: Mumbai
state: Maharashtra
customer_segment: Premium
```

**fact_sales Record:**

```
sale_key: 1001
date_key: 20240301
product_key: 1
customer_key: 2
quantity_sold: 1
unit_price: 45999.00
discount_amount: 0.00
total_amount: 45999.00
```

### Sample Query Using This Data:

```sql
SELECT
    d.month_name,
    p.category,
    c.customer_name,
    SUM(f.total_amount) as sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE d.year = 2024
GROUP BY d.month_name, p.category, c.customer_name
ORDER BY d.month_name DESC, sales DESC;
```

This query naturally demonstrates the star schema's power - single fact table connecting to multiple dimensions for rich analysis.

---

## Benefits of This Star Schema Design

1. **Query Performance:** Single fact table join reduces query complexity
2. **Maintainability:** Clear separation of dimensions and facts
3. **Scalability:** Dimensions change independently of facts
4. **Understandability:** Intuitive structure for business users
5. **Flexibility:** Supports any combination of dimensional analysis
6. **Aggregation:** Built-in support for drill-down/roll-up operations
