# intern-razeen-dw-project

# Retail Sales Data Engineering Project

End-to-end ETL pipeline built on Microsoft Fabric, transforming raw retail sales CSV data into a curated, analytics-ready Delta table and a multi-page Power BI dashboard.

## Problem

Raw retail sales data (orders, regions, segments, ship modes) arrives as disconnected CSV exports with mixed data types, no relationships, and no derived business metrics. Analysts need a single, clean, joined table with accurate types and calculated KPIs (profit margin, discount amount) to build reporting on top of — without re-deriving that logic in every report.

## Architecture

```
[Raw CSV Files: fact_sales, dim_category, dim_region, dim_segment, dim_shipmode]
                              │
                              ▼
                  Fabric Lakehouse — Files/
                  (raw landing zone)
                              │
                              ▼  PySpark: ingest, dedupe, drop nulls
                  Bronze Layer — bronze_superstore
                              │
                              ▼  PySpark: clean, type-cast, join into a single wide table
                  Silver Layer — silver_superstore
                              │
                              ▼  PySpark: derived metrics (profit margin, discount amount)
                  Gold Layer — gold_sales (Delta Table)
                              │
                              ▼
                  Power BI Dashboard
                  (Executive / Sales / Profit / Shipping)
```

Orchestrated end-to-end with a Fabric Data Pipeline (`RetailSales_ETL_Daily`) running the ETL notebook on a daily schedule.

**Note on architecture:** the original reference design specifies three physically separate ADLS Gen2 containers (Bronze/Silver/Gold) plus an Azure SQL DB warehouse layer. This project uses Microsoft Fabric instead of Databricks/ADLS, which consolidates raw files, Bronze, Silver, and Gold into a single Lakehouse (OneLake) with logical table separation rather than physical container separation, and serves Power BI directly off the Gold Delta table via the Lakehouse SQL endpoint, skipping a separate Azure SQL DB warehouse. This is a deliberate platform substitution, not a missed requirement — Fabric's unified Lakehouse model removes the need for a separate warehouse hop while still preserving the same logical Bronze → Silver → Gold stages.

## Tech Stack

- **Microsoft Fabric** — Lakehouse, Notebooks (PySpark), Data Pipelines
- **Delta Lake** — table format for Bronze/Silver/Gold layers
- **Power BI** — dashboard and reporting layer
- **Python / PySpark** — transformation logic

## Lakehouse Structure

```
SuperstoreLakehouse/
├── Tables/dbo/
│   ├── bronze_superstore
│   ├── silver_superstore
│   ├── gold_sales
│   ├── fact_sales
│   ├── dim_category
│   ├── dim_region
│   ├── dim_segment
│   ├── dim_shipmode
│   └── dim_date
└── Files/PowerBI/
    ├── fact_sales/
    ├── dim_category/
    ├── dim_region/
    ├── dim_segment/
    └── dim_shipmode/
```

## Setup Steps

1. **Create a Fabric workspace** — `RetailSalesProject`
2. **Create a Lakehouse** — `SuperstoreLakehouse`
3. **Upload source CSVs** to `Files/PowerBI/` (fact_sales, dim_category, dim_region, dim_segment, dim_shipmode)
4. **Create a Notebook** attached to the Lakehouse, containing the ETL logic:
   - Read all 5 CSVs with inferred schema
   - Cast key columns and numeric fields to correct types
   - Join fact table to dimension tables on surrogate keys (left joins)
   - Calculate `profit_margin` (guarded against division by zero) and `discount_amount`
   - Write result to the `gold_sales` Delta table (`overwrite` mode, schema overwrite enabled)
5. **Create a Data Pipeline** — `RetailSales_ETL_Daily`
6. **Add a Notebook activity** pointing at the ETL notebook
7. **Schedule** the pipeline to run daily at 8:00 AM
8. **Connect Power BI** to the Lakehouse via `Get Data → Microsoft Fabric → Lakehouse`, load `gold_sales`
9. **Build the dashboard** (see below) and publish to the workspace

## Orchestration Notes

The pipeline runs the ETL notebook on a daily schedule via Fabric Data Pipelines. A failure-notification activity (Office 365 Outlook, then Microsoft Teams) was attempted on the pipeline's failure path but was blocked by tenant-level restrictions (`MailboxNotEnabledForRESTAPI` on the institutional email account, and no accessible Teams channel). This was scoped out of the current build — in a production environment, this would be resolved via tenant admin configuration or a dedicated service account, and the pipeline's native run-history/alert monitoring in Fabric workspace settings can serve as a fallback in the meantime.

## Dashboard

Four-page Power BI report (`Retail Sales Dashboard`):

- **Executive** — KPI summary (Total Sales $2.30M, Total Profit $286.24K, Profit Margin 12.47%, Avg Discount 0.16, Total Quantity 37.82K), sales by category/segment/ship mode, profit by region, sales by state/city
- **Sales** — category and quantity breakdowns, sales by city/state, with category/region/segment/ship mode slicers
- **Profit** — category profit, average discount vs. profit by category, city profit ranking, loss state map
- **Shipping** — ship mode usage and profit, region profit/sales, ship mode sales

## Sample SQL Queries

Run against the Lakehouse SQL endpoint:

```sql
-- Total sales and profit by category
SELECT category, SUM(sales) AS total_sales, SUM(profit) AS total_profit
FROM gold_sales
GROUP BY category
ORDER BY total_sales DESC;

-- Average profit margin by region
SELECT region, AVG(profit_margin) AS avg_profit_margin
FROM gold_sales
GROUP BY region
ORDER BY avg_profit_margin DESC;

-- Top 10 cities by sales
SELECT city, SUM(sales) AS total_sales
FROM gold_sales
GROUP BY city
ORDER BY total_sales DESC
LIMIT 10;

-- Ship mode usage and average discount
SELECT ship_mode, COUNT(*) AS order_count, AVG(discount) AS avg_discount
FROM gold_sales
GROUP BY ship_mode;
```

## Key Learnings

- **Division-by-zero handling**: the initial `profit_margin` calculation (`profit / sales * 100`) produced `inf`/null errors on zero-sales rows. Fixed with a `when(col("sales") != 0, ...).otherwise(None)` guard.
- **Schema inference**: `inferSchema=True` on CSV reads is convenient but not reliable for production — explicit `.cast()` calls on key and numeric columns were necessary to prevent type mismatches during joins.
- **Variable ordering in notebooks**: an early debugging pass referenced `sales_gold` before it was defined, a reminder that notebook cell execution order matters independently of file order.
- **Platform substitution tradeoffs**: choosing Fabric over Databricks/ADLS simplified the architecture (single Lakehouse vs. three storage containers + separate SQL DB) at the cost of less granular control over each medallion layer's physical storage — a reasonable tradeoff for a project at this scale.
- **Tenant restrictions are a real constraint**: institutional email/Teams accounts in education tenants often block REST API-based notification connectors; build failure-handling with a fallback plan rather than assuming connector access.

## Repository Structure

```
├── README.md
├── notebooks/
│   └── ETL_Notebook.py
├── sql/
│   └── sample_queries.sql
└── screenshots/
    ├── executive_dashboard.png
    ├── sales_page.png
    ├── profit_page.png
    ├── shipping_page.png
    └── lakehouse_tables.png
```
