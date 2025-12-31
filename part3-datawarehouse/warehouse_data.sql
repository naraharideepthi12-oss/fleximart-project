-- ============================================================================
-- DATA WAREHOUSE DATA INSERTION - FLEXIMART
-- ============================================================================
-- Inserts sample data into star schema (dimension and fact tables)
-- Database: fleximart_dw

USE fleximart_dw;

-- ============================================================================
-- DIM_DATE Table Data (30 dates: January-February 2024)
-- ============================================================================

INSERT INTO dim_date VALUES
-- January 2024
(20240101, '2024-01-01', 'Monday', 1, 1, 'January', 'Q1', 2024, FALSE),
(20240102, '2024-01-02', 'Tuesday', 2, 1, 'January', 'Q1', 2024, FALSE),
(20240103, '2024-01-03', 'Wednesday', 3, 1, 'January', 'Q1', 2024, FALSE),
(20240104, '2024-01-04', 'Thursday', 4, 1, 'January', 'Q1', 2024, FALSE),
(20240105, '2024-01-05', 'Friday', 5, 1, 'January', 'Q1', 2024, FALSE),
(20240106, '2024-01-06', 'Saturday', 6, 1, 'January', 'Q1', 2024, TRUE),
(20240107, '2024-01-07', 'Sunday', 7, 1, 'January', 'Q1', 2024, TRUE),
(20240115, '2024-01-15', 'Monday', 15, 1, 'January', 'Q1', 2024, FALSE),
(20240116, '2024-01-16', 'Tuesday', 16, 1, 'January', 'Q1', 2024, FALSE),
(20240118, '2024-01-18', 'Thursday', 18, 1, 'January', 'Q1', 2024, FALSE),
(20240120, '2024-01-20', 'Saturday', 20, 1, 'January', 'Q1', 2024, TRUE),
(20240121, '2024-01-21', 'Sunday', 21, 1, 'January', 'Q1', 2024, TRUE),
(20240125, '2024-01-25', 'Thursday', 25, 1, 'January', 'Q1', 2024, FALSE),
(20240128, '2024-01-28', 'Sunday', 28, 1, 'January', 'Q1', 2024, TRUE),
-- February 2024
(20240201, '2024-02-01', 'Thursday', 1, 2, 'February', 'Q1', 2024, FALSE),
(20240205, '2024-02-05', 'Monday', 5, 2, 'February', 'Q1', 2024, FALSE),
(20240210, '2024-02-10', 'Saturday', 10, 2, 'February', 'Q1', 2024, TRUE),
(20240212, '2024-02-12', 'Monday', 12, 2, 'February', 'Q1', 2024, FALSE),
(20240215, '2024-02-15', 'Thursday', 15, 2, 'February', 'Q1', 2024, FALSE),
(20240218, '2024-02-18', 'Sunday', 18, 2, 'February', 'Q1', 2024, TRUE),
(20240220, '2024-02-20', 'Tuesday', 20, 2, 'February', 'Q1', 2024, FALSE),
(20240225, '2024-02-25', 'Sunday', 25, 2, 'February', 'Q1', 2024, TRUE),
(20240228, '2024-02-28', 'Wednesday', 28, 2, 'February', 'Q1', 2024, FALSE),
-- March 2024
(20240301, '2024-03-01', 'Friday', 1, 3, 'March', 'Q1', 2024, FALSE),
(20240305, '2024-03-05', 'Tuesday', 5, 3, 'March', 'Q1', 2024, FALSE),
(20240310, '2024-03-10', 'Sunday', 10, 3, 'March', 'Q1', 2024, TRUE),
(20240315, '2024-03-15', 'Friday', 15, 3, 'March', 'Q1', 2024, FALSE),
(20240320, '2024-03-20', 'Wednesday', 20, 3, 'March', 'Q1', 2024, FALSE),
(20240325, '2024-03-25', 'Monday', 25, 3, 'March', 'Q1', 2024, FALSE),
(20240330, '2024-03-30', 'Saturday', 30, 3, 'March', 'Q1', 2024, TRUE);

-- ============================================================================
-- DIM_PRODUCT Table Data (15 products across 3 categories)
-- ============================================================================

INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
-- Electronics (6 products)
('P001', 'Samsung Galaxy S21', 'Electronics', 'Smartphones', 45999.00),
('P003', 'Apple MacBook Pro', 'Electronics', 'Laptops', 189999.00),
('P005', 'Sony Headphones', 'Electronics', 'Audio', 29990.00),
('P007', 'HP Laptop', 'Electronics', 'Laptops', 52999.00),
('P012', 'Dell Monitor 24inch', 'Electronics', 'Monitors', 12999.00),
('P014', 'iPhone 13', 'Electronics', 'Smartphones', 69999.00),

-- Fashion (6 products)
('P002', 'Nike Running Shoes', 'Fashion', 'Footwear', 12995.00),
('P004', 'Levi\'s Jeans', 'Fashion', 'Clothing', 3499.00),
('P008', 'Adidas T-Shirt', 'Fashion', 'Clothing', 1499.00),
('P011', 'Puma Sneakers', 'Fashion', 'Footwear', 4599.00),
('P013', 'Woodland Shoes', 'Fashion', 'Footwear', 5499.00),
('P020', 'Reebok Trackpants', 'Fashion', 'Clothing', 1899.00),

-- Groceries (3 products)
('P006', 'Organic Almonds', 'Groceries', 'Dry Goods', 899.00),
('P009', 'Basmati Rice 5kg', 'Groceries', 'Grains', 650.00),
('P015', 'Organic Honey 500g', 'Groceries', 'Condiments', 450.00);

-- ============================================================================
-- DIM_CUSTOMER Table Data (12 customers across 4 cities)
-- ============================================================================

INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
-- Bangalore
('C001', 'Rahul Sharma', 'Bangalore', 'Karnataka', 'Premium'),
('C006', 'Anjali Mehta', 'Bangalore', 'Karnataka', 'Regular'),
('C016', 'Divya Menon', 'Bangalore', 'Karnataka', 'Regular'),

-- Mumbai
('C002', 'Priya Patel', 'Mumbai', 'Maharashtra', 'Premium'),
('C013', 'Suresh Patel', 'Mumbai', 'Maharashtra', 'Regular'),
('C014', 'Neha Shah', 'Mumbai', 'Maharashtra', 'Premium'),

-- Delhi
('C003', 'Amit Kumar', 'Delhi', 'Delhi', 'Regular'),
('C010', 'Deepa Gupta', 'Delhi', 'Delhi', 'Occasional'),
('C017', 'Rajesh Kumar', 'Delhi', 'Delhi', 'Premium'),

-- Hyderabad
('C004', 'Sneha Reddy', 'Hyderabad', 'Telangana', 'Regular'),
('C011', 'Arjun Rao', 'Hyderabad', 'Telangana', 'Premium'),
('C018', 'Kavya Reddy', 'Hyderabad', 'Telangana', 'Occasional');

-- ============================================================================
-- FACT_SALES Table Data (40 sales transactions)
-- ============================================================================

-- January Sales (higher variety, mix of weekend and weekday)
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
(20240101, 1, 1, 1, 45999.00, 0, 45999.00),
(20240102, 2, 2, 2, 12995.00, 1299.00, 24691.00),
(20240103, 3, 3, 1, 29990.00, 0, 29990.00),
(20240104, 4, 4, 1, 3499.00, 349.90, 3149.10),
(20240105, 5, 5, 3, 1499.00, 0, 4497.00),
(20240106, 6, 6, 1, 899.00, 0, 899.00),
(20240107, 7, 7, 2, 650.00, 0, 1300.00),
(20240115, 8, 8, 1, 52999.00, 0, 52999.00),
(20240116, 9, 9, 1, 12999.00, 1299.90, 11699.10),
(20240118, 10, 10, 2, 69999.00, 0, 139998.00),
(20240120, 11, 11, 1, 4599.00, 459.90, 4139.10),
(20240121, 12, 12, 3, 450.00, 0, 1350.00),
(20240125, 13, 1, 1, 5499.00, 549.90, 4949.10),
(20240128, 14, 2, 1, 1899.00, 0, 1899.00),

-- February Sales (mix of products, weekend promotions)
(20240201, 1, 3, 1, 45999.00, 2299.95, 43699.05),
(20240205, 2, 4, 2, 12995.00, 0, 25990.00),
(20240210, 3, 5, 1, 29990.00, 0, 29990.00),
(20240212, 4, 6, 3, 3499.00, 0, 10497.00),
(20240215, 5, 7, 2, 1499.00, 299.80, 2198.20),
(20240218, 6, 8, 5, 899.00, 0, 4495.00),
(20240220, 7, 9, 3, 650.00, 195.00, 1755.00),
(20240225, 8, 10, 1, 52999.00, 5299.90, 47699.10),
(20240228, 9, 11, 1, 12999.00, 1299.90, 11699.10),

-- March Sales (spring season, higher electronics sales)
(20240301, 1, 12, 1, 45999.00, 0, 45999.00),
(20240305, 10, 1, 1, 69999.00, 3499.95, 66499.05),
(20240310, 11, 2, 2, 4599.00, 0, 9198.00),
(20240315, 2, 3, 1, 12995.00, 0, 12995.00),
(20240320, 3, 4, 2, 29990.00, 5998.00, 53982.00),
(20240325, 4, 5, 3, 3499.00, 0, 10497.00),
(20240330, 5, 6, 2, 1499.00, 0, 2998.00),

-- Additional Sales for full 40 records
(20240101, 8, 2, 1, 52999.00, 0, 52999.00),
(20240106, 9, 3, 1, 12999.00, 1299.90, 11699.10),
(20240120, 12, 4, 8, 450.00, 0, 3600.00),
(20240201, 2, 5, 2, 12995.00, 1299.50, 24690.50),
(20240210, 13, 6, 1, 5499.00, 0, 5499.00),
(20240218, 14, 7, 1, 1899.00, 189.90, 1709.10),
(20240228, 10, 8, 1, 69999.00, 0, 69999.00),
(20240305, 6, 9, 4, 899.00, 0, 3596.00),
(20240315, 7, 10, 2, 650.00, 0, 1300.00),
(20240325, 11, 11, 1, 4599.00, 459.90, 4139.10),
(20240330, 1, 12, 1, 45999.00, 0, 45999.00);

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Check record counts
SELECT 'dim_date' as table_name, COUNT(*) as record_count FROM dim_date
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_customer', COUNT(*) FROM dim_customer
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM fact_sales;

-- Check total sales revenue
SELECT ROUND(SUM(total_amount), 2) as total_revenue FROM fact_sales;

-- Check sales by category
SELECT 
    p.category,
    COUNT(f.sale_key) as transaction_count,
    ROUND(SUM(f.total_amount), 2) as category_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY category_revenue DESC;

-- ============================================================================
-- End of Data Insertion
-- ============================================================================
