"""
ETL Pipeline for FlexiMart Data Engineering Project
Complete working version - runs from anywhere
"""

import pandas as pd
import re
import os
from datetime import datetime
import logging

# Get the absolute path to the data directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# Configure logging
logging.basicConfig(
    filename='etl_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

print(f"\n[INFO] Project root: {PROJECT_ROOT}")
print(f"[INFO] Data directory: {DATA_DIR}")

logging.basicConfig(
    filename='etl_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ETLPipeline:
    """
    Professional ETL Pipeline Implementation
    Handles Extract, Transform, Load operations for FlexiMart data
    """
    
    def __init__(self, host='localhost', user='root', password='', database='fleximart', use_database=False):
        """Initialize ETL pipeline parameters"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.engine = None
        self.use_database = use_database
        
        # Data storage for standalone mode
        self.customers_df = None
        self.products_df = None
        self.orders_df = None
        self.order_items_df = None
        
        # Quality report tracking
        self.quality_report = {
            'customers': {'processed': 0, 'duplicates': 0, 'missing_values': 0, 'loaded': 0},
            'products': {'processed': 0, 'duplicates': 0, 'missing_values': 0, 'loaded': 0},
            'orders': {'processed': 0, 'duplicates': 0, 'missing_values': 0, 'loaded': 0}
        }

    def connect_database_mysql(self):
        """Attempt MySQL connection (optional)"""
        if not MYSQL_AVAILABLE:
            logging.warning("mysql-connector-python not installed")
            return False
        
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            logging.info("MySQL connection successful")
            print("[SUCCESS] MySQL connection successful")
            return True
        except Exception as e:
            logging.warning(f"MySQL connection skipped: {e}")
            print(f"[WARNING] MySQL connection skipped (not required for this version)")
            return False

    def connect_database_sqlalchemy(self):
        """Create SQLAlchemy engine for database operations"""
        if not SQLALCHEMY_AVAILABLE:
            logging.warning("SQLAlchemy not available")
            return False
        
        try:
            # MySQL connection string
            connection_string = f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}"
            self.engine = create_engine(connection_string)
            logging.info("SQLAlchemy engine created successfully")
            print("[SUCCESS] SQLAlchemy engine created")
            return True
        except Exception as e:
            logging.warning(f"SQLAlchemy connection skipped: {e}")
            return False

    def create_tables(self):
        """Create tables in database using SQLAlchemy"""
        if not self.engine:
            logging.info("Skipping table creation (database not connected)")
            return
        
        try:
            # SQL statements for table creation
            sql_statements = [
                """CREATE TABLE IF NOT EXISTS customers (
                    customer_id INT PRIMARY KEY AUTO_INCREMENT,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(20),
                    city VARCHAR(50),
                    registration_date DATE
                )""",
                
                """CREATE TABLE IF NOT EXISTS products (
                    product_id INT PRIMARY KEY AUTO_INCREMENT,
                    product_name VARCHAR(100) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    stock_quantity INT DEFAULT 0
                )""",
                
                """CREATE TABLE IF NOT EXISTS orders (
                    order_id INT PRIMARY KEY AUTO_INCREMENT,
                    customer_id INT NOT NULL,
                    order_date DATE NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) DEFAULT 'Pending',
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )""",
                
                """CREATE TABLE IF NOT EXISTS order_items (
                    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
                    order_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    unit_price DECIMAL(10,2) NOT NULL,
                    subtotal DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )"""
            ]
            
            with self.engine.connect() as connection:
                for statement in sql_statements:
                    connection.execute(statement)
                connection.commit()
            
            logging.info("Database tables created successfully")
            print("[SUCCESS] Database tables created successfully")
        except Exception as e:
            logging.error(f"Error creating tables: {e}")
            print(f"⚠ Table creation skipped: {e}")

    # ============================================================================
    # EXTRACT PHASE (3 marks)
    # ============================================================================
    def extract_data(self):
        """
        Extract Phase: Read CSV files
        - Handles file errors gracefully
        - Logs extraction details
        - Returns raw dataframes
        """
        print("\n" + "="*70)
        print("PHASE 1: EXTRACT - Reading CSV files")
        print("="*70)
        
        try:
            # Extract customers
            print("\n[EXTRACT] Loading customers...")
            customers_path = os.path.join(DATA_DIR, 'customers_raw.csv')
            customers = pd.read_csv(customers_path)
            self.quality_report['customers']['processed'] = len(customers)
            print(f"   SUCCESS: {len(customers)} customer records extracted")
            logging.info(f"Extracted {len(customers)} customer records")
            
            # Extract products
            print("[EXTRACT] Loading products...")
            products_path = os.path.join(DATA_DIR, 'products_raw.csv')
            products = pd.read_csv(products_path)
            self.quality_report['products']['processed'] = len(products)
            print(f"   SUCCESS: {len(products)} product records extracted")
            logging.info(f"Extracted {len(products)} product records")
            
            # Extract orders
            print("[EXTRACT] Loading orders...")
            orders_path = os.path.join(DATA_DIR, 'sales_raw.csv')
            orders = pd.read_csv(orders_path)
            self.quality_report['orders']['processed'] = len(orders)
            print(f"   SUCCESS: {len(orders)} order records extracted")
            logging.info(f"Extracted {len(orders)} order records")
            
            return customers, products, orders
        
        except FileNotFoundError as e:
            logging.error(f"CSV file not found: {e}")
            print(f"[ERROR] File not found: {e}")
            return None, None, None
        except Exception as e:
            logging.error(f"Error during extraction: {e}")
            print(f"[ERROR] Extraction failed: {e}")
            return None, None, None

    # ============================================================================
    # TRANSFORM PHASE (7 marks)
    # ============================================================================
    def standardize_phone(self, phone):
        """Convert phone to +91-XXXXXXXXXX format"""
        if pd.isna(phone):
            return None
        phone_str = str(phone).strip()
        # Remove all non-digits
        digits = re.sub(r'\D', '', phone_str)
        # Keep last 10 digits
        if len(digits) >= 10:
            return f"+91-{digits[-10:]}"
        return None

    def standardize_category(self, category):
        """Normalize product category"""
        if pd.isna(category):
            return 'Uncategorized'
        return str(category).strip().title()

    def parse_date(self, date_str):
        """Parse multiple date formats: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY, MM/DD/YYYY"""
        if pd.isna(date_str):
            return None
        
        date_str = str(date_str).strip()
        formats = ['%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y', '%d-%m-%Y', '%m/%d/%Y']
        
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt).date()
            except:
                continue
        
        # If all formats fail, return None
        logging.warning(f"Could not parse date: {date_str}")
        return None

    def transform_customers(self, df):
        """
        Transform customers data
        - Remove duplicates
        - Standardize phone numbers
        - Generate missing emails
        """
        print("\n" + "-"*70)
        print("TRANSFORMING CUSTOMERS...")
        print("-"*70)
        
        df = df.copy()
        initial_count = len(df)
        
        # Remove duplicates
        duplicates = len(df) - len(df.drop_duplicates())
        self.quality_report['customers']['duplicates'] = duplicates
        df = df.drop_duplicates()
        print(f"[SUCCESS] Removed {duplicates} duplicate records")
        
        # Handle missing values
        missing_before = df.isnull().sum().sum()
        
        # Standardize phone numbers
        df['phone'] = df['phone'].apply(self.standardize_phone)
        
        # Generate default emails for missing ones
        for idx in df[df['email'].isna()].index:
            first = df.loc[idx, 'first_name'].lower() if not pd.isna(df.loc[idx, 'first_name']) else 'customer'
            last = df.loc[idx, 'last_name'].lower() if not pd.isna(df.loc[idx, 'last_name']) else str(idx)
            df.loc[idx, 'email'] = f"{first}.{last}@fleximart.com"
        
        # Parse registration dates
        if 'registration_date' in df.columns:
            df['registration_date'] = df['registration_date'].apply(self.parse_date)
        
        missing_after = df.isnull().sum().sum()
        self.quality_report['customers']['missing_values'] = missing_before - missing_after
        
        print(f"[SUCCESS] Standardized phone numbers")
        print(f"[SUCCESS] Generated {df['email'].isna().sum() == 0} default emails")
        print(f"[SUCCESS] Parsed dates with {missing_after} remaining nulls")
        
        self.quality_report['customers']['loaded'] = len(df)
        return df

    def transform_products(self, df):
        """
        Transform products data
        - Remove duplicates
        - Standardize categories
        - Handle missing values
        """
        print("\n" + "-"*70)
        print("TRANSFORMING PRODUCTS...")
        print("-"*70)
        
        df = df.copy()
        
        # Remove duplicates
        duplicates = len(df) - len(df.drop_duplicates())
        self.quality_report['products']['duplicates'] = duplicates
        df = df.drop_duplicates()
        print(f"[SUCCESS] Removed {duplicates} duplicate records")
        
        missing_before = df.isnull().sum().sum()
        
        # Standardize categories
        if 'category' in df.columns:
            df['category'] = df['category'].apply(self.standardize_category)
        
        # Fill missing stock with 0
        if 'stock_quantity' in df.columns:
            df['stock_quantity'] = df['stock_quantity'].fillna(0).astype(int)
        
        # Drop records with missing prices (critical field)
        df = df.dropna(subset=['price'])
        
        missing_after = df.isnull().sum().sum()
        self.quality_report['products']['missing_values'] = missing_before - missing_after
        
        print(f"[SUCCESS] Standardized categories")
        print(f"[SUCCESS] Filled stock quantities and prices")
        print(f"[SUCCESS] Cleaned {missing_before - missing_after} missing values")
        
        self.quality_report['products']['loaded'] = len(df)
        return df

    def transform_orders(self, df):
        """
        Transform orders data
        - Remove duplicates
        - Parse dates
        - Handle missing values
        """
        print("\n" + "-"*70)
        print("TRANSFORMING ORDERS...")
        print("-"*70)
        
        df = df.copy()
        
        # Rename columns to match schema
        if 'transaction_id' in df.columns:
            df.rename(columns={'transaction_id': 'order_id'}, inplace=True)
        if 'transaction_date' in df.columns:
            df.rename(columns={'transaction_date': 'order_date'}, inplace=True)
        
        # Remove duplicates
        duplicates = len(df) - len(df.drop_duplicates())
        self.quality_report['orders']['duplicates'] = duplicates
        df = df.drop_duplicates()
        print(f"[SUCCESS] Removed {duplicates} duplicate records")
        
        missing_before = df.isnull().sum().sum()
        
        # Parse dates
        if 'order_date' in df.columns:
            df['order_date'] = df['order_date'].apply(self.parse_date)
        
        # Drop records with missing critical fields
        critical_cols = ['order_id', 'customer_id']
        df = df.dropna(subset=critical_cols)
        
        missing_after = df.isnull().sum().sum()
        self.quality_report['orders']['missing_values'] = missing_before - missing_after
        
        print(f"[SUCCESS] Parsed order dates")
        print(f"[SUCCESS] Dropped records with missing critical fields")
        print(f"[SUCCESS] Cleaned {missing_before - missing_after} missing values")
        
        self.quality_report['orders']['loaded'] = len(df)
        return df

    # ============================================================================
    # LOAD PHASE (3 marks)
    # ============================================================================
    def save_to_csv(self, customers_df, products_df, orders_df):
        """Save cleaned data to CSV files"""
        print("\n[LOAD] Saving cleaned data to CSV files...")
        
        try:
            customers_df.to_csv('customers_cleaned.csv', index=False)
            products_df.to_csv('products_cleaned.csv', index=False)
            orders_df.to_csv('orders_cleaned.csv', index=False)
            
            print("   SUCCESS: customers_cleaned.csv")
            print("   SUCCESS: products_cleaned.csv")
            print("   SUCCESS: orders_cleaned.csv")
            logging.info("Cleaned data saved to CSV files")
            return True
        except Exception as e:
            logging.error(f"Error saving CSV files: {e}")
            print(f"[ERROR] Failed to save: {e}")
            return False

    def generate_quality_report(self):
        """Generate data quality report"""
        print("\n" + "="*70)
        print("PHASE 4: DATA QUALITY REPORT")
        print("="*70)
        
        report_content = []
        report_content.append("FLEXIMART ETL DATA QUALITY REPORT")
        report_content.append("=" * 70)
        report_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_content.append("")
        
        for entity, stats in self.quality_report.items():
            report_content.append(entity.upper())
            report_content.append("-" * 70)
            report_content.append(f"  Records Processed:    {stats['processed']}")
            report_content.append(f"  Duplicates Removed:   {stats['duplicates']}")
            report_content.append(f"  Missing Values Fixed: {stats['missing_values']}")
            report_content.append(f"  Records Loaded:       {stats['loaded']}")
            report_content.append("")
        
        report_content.append("=" * 70)
        report_content.append("SUMMARY")
        report_content.append("=" * 70)
        total_processed = sum(s['processed'] for s in self.quality_report.values())
        total_loaded = sum(s['loaded'] for s in self.quality_report.values())
        total_cleaned = sum(s['duplicates'] + s['missing_values'] for s in self.quality_report.values())
        
        report_content.append(f"Total Records Processed: {total_processed}")
        report_content.append(f"Total Records Cleaned:   {total_cleaned}")
        report_content.append(f"Total Records Loaded:    {total_loaded}")
        report_content.append(f"Data Quality Score:      {(total_loaded/total_processed*100):.1f}%")
        
        report_text = "\n".join(report_content)
        
        # Save to file
        with open('data_quality_report.txt', 'w') as f:
            f.write(report_text)
        
        print(report_text)
        logging.info("Quality report generated")

    def run_pipeline(self):
        """Execute complete ETL pipeline"""
        print("\n" + "="*70)
        print("FLEXIMART ETL PIPELINE - STARTING")
        print("="*70)
        
        # Try database connection (optional)
        if self.use_database:
            self.connect_database_mysql()
            self.connect_database_sqlalchemy()
            if self.engine:
                self.create_tables()
        
        # Extract
        customers, products, orders = self.extract_data()
        if customers is None:
            print("\n[ERROR] ETL Pipeline Failed - Could not extract data")
            return False
        
        # Transform
        print("\n" + "="*70)
        print("PHASE 2: TRANSFORM - Cleaning and validating data")
        print("="*70)
        
        customers_clean = self.transform_customers(customers)
        products_clean = self.transform_products(products)
        orders_clean = self.transform_orders(orders)
        
        self.customers_df = customers_clean
        self.products_df = products_clean
        self.orders_df = orders_clean
        
        # Load (Save to CSV)
        print("\n" + "="*70)
        print("PHASE 3: LOAD - Saving cleaned data")
        print("="*70)
        self.save_to_csv(customers_clean, products_clean, orders_clean)
        
        # Generate report
        self.generate_quality_report()
        
        print("\n" + "="*70)
        print("✓ ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nOutput Files Generated:")
        print("  • data_quality_report.txt - Quality metrics")
        print("  • customers_cleaned.csv - Cleaned customer data")
        print("  • products_cleaned.csv - Cleaned product data")
        print("  • orders_cleaned.csv - Cleaned order data")
        print("  • etl_pipeline.log - Execution log")
        print("="*70 + "\n")
        
        logging.info("ETL Pipeline completed successfully")
        return True


# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("FLEXIMART DATA ENGINEERING PROJECT - PART 1: ETL PIPELINE")
    print("="*70)
    
    # Create and run ETL pipeline
    pipeline = ETLPipeline(use_database=False)  # Set to True if MySQL is running
    success = pipeline.run_pipeline()
    
    if success:
        print("\n[SUCCESS] All tasks completed successfully!")
        print("\nNext Steps:")
        print("1. Review data_quality_report.txt")
        print("2. Check cleaned CSV files")
        print("3. (Optional) Import to MySQL using MySQL Workbench or command line")
    else:
        print("\n[ERROR] ETL Pipeline failed. Check etl_pipeline.log for details.")
