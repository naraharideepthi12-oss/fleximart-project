# Part 1: ETL Pipeline & OLTP Database

## Overview

Part 1 implements an ETL (Extract-Transform-Load) pipeline that ingests raw CSV data with quality issues into a normalized MySQL/PostgreSQL database.

**Components:**

- ETL Pipeline Implementation
- Database Schema Documentation
- Business Intelligence Queries

---

## Files

### `etl_pipeline.py`

Complete ETL script with:

- **Extract Phase:** Reads CSV files (customers, products, sales)
- **Transform Phase:**
  - Removes duplicates
  - Standardizes phone numbers (+91-XXXXXXXXXX)
  - Normalizes categories
  - Handles multiple date formats (YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY)
  - Processes missing values
- **Load Phase:** Inserts cleaned data into MySQL database

### `data_quality_report.txt`

Auto-generated report showing:

- Records processed vs. loaded
- Duplicates removed
- Missing values handled

### `schema_documentation.md`

- Entity-Relationship diagram description
- Normalization explanation (3NF compliance)
- Sample data records

### `business_queries.sql`

Complex SQL queries demonstrating:

- Multi-table JOINs
- Aggregations (GROUP BY, ORDER BY)
- Filtering with WHERE clauses

---

## Running the Pipeline

### Prerequisites

```bash
# Install dependencies
pip install pandas mysql-connector-python

# Create MySQL database
mysql -u root -p -e "CREATE DATABASE fleximart;"
```

### Execute

```bash
# Update database credentials in etl_pipeline.py (if needed)
python etl_pipeline.py
```

### Verify

```bash
# Check the generated quality report
cat data_quality_report.txt
```

### Expected Output

```
✓ Database connection successful
✓ Database tables created
✓ ETL Pipeline completed
✓ Quality report saved
```

---

## Database Tables

**customers** - Customer information

- customer_id (PK)
- name, email, phone
- unique constraint on email

**products** - Product catalog

- product_id (PK)
- name, category, price, stock

**orders** - Sales transactions

- order_id (PK)
- customer_id (FK), order_date, total_amount

**order_items** - Order line items

- order_item_id (PK)
- order_id (FK), product_id (FK)
- quantity, unit_price

---

## Relationships

- One customer → Many orders (1:M)
- One order → Many order_items (1:M)
- One product → Many order_items (1:M)

All tables designed in 3rd Normal Form (3NF) to eliminate anomalies.
