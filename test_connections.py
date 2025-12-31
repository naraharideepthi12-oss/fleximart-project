"""
MySQL Connector & Database Test Script
Tests connection to MySQL and MongoDB with detailed output
Run this to verify all connections are working
"""

import sys
import os

print("=" * 60)
print("FlexiMart Database Connection Tester")
print("=" * 60)

# ============================================================================
# PART 1: MySQL Connection Test
# ============================================================================
print("\n📊 TESTING MYSQL CONNECTION...\n")

try:
    import mysql.connector
    from mysql.connector import Error
    print("✓ mysql-connector-python library found")
    
    # MySQL Configuration - UPDATE THESE VALUES
    mysql_config = {
        'host': 'localhost',      # Your MySQL host
        'user': 'root',           # Your MySQL username
        'password': 'mysql123',   # Your MySQL password (change if different)
        'database': 'fleximart'   # Your database name
    }
    
    print(f"\nAttempting to connect to MySQL:")
    print(f"  Host: {mysql_config['host']}")
    print(f"  User: {mysql_config['user']}")
    print(f"  Database: {mysql_config['database']}")
    
    # Establish connection
    mysql_connection = mysql.connector.connect(**mysql_config)
    mysql_cursor = mysql_connection.cursor()
    
    print("\n✓ MYSQL CONNECTION SUCCESSFUL!\n")
    
    # Test query
    print("Testing with sample queries:")
    
    # Check tables exist
    mysql_cursor.execute("SHOW TABLES;")
    tables = mysql_cursor.fetchall()
    
    if tables:
        print(f"\n  Found {len(tables)} tables:")
        for table in tables:
            print(f"    - {table[0]}")
    else:
        print("  ⚠ No tables found. Run ETL pipeline first.")
    
    # Count records
    try:
        mysql_cursor.execute("SELECT COUNT(*) FROM customers;")
        count = mysql_cursor.fetchone()[0]
        print(f"\n  Customers table: {count} records")
    except:
        print(f"  ⚠ Customers table not found")
    
    mysql_cursor.close()
    mysql_connection.close()
    mysql_status = "✓ SUCCESS"
    
except ImportError:
    print("✗ mysql-connector-python not installed")
    print("  Install with: pip install mysql-connector-python")
    mysql_status = "✗ FAILED"
except Error as e:
    print(f"✗ MySQL Connection Error: {e}")
    print("\nTroubleshooting:")
    print("  1. Is MySQL Server running?")
    print("  2. Check host, user, password in config")
    print("  3. Does database 'fleximart' exist?")
    mysql_status = "✗ FAILED"
except Exception as e:
    print(f"✗ Unexpected Error: {e}")
    mysql_status = "✗ FAILED"

# ============================================================================
# PART 2: MongoDB Connection Test
# ============================================================================
print("\n" + "=" * 60)
print("📊 TESTING MONGODB CONNECTION...\n")

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutException
    print("✓ pymongo library found")
    
    # MongoDB Configuration
    mongo_config = {
        'url': 'mongodb://localhost:27017/',
        'database': 'fleximart_nosql',
        'timeout': 5000
    }
    
    print(f"\nAttempting to connect to MongoDB:")
    print(f"  URL: {mongo_config['url']}")
    print(f"  Database: {mongo_config['database']}")
    
    # Establish connection
    client = MongoClient(mongo_config['url'], serverSelectionTimeoutMS=mongo_config['timeout'])
    
    # Test connection
    client.server_info()
    
    print("\n✓ MONGODB CONNECTION SUCCESSFUL!\n")
    
    # Get database and collections
    db = client[mongo_config['database']]
    
    # Check collections
    collections = db.list_collection_names()
    
    if collections:
        print(f"Found {len(collections)} collections:")
        for collection in collections:
            count = db[collection].count_documents({})
            print(f"  - {collection}: {count} documents")
    else:
        print("⚠ No collections found. Run MongoDB import first.")
    
    client.close()
    mongo_status = "✓ SUCCESS"
    
except ImportError:
    print("✗ pymongo not installed")
    print("  Install with: pip install pymongo")
    mongo_status = "✗ FAILED"
except (ConnectionFailure, ServerSelectionTimeoutException) as e:
    print(f"✗ MongoDB Connection Error: {e}")
    print("\nTroubleshooting:")
    print("  1. Is MongoDB Server running?")
    print("  2. Run: Get-Service MongoDB (Windows)")
    print("  3. Check if port 27017 is accessible")
    mongo_status = "✗ FAILED"
except Exception as e:
    print(f"✗ Unexpected Error: {e}")
    mongo_status = "✗ FAILED"

# ============================================================================
# PART 3: Python Libraries Check
# ============================================================================
print("\n" + "=" * 60)
print("📦 CHECKING PYTHON LIBRARIES...\n")

required_libraries = {
    'pandas': 'Data manipulation',
    'mysql.connector': 'MySQL connection',
    'pymongo': 'MongoDB connection',
    'dotenv': 'Environment variables'
}

library_status = {}
for lib, purpose in required_libraries.items():
    try:
        __import__(lib)
        print(f"✓ {lib:25} - {purpose}")
        library_status[lib] = True
    except ImportError:
        print(f"✗ {lib:25} - {purpose}")
        library_status[lib] = False

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("📋 FINAL SUMMARY\n")

print(f"MySQL Connection:    {mysql_status}")
print(f"MongoDB Connection:  {mongo_status}")

missing_libs = [lib for lib, installed in library_status.items() if not installed]
if missing_libs:
    print(f"Missing Libraries:   {', '.join(missing_libs)}")
    print(f"\nInstall missing libraries with:")
    print(f"  pip install {' '.join(missing_libs)}")
else:
    print("All Libraries:       ✓ INSTALLED")

print("\n" + "=" * 60)

# Recommendation
if mysql_status == "✓ SUCCESS" and mongo_status == "✓ SUCCESS" and len(missing_libs) == 0:
    print("✓ ALL SYSTEMS READY FOR EXECUTION!")
    print("\nNext steps:")
    print("  1. Run ETL Pipeline: python part1-database-etl/etl_pipeline.py")
    print("  2. Execute Business Queries in MySQL Workbench")
    print("  3. Load MongoDB data: mongosh < part2-nosql/mongodb_operations.js")
    print("  4. Create Data Warehouse: mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql")
else:
    print("⚠ SOME SYSTEMS NOT READY")
    print("\nPlease fix the issues above before proceeding.")
    print("\nRefer to SETUP_GUIDE.md for detailed troubleshooting.")

print("=" * 60)
