#!/usr/bin/env python
# coding: utf-8

# ## Sample Queries
# 
# New notebook

# In[3]:


# The command is not a standard IPython magic command. It is designed for use within Fabric notebooks only.
# %%sql
# -- Total sales and profit by category
# SELECT category, SUM(sales) AS total_sales, SUM(profit) AS total_profit
# FROM gold_sales
# GROUP BY category
# ORDER BY total_sales DESC


# In[4]:


# The command is not a standard IPython magic command. It is designed for use within Fabric notebooks only.
# %%sql
# -- Average profit margin by region
# SELECT region, AVG(profit_margin) AS avg_profit_margin
# FROM gold_sales
# GROUP BY region
# ORDER BY avg_profit_margin DESC


# In[5]:


# The command is not a standard IPython magic command. It is designed for use within Fabric notebooks only.
# %%sql
# -- Top 10 cities by sales
# SELECT city, SUM(sales) AS total_sales
# FROM gold_sales
# GROUP BY city
# ORDER BY total_sales DESC
# LIMIT 10


# In[6]:


# The command is not a standard IPython magic command. It is designed for use within Fabric notebooks only.
# %%sql
# -- Ship mode usage and average discount
# SELECT ship_mode, COUNT(*) AS order_count, AVG(discount) AS avg_discount
# FROM gold_sales
# GROUP BY ship_mode

