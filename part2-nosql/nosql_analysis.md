# NoSQL Analysis Report - FlexiMart Product Catalog

## Section A: Limitations of RDBMS for Product Catalog (4 marks - 150 words)

### Problem: Handling Diverse Product Attributes

The current relational database schema faces significant challenges when managing products with varying attributes:

**Product Heterogeneity Challenge:**
Different product types require different attributes. A laptop needs CPU, RAM, and storage specifications, while a shoe requires size, color, and material. In RDBMS, this would require either:

- Creating a universal products table with null values for unused attributes (wasting space)
- Creating separate tables for each product type (leading to schema proliferation)
- Using separate attribute tables with EAV (Entity-Attribute-Value) pattern (complex joins)

**Schema Rigidity Issues:**
When FlexiMart wants to add new product types (e.g., smart home devices, furniture), the schema must be altered. This requires:

- Table modifications (ALTER TABLE statements)
- Application code changes
- Data migration and downtime
- Testing and validation cycles

**Nested Data Limitation:**
Customer reviews are hierarchical data that RDBMS handles poorly. Storing reviews in a separate table creates performance issues when retrieving products with reviews (requires multiple joins and aggregations).

**Scalability Constraints:**
As product diversity increases, the schema becomes increasingly complex and performance degrades due to multiple joins required to reconstruct complete product documents.

---

## Section B: NoSQL Benefits - MongoDB Solutions (4 marks - 150 words)

### How MongoDB Solves These Problems

**Flexible Schema:**
MongoDB's document-oriented model allows each product document to have unique attributes without affecting others. A laptop document can contain CPU and RAM fields while a shoe document contains size and color fields in the same collection. No NULL values, no wasted space, no separate tables.

**Schema Evolution:**
Adding new product attributes (like warranty information or eco-rating) requires no schema migration. Simply include the new fields in new documents. Existing documents continue working unchanged. This enables rapid product catalog expansion.

**Embedded Documents:**
Reviews are embedded within product documents as arrays of review objects. This eliminates join operations. Retrieving a product automatically includes all associated reviews without additional queries or complex aggregations.

**Horizontal Scalability:**
MongoDB supports sharding, distributing large product catalogs across multiple servers. This provides better performance for diverse, growing datasets compared to RDBMS.

**Query Flexibility:**
MongoDB's aggregation pipeline allows complex queries on nested data (e.g., "find products with average rating > 4") without expensive multi-table joins.

**Developer-Friendly:**
Documents map naturally to application objects (JSON/BSON), eliminating impedance mismatch and reducing code complexity.

---

## Section C: Trade-offs and Disadvantages (2 marks - 100 words)

### Two Key Disadvantages of MongoDB vs MySQL

**1. Data Consistency and ACID Limitations:**
MongoDB traditionally lacked multi-document ACID transactions (added in v4.0+). For the product catalog, this means concurrent updates might create inconsistencies. If updating product price in multiple places (e.g., inventory sync), MySQL's transaction guarantee ensures all-or-nothing updates. MongoDB requires careful application-level logic.

**2. Memory Overhead and Storage Inefficiency:**
MongoDB stores entire documents, including repeated fields in reviews array. For products with 100+ reviews, this creates significant data duplication. MySQL's normalized design stores review data once, creating more efficient storage. Additionally, MongoDB indexes require more memory than traditional relational indexes for the same query performance.

---

## Implementation Recommendation

**MongoDB is recommended for FlexiMart when:**

- Product catalog needs frequent schema changes
- Review and specification data growth is unpredictable
- Real-time flexibility is prioritized over strict consistency
- Horizontal scaling is a requirement

**MySQL should be retained for:**

- Order and transaction management (ACID critical)
- Customer data (requires consistent updates)
- Financial reporting (needs strict consistency)

**Hybrid Approach:**
Use MongoDB for product catalog (flexible) and MySQL for orders/transactions (consistent). This balances flexibility with reliability.
