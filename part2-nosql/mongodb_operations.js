// ============================================================================
// MongoDB Operations for FlexiMart Product Catalog
// ============================================================================

// Database: fleximart_nosql
// Collection: products

// ============================================================================
// Operation 1: Load Data (1 mark)
// ============================================================================
// Import the provided JSON file into collection 'products'

// Command to execute from terminal:
// mongoimport --db fleximart_nosql --collection products --file products_catalog.json --jsonArray

// Alternatively, use MongoDB Compass or the following JavaScript:
db.products.insertMany([
  {
    "product_id": "ELEC001",
    "name": "Samsung Galaxy S21 Ultra",
    "category": "Electronics",
    "subcategory": "Smartphones",
    "price": 79999.00,
    "stock": 150,
    "specifications": {
      "brand": "Samsung",
      "ram": "12GB",
      "storage": "256GB",
      "screen_size": "6.8 inches",
      "processor": "Exynos 2100",
      "battery": "5000mAh",
      "camera": "108MP + 12MP + 10MP"
    },
    "reviews": [
      {
        "user_id": "U001",
        "username": "TechGuru",
        "rating": 5,
        "comment": "Excellent phone with amazing camera quality!",
        "date": new Date("2024-01-15")
      },
      {
        "user_id": "U012",
        "username": "MobileUser",
        "rating": 4,
        "comment": "Great performance but a bit pricey.",
        "date": new Date("2024-02-10")
      },
      {
        "user_id": "U023",
        "username": "PhotoEnthusiast",
        "rating": 5,
        "comment": "Best camera phone I've ever used!",
        "date": new Date("2024-03-05")
      }
    ],
    "tags": ["flagship", "5G", "android", "photography"],
    "warranty_months": 12,
    "created_at": new Date("2023-12-01T10:00:00Z"),
    "updated_at": new Date("2024-03-20T14:30:00Z")
  }
  // ... additional products from products_catalog.json
]);

// ============================================================================
// Operation 2: Basic Query (2 marks)
// ============================================================================
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock

db.products.find(
  {
    "category": "Electronics",
    "price": { $lt: 50000 }
  },
  {
    "name": 1,
    "price": 1,
    "stock": 1,
    "_id": 0
  }
);

// Alternative with aggregation pipeline for more control:
db.products.aggregate([
  {
    $match: {
      "category": "Electronics",
      "price": { $lt: 50000 }
    }
  },
  {
    $project: {
      "name": 1,
      "price": 1,
      "stock": 1,
      "_id": 0
    }
  }
]);

// ============================================================================
// Operation 3: Review Analysis (2 marks)
// ============================================================================
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array

db.products.aggregate([
  {
    // Add a field with the average rating calculated from reviews array
    $addFields: {
      "avg_rating": {
        $avg: "$reviews.rating"
      }
    }
  },
  {
    // Filter products with average rating >= 4.0
    $match: {
      "avg_rating": { $gte: 4.0 }
    }
  },
  {
    // Project only relevant fields
    $project: {
      "product_id": 1,
      "name": 1,
      "category": 1,
      "price": 1,
      "avg_rating": { $round: ["$avg_rating", 2] },
      "review_count": { $size: "$reviews" },
      "_id": 0
    }
  },
  {
    // Sort by average rating descending
    $sort: { "avg_rating": -1 }
  }
]);

// ============================================================================
// Operation 4: Update Operation (2 marks)
// ============================================================================
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}

db.products.updateOne(
  {
    "product_id": "ELEC001"
  },
  {
    $push: {
      "reviews": {
        "user_id": "U999",
        "username": "NewReviewer",
        "rating": 4,
        "comment": "Good value",
        "date": new Date("2024-03-30")
      }
    }
  }
);

// Verify the update was successful:
db.products.findOne(
  { "product_id": "ELEC001" },
  { "reviews": 1, "_id": 0 }
);

// ============================================================================
// Operation 5: Complex Aggregation (3 marks)
// ============================================================================
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending

db.products.aggregate([
  {
    // Group by category and calculate statistics
    $group: {
      "_id": "$category",
      "avg_price": {
        $avg: "$price"
      },
      "product_count": {
        $sum: 1
      },
      "min_price": {
        $min: "$price"
      },
      "max_price": {
        $max: "$price"
      }
    }
  },
  {
    // Project the results in desired format
    $project: {
      "_id": 0,
      "category": "$_id",
      "avg_price": { $round: ["$avg_price", 2] },
      "product_count": 1,
      "min_price": { $round: ["$min_price", 2] },
      "max_price": { $round: ["$max_price", 2] }
    }
  },
  {
    // Sort by average price descending
    $sort: { "avg_price": -1 }
  }
]);

// ============================================================================
// Additional Useful Operations
// ============================================================================

// Get products with stock below threshold
db.products.aggregate([
  {
    $match: {
      "stock": { $lt: 50 }
    }
  },
  {
    $project: {
      "product_id": 1,
      "name": 1,
      "category": 1,
      "stock": 1,
      "_id": 0
    }
  },
  {
    $sort: { "stock": 1 }
  }
]);

// Search products by tag
db.products.find(
  {
    "tags": "5G"
  },
  {
    "name": 1,
    "category": 1,
    "price": 1,
    "tags": 1,
    "_id": 0
  }
);

// Find products by partial name match
db.products.find(
  {
    "name": /^Samsung/i  // Case-insensitive regex
  },
  {
    "product_id": 1,
    "name": 1,
    "price": 1,
    "_id": 0
  }
);

// Get products with more than 3 reviews
db.products.aggregate([
  {
    $addFields: {
      "review_count": { $size: "$reviews" }
    }
  },
  {
    $match: {
      "review_count": { $gt: 3 }
    }
  },
  {
    $project: {
      "product_id": 1,
      "name": 1,
      "review_count": 1,
      "_id": 0
    }
  }
]);

// Get most recent reviews across all products
db.products.aggregate([
  {
    $unwind: "$reviews"  // Flatten reviews array
  },
  {
    $sort: { "reviews.date": -1 }
  },
  {
    $limit: 10
  },
  {
    $project: {
      "product_name": "$name",
      "username": "$reviews.username",
      "rating": "$reviews.rating",
      "comment": "$reviews.comment",
      "date": "$reviews.date",
      "_id": 0
    }
  }
]);

// ============================================================================
// Index Creation for Performance (Optional but Recommended)
// ============================================================================

// Create index on category for faster filtering
db.products.createIndex({ "category": 1 });

// Create index on price for range queries
db.products.createIndex({ "price": 1 });

// Create compound index for Electronics category with specific prices
db.products.createIndex({ "category": 1, "price": 1 });

// Create text search index on product name
db.products.createIndex({ "name": "text", "description": "text" });

// ============================================================================
// Example Query Results
// ============================================================================

/*
OPERATION 2 EXPECTED OUTPUT:
{
  "name": "OnePlus Nord CE 3",
  "price": 26999,
  "stock": 180
}
{
  "name": "Sony WH-1000XM5 Headphones",
  "price": 29990,
  "stock": 200
}

OPERATION 3 EXPECTED OUTPUT:
{
  "product_id": "ELEC001",
  "name": "Samsung Galaxy S21 Ultra",
  "category": "Electronics",
  "price": 79999,
  "avg_rating": 4.67,
  "review_count": 3
}

OPERATION 5 EXPECTED OUTPUT:
{
  "category": "Electronics",
  "avg_price": 53764.67,
  "product_count": 6,
  "min_price": 26999,
  "max_price": 189999
}
{
  "category": "Fashion",
  "avg_price": 6132.50,
  "product_count": 6,
  "min_price": 1499,
  "max_price": 12995
}
*/
