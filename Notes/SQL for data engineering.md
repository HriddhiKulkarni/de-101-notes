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
Do you want to see how to do this same "bypass" using a Window Function to filter for the top record in a group?




sure
To filter for the "top" record (like the most recent login or the highest sale), you can't put a Window Function directly in a WHERE clause. You have to "wrap" it in a CTE or Subquery first.
❌ The "Wrong" Way (Fails)
The SQL engine runs WHERE before it calculates the Window Function, so it doesn't know what the rank is yet.
sql
SELECT user_id, login_date, 
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date DESC) as latest_rank
FROM user_logins
WHERE latest_rank = 1; -- ❌ ERROR: column "latest_rank" does not exist
Use code with caution.

✅ The "Data Engineer" Way (CTE Bypass)
By using a CTE, you "bake" the rank into a temporary table, then filter it in the next step.
sql
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

<!-- Credits from: 
https://www.google.com/, https://www.linkedin.com/posts/mukilanashokraj_dataengineering-sql-bigdata-activity-7430334953915281408-BykO#:~:text=2w,15. <br/>
-->
