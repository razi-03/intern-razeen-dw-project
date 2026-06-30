#!/usr/bin/env python
# coding: utf-8

# ## ETL Notebook
# 
# null

# In[55]:


# ## ETL Notebook - Corrected Version
# 
# This notebook demonstrates a complete ETL pipeline:
# 1. Read dimension and fact tables from CSV
# 2. Cast columns to appropriate data types
# 3. Join dimensions to fact table
# 4. Calculate derived metrics
# 5. Save to Delta table

# In[1]:

from pyspark.sql.functions import *

# ----------------------------
# Drop existing table
# ----------------------------

spark.sql("DROP TABLE IF EXISTS gold_sales")

# ----------------------------
# Read CSV files
# ----------------------------

print("Reading CSV files...")

fact_sales = spark.read.option("header", True).option("inferSchema", True).csv(
    "Files/PowerBI/fact_sales/part-00000-fc0c9d8e-3b46-459d-9ad0-7b509168060e-c000.csv"
)

dim_category = spark.read.option("header", True).option("inferSchema", True).csv(
    "Files/PowerBI/dim_category/part-00000-0977dd15-42ed-451d-8134-2589897d5f6c-c000.csv"
)

dim_region = spark.read.option("header", True).option("inferSchema", True).csv(
    "Files/PowerBI/dim_region/part-00000-e6852d3a-ba12-46c7-977a-25f237018de1-c000.csv"
)

dim_segment = spark.read.option("header", True).option("inferSchema", True).csv(
    "Files/PowerBI/dim_segment/part-00000-5325ce96-f54c-42be-8e92-5950e05f520e-c000.csv"
)

dim_shipmode = spark.read.option("header", True).option("inferSchema", True).csv(
    "Files/PowerBI/dim_shipmode/part-00000-d21d1281-6605-4299-ae9f-e2c61abfb617-c000.csv"
)

print("CSV files loaded successfully!")

# In[2]:

# ----------------------------
# Cast key columns
# ----------------------------

print("Casting data types...")

fact_sales = (
    fact_sales
    .withColumn("category_key", col("category_key").cast("int"))
    .withColumn("region_key", col("region_key").cast("int"))
    .withColumn("segment_key", col("segment_key").cast("int"))
    .withColumn("shipmode_key", col("shipmode_key").cast("int"))
    .withColumn("sales", col("sales").cast("double"))
    .withColumn("quantity", col("quantity").cast("int"))
    .withColumn("discount", col("discount").cast("double"))
    .withColumn("profit", col("profit").cast("double"))
)

dim_category = dim_category.withColumn("category_key", col("category_key").cast("int"))
dim_region = dim_region.withColumn("region_key", col("region_key").cast("int"))
dim_segment = dim_segment.withColumn("segment_key", col("segment_key").cast("int"))
dim_shipmode = dim_shipmode.withColumn("shipmode_key", col("shipmode_key").cast("int"))

print("Data types casted successfully!")

# In[3]:

# ----------------------------
# Join dimensions
# ----------------------------

print("Joining dimensions to fact table...")

sales_gold = (
    fact_sales
    .join(dim_category.select("category_key", "category"), "category_key", "left")
    .join(
        dim_region.select(
            "region_key",
            "country",
            "region",
            "state",
            "city",
            "postal_code"
        ),
        "region_key",
        "left"
    )
    .join(dim_segment.select("segment_key", "segment"), "segment_key", "left")
    .join(dim_shipmode.select("shipmode_key", "ship_mode"), "shipmode_key", "left")
)

print("Dimensions joined successfully!")

# In[4]:

# ----------------------------
# Derived metrics
# ----------------------------

print("Calculating derived metrics...")

sales_gold = (
    sales_gold
    .withColumn(
        "profit_margin",
        when(col("sales") != 0, round(col("profit") / col("sales") * 100, 2)).otherwise(None)
    )
    .withColumn(
        "discount_amount",
        round(col("sales") * col("discount"), 2)
    )
)

print("Derived metrics calculated successfully!")

# In[5]:

# ----------------------------
# Display schema and sample data
# ----------------------------

print("\n=== GOLD SALES TABLE SCHEMA ===")
sales_gold.printSchema()

print("\n=== COLUMN NAMES ===")
print(sales_gold.columns)

print("\n=== SAMPLE DATA ===")
display(sales_gold)

# In[6]:

# ----------------------------
# Save table
# ----------------------------

print("\nSaving to Delta table...")

sales_gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_sales")

print("\n✓ ETL completed successfully!")
print(f"Total records: {sales_gold.count()}")

