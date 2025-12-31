# Database Schema Documentation - FlexiMart

## Entity-Relationship Description (Text Format)

### ENTITY: customers

**Purpose:** Stores customer information including registration details and contact information

**Attributes:**

- `customer_id` (INT, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each customer
- `first_name` (VARCHAR(50), NOT NULL): Customer's first name
- `last_name` (VARCHAR(50), NOT NULL): Customer's last name
- `email` (VARCHAR(100), UNIQUE, NOT NULL): Customer's email address (unique constraint ensures no duplicate emails)
- `phone` (VARCHAR(20)): Customer's phone number in standardized format (+91-XXXXXXXXXX)
- `city` (VARCHAR(50)): Customer's city of residence
- `registration_date` (DATE): Date when customer registered with FlexiMart platform

**Relationships:**

- One customer can place MANY orders (1:M with orders table)

---

### ENTITY: products

**Purpose:** Stores product information including pricing and inventory details

**Attributes:**

- `product_id` (INT, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each product
- `product_name` (VARCHAR(100), NOT NULL): Name of the product
- `category` (VARCHAR(50), NOT NULL): Product category (Electronics, Fashion, Groceries)
- `price` (DECIMAL(10,2), NOT NULL): Product price in rupees
- `stock_quantity` (INT, DEFAULT 0): Current inventory stock level

**Relationships:**

- One product can be ordered in MANY order_items (1:M with order_items table)

---

### ENTITY: orders

**Purpose:** Stores order/transaction information for sales tracking

**Attributes:**

- `order_id` (INT, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each order
- `customer_id` (INT, NOT NULL, FOREIGN KEY): References customer who placed the order
- `order_date` (DATE, NOT NULL): Date when order was placed
- `total_amount` (DECIMAL(10,2), NOT NULL): Total amount of the order in rupees
- `status` (VARCHAR(20), DEFAULT 'Pending'): Order status (Pending, Completed, Cancelled)

**Relationships:**

- Many orders belong to ONE customer (M:1 with customers table)
- One order can contain MANY order_items (1:M with order_items table)

---

### ENTITY: order_items

**Purpose:** Stores line-item details for each order (bridge table for orders and products)

**Attributes:**

- `order_item_id` (INT, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each line item
- `order_id` (INT, NOT NULL, FOREIGN KEY): References the order this item belongs to
- `product_id` (INT, NOT NULL, FOREIGN KEY): References the product being ordered
- `quantity` (INT, NOT NULL): Number of units of this product in the order
- `unit_price` (DECIMAL(10,2), NOT NULL): Price per unit at the time of order
- `subtotal` (DECIMAL(10,2), NOT NULL): Line item total (quantity × unit_price)

**Relationships:**

- Many order_items belong to ONE order (M:1 with orders table)
- Many order_items reference ONE product (M:1 with products table)

---

## Normalization Explanation (3NF Compliance)

### Why This Design is in Third Normal Form (3NF)?

The FlexiMart database schema is designed to be in **Third Normal Form (3NF)**, which means it satisfies all requirements of both 1NF and 2NF, plus the additional 3NF requirement that no non-prime attribute (non-key attribute) is transitively dependent on a primary key.

**Functional Dependencies:**

1. **customers table:**

   - customer_id → {first_name, last_name, email, phone, city, registration_date}
   - Primary functional dependency: All attributes depend only on customer_id

2. **products table:**

   - product_id → {product_name, category, price, stock_quantity}
   - Primary functional dependency: All attributes depend only on product_id

3. **orders table:**

   - order_id → {customer_id, order_date, total_amount, status}
   - customer_id is a foreign key, not a non-prime attribute creating transitive dependency
   - Total_amount can be derived but is stored for query efficiency

4. **order_items table:**
   - order_item_id → {order_id, product_id, quantity, unit_price, subtotal}
   - Both foreign keys are necessary for the relationship
   - Subtotal is stored for query efficiency (not a transitive dependency)

**Avoidance of Anomalies:**

1. **Update Anomalies:** If a customer's email changes, we only update one record in the customers table. Without normalization, updating customer information in orders would create inconsistencies.

2. **Insert Anomalies:** We can insert a new product without requiring an order to exist. Without normalization (flat table), we'd need dummy order data.

3. **Delete Anomalies:** If we delete all orders, customer information is preserved in the customers table. Without normalization, deleting an order might remove customer data.

The design achieves 3NF by:

- Separating customer data from transaction data
- Separating product data from order data
- Using junction table (order_items) to manage the M:M relationship between orders and products
- Eliminating transitive dependencies through proper use of foreign keys

---

## Sample Data Representation

### CUSTOMERS Table (Sample Records)

| customer_id | first_name | last_name | email                    | phone          | city      | registration_date |
| ----------- | ---------- | --------- | ------------------------ | -------------- | --------- | ----------------- |
| 1           | Rahul      | Sharma    | rahul.sharma@gmail.com   | +91-9876543210 | Bangalore | 2023-01-15        |
| 2           | Priya      | Patel     | priya.patel@yahoo.com    | +91-9988776655 | Mumbai    | 2023-02-20        |
| 3           | Amit       | Kumar     | amit.kumar@fleximart.com | +91-9765432109 | Delhi     | 2023-03-10        |

### PRODUCTS Table (Sample Records)

| product_id | product_name       | category    | price    | stock_quantity |
| ---------- | ------------------ | ----------- | -------- | -------------- |
| 1          | Samsung Galaxy S21 | Electronics | 45999.00 | 150            |
| 2          | Nike Running Shoes | Fashion     | 3499.00  | 80             |
| 3          | Organic Almonds    | Groceries   | 899.00   | 0              |

### ORDERS Table (Sample Records)

| order_id | customer_id | order_date | total_amount | status    |
| -------- | ----------- | ---------- | ------------ | --------- |
| 1        | 1           | 2024-01-15 | 45999.00     | Completed |
| 2        | 2           | 2024-01-16 | 6998.00      | Completed |
| 3        | 3           | 2024-01-20 | 2925.00      | Pending   |

### ORDER_ITEMS Table (Sample Records)

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
| ------------- | -------- | ---------- | -------- | ---------- | -------- |
| 1             | 1        | 1          | 1        | 45999.00   | 45999.00 |
| 2             | 2        | 2          | 2        | 3499.00    | 6998.00  |
| 3             | 3        | 3          | 5        | 650.00     | 3250.00  |

---

## Database Diagram (Relational View)

```
customers (1)
    ├─→ (1:M) ─→ orders (M)

orders (1)
    └─→ (1:M) ─→ order_items (M)

order_items (M)
    └─→ (M:1) ─→ products (1)
```

This normalized design supports efficient querying and maintains data integrity across all operations.
