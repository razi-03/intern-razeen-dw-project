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