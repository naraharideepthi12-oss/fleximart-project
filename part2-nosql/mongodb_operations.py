"""
MongoDB Operations for FlexiMart Project
Part 2: NoSQL Database Implementation
Python version of mongodb_operations.js
"""

import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutException
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    filename='mongodb_operations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MongoDBOperations:
    def __init__(self, mongo_url='mongodb://localhost:27017/', database='fleximart_nosql'):
        """Initialize MongoDB connection"""
        self.mongo_url = mongo_url
        self.database_name = database
        self.client = None
        self.db = None
        self.products = None
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.mongo_url, serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Test connection
            self.db = self.client[self.database_name]
            self.products = self.db['products']
            logging.info("MongoDB connection successful")
            print("✓ MongoDB connection successful")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutException) as e:
            logging.error(f"MongoDB connection failed: {e}")
            print(f"✗ MongoDB connection failed: {e}")
            return False
    
    def load_data(self, json_file_path):
        """
        OPERATION 1: Load data from JSON file into MongoDB
        """
        print("\n" + "="*60)
        print("OPERATION 1: Load Data from JSON")
        print("="*60)
        
        try:
            # Drop existing collection
            self.products.drop()
            print("✓ Cleared existing products collection")
            
            # Read JSON file
            with open(json_file_path, 'r', encoding='utf-8') as file:
                products_data = json.load(file)
            
            print(f"✓ Loaded {len(products_data)} products from {json_file_path}")
            
            # Insert into MongoDB
            result = self.products.insert_many(products_data)
            
            print(f"✓ Inserted {len(result.inserted_ids)} documents into 'products' collection")
            logging.info(f"Loaded {len(result.inserted_ids)} products from JSON")
            
            return True
        
        except FileNotFoundError:
            print(f"✗ File not found: {json_file_path}")
            logging.error(f"File not found: {json_file_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON format: {e}")
            logging.error(f"Invalid JSON format: {e}")
            return False
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            logging.error(f"Error loading data: {e}")
            return False
    
    def basic_query(self):
        """
        OPERATION 2: Find all products in "Electronics" category with price < 50000
        Return only: name, price, stock
        """
        print("\n" + "="*60)
        print("OPERATION 2: Basic Query - Electronics under ₹50,000")
        print("="*60)
        
        try:
            # Query: category = "Electronics" AND price < 50000
            query = {
                "category": "Electronics",
                "price": {"$lt": 50000}
            }
            
            # Projection: only return name, price, stock
            projection = {
                "name": 1,
                "price": 1,
                "stock": 1,
                "_id": 0
            }
            
            # Execute query
            results = list(self.products.find(query, projection))
            
            print(f"\n✓ Found {len(results)} products\n")
            
            if results:
                print("Results:")
                print(f"{'Product Name':<30} {'Price':>12} {'Stock':>10}")
                print("-" * 52)
                for product in results:
                    name = product.get('name', 'N/A')[:28]
                    price = product.get('price', 0)
                    stock = product.get('stock', 0)
                    print(f"{name:<30} ₹{price:>10,.2f} {stock:>10}")
            
            logging.info(f"Basic query returned {len(results)} products")
            return results
        
        except Exception as e:
            print(f"✗ Query error: {e}")
            logging.error(f"Query error: {e}")
            return []
    
    def review_analysis(self):
        """
        OPERATION 3: Find products with average rating >= 4.0
        Use aggregation to calculate average from reviews array
        """
        print("\n" + "="*60)
        print("OPERATION 3: Review Analysis - Average Rating >= 4.0")
        print("="*60)
        
        try:
            # Aggregation pipeline
            pipeline = [
                {
                    # Add average rating field
                    "$addFields": {
                        "average_rating": {
                            "$cond": [
                                {"$gt": [{"$size": "$reviews"}, 0]},
                                {"$avg": "$reviews.rating"},
                                0
                            ]
                        }
                    }
                },
                {
                    # Filter: average_rating >= 4.0
                    "$match": {
                        "average_rating": {"$gte": 4.0}
                    }
                },
                {
                    # Sort by rating descending
                    "$sort": {"average_rating": -1}
                },
                {
                    # Project only needed fields
                    "$project": {
                        "name": 1,
                        "average_rating": 1,
                        "review_count": {"$size": "$reviews"},
                        "_id": 0
                    }
                }
            ]
            
            results = list(self.products.aggregate(pipeline))
            
            print(f"\n✓ Found {len(results)} products with high ratings\n")
            
            if results:
                print("Results:")
                print(f"{'Product Name':<35} {'Avg Rating':>12} {'Reviews':>10}")
                print("-" * 57)
                for product in results:
                    name = product.get('name', 'N/A')[:33]
                    rating = product.get('average_rating', 0)
                    reviews = product.get('review_count', 0)
                    print(f"{name:<35} {rating:>12.1f}⭐ {reviews:>10}")
            
            logging.info(f"Review analysis returned {len(results)} products")
            return results
        
        except Exception as e:
            print(f"✗ Aggregation error: {e}")
            logging.error(f"Aggregation error: {e}")
            return []
    
    def update_review(self, product_id="ELEC001"):
        """
        OPERATION 4: Add a new review to a product
        """
        print("\n" + "="*60)
        print(f"OPERATION 4: Add Review to Product {product_id}")
        print("="*60)
        
        try:
            # New review
            new_review = {
                "user_id": "U999",
                "username": "NewUser",
                "rating": 4,
                "comment": "Good value for money!",
                "date": datetime.now().isoformat()
            }
            
            # Update: add review to reviews array
            result = self.products.update_one(
                {"product_id": product_id},
                {"$push": {"reviews": new_review}}
            )
            
            if result.matched_count > 0:
                print(f"\n✓ Successfully added review to {product_id}")
                print(f"  User: {new_review['username']}")
                print(f"  Rating: {new_review['rating']}/5")
                print(f"  Comment: {new_review['comment']}")
                
                # Show updated product
                updated = self.products.find_one(
                    {"product_id": product_id},
                    {"name": 1, "reviews": 1, "_id": 0}
                )
                print(f"\n  Total reviews: {len(updated.get('reviews', []))}")
                
                logging.info(f"Added review to {product_id}")
            else:
                print(f"\n✗ Product {product_id} not found")
            
            return result.matched_count > 0
        
        except Exception as e:
            print(f"✗ Update error: {e}")
            logging.error(f"Update error: {e}")
            return False
    
    def category_analysis(self):
        """
        OPERATION 5: Complex Aggregation - Average price by category
        Calculate: category, avg_price, product_count
        Sort by avg_price descending
        """
        print("\n" + "="*60)
        print("OPERATION 5: Category Analysis - Avg Price by Category")
        print("="*60)
        
        try:
            # Aggregation pipeline
            pipeline = [
                {
                    "$group": {
                        "_id": "$category",
                        "avg_price": {"$avg": "$price"},
                        "product_count": {"$sum": 1},
                        "min_price": {"$min": "$price"},
                        "max_price": {"$max": "$price"},
                        "total_stock": {"$sum": "$stock"}
                    }
                },
                {
                    "$sort": {"avg_price": -1}
                },
                {
                    "$project": {
                        "category": "$_id",
                        "avg_price": 1,
                        "product_count": 1,
                        "min_price": 1,
                        "max_price": 1,
                        "total_stock": 1,
                        "_id": 0
                    }
                }
            ]
            
            results = list(self.products.aggregate(pipeline))
            
            print(f"\n✓ Analysis complete for {len(results)} categories\n")
            
            if results:
                print("Results:")
                print(f"{'Category':<20} {'Avg Price':>12} {'Products':>10} {'Stock':>10}")
                print("-" * 52)
                for item in results:
                    category = item.get('category', 'N/A')
                    avg_price = item.get('avg_price', 0)
                    count = item.get('product_count', 0)
                    stock = item.get('total_stock', 0)
                    print(f"{category:<20} ₹{avg_price:>10,.0f} {count:>10} {stock:>10}")
                
                print("\n\nDetailed Summary:")
                for item in results:
                    print(f"\n{item.get('category')} Category:")
                    print(f"  Average Price: ₹{item.get('avg_price', 0):,.0f}")
                    print(f"  Min Price: ₹{item.get('min_price', 0):,.0f}")
                    print(f"  Max Price: ₹{item.get('max_price', 0):,.0f}")
                    print(f"  Products: {item.get('product_count', 0)}")
                    print(f"  Total Stock: {item.get('total_stock', 0)} units")
            
            logging.info(f"Category analysis returned {len(results)} categories")
            return results
        
        except Exception as e:
            print(f"✗ Aggregation error: {e}")
            logging.error(f"Aggregation error: {e}")
            return []
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("\n✓ MongoDB connection closed")

def main():
    """Run all MongoDB operations"""
    
    print("\n" + "="*60)
    print("FlexiMart MongoDB Operations")
    print("="*60)
    
    # Initialize MongoDB operations
    mongo_ops = MongoDBOperations(
        mongo_url='mongodb://localhost:27017/',
        database='fleximart_nosql'
    )
    
    # Connect to MongoDB
    if not mongo_ops.connect():
        print("\n✗ Cannot proceed without MongoDB connection")
        return
    
    # Get the directory of this script
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, 'products_catalog.json')
    
    # Run operations
    mongo_ops.load_data(json_file_path)
    mongo_ops.basic_query()
    mongo_ops.review_analysis()
    mongo_ops.update_review("ELEC001")
    mongo_ops.category_analysis()
    
    # Disconnect
    mongo_ops.disconnect()
    
    print("\n" + "="*60)
    print("✓ All MongoDB operations completed successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
