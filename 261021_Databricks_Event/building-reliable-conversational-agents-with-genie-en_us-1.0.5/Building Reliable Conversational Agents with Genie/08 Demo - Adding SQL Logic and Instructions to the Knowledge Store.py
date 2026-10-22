# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Adding SQL Logic and Instructions to the Knowledge Store
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC In the previous demo, you added table and column descriptions, synonyms, and prompt matching to improve Genie's understanding of your data. While descriptions help Genie know **what** each column contains, they cannot define **business terms**, teach **complex query patterns**, or create **derived columns** like region.
# MAGIC
# MAGIC In this demo, you will add the remaining curation tools to address the benchmark failures that metadata alone could not fix:
# MAGIC   - **Joins**
# MAGIC   - **SQL expressions**, 
# MAGIC   - **SQL queries**
# MAGIC   - **Text** instructions
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this demo, you will be able to:
# MAGIC
# MAGIC 1. **Add SQL expressions** in the Knowledge Store to define derived columns like region.
# MAGIC 2. **Add example SQL queries** to teach Genie complex query patterns like LEFT JOIN.
# MAGIC 3. **Add text instructions** to define ambiguous business terms and set default behaviors.
# MAGIC 4. **Re-run benchmarks** to measure the impact of SQL logic and instructions on accuracy.
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #f44336;
# MAGIC   background: #ffebee;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Prerequisites</strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Complete **the previous demonstrations** before proceeding. This demo builds on the metadata and benchmarks from previous demos.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - SELECT A COMPUTE ENVIRONMENT
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #f44336;
# MAGIC   background: #ffebee;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Select a Serverless SQL Warehouse</strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Before starting this notebook, select the required compute environment listed below.
# MAGIC
# MAGIC - **Serverless SQL Warehouse (2X-Small is sufficient)**
# MAGIC   - Select **Compute** > **More** > **SQL Warehouse** > Select a SQL Warehouse you have access to.
# MAGIC
# MAGIC **NOTE:** This notebook was **developed and tested using Serverless SQL Warehouse**. Other compute options may work but are not guaranteed to behave the same or support all features demonstrated.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Classroom Setup
# MAGIC
# MAGIC 1. Run the cell below to set your default catalog and schema.
# MAGIC     - This assumes you have already run the setup from a prior demo and your tables exist in **labuser_YOUR_USER_NAME.genie_course_bakehouse**.

# COMMAND ----------

# MAGIC %run ./Includes/Classroom-Setup-adding-sql-logic-instructions

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## B. Genie Agent Authoring Checklist
# MAGIC
# MAGIC We are now on steps **4** and **5** of the authoring checklist: encoding business logic in SQL and adding text instructions.
# MAGIC
# MAGIC <br></br>
# MAGIC <!--
# MAGIC   Focus variant of the Genie Agent Authoring Checklist.
# MAGIC   Each step card shows its full-color inline styles AND a commented "ACTIVE" version for the dimmed cards.
# MAGIC   To bring a dimmed step back to color: swap the dimmed <div> opening with the line marked "ACTIVE", and restore the inner number/title colors.
# MAGIC -->
# MAGIC
# MAGIC <div style="max-width: 1280px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <!-- 6-STEP FLOW -->
# MAGIC <div style="display: grid; grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr; gap: 0; align-items: stretch;">
# MAGIC
# MAGIC   <!-- STEP 1 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #2574B5; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">1</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Start with purpose<br>and questions</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 2 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #02A36F; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">2</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Select a minimal<br>data slice</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 3 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #F8A805; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">3</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Add metadata<br>and synonyms</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 4 (active) -->
# MAGIC   <div style="background: #F9F7F4; border: 3px solid #FF5F46; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #FF5F46; line-height: 1; margin-bottom: 8px;">4</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Encode business<br>logic in SQL</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 5 (active) -->
# MAGIC   <div style="background: #F9F7F4; border: 3px solid #98182A; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #98182A; line-height: 1; margin-bottom: 8px;">5</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Add light global<br>text instructions</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 6 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #1C3037; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">6</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Test, benchmark,<br>and iterate with users</div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B1. What Still Needs Fixing (Most Likely, Results Can Vary)
# MAGIC
# MAGIC After adding descriptions and synonyms, we re-ran our benchmarks. 
# MAGIC
# MAGIC Some improved, but several still fail because metadata alone cannot solve them.
# MAGIC
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Remaining Benchmark Failures (Can Vary)
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC | # | Benchmark Question | Problem | Fix |
# MAGIC |---|-------------------|---------|-----|
# MAGIC | 3 | *Who are our best customers?* | "Best" is undefined. Genie guesses, adds extra columns, and does not limit results | **Text instruction** defining best = highest total spend, return top 10 |
# MAGIC | 4 | *How many franchises does each supplier serve?* | Genie uses INNER JOIN, dropping 21 orphaned franchises | **Example SQL query** demonstrating the LEFT JOIN + COALESCE pattern |
# MAGIC | 5 | *What are total sales by region?* | No `region` column — Genie groups by country instead | **SQL expression** mapping countries to APJ, AMER, EMEA |
# MAGIC
# MAGIC Descriptions explain **what the data means**. 
# MAGIC
# MAGIC SQL logic and instructions teach Genie **how to query it** and **what business terms mean**.
# MAGIC
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Knowledge Mining Overview
# MAGIC
# MAGIC Knowledge mining helps improve Genie by automatically suggesting updates to the knowledge store, reducing manual curation and improving answer accuracy.
# MAGIC
# MAGIC 1. Navigate to your **Benchmarks**.
# MAGIC
# MAGIC 2. Select the **Evaluations** tab.
# MAGIC
# MAGIC 3. Select your latest evaluation where you tested all of **six** of your benchmarks.
# MAGIC
# MAGIC 4. Select the **What Are Total Sales by Region?** benchmark (It should most likely have failed so far).
# MAGIC
# MAGIC 5. Select the **Review proposed fixes**.
# MAGIC
# MAGIC <img src="https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/sql-logic-instructions/knowledge-mining.png" width="1300">
# MAGIC
# MAGIC 6. You should see a pop up with **Review knowledge snippets**
# MAGIC     - **New Suggestions** - Suggestions for the specific question.
# MAGIC     - **More Suggestions** - Additional suggestions found for **Genie**.
# MAGIC
# MAGIC 7. (This might vary) Under **New Suggestions** see if there is a **SQL Expressions** suggestions for **FIELD** `region`. If there is, review the:
# MAGIC     - **SQL Expression**
# MAGIC     - **Instructions**
# MAGIC
# MAGIC 8. Select **Cancel**.
# MAGIC
# MAGIC #### For the purpose of the training we will manually add some of the suggestions found in the **Review knowledge snippets**. 
# MAGIC
# MAGIC #### However, once you understand **Joins**, **SQL Expressions** and **SQL Queries** using the suggested snippets is extremely beneficial.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     How Knowledge Mining Works
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC That “Review knowledge snippets” pop-up in the Benchmarks flow is one of the knowledge mining / extraction entry points in Genie.
# MAGIC
# MAGIC Behind the scenes, Genie is analyzing failed or reviewed benchmark runs and proposing knowledge snippets (measures, filters, joins, etc.) as recommendations to add to the knowledge store that recommendation surface is exactly what we call knowledge mining in the docs and GA blog. 
# MAGIC
# MAGIC
# MAGIC - Visit the Knowledge mining recommendations documentation for more information:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/knowledge-store#knowledge-mining-recommendations) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/tune-quality#knowledge-mining-recommendations) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/knowledge-store#knowledge-mining-recommendations)
# MAGIC
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Add a SQL Expression to the Knowledge Store
# MAGIC
# MAGIC SQL expressions let you define **derived columns**. 
# MAGIC
# MAGIC That is, values that do not exist in the data but can be computed from existing columns. 
# MAGIC
# MAGIC Genie can use these expressions in generated SQL.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### D1. Add a Region SQL Expression to the Knowledge Store
# MAGIC
# MAGIC Our business groups franchise countries into three specific regions:
# MAGIC   - **APJ**
# MAGIC   - **EMEA**
# MAGIC   - **AMER**
# MAGIC
# MAGIC This mapping does not exist as a column, we need to teach it to Genie as a SQL expression.
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Benchmark This Fixes
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC **Benchmark #5: What are total sales by region?** - Genie most likely groups by `country` because there is no `region` column. This expression creates the mapping.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC 1. In your Genie Agent, select **Configure** > **Examples** > **Add**.
# MAGIC
# MAGIC 2. Select **+ Add** > **Field**.
# MAGIC
# MAGIC 3. **Name the Field:** `region`
# MAGIC
# MAGIC 4. Run the cell below to generate your specific **SQL Expression** (adds your unique catalog name in the expression for you).
# MAGIC     - **NOTES:** 
# MAGIC         - When referencing the column in the expression, we are using a three level-namespace + the column name
# MAGIC         - `YOUR_CATALOG.genie_course_bakehouse.sales_franchises_gold.country`

# COMMAND ----------

# MAGIC %sql
# MAGIC DECLARE OR REPLACE my_query STRING DEFAULT "";
# MAGIC
# MAGIC SET VAR my_query = "
# MAGIC CASE
# MAGIC     WHEN " || my_catalog || ".genie_course_bakehouse.sales_franchises_gold.country IN ('Japan', 'Australia') 
# MAGIC       THEN 'APJ'
# MAGIC     WHEN " || my_catalog || ".genie_course_bakehouse.sales_franchises_gold.country IN ('US', 'Canada') 
# MAGIC       THEN 'AMER'
# MAGIC     WHEN " || my_catalog || ".genie_course_bakehouse.sales_franchises_gold.country IN ('Netherlands', 'France', 'Germany', 'Italy', 'Sweden')
# MAGIC       THEN 'EMEA' 
# MAGIC     ELSE 'Other'
# MAGIC END
# MAGIC ";
# MAGIC
# MAGIC SELECT my_query;

# COMMAND ----------

# MAGIC %md
# MAGIC 5. Copy the output above and paste into the **Code** field and review the query.
# MAGIC
# MAGIC 6. Add the following:
# MAGIC     - **Synonyms**: `franchise region, region sales`
# MAGIC     - **Instructions**: `When user asks for metrics by 'region' where region is defined by business mapping of country to APJ, AMER, EMEA, or Other; SCOPE_TABLES: Use with sales_franchises_gold and sales_transactions_gold, grouping or reporting at the franchise-location level; RISK_IF_MISUSED: Do not use unless the user explicitly refers to regions per this mapping (e.g., could mislead if a different regional breakdown is implied). This is a company-specific mapping.`
# MAGIC
# MAGIC 7. Select **Save**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Add an Example SQL Query
# MAGIC
# MAGIC Example SQL queries teach Genie **query patterns** that it is unlikely to generate on its own. 
# MAGIC
# MAGIC Genie uses these as trusted templates when similar questions are asked.
# MAGIC
# MAGIC **Add example SQL queries and functions** - [AWS](https://docs.databricks.com/aws/en/genie-agents/tune-quality#-add-example-sql-queries-and-functions) |
# MAGIC  [Azure](https://learn.microsoft.com/en-us/azure/databricks/genie-agents/tune-quality#-add-example-sql-queries-and-functions) | 
# MAGIC  [GCP](https://docs.databricks.com/gcp/en/genie-agents/tune-quality#-add-example-sql-queries-and-functions)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ### E1. Add Example Query: Who are our best customers?
# MAGIC
# MAGIC Teach Genie what query to use when you get the best customers question.
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Benchmark This Fixes (and other additional context is added)
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC **Benchmark #3: Who are our best customers?** — Genie currently guesses what "best" means, adds extra columns, and does not limit results. This instruction locks in the definition.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC 1. In your Genie Agent, select **Configure** > **Examples**.
# MAGIC
# MAGIC 2. Select **+ Add** > **Example query**.
# MAGIC
# MAGIC 3. Enter the question: `Who are our best customers?`
# MAGIC
# MAGIC 4. Run the cell below to generate the query with your catalog name, then paste it as the SQL query.

# COMMAND ----------

# MAGIC %sql
# MAGIC DECLARE OR REPLACE my_query STRING DEFAULT "";
# MAGIC
# MAGIC SET VAR my_query = "
# MAGIC
# MAGIC SELECT
# MAGIC   c.customerID,
# MAGIC   c.first_name,
# MAGIC   c.last_name,
# MAGIC   SUM(t.totalPrice) AS total_spend
# MAGIC FROM
# MAGIC   " || my_catalog || ".genie_course_bakehouse.sales_transactions_gold AS t
# MAGIC     JOIN " || my_catalog || ".genie_course_bakehouse.sales_customers_gold AS c
# MAGIC       ON t.customerID = c.customerID
# MAGIC GROUP BY
# MAGIC   c.customerID,
# MAGIC   c.first_name,
# MAGIC   c.last_name
# MAGIC ORDER BY
# MAGIC   total_spend DESC
# MAGIC LIMIT 10
# MAGIC ";
# MAGIC
# MAGIC SELECT my_query;

# COMMAND ----------

# MAGIC %md
# MAGIC 5. Expand **Usage Guidance**.
# MAGIC
# MAGIC 6. Add the following: ```When users ask for the best customers make sure you aggregate by total price and return the top 10 customers.```
# MAGIC
# MAGIC 7. Select **Preview** to view the results.
# MAGIC
# MAGIC 8. Then **Save**.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### E2. Add Example Query: Franchises per Supplier (LEFT JOIN Pattern)
# MAGIC
# MAGIC This teaches Genie the `LEFT JOIN + COALESCE` pattern needed to include franchises that do not have a matching supplier.
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Benchmark This Fixes
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC **Benchmark #4: How many franchises does each supplier serve?** - Genie currently uses an INNER JOIN, silently dropping 21 of 48 franchises. This example teaches the correct LEFT JOIN pattern.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC 1. In your Genie Agent, select **Configure** > **Examples**.
# MAGIC
# MAGIC 2. Select **Add** > **Example query**.
# MAGIC
# MAGIC 3. Enter the question: `How many franchises does each supplier serve?`
# MAGIC
# MAGIC 4. Run the cell below to generate the query with your catalog name, then paste it as the SQL answer.

# COMMAND ----------

# MAGIC %sql
# MAGIC DECLARE OR REPLACE my_query STRING DEFAULT "";
# MAGIC
# MAGIC SET VAR my_query = "
# MAGIC SELECT
# MAGIC     COALESCE(s.name, 'No Matching Supplier') AS supplier_name,
# MAGIC     COUNT(f.franchiseID) AS franchise_count
# MAGIC FROM " || my_catalog || ".genie_course_bakehouse.sales_franchises_gold AS f
# MAGIC LEFT JOIN " || my_catalog || ".genie_course_bakehouse.sales_suppliers_gold AS s
# MAGIC     ON f.supplierID = s.supplierID
# MAGIC GROUP BY
# MAGIC     s.name
# MAGIC ORDER BY
# MAGIC     franchise_count DESC
# MAGIC ";
# MAGIC
# MAGIC SELECT my_query;

# COMMAND ----------

# MAGIC %md
# MAGIC 5. Copy the output above and paste into the **SQL query** field.
# MAGIC
# MAGIC 6. Select **Preview** and review the results. They should look like this:
# MAGIC
# MAGIC | supplier_name         | franchise_count |
# MAGIC |----------------------|-----------------|
# MAGIC | No Matching Supplier | 21              |
# MAGIC | Nutmeg Nirvana       | 1               |
# MAGIC | Honey Hives          | 1               |
# MAGIC | Cardamom Cove        | 1               |
# MAGIC | Pistachio Palace     | 1               |
# MAGIC
# MAGIC 7. Select **Save**

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Example SQL Queries in Genie
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Example SQL queries help Genie understand how to answer your users' questions correctly.
# MAGIC
# MAGIC - Add queries that match real business questions your users ask  
# MAGIC - Use clear, natural language for the title, this helps Genie match prompts  
# MAGIC - Write clean, production-quality SQL  
# MAGIC
# MAGIC Genie uses these in two ways:
# MAGIC - It can **use the query directly**
# MAGIC - Or **learn from it** to generate similar queries  
# MAGIC
# MAGIC #### Note on Parameterized Queries
# MAGIC - Genie also supports parameterized queries for dynamic inputs  
# MAGIC - These can produce **Trusted** responses when used directly  
# MAGIC - We are not covering parameterized queries in this training  
# MAGIC
# MAGIC If you're interested, see the documentation use parameters in SQL queries in Genie:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/add-instructions#add-query-parameters) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/tune-quality#add-query-parameters) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/add-instructions#add-query-parameters)
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### Key Idea
# MAGIC Think of example queries as **teaching Genie patterns**, not just answers  
# MAGIC
# MAGIC - For more information check out the documentation:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie-agents/tune-quality#build-a-knowledge-store) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/tune-quality#build-a-knowledge-store) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie-agents/tune-quality#build-a-knowledge-store)
# MAGIC
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## F. Add a SQL Join
# MAGIC
# MAGIC Let's view the SQL joins in the knowledge store and add one.
# MAGIC
# MAGIC 1. Select **Examples > Add**
# MAGIC
# MAGIC 2. Select **Join** 
# MAGIC
# MAGIC 3. Add a join:
# MAGIC     - Left Table: **sales_franchises_gold**
# MAGIC     - Right Table: **sales_suppliers_gold**.
# MAGIC     - Join Condition: **SupplierID** on both.
# MAGIC     - Relationship Type: **Many to One**
# MAGIC
# MAGIC 4. Add the following to the **Instructions**: `Many franchiseID values in the sales_franchises_gold table do not have a match in the sales_suppliers_gold table. This is important information and make sure to display the orphaned rows.`
# MAGIC
# MAGIC 6. Select **Save**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## G. Add Text Instructions
# MAGIC
# MAGIC Text instructions define **business terms** and **default behaviors** that cannot be expressed in SQL or metadata. 
# MAGIC
# MAGIC Use them only for what SQL and descriptions cannot handle.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### G1. Add General Instructions

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC 1. In your Genie Agent, select **Configure** > **Instructions**.
# MAGIC
# MAGIC 2. Add the following instructions:
# MAGIC
# MAGIC
# MAGIC <button onclick="copyBlock()">Copy to clipboard</button>
# MAGIC
# MAGIC <pre id="copy-block" style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; border:1px solid #e5e7eb; border-radius:10px; background:#f8fafc; padding:14px 16px; font-size:0.85rem; line-height:1.35; white-space:pre;">
# MAGIC <code>
# MAGIC <!-------------------ADD SOLUTION CODE BELOW------------------->
# MAGIC - Formatting
# MAGIC     - Format all results using US dollars  
# MAGIC     - Round all currency values to 2 decimal places.
# MAGIC
# MAGIC - Business Rules
# MAGIC     - `totalPrice` represents both revenue and sales volume  
# MAGIC     - Always include franchise name with franchise ID  
# MAGIC     - Use `totalPrice` for total sales and performance comparisons  
# MAGIC
# MAGIC - Fiscal Calendar
# MAGIC     - Fiscal year starts in February  
# MAGIC     - Q1: February, March, April  
# MAGIC     - Q2: May, June, July  
# MAGIC     - Q3: August, September, October  
# MAGIC     - Q4: November, December, January  
# MAGIC
# MAGIC <!-------------------END SOLUTION CODE------------------->
# MAGIC </code></pre>
# MAGIC
# MAGIC <script>
# MAGIC function copyBlock() {
# MAGIC   const el = document.getElementById("copy-block");
# MAGIC   if (!el) return;
# MAGIC
# MAGIC   const text = el.innerText;
# MAGIC
# MAGIC   // Preferred modern API
# MAGIC   if (navigator.clipboard && navigator.clipboard.writeText) {
# MAGIC     navigator.clipboard.writeText(text)
# MAGIC       .then(() => alert("Copied to clipboard"))
# MAGIC       .catch(err => {
# MAGIC         console.error("Clipboard write failed:", err);
# MAGIC         fallbackCopy(text);
# MAGIC       });
# MAGIC   } else {
# MAGIC     fallbackCopy(text);
# MAGIC   }
# MAGIC }
# MAGIC
# MAGIC function fallbackCopy(text) {
# MAGIC   const textarea = document.createElement("textarea");
# MAGIC   textarea.value = text;
# MAGIC   textarea.style.position = "fixed";
# MAGIC   textarea.style.left = "-9999px";
# MAGIC   document.body.appendChild(textarea);
# MAGIC   textarea.select();
# MAGIC   try {
# MAGIC     document.execCommand("copy");
# MAGIC     alert("Copied to clipboard");
# MAGIC   } catch (err) {
# MAGIC     console.error("Fallback copy failed:", err);
# MAGIC     alert("Could not copy to clipboard. Please copy manually.");
# MAGIC   } finally {
# MAGIC     document.body.removeChild(textarea);
# MAGIC   }
# MAGIC }
# MAGIC </script>
# MAGIC
# MAGIC
# MAGIC 3. Select **Save**.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Best Practice
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Keep text instructions **short and specific**. Avoid duplicating what is already defined in SQL expressions, column descriptions, or example queries. Instructions are for behavior and edge cases only.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## H. Run Benchmarks
# MAGIC
# MAGIC Now that you have added SQL expressions, example queries, and text instructions, re-run your benchmarks to measure the impact.
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Why Re-Run Benchmarks Now?
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Each time you make a change to your Genie Agent, you should re-run benchmarks to confirm:
# MAGIC - Did the change **fix** the questions it was intended to fix?
# MAGIC - Did the change **break** anything that was already working?
# MAGIC
# MAGIC This is the **test, benchmark, and iterate** step from the authoring checklist.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### H1. Run All Benchmarks (Chat Mode)
# MAGIC
# MAGIC 1. In your Genie Agent, select **Benchmarks** > **Run all benchmarks**.
# MAGIC
# MAGIC 2. As each benchmark completes, review the results!

# COMMAND ----------

# MAGIC %md
# MAGIC ### H2. Review Results
# MAGIC
# MAGIC Compare your results against what you expect after adding SQL logic and instructions. 
# MAGIC
# MAGIC The goal is that all all benchmarks should pass.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## I. What SQL Logic and Instructions Solved
# MAGIC
# MAGIC <style>
# MAGIC table td, table th {
# MAGIC   font-size: 14pt !important;
# MAGIC }
# MAGIC </style>
# MAGIC
# MAGIC <table style="width: 100%; border-collapse: collapse; line-height: 1.5;">
# MAGIC   <thead>
# MAGIC     <tr style="background: #1B5162; color: white;">
# MAGIC       <th style="padding: 12px 10px; text-align: center; width: 40px; border: 1px solid #EEEDE9;">#</th>
# MAGIC       <th style="padding: 12px 14px; text-align: left; border: 1px solid #EEEDE9;">Benchmark Question</th>
# MAGIC       <th style="padding: 12px 14px; text-align: left; border: 1px solid #EEEDE9;">What We Added</th>
# MAGIC       <th style="padding: 12px 14px; text-align: left; border: 1px solid #EEEDE9;">Expected Result</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background: #E8F7EF;">
# MAGIC       <td style="padding: 12px 10px; text-align: center; border: 1px solid #EEEDE9;">1</td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><em>How many customers do we have?</em></td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;">Simple, should have passed</td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><strong>Should pass</strong> — simple COUNT(*)</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #E8F7EF;">
# MAGIC       <td style="padding: 12px 10px; text-align: center; border: 1px solid #EEEDE9;">2</td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><em>What are the top 5 franchise locations by total revenue?</em></td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;">Should have already passed with metadata alone</td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><strong>Should pass</strong> — no regression expected</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #E8F7EF;">
# MAGIC       <td style="padding: 12px 10px; text-align: center; border: 1px solid #EEEDE9;">3</td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><em>Who are our best customers?</em></td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><strong>SQL Query</strong></td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><strong>Should improve</strong> — may now use SUM(totalPrice) + LIMIT 10</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #E8F7EF;">
# MAGIC       <td style="padding: 12px 10px; text-align: center; border: 1px solid #EEEDE9;">4</td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><em>How many franchises does each supplier serve?</em></td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><strong>SQL Query + Join</strong></td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><strong>Should improve</strong> — Genie has a trusted pattern to follow</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #E8F7EF;">
# MAGIC       <td style="padding: 12px 10px; text-align: center; border: 1px solid #EEEDE9;">5</td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><em>What are total sales by region?</em></td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><strong>SQL expression mapping countries to APJ / AMER / EMEA</strong></td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><strong>Should improve</strong> — Genie now knows the region mapping</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #E8F7EF;">
# MAGIC       <td style="padding: 12px 10px; text-align: center; border: 1px solid #EEEDE9;">6</td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><em>Count of bad reviews by location?</em></td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;">Metadata should have improved this</td>
# MAGIC       <td style="padding: 12px 14px; border: 1px solid #EEEDE9;"><strong>Should pass</strong> — no regression expected</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 1300px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 14px;">General Steps</div>
# MAGIC
# MAGIC <div style="display: flex; gap: 16px;">
# MAGIC
# MAGIC   <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px 20px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC     <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #00A972; border-radius: 8px 8px 0 0;"></div>
# MAGIC     <div style="display: flex; align-items: center; gap: 12px; margin-top: 4px;">
# MAGIC       <div style="width: 36px; height: 36px; border-radius: 50%; background: #00A972; color: white; font-size: 16pt; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">1</div>
# MAGIC       <div>
# MAGIC         <div style="font-size: 16pt; font-weight: 700; color: #0b2026;">Metadata</div>
# MAGIC         <div style="font-size: 14pt; color: #5A6F77; margin-top: 2px;">Easiest to add, highest immediate impact</div>
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px 20px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC     <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #4299E0; border-radius: 8px 8px 0 0;"></div>
# MAGIC     <div style="display: flex; align-items: center; gap: 12px; margin-top: 4px;">
# MAGIC       <div style="width: 36px; height: 36px; border-radius: 50%; background: #4299E0; color: white; font-size: 16pt; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">2</div>
# MAGIC       <div>
# MAGIC         <div style="font-size: 16pt; font-weight: 700; color: #0b2026;">SQL Logic</div>
# MAGIC         <div style="font-size: 14pt; color: #5A6F77; margin-top: 2px;">Most precise: <strong>Joins, SQL Expressions, SQL Queries</strong></div>
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px 20px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC     <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #FFAB00; border-radius: 8px 8px 0 0;"></div>
# MAGIC     <div style="display: flex; align-items: center; gap: 12px; margin-top: 4px;">
# MAGIC       <div style="width: 36px; height: 36px; border-radius: 50%; background: #FFAB00; color: white; font-size: 16pt; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">3</div>
# MAGIC       <div>
# MAGIC         <div style="font-size: 16pt; font-weight: 700; color: #0b2026;">Instructions</div>
# MAGIC         <div style="font-size: 14pt; color: #5A6F77; margin-top: 2px;">Last resort for what SQL cannot express</div>
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Results May Still Vary
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Even with SQL logic and instructions, Genie may not match the ground truth SQL exactly. It may add extra columns, use slightly different syntax, or interpret the instruction differently.
# MAGIC
# MAGIC The goal is **directional improvement**. 
# MAGIC
# MAGIC Are the results closer to what you expect? Over time, you refine further by adding more examples, adjusting instructions, and reviewing user feedback through Monitoring.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## J. What We Did Not Cover
# MAGIC
# MAGIC This course focused on the core Knowledge Store curation tools: descriptions, synonyms, prompt matching, SQL expressions, example queries, text instructions, and benchmarks.
# MAGIC
# MAGIC These cover most of what you need to build an effective Genie Agent, but there are additional capabilities worth exploring.
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 1200px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
# MAGIC
# MAGIC <!-- Trusted Assets -->
# MAGIC <div style="flex: 1; min-width: 320px; max-width: 380px; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #02A36F; border-radius: 8px 8px 0 0;"></div>
# MAGIC
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 8px; margin-top: 6px;">Trusted Assets</div>
# MAGIC
# MAGIC   <div style="font-weight: 600; font-size: 14pt; margin-bottom: 4px;">What it is</div>
# MAGIC   <ul style="padding-left: 18px; margin: 0 0 8px 0; font-size: 14pt; color: #333; line-height: 1.5;">
# MAGIC     <li>SQL functions registered in Unity Catalog</li>
# MAGIC     <li>Genie calls them directly to answer questions</li>
# MAGIC     <li>Responses labeled <strong>"Trusted"</strong></li>
# MAGIC   </ul>
# MAGIC
# MAGIC   <div style="font-weight: 600; font-size: 14pt; margin-bottom: 4px;">Why it matters</div>
# MAGIC   <ul style="padding-left: 18px; margin: 0; font-size: 14pt; color: #555; line-height: 1.4;">
# MAGIC     <li>Guaranteed, repeatable answers</li>
# MAGIC     <li>Ideal for KPIs, compliance, executive reporting</li>
# MAGIC   </ul>
# MAGIC
# MAGIC   <div style="margin-top: 12px; background: rgba(2,163,111,0.10); border-left: 4px solid #02A36F; padding: 8px 10px; border-radius: 6px; font-size: 14pt;">
# MAGIC     <strong>Documentation:</strong> <a href="https://docs.databricks.com/aws/en/genie/add-instructions#trusted-assets" target="_blank">AWS</a> | <a href="https://learn.microsoft.com/en-us/azure/databricks/genie-agents/tune-quality#trusted-assets" target="_blank">Azure</a> | <a href="https://docs.databricks.com/gcp/en/genie/add-instructions#trusted-assets" target="_blank">GCP</a>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC
# MAGIC <!-- Parameterized Queries -->
# MAGIC <div style="flex: 1; min-width: 320px; max-width: 380px; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #2574B5; border-radius: 8px 8px 0 0;"></div>
# MAGIC
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 8px; margin-top: 6px;">Parameterized Queries</div>
# MAGIC
# MAGIC   <div style="font-weight: 600; font-size: 14pt; margin-bottom: 4px;">What it is</div>
# MAGIC   <ul style="padding-left: 18px; margin: 0 0 8px 0; font-size: 14pt; color: #333; line-height: 1.5;">
# MAGIC     <li>Queries with named parameters like <code>:limit</code>, <code>:country</code></li>
# MAGIC     <li>One query supports many variations</li>
# MAGIC     <li>Examples: top 3, top 10, top in Japan</li>
# MAGIC   </ul>
# MAGIC
# MAGIC   <div style="font-weight: 600; font-size: 14pt; margin-bottom: 4px;">Why it matters</div>
# MAGIC   <ul style="padding-left: 18px; margin: 0; font-size: 14pt; color: #555; line-height: 1.4;">
# MAGIC     <li>Reduces number of example queries needed</li>
# MAGIC     <li>Still produces <strong>"Trusted"</strong> responses when used directly</li>
# MAGIC   </ul>
# MAGIC
# MAGIC   <div style="margin-top: 12px; background: rgba(37,116,181,0.10); border-left: 4px solid #2574B5; padding: 8px 10px; border-radius: 6px; font-size: 14pt;">
# MAGIC     <strong>Documentation:</strong> <a href="https://docs.databricks.com/aws/en/genie/add-instructions#add-query-parameters" target="_blank">AWS</a> | <a href="https://learn.microsoft.com/en-us/azure/databricks/genie-agents/tune-quality#add-query-parameters" target="_blank">Azure</a> | <a href="https://docs.databricks.com/gcp/en/genie/add-instructions#add-query-parameters" target="_blank">GCP</a>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Metric Views -->
# MAGIC <div style="flex: 1; min-width: 320px; max-width: 380px; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #F8A805; border-radius: 8px 8px 0 0;"></div>
# MAGIC
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 8px; margin-top: 6px;">Metric Views</div>
# MAGIC
# MAGIC   <div style="font-weight: 600; font-size: 14pt; margin-bottom: 4px;">What it is</div>
# MAGIC   <ul style="padding-left: 18px; margin: 0 0 8px 0; font-size: 14pt; color: #333; line-height: 1.5;">
# MAGIC     <li>Code-managed semantic layer in Unity Catalog</li>
# MAGIC     <li>Defined using YAML</li>
# MAGIC     <li>Includes metrics, dimensions, synonyms, formatting</li>
# MAGIC   </ul>
# MAGIC
# MAGIC   <div style="font-weight: 600; font-size: 14pt; margin-bottom: 4px;">Why it matters</div>
# MAGIC   <ul style="padding-left: 18px; margin: 0; font-size: 14pt; color: #555; line-height: 1.4;">
# MAGIC     <li>Shared across Genie and AI/BI dashboards</li>
# MAGIC     <li>Ensures consistent metric definitions</li>
# MAGIC   </ul>
# MAGIC
# MAGIC   <div style="margin-top: 12px; background: rgba(248,168,5,0.15); border-left: 4px solid #F8A805; padding: 8px 10px; border-radius: 6px; font-size: 14pt;">
# MAGIC     <strong>Documentation:</strong> <a href="https://docs.databricks.com/aws/en/metric-views/" target="_blank">AWS</a> | <a href="https://learn.microsoft.com/en-us/azure/databricks/metric-views/" target="_blank">Azure</a> | <a href="https://docs.databricks.com/gcp/en/metric-views/" target="_blank">GCP</a>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## K. Conclusion
# MAGIC
# MAGIC In this demo, you:
# MAGIC
# MAGIC 1. Added a **SQL expression** to define business regions (APJ, AMER, EMEA) from franchise country data.
# MAGIC 2. Added an **example SQL query** to teach Genie the LEFT JOIN + COALESCE pattern for franchise-supplier relationships.
# MAGIC 3. Added **text instructions** to define "best customer" as highest total spend (top 10), standardize COUNT(*) behavior, and enforce LEFT JOIN usage for suppliers.
# MAGIC 4. Re-ran benchmarks and observed improvement across previously failing questions.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
