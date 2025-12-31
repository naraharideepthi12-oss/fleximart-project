-- ============================================================================
-- DATA WAREHOUSE SCHEMA - FLEXIMART
-- ============================================================================
-- Database: fleximart_dw
-- Purpose: OLAP data warehouse for analytical reporting
-- Type: Star Schema with 1 Fact Table and 3 Dimension Tables

-- ============================================================================
-- Create Database
-- ============================================================================
CREATE DATABASE IF NOT EXISTS fleximart_dw;
USE fleximart_dw;

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

-- Dimension 1: Date Dimension
-- Covers dates from 2024-01-01 to 2024-12-31
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week VARCHAR(10),
    day_of_month INT,
    month INT,
    month_name VARCHAR(10),
    quarter VARCHAR(2),
    year INT,
    is_weekend BOOLEAN,
    UNIQUE KEY uk_full_date (full_date)
);

-- Dimension 2: Product Dimension
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY AUTO_INCREMENT,
    product_id VARCHAR(20),
    product_name VARCHAR(100),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    unit_price DECIMAL(10,2),
    UNIQUE KEY uk_product_id (product_id)
);

-- Dimension 3: Customer Dimension
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    customer_id VARCHAR(20),
    customer_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    customer_segment VARCHAR(20),
    UNIQUE KEY uk_customer_id (customer_id)
);

-- ============================================================================
-- FACT TABLE
-- ============================================================================

-- Fact Table: Sales
CREATE TABLE fact_sales (
    sale_key INT PRIMARY KEY AUTO_INCREMENT,
    date_key INT NOT NULL,
    product_key INT NOT NULL,
    customer_key INT NOT NULL,
    quantity_sold INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    INDEX idx_date_key (date_key),
    INDEX idx_product_key (product_key),
    INDEX idx_customer_key (customer_key)
);

-- ============================================================================
-- Create Indexes for Performance
-- ============================================================================

-- Composite indexes for common query patterns
CREATE INDEX idx_fs_date_product ON fact_sales(date_key, product_key);
CREATE INDEX idx_fs_date_customer ON fact_sales(date_key, customer_key);
CREATE INDEX idx_fs_product_category ON dim_product(category);
CREATE INDEX idx_fs_customer_city ON dim_customer(city);

-- ============================================================================
-- End of Schema Definition
-- ============================================================================
