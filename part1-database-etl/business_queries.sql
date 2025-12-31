-- ============================================================================
-- BUSINESS QUERIES FOR FLEXIMART
-- ============================================================================

-- ============================================================================
-- Query 1: Customer Purchase History
-- ============================================================================
-- Business Question: "Generate a detailed report showing each customer's name, 
-- email, total number of orders placed, and total amount spent. Include only 
-- customers who have placed at least 2 orders and spent more than ₹5,000. 
-- Order by total amount spent in descending order."

-- Requirements:
-- - Must join: customers, orders, order_items tables
-- - Use GROUP BY with HAVING clause
-- - Calculate aggregates: COUNT of orders, SUM of amounts

SELECT 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
HAVING COUNT(DISTINCT o.order_id) >= 2 AND SUM(o.total_amount) > 5000
ORDER BY total_spent DESC;

-- ============================================================================
-- Query 2: Product Sales Analysis
-- ============================================================================
-- Business Question: "For each product category, show the category name, 
-- number of different products sold, total quantity sold, and total revenue 
-- generated. Only include categories that have generated more than ₹10,000 
-- in revenue. Order by total revenue descending."

-- Requirements:
-- - Must join: products, order_items tables
-- - Use GROUP BY with HAVING clause
-- - Calculate: COUNT(DISTINCT), SUM aggregates

SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) AS num_products,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
HAVING SUM(oi.quantity * oi.unit_price) > 10000
ORDER BY total_revenue DESC;

-- ============================================================================
-- Query 3: Monthly Sales Trend
-- ============================================================================
-- Business Question: "Show monthly sales trends for the year 2024. For each 
-- month, display the month name, total number of orders, total revenue, and 
-- the running total of revenue (cumulative revenue from January to that month)."

-- Requirements:
-- - Use window function (SUM() OVER) for running total
-- - Extract month from order_date
-- - Group by month
-- - Order chronologically

SELECT 
    MONTHNAME(o.order_date) AS month_name,
    MONTH(o.order_date) AS month_num,
    YEAR(o.order_date) AS year_num,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS monthly_revenue,
    ROUND(
        SUM(SUM(o.total_amount)) OVER (
            ORDER BY YEAR(o.order_date), MONTH(o.order_date)
        ), 2
    ) AS cumulative_revenue
FROM orders o
WHERE YEAR(o.order_date) = 2024
GROUP BY 
    YEAR(o.order_date), 
    MONTH(o.order_date), 
    MONTHNAME(o.order_date)
ORDER BY year_num, month_num;

-- ============================================================================
-- Additional Useful Queries
-- ============================================================================

-- Query to check data integrity (count of records)
SELECT 
    'customers' AS table_name,
    COUNT(*) AS record_count
FROM customers
UNION ALL
SELECT 
    'products' AS table_name,
    COUNT(*) AS record_count
FROM products
UNION ALL
SELECT 
    'orders' AS table_name,
    COUNT(*) AS record_count
FROM orders
UNION ALL
SELECT 
    'order_items' AS table_name,
    COUNT(*) AS record_count
FROM order_items;

-- Query to find top 5 best-selling products
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_units_sold DESC
LIMIT 5;

-- Query to find customers with highest spending
SELECT 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.city,
    ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city
ORDER BY total_spent DESC
LIMIT 10;
