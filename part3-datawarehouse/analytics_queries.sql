-- ============================================================================
-- OLAP ANALYTICS QUERIES - FLEXIMART DATA WAREHOUSE
-- ============================================================================
-- Database: fleximart_dw
-- Purpose: Analytical queries for business insights

USE fleximart_dw;

-- ============================================================================
-- Query 1: Monthly Sales Drill-Down Analysis (5 marks)
-- ============================================================================
-- Business Scenario: "The CEO wants to see sales performance broken down by 
-- time periods. Start with yearly total, then quarterly, then monthly sales 
-- for 2024."

-- Requirements:
-- - Show: year, quarter, month, total_sales, total_quantity
-- - Group by year, quarter, month
-- - Order chronologically
-- - Demonstrates drill-down (Year → Quarter → Month)

SELECT 
    d.year,
    d.quarter,
    d.month_name,
    d.month,
    COUNT(DISTINCT f.sale_key) as total_orders,
    SUM(f.quantity_sold) as total_quantity,
    ROUND(SUM(f.total_amount), 2) as monthly_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY 
    d.year,
    d.quarter,
    d.month,
    d.month_name
ORDER BY 
    d.year ASC,
    d.month ASC;

-- Alternative with Cumulative (Running Total) - Advanced Drill-Down
SELECT 
    d.year,
    d.quarter,
    d.month_name,
    COUNT(DISTINCT f.sale_key) as total_orders,
    SUM(f.quantity_sold) as total_quantity,
    ROUND(SUM(f.total_amount), 2) as monthly_revenue,
    ROUND(
        SUM(SUM(f.total_amount)) OVER (
            PARTITION BY d.year 
            ORDER BY d.month
        ), 2
    ) as cumulative_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY 
    d.year,
    d.quarter,
    d.month,
    d.month_name
ORDER BY 
    d.year ASC,
    d.month ASC;

-- ============================================================================
-- Query 2: Product Performance Analysis (5 marks)
-- ============================================================================
-- Business Scenario: "The product manager needs to identify top-performing 
-- products. Show the top 10 products by revenue, along with their category, 
-- total units sold, and revenue contribution percentage."

-- Requirements:
-- - Join fact_sales with dim_product
-- - Calculate: total revenue, total quantity per product
-- - Calculate: percentage of total revenue
-- - Order by revenue descending
-- - Limit to top 10

SELECT 
    p.product_name,
    p.category,
    SUM(f.quantity_sold) as units_sold,
    ROUND(SUM(f.total_amount), 2) as revenue,
    ROUND(
        (SUM(f.total_amount) / SUM(SUM(f.total_amount)) OVER ()) * 100, 
        2
    ) as revenue_percentage
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY 
    p.product_key,
    p.product_name,
    p.category
ORDER BY 
    revenue DESC
LIMIT 10;

-- Alternative with CTE for clarity
WITH product_sales AS (
    SELECT 
        p.product_name,
        p.category,
        p.product_key,
        SUM(f.quantity_sold) as units_sold,
        SUM(f.total_amount) as total_revenue
    FROM fact_sales f
    JOIN dim_product p ON f.product_key = p.product_key
    GROUP BY p.product_key, p.product_name, p.category
),
total_revenue AS (
    SELECT SUM(total_revenue) as company_revenue FROM product_sales
)
SELECT 
    ps.product_name,
    ps.category,
    ps.units_sold,
    ROUND(ps.total_revenue, 2) as revenue,
    ROUND((ps.total_revenue / tr.company_revenue) * 100, 2) as revenue_percentage
FROM product_sales ps
CROSS JOIN total_revenue tr
ORDER BY ps.total_revenue DESC
LIMIT 10;

-- ============================================================================
-- Query 3: Customer Segmentation Analysis (5 marks)
-- ============================================================================
-- Business Scenario: "Marketing wants to target high-value customers. 
-- Segment customers into 'High Value' (>₹50,000 spent), 'Medium Value' 
-- (₹20,000-₹50,000), and 'Low Value' (<₹20,000). Show count of customers 
-- and total revenue in each segment."

-- Requirements:
-- - Calculate total spending per customer
-- - Use CASE statement to create segments
-- - Group by segment
-- - Show: segment, customer_count, total_revenue, avg_revenue_per_customer

WITH customer_spending AS (
    SELECT 
        c.customer_key,
        c.customer_name,
        c.city,
        ROUND(SUM(f.total_amount), 2) as total_spent
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_key, c.customer_name, c.city
),
segmented_customers AS (
    SELECT 
        total_spent,
        CASE 
            WHEN total_spent > 50000 THEN 'High Value'
            WHEN total_spent >= 20000 AND total_spent <= 50000 THEN 'Medium Value'
            ELSE 'Low Value'
        END as customer_segment
    FROM customer_spending
)
SELECT 
    customer_segment,
    COUNT(*) as customer_count,
    ROUND(SUM(total_spent), 2) as total_revenue,
    ROUND(AVG(total_spent), 2) as avg_revenue_per_customer
FROM segmented_customers
GROUP BY customer_segment
ORDER BY 
    CASE 
        WHEN customer_segment = 'High Value' THEN 1
        WHEN customer_segment = 'Medium Value' THEN 2
        ELSE 3
    END;

-- ============================================================================
-- ADDITIONAL ANALYTICAL QUERIES
-- ============================================================================

-- Query: Sales by Day of Week (Weekend vs Weekday Analysis)
SELECT 
    CASE 
        WHEN d.is_weekend = TRUE THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    d.day_of_week,
    COUNT(f.sale_key) as transaction_count,
    SUM(f.quantity_sold) as total_units,
    ROUND(AVG(f.total_amount), 2) as avg_transaction_value,
    ROUND(SUM(f.total_amount), 2) as total_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY 
    d.is_weekend,
    d.day_of_week
ORDER BY 
    d.is_weekend DESC,
    FIELD(d.day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

-- Query: Top Categories by Revenue
SELECT 
    p.category,
    COUNT(DISTINCT f.sale_key) as transaction_count,
    COUNT(DISTINCT p.product_key) as product_count,
    SUM(f.quantity_sold) as units_sold,
    ROUND(SUM(f.total_amount), 2) as total_revenue,
    ROUND(AVG(f.total_amount), 2) as avg_transaction_value,
    ROUND(SUM(f.total_amount) / SUM(f.quantity_sold), 2) as avg_unit_price
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Query: Customer City Analysis
SELECT 
    c.city,
    COUNT(DISTINCT c.customer_key) as customer_count,
    COUNT(f.sale_key) as transaction_count,
    SUM(f.quantity_sold) as units_purchased,
    ROUND(SUM(f.total_amount), 2) as total_spent,
    ROUND(AVG(f.total_amount), 2) as avg_transaction_value
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.city
ORDER BY total_spent DESC;

-- Query: Monthly Growth Analysis
SELECT 
    d.month_name,
    d.month,
    COUNT(f.sale_key) as transactions,
    ROUND(SUM(f.total_amount), 2) as revenue,
    LAG(SUM(f.total_amount)) OVER (ORDER BY d.month) as prev_month_revenue,
    ROUND(
        ((SUM(f.total_amount) - LAG(SUM(f.total_amount)) OVER (ORDER BY d.month)) 
         / LAG(SUM(f.total_amount)) OVER (ORDER BY d.month)) * 100, 
        2
    ) as month_over_month_growth_percent
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY d.month, d.month_name
ORDER BY d.month;

-- Query: Product-Customer Matrix (Top 5 products for each city)
WITH ranked_products AS (
    SELECT 
        c.city,
        p.product_name,
        SUM(f.total_amount) as revenue,
        ROW_NUMBER() OVER (PARTITION BY c.city ORDER BY SUM(f.total_amount) DESC) as rank
    FROM fact_sales f
    JOIN dim_product p ON f.product_key = p.product_key
    JOIN dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.city, p.product_name
)
SELECT 
    city,
    product_name,
    revenue
FROM ranked_products
WHERE rank <= 5
ORDER BY city, rank;

-- Query: Discount Impact Analysis
SELECT 
    CASE 
        WHEN discount_amount = 0 THEN 'No Discount'
        WHEN discount_amount > 0 AND discount_amount < 1000 THEN 'Small Discount (< ₹1000)'
        WHEN discount_amount >= 1000 AND discount_amount < 5000 THEN 'Medium Discount (₹1000-₹5000)'
        ELSE 'Large Discount (> ₹5000)'
    END as discount_range,
    COUNT(f.sale_key) as transaction_count,
    ROUND(SUM(discount_amount), 2) as total_discount_amount,
    ROUND(AVG(discount_amount), 2) as avg_discount,
    ROUND(SUM(total_amount), 2) as revenue_after_discount
FROM fact_sales f
GROUP BY discount_range
ORDER BY avg_discount DESC;

-- Query: Quarter-over-Quarter Performance
SELECT 
    d.quarter,
    COUNT(f.sale_key) as transactions,
    SUM(f.quantity_sold) as units_sold,
    ROUND(SUM(f.total_amount), 2) as quarter_revenue,
    ROUND(SUM(f.total_amount) / COUNT(f.sale_key), 2) as avg_transaction_value
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY d.quarter
ORDER BY d.quarter;

-- ============================================================================
-- Performance Optimization Notes
-- ============================================================================
/*
These queries are optimized for:
1. Join on fact table with dimensions
2. Use of window functions for running totals and rankings
3. CTEs for complex logic segmentation
4. Indexed columns (date_key, product_key, customer_key)

For even better performance in production:
- Create materialized views for frequently used aggregations
- Add columnstore indexes for large-scale data
- Implement query caching for dashboard queries
- Use partitioning on fact_sales table by date_key
*/
