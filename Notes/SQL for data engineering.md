| Method | What is it? | Define| Keyword | Real-World Example | Query (using a simple e-commerce setup (users, orders, products))|
| :--- | :--- | :--- | :--- | :--- | :-- |
| SELECT | 👀 The Viewer | Core data retrieval for exploration, validation, and downstream transformations. | SELECT | Grabbing only the username and avatar_url for a profile page. | SELECT username, email FROM users; |
| WHERE | 📝 The Filter | Filters rows early to reduce scan cost and improve pipeline performance. | WHERE | Finding users who haven't logged in since 2023-01-01. | SELECT * FROM orders WHERE status = 'shipped'; |
| ORDER BY | 📏 The Organizer | Sorts datasets for ranking, audits, and time-based validations. | ORDER BY | Sorting a high-score lobby from DESC (highest) to lowest. | SELECT * FROM products ORDER BY price DESC; |
| GROUP BY | 📦 The Bucket | Aggregates metrics across dimensions like region, product, or customer. | GROUP BY | Seeing how many total tickets were sold per movie_title. | SELECT category, COUNT(*) FROM products GROUP BY category; |
| HAVING | 🕵️ The Auditor | Filters aggregated results after grouping — essential for KPI thresholds. | HAVING | Filtering that movie list to only show blockbusters with COUNT > 1,000,000. | SELECT user_id, SUM(amount) FROM orders GROUP BY user_id HAVING SUM(amount) > 500; |
| INNER JOIN | 💍 The Perfect Match | Combines matching records across tables for fact–dimension modeling. (Middle only) | INNER JOIN | Linking Orders to Customers only if both exist. | SELECT users.name, orders.order_id FROM users INNER JOIN orders ON users.id = orders.user_id; |
| LEFT JOIN | 🏠 The Homebody | Enriches datasets while preserving all records from the primary table. (All left + Matching Right) | LEFT JOIN | Listing every Product even if it has zero Sales records. | SELECT users.name, orders.order_id FROM users LEFT JOIN orders ON users.id = orders.user_id; |
| FULL OUTER JOIN | 🤝 The Mixer | Reconciles mismatches between systems during data comparisons. (Everyone) | FULL JOIN | Merging two massive mailing lists to see who is on either (or both). | SELECT a.name, b.name FROM internal_leads a FULL JOIN external_leads b ON a.email = b.email; |
| DISTINCT | 🦄 The Unique Finder | Removes duplicates and validates uniqueness in raw ingestion layers. | DISTINCT | Getting a list of all unique job_titles in a 10k-row table. | SELECT DISTINCT country FROM users; |
| CASE WHEN | 🚦 The Logic Switch | Adds business logic directly inside transformations and derived columns. | CASE | Categorizing age into 'Minor', 'Adult', or 'Senior'. | SELECT name, CASE WHEN price > 100 THEN 'Premium' ELSE 'Standard' END as tier FROM products;
| MERGE / UPSERT | 🔄 The Syncer | Powers incremental loads and CDC pipelines in modern warehouses. | MERGE INTO (SQL) / INSERT... ON CONFLICT DO UPDATE (PostgreSPL) | Updating a user’s last_login if they exist, or adding them if they’re new. | MERGE INTO customers AS target USING new_leads AS source ON target.email = source.email WHEN MATCHED THEN UPDATE SET name = source.name WHEN NOT MATCHED THEN INSERT (name, email) VALUES (source.name, source.email); |
| WINDOW FUNCTIONS | 🪟 The Context King | Nest logic for conditional filtering and dependent calculations. | OVER | Calculating a SUM(sales) for the month without collapsing individual rows. | SELECT name, price, RANK() OVER (PARTITION BY category ORDER BY price DESC) as rank FROM products; |
| SUBQUERIES | 📦 The Inception | Nest logic for conditional filtering and dependent calculations. | (SELECT...) | Finding users whose id is in a secret list of "VIP" IDs. | SELECT name FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000); |
| Common Table Expressions (CTEs) | 🧱 The Lego Block | Make complex transformations readable, modular, and easier to debug. | WITH | Breaking a 300-line monster query into readable parts like cleaned_logs. | WITH high_value_orders AS ( SELECT * FROM orders WHERE amount > 1000 ) SELECT * FROM high_value_orders WHERE status = 'pending'; |
| ADVANCED AGGREGATIONS | 📈 The Stat Master | Calculates hierarchical totals and a grand total in a single pass. | ROLLUP | Creating a report that shows sales by State, then City, then a Grand Total. | SELECT region, city, SUM(sales) FROM store_sales GROUP BY ROLLUP(region, city); |
| UNION / UNION ALL | 📑 The Stacker | Combine datasets vertically across partitions or time ranges. Pro-Tip: UNION removes duplicates (slow); UNION ALL keeps everything (fast). | UNION / UNION ALL | Combining two similar lists of active_users and archived_users into one master list. | SELECT email FROM newsletter_subs UNION ALL SELECT email FROM customer_emails; |

**How does a SQL engine run a query?**
To a human, SQL reads from top to bottom. To the SQL Engine, it executes in a specific logical order to filter data as early as possible.<br/>

🏎️ The SQL Execution Order<br/>

FROM / JOIN | 📁 The Source | The engine identifies which tables to grab and joins them into one big dataset.<br/>
WHERE | ✂️ The Filter | It throws away rows that don't meet your criteria before doing any heavy lifting.<br/>
GROUP BY | 📦 The Bucket | It collapses the remaining rows into groups based on your columns.<br/>
HAVING | 🕵️ The Auditor | It filters those groups (e.g., "only show groups with a count > 10").<br/>
WINDOW FUNCTIONS | 🪟 The Context | It calculates things like RANK() or ROW_NUMBER() across the filtered groups.<br/>
SELECT | 🎨 The Output | It finally picks the specific columns you asked for and applies aliases.<br/>
DISTINCT | 🦄 The Unique | It removes any duplicate rows from the final selection.<br/>
ORDER BY | 📏 The Organizer | It sorts the final result set for your eyes.<br/>
LIMIT / OFFSET | 🛑 The Slicer | It chops the list to the specific number of rows requested.<br/>

<br/>
💡 Why it matters is because you cannot use a column alias created in the SELECT clause inside your WHERE clause — the WHERE step happens long before the SELECT step even knows that alias exists!
<br/>

To bypass the above restriction where the WHERE clause can't "see" an alias from the SELECT clause, we use a CTE. This forces the SQL engine to complete the calculation before the final filtering happens. <br/>

The "Alias Problem" Example
In a standard query, this fails:

```[language-identifier]
SELECT price * 0.10 AS discount_amount
FROM products
WHERE discount_amount > 50; -- ❌ ERROR: 'discount_amount' does not exist yet!
```

The CTE "Bypass" Solution
By wrapping the calculation in a CTE, you create a temporary table where discount_amount is a real column that the final WHERE clause can see.
<br/>
```[language-identifier]
WITH calculated_discounts AS (
  -- Step 1: Define the alias here
  SELECT 
    product_name, 
    price * 0.10 AS discount_amount 
  FROM products
)
-- Step 2: Now the engine treats it like a real column
SELECT * 
FROM calculated_discounts 
WHERE discount_amount > 50; -- ✅ SUCCESS!
```
<br/>
Why this works:

Step 1 (The CTE): The engine runs the SELECT inside the WITH block first.

Step 2 (The Main Query): The engine then treats calculated_discounts as a physical table where discount_amount is already "baked in" and ready to be filtered.

How to do this same "bypass" using a Window Function to filter for the top record in a group?

To filter for the "top" record (like the most recent login or the highest sale), you can't put a Window Function directly in a WHERE clause. You have to "wrap" it in a CTE or Subquery first.
❌ The "Wrong" Way (Fails)

The SQL engine runs WHERE before it calculates the Window Function, so it doesn't know what the rank is yet.

```
SELECT user_id, login_date, 
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date DESC) as latest_rank
FROM user_logins
WHERE latest_rank = 1; -- ❌ ERROR: column "latest_rank" does not exist
```

✅ The "Data Engineer" Way (CTE Bypass)

By using a CTE, you "bake" the rank into a temporary table, then filter it in the next step.

```
WITH ranked_logins AS (
  SELECT 
    user_id, 
    login_date, 
    -- 1. Assign a 1 to the most recent login for each user
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date DESC) as latest_rank
  FROM user_logins
)
-- 2. Now 'latest_rank' is a real column we can filter on
SELECT user_id, login_date
FROM ranked_logins
WHERE latest_rank = 1; 
```

🧠 Why this is a "Power Pattern"

Deduplication: This is the #1 way to remove duplicate records in a data warehouse (like Snowflake or BigQuery).

Top N: Change WHERE latest_rank = 1 to WHERE latest_rank <= 5 to get the top 5 records per category.

Cleanliness: It keeps your logic separated—Step 1 identifies the order, Step 2 picks the winner.

**🏆 The Top 5 Window Functions**

**ROW_NUMBER()** | 🆔 The Unique Identifier

What it does: Assigns a unique, sequential integer to rows (1, 2, 3, 4...).

Engineer Use Case: Deduplication. Use it to find the "newest" version of a record and filter for row_num = 1.

Pattern: ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC)

**RANK() / DENSE_RANK()** | 🏅 The Medalist

What it does: Assigns ranks, but handles "ties" differently. RANK skips numbers after a tie (1, 2, 2, 4); DENSE_RANK does not (1, 2, 2, 3).

Engineer Use Case: Top N Analysis. Identifying the top 3 selling products in every category.

Pattern: DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC)

**LAG() / LEAD()** | ⏪⏩ The Time Traveler

What it does: Accesses data from the row before (LAG) or the row after (LEAD) without a join.

Engineer Use Case: Period-over-Period Growth. Comparing this month’s revenue to last month’s.

Pattern: LAG(revenue) OVER (ORDER BY fiscal_month)

**SUM() / AVG() OVER** | 📈 The Rolling Metric

What it does: Calculates a running total or moving average while keeping all individual rows visible.

Engineer Use Case: Cumulative Growth. Tracking "Total Sales to Date" or a "7-Day Rolling Average" of active users.

Pattern: SUM(daily_sales) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

**FIRST_VALUE() / LAST_VALUE()** | 🏁 The Anchor

What it does: Grabs the very first or very last value in a specific window of data.

Engineer Use Case: Attribution Modeling. Finding the very first touchpoint (ad click) that led a user to sign up, even if they clicked 20 other things later.

Pattern: FIRST_VALUE(referral_source) OVER (PARTITION BY user_id ORDER BY click_time)


Let's see how to use LAG() in this same CTE style to calculate month-over-month growth

But first, what is LAG()?

LAG() is a window function that lets you "look back" at a previous row without using a self-join. It pulls data from a row above the current one, which is perfect for comparing today’s numbers to yesterday’s.

LAG() | ⏪ The Look-Back | LAG(column, offset) | Comparing this month's revenue to last month's to see if you're growing.

📈 Month-over-Month Growth Pattern

To calculate growth, you need the "Current Month" and "Previous Month" on the same row. Since WHERE can't see the previous row, we use a CTE to align them.

```
WITH monthly_sales AS (
  SELECT 
    month,
    total_revenue,
    -- 1. Grab the revenue from the row immediately above this one
    LAG(total_revenue) OVER (ORDER BY month) AS previous_month_revenue
  FROM sales_stats
)
-- 2. Use the aligned data to do the math
SELECT 
  month,
  total_revenue,
  previous_month_revenue,
  (total_revenue - previous_month_revenue) / previous_month_revenue * 100 AS growth_percent
FROM monthly_sales;
```

🧠 How it looks in your head

Imagine a spreadsheet where you copy a value from Cell B2 and paste it into Cell C3. LAG() does that automatically for every row in your dataset.

| Month |	Revenue	| LAG(Revenue)	| Result |
| :-- | :-- | :-- | :-- |
| Jan	| 100	| NULL | (First row has no "back") |
| Feb	| 120	| 100	| +20% Growth |
| Mar	| 150 |	120	| +25% Growth |

**🛠 Pro Tip: LEAD()**

If LAG() is the rearview mirror, LEAD() is the windshield. It does the exact same thing but looks at the next row instead of the previous one.

💡 Pro-Tip for Interviews

If an interviewer asks how to find the "difference between two rows," always start your answer with: "I'd use a CTE to wrap a LAG() function..." It shows you understand both the logic and the execution order.

We are going to find the top-selling product for each category and compare its sales to the previous month to see the growth—all in one clean, readable block.

**🐉 The "Boss Level" Pattern**

This query combines a CTE, Window Functions (RANK, LAG), Aggregations, and an Inner Join.

```
WITH monthly_product_performance AS (
  -- STEP 1: Aggregate raw sales and 'Look Back' using LAG
  SELECT 
    p.category,
    p.product_name,
    DATE_TRUNC('month', o.order_date) as sales_month,
    SUM(o.amount) as current_month_sales,
    LAG(SUM(o.amount)) OVER (
      PARTITION BY p.product_name 
      ORDER BY DATE_TRUNC('month', o.order_date)
    ) as prev_month_sales
  FROM products p
  INNER JOIN orders o ON p.id = o.product_id
  GROUP BY 1, 2, 3
),
ranked_performance AS (
  -- STEP 2: Rank products within their category
  SELECT 
    *,
    DENSE_RANK() OVER (
      PARTITION BY category, sales_month 
      ORDER BY current_month_sales DESC
    ) as sales_rank
  FROM monthly_product_performance
)
-- STEP 3: Final Filter for the #1 Product
SELECT 
  category,
  product_name,
  sales_month,
  current_month_sales,
  ((current_month_sales - prev_month_sales) / prev_month_sales * 100) as growth_pct
FROM ranked_performance
WHERE sales_rank = 1;
```

🧠 Why this is "High Seniority" SQL:

Readability: Using two CTEs (monthly_product_performance and ranked_performance) makes it impossible to get lost.

Efficiency: It uses Window Functions instead of expensive self-joins to get the previous month's data.

The "Bypass": It filters on sales_rank = 1 in the final step because it knows the WHERE clause can't see that rank in Step 2.

The Join: It uses an Inner Join to ensure we only look at products that actually have sales.

**Performance Tuning:**

**Indexing:** The "Shortcut"<br/>

Definition: A separate, sorted map (usually a B-Tree) that points to the exact physical location of a row based on a specific column.<br/>

How it works: Instead of reading every row in a table (a "Full Table Scan"), the database looks at the index first, finds the "page number," and jumps straight to the data.<br/>

Best For: Point Lookups. 
- Use this when you need to find one specific record (e.g., WHERE user_id = 505) or a very small subset of rows.<br/>

DE Reality Check: It makes Reads fast but Writes slow. Every time you INSERT a row, the database has to stop and update the index "map" too.<br/>

**Partitioning:** The "Folder System"<br/>

Definition: Physically splitting one massive table into smaller, independent sub-tables (partitions) on the hard drive, usually based on a date or category.<br/>

How it works: When you query a specific date, the database engine uses "Partition Pruning"—it completely ignores the folders (files) it doesn't need and only scans the relevant one.<br/>

Best For: Massive Scans & Data Lifecycles. 
- Use this for huge analytical tables (e.g., WHERE event_date = '2024-03-01').<br/>

DE Reality Check: It makes maintenance easy. Need to delete data from 2018? Don't run a slow DELETE query; just "Drop" that specific partition. It’s instantaneous and uses zero processing power.<br/>

**📑 SQL Data Engineer Cheat Sheet: Summary**

| Level | Pattern | Keyword | Real-World Example |
| :--- | :--- | :--- | :--- |
| **Basics** | SELECT / WHERE | FILTER | Grabbing active users from a table. |
| **Joins** | LEFT / INNER | JOIN | All Customers + matching Orders. |
| **Logic** | CASE WHEN | IF/THEN | Labeling sales as 'High' or 'Low' value. |
| **Sync** | UPSERT | ON CONFLICT | Update user last_login or insert if new. |
| **Blocks** | CTEs | WITH | Breaking 300 lines into "lego blocks." |
| **Context** | WINDOW | OVER | Ranking sales without collapsing rows. |
| **Trends** | LAG / LEAD | LOOK BACK | Comparing this month to last month. |
| **Stats** | ROLLUP | SUBTOTAL | Sales by City, State, and Grand Total. |
| **Speed** | INDEXING | CREATE INDEX | Speeding up lookups on a billion-row table. |
| **Storage** | PARTITION | PARTITION BY | Splitting a massive table into monthly chunks. |

**5 real-world queries covering the patterns that's used daily:**

1. The "Deduplication" Pattern

Data pipelines often ingest duplicate events due to network retries or upstream bugs. This query identifies and keeps only the most recent version of each record. 

```
WITH ranked_events AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY order_id 
               ORDER BY updated_at DESC
           ) as rn
    FROM raw_orders
)
SELECT * 
FROM ranked_events 
WHERE rn = 1;
```

Explanation: ROW_NUMBER() assigns a sequence to each row within its "group" (PARTITION BY order_id). By ordering by a timestamp (updated_at DESC), the latest record always gets rn = 1. 

<!-- Credits from: 
https://www.google.com/, https://www.linkedin.com/posts/mukilanashokraj_dataengineering-sql-bigdata-activity-7430334953915281408-BykO#:~:text=2w,15. <br/>
-->
