-- Databricks notebook source
-- MAGIC %md
-- MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC # Demo - Adding Genie Benchmarks
-- MAGIC
-- MAGIC ## Overview
-- MAGIC
-- MAGIC In the previous demo, you created a Genie Agent, explored the UI, asked your first question, and saved it as a benchmark. 
-- MAGIC
-- MAGIC In this demo, you will add **additional benchmarks** to build a complete test suite for Genie as you continue to build.
-- MAGIC
-- MAGIC These benchmarks define what "correct" looks like for your space. Each one targets a specific challenge like multi-table joins, ambiguous business terms, data quality issues, and business-defined groupings. 
-- MAGIC
-- MAGIC Our goal throughout this course is to improve the Genie Agent in later demos and re-run these benchmarks to measure progress as we add context.
-- MAGIC
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this demo, you will be able to:
-- MAGIC
-- MAGIC 1. **Add benchmarks with ground truth SQL** to a Genie Agent.
-- MAGIC 2. **Run all benchmarks** and interpret the results.
-- MAGIC 3. **Establish a baseline accuracy** for an unconfigured Genie Agent.
-- MAGIC 4. **Identify which questions Genie struggles with** and why before any metadata or instructions have been added.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #f44336;
-- MAGIC   background: #ffebee;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Prerequisites</strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Complete the **previous demonstrations** before proceeding. This demo builds on the Genie created in the previous demonstration.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## REQUIRED - SELECT A COMPUTE ENVIRONMENT
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #f44336;
-- MAGIC   background: #ffebee;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Select a Serverless SQL Warehouse</strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Before starting this notebook, select the required compute environment listed below.
-- MAGIC
-- MAGIC - **Serverless SQL Warehouse (2X-Small is sufficient)**
-- MAGIC   - Select **Compute** > **More** > **SQL Warehouse** > Select a SQL Warehouse you have access to.
-- MAGIC
-- MAGIC **NOTE:** This notebook was **developed and tested using Serverless SQL Warehouse**. Other compute options may work but are not guaranteed to behave the same or support all features demonstrated.
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## A. Classroom Setup
-- MAGIC
-- MAGIC 1. Run the cell below to set your default catalog and schema.
-- MAGIC     - This assumes you have already run the setup from a prior demo and your tables exist in **labuser_YOUR_USER_NAME.genie_course_bakehouse**.

-- COMMAND ----------

-- MAGIC %run ./Includes/Classroom-Setup-adding-benchmarks

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Add Additional Benchmarks
-- MAGIC
-- MAGIC We added our first benchmark in the previous demonstration by asking Genie a question and saving the response.
-- MAGIC
-- MAGIC As a Genie curator, think of benchmarks as part of your **workflow**. Run them regularly as you refine your space to track progress and catch regressions early.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
-- MAGIC
-- MAGIC <style scoped>
-- MAGIC .bench-header {
-- MAGIC   background: #1B5162;
-- MAGIC   color: white;
-- MAGIC   border-radius: 10px 10px 4px 4px;
-- MAGIC   padding: 22px 28px;
-- MAGIC   display: flex;
-- MAGIC   align-items: center;
-- MAGIC   gap: 20px;
-- MAGIC   margin-bottom: 14px;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-header img {
-- MAGIC   height: 56px;
-- MAGIC   width: auto;
-- MAGIC   flex-shrink: 0;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-header-title {
-- MAGIC   font-size: 22pt;
-- MAGIC   font-weight: 700;
-- MAGIC   line-height: 1.2;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-header-sub {
-- MAGIC   font-size: 15pt;
-- MAGIC   opacity: 0.88;
-- MAGIC   margin-top: 4px;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-row {
-- MAGIC   display: flex;
-- MAGIC   gap: 14px;
-- MAGIC   margin-bottom: 14px;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-card {
-- MAGIC   flex: 1;
-- MAGIC   background: #F9F7F4;
-- MAGIC   border-radius: 8px;
-- MAGIC   padding: 20px 22px;
-- MAGIC   position: relative;
-- MAGIC   box-shadow: 0 2px 8px rgba(27,49,57,0.06);
-- MAGIC   box-sizing: border-box;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-card::before {
-- MAGIC   content: "";
-- MAGIC   position: absolute;
-- MAGIC   top: 0;
-- MAGIC   left: 0;
-- MAGIC   width: 100%;
-- MAGIC   height: 6px;
-- MAGIC   border-radius: 8px 8px 0 0;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-card.blue::before { background: #4299E0; }
-- MAGIC .bench-card.green::before { background: #00A972; }
-- MAGIC .bench-card.amber::before { background: #FFAB00; }
-- MAGIC
-- MAGIC .bench-card-title {
-- MAGIC   font-size: 16pt;
-- MAGIC   font-weight: 700;
-- MAGIC   color: #0b2026;
-- MAGIC   margin-bottom: 12px;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-card ul {
-- MAGIC   margin: 0;
-- MAGIC   padding-left: 20px;
-- MAGIC   font-size: 14pt;
-- MAGIC   color: #5A6F77;
-- MAGIC   line-height: 1.6;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-card li {
-- MAGIC   margin-bottom: 10px;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-card li:last-child {
-- MAGIC   margin-bottom: 0;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-ratings {
-- MAGIC   background: #F9F7F4;
-- MAGIC   border-radius: 8px;
-- MAGIC   padding: 18px 22px;
-- MAGIC   box-shadow: 0 2px 8px rgba(27,49,57,0.06);
-- MAGIC   margin-bottom: 14px;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-ratings-title {
-- MAGIC   font-size: 15pt;
-- MAGIC   font-weight: 700;
-- MAGIC   color: #0b2026;
-- MAGIC   margin-bottom: 12px;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-ratings-row {
-- MAGIC   display: flex;
-- MAGIC   gap: 12px;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-rating-pill {
-- MAGIC   flex: 1;
-- MAGIC   border-radius: 6px;
-- MAGIC   padding: 12px 16px;
-- MAGIC   font-size: 14pt;
-- MAGIC   line-height: 1.5;
-- MAGIC   color: #0b2026;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-rating-pill.good {
-- MAGIC   background: rgba(0,169,114,0.10);
-- MAGIC   border-left: 4px solid #00A972;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-rating-pill.bad {
-- MAGIC   background: rgba(152,16,42,0.08);
-- MAGIC   border-left: 4px solid #98102A;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-rating-pill.manual {
-- MAGIC   background: rgba(255,171,0,0.10);
-- MAGIC   border-left: 4px solid #FFAB00;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-rating-label {
-- MAGIC   font-weight: 700;
-- MAGIC   display: block;
-- MAGIC   margin-bottom: 4px;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-note {
-- MAGIC   background: #F8F9FC;
-- MAGIC   border-left: 4px solid #1B5162;
-- MAGIC   border-radius: 6px;
-- MAGIC   padding: 12px 18px;
-- MAGIC   font-size: 14pt;
-- MAGIC   color: #5A6F77;
-- MAGIC   margin-bottom: 14px;
-- MAGIC   line-height: 1.5;
-- MAGIC }
-- MAGIC
-- MAGIC .bench-link {
-- MAGIC   display: block;
-- MAGIC   margin-top: 12px;
-- MAGIC   font-size: 14pt;
-- MAGIC   color: #4299E0;
-- MAGIC }
-- MAGIC </style>
-- MAGIC
-- MAGIC <!-- Header -->
-- MAGIC <div class="bench-header">
-- MAGIC   <div>
-- MAGIC     <div class="bench-header-title">Benchmarks Overview</div>
-- MAGIC     <div class="bench-header-sub">A set of test questions to assess Genie's overall response accuracy. Up to 500 per space.<br></br>
-- MAGIC     Think of benchmarks as your <strong>acceptance criteria</strong>. They define what <strong>good</strong> looks like for your Genie Agent. As you iterate, re-run them to measure whether your changes actually improved accuracy.
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- Row 1: What a benchmark contains -->
-- MAGIC <div class="bench-row">
-- MAGIC   <div class="bench-card blue" style="flex: 1;">
-- MAGIC     <div class="bench-card-title">Each Benchmark Contains</div>
-- MAGIC     <ul>
-- MAGIC       <li>A <strong>natural language question</strong> - phrased the way a real user would ask it</li>
-- MAGIC       <li>An optional <strong>SQL Answer</strong> - the correct result used for automated accuracy scoring</li>
-- MAGIC       <li style="background: rgba(66,153,224,0.12); border-radius: 6px; padding: 8px 10px; list-style: none; margin-left: -20px; padding-left: 30px;">Questions run as <strong>new conversations</strong> and no thread context is carried over</li>
-- MAGIC     </ul>
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- Row 2: Two purposes -->
-- MAGIC <div class="bench-row">
-- MAGIC   <div class="bench-card green">
-- MAGIC     <div class="bench-card-title">Assess Accuracy</div>
-- MAGIC     <ul>
-- MAGIC       <li>Run benchmarks to evaluate Genie's response accuracy across your question set</li>
-- MAGIC       <li>Include <strong>2–4 phrasings</strong> of the same question to test variation in how users ask it</li>
-- MAGIC       <li>Only questions with a <strong>SQL Answer</strong> can be auto-scored. Others will require manual review</li>
-- MAGIC     </ul>
-- MAGIC   </div>
-- MAGIC   <div class="bench-card amber">
-- MAGIC     <div class="bench-card-title">Evaluate as You Refine</div>
-- MAGIC     <ul>
-- MAGIC       <li>Run benchmarks regularly as you add instructions, metadata, and example SQL</li>
-- MAGIC       <li>Re-run a <strong>subset of questions</strong> from a previous result to test specific improvements</li>
-- MAGIC       <li>Track accuracy over time using the timestamped <strong>Evaluations tab</strong></li>
-- MAGIC     </ul>
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- Ratings -->
-- MAGIC <div class="bench-ratings">
-- MAGIC   <div class="bench-ratings-title">How Responses Are Rated</div>
-- MAGIC   <div class="bench-ratings-row">
-- MAGIC     <div class="bench-rating-pill good">
-- MAGIC       <span class="bench-rating-label" style="color: #00A972;">Good</span>
-- MAGIC       <ul style="margin: 0; padding-left: 18px; font-size: 14pt; color: #0b2026; line-height: 1.6;">
-- MAGIC         <li style="margin-bottom: 8px;">SQL exactly matches ground truth</li>
-- MAGIC         <li style="margin-bottom: 8px;">Result sets match exactly</li>
-- MAGIC         <li style="margin-bottom: 8px;">Results match, different sort order</li>
-- MAGIC         <li>Numeric values round to same 4 significant digits</li>
-- MAGIC       </ul>
-- MAGIC     </div>
-- MAGIC     <div class="bench-rating-pill bad">
-- MAGIC       <span class="bench-rating-label" style="color: #98102A;">Bad</span>
-- MAGIC       <ul style="margin: 0; padding-left: 18px; font-size: 14pt; color: #0b2026; line-height: 1.6;">
-- MAGIC         <li style="margin-bottom: 8px;">Empty result set or error</li>
-- MAGIC         <li style="margin-bottom: 8px;">Extra columns returned</li>
-- MAGIC         <li>Single-cell result differs from ground truth</li>
-- MAGIC       </ul>
-- MAGIC     </div>
-- MAGIC     <div class="bench-rating-pill manual">
-- MAGIC       <span class="bench-rating-label" style="color: #b07d00;">Manual Review</span>
-- MAGIC       <ul style="margin: 0; padding-left: 18px; font-size: 14pt; color: #0b2026; line-height: 1.6;">
-- MAGIC         <li style="margin-bottom: 8px;">No SQL Answer provided</li>
-- MAGIC         <li style="margin-bottom: 8px;">Results don't match closely enough for auto-scoring</li>
-- MAGIC         <li>A human must mark Good or Bad</li>
-- MAGIC       </ul>
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- Retention note -->
-- MAGIC <div class="bench-note">
-- MAGIC   <strong>Note:</strong> Evaluation response results are visible for <strong>one week</strong>. After that, results are no longer visible, but the generated SQL and example SQL statements remain.
-- MAGIC </div>
-- MAGIC
-- MAGIC
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC Use benchmarks in a Genie Agent - 
-- MAGIC [AWS](https://docs.databricks.com/aws/en/genie/benchmarks) |
-- MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/genie-agents/monitor) |
-- MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/benchmarks)
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### B1. Add Benchmark: What Are the Top 5 Franchise Locations by Total Revenue?
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Why This Benchmark?
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC - This tests whether Genie can correctly **join two tables** (`sales_franchises_gold` and `sales_transactions_gold`) and use `SUM(totalPrice)` for revenue. 
-- MAGIC
-- MAGIC - It also tests whether Genie can figure out that:
-- MAGIC   - franchise names that appear in multiple cities
-- MAGIC   - some franchises share the same name but are in different locations.
-- MAGIC
-- MAGIC - One thing to notice is our benchmark will take ties into account. 
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. In Genie, select **Benchmark** > **+ Add benchmark**.
-- MAGIC
-- MAGIC 2. Enter the question: `What are the top 5 franchise locations by total revenue?`
-- MAGIC
-- MAGIC 3. Select **Generate SQL** to auto generate SQL for the **Ground truth SQL answer** for this question.
-- MAGIC     - **NOTE:** You can also write the query yourself if you'd like. 
-- MAGIC
-- MAGIC 4. For training purposes (consistency), run the cell below and copy the query and **replace the auto generated query** in your benchmark. 
-- MAGIC
-- MAGIC 5. Select **Add benchmark**.

-- COMMAND ----------

DECLARE OR REPLACE my_query STRING DEFAULT "";

SET VAR my_query = "
WITH franchise_revenue AS (
  SELECT
    f.`franchiseID`,
    f.`city`,
    f.`name`,
    SUM(t.`totalPrice`) AS total_revenue
  FROM
    `" || my_catalog || "`.`genie_course_bakehouse`.`sales_transactions_gold` t
      JOIN `" || my_catalog || "`.`genie_course_bakehouse`.`sales_franchises_gold` f
        ON t.`franchiseID` = f.`franchiseID`
  WHERE
    t.`franchiseID` IS NOT NULL
    AND t.`totalPrice` IS NOT NULL
    AND f.`city` IS NOT NULL
  GROUP BY
    f.`franchiseID`,
    f.`city`,
    f.`name`
)
SELECT
  city,
  name,
  total_revenue
FROM
  (
    SELECT
      city,
      name,
      total_revenue,
      RANK() OVER (ORDER BY total_revenue DESC) AS rank
    FROM
      franchise_revenue
  )
WHERE
  rank <= 5
"

;

SELECT my_query;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Generated SQL Review
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC When generating SQL for your **Ground truth SQL answer** you should always review the output and confirm it's what you are expecting.
-- MAGIC
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### B2. Add Benchmark: Who Are Our Best Customers?
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Why This Benchmark?
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC - This tests how Genie handles an **ambiguous business term**. 
-- MAGIC
-- MAGIC - "Best" has no defined meaning in the data. Our business defines it as **highest total spend** using `SUM(totalPrice)`. 
-- MAGIC
-- MAGIC - Without instructions, Genie must guess. It may: 
-- MAGIC   - rank by number of transactions, 
-- MAGIC   - most recent purchase 
-- MAGIC   - or something else entirely
-- MAGIC   - **NOTE:** Different runs may produce different interpretations
-- MAGIC
-- MAGIC - How does Genie determine how many customers to return to you? 5? 10? 100?
-- MAGIC
-- MAGIC - One thing to notice is our benchmark does not take ties into account. 
-- MAGIC
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Instead of auto generating the SQL, run the cell below to run your own query with the correct result.

-- COMMAND ----------

SELECT
    c.customerID,
    c.first_name,
    c.last_name,
    SUM(t.totalPrice) AS total_spend
FROM sales_transactions_gold AS t
JOIN sales_customers_gold AS c
    ON t.customerID = c.customerID
GROUP BY
    c.customerID,
    c.first_name,
    c.last_name
ORDER BY
    total_spend DESC
LIMIT 10

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. In Genie, select **Benchmark** > **+ Add benchmark**.
-- MAGIC
-- MAGIC 3. Enter the question: `Who are our best customers?`
-- MAGIC
-- MAGIC 4. Run the cell below to generate the query from above with your catalog name.

-- COMMAND ----------

DECLARE OR REPLACE my_query STRING DEFAULT "";

SET VAR my_query = "
SELECT
    c.customerID,
    c.first_name,
    c.last_name,
    SUM(t.totalPrice) AS total_spend
FROM " || my_catalog || ".genie_course_bakehouse.sales_transactions_gold AS t
JOIN " || my_catalog || ".genie_course_bakehouse.sales_customers_gold AS c
    ON t.customerID = c.customerID
GROUP BY
    c.customerID,
    c.first_name,
    c.last_name
ORDER BY
    total_spend DESC
LIMIT 10
";

SELECT my_query;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Copy the output above and paste into the **Ground truth SQL answer** field.
-- MAGIC
-- MAGIC 6. Select **Add benchmark**.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### B3. Add Benchmark: How Many Franchises Does Each Supplier Serve?
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Why This Benchmark?
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC - This tests whether Genie handles a **data quality issue**. 
-- MAGIC
-- MAGIC - In the previous demo, we discovered that **21 out of 48 franchises** have a `supplierID` that does not match any record in the suppliers table. 
-- MAGIC
-- MAGIC - Genie will likely use an `INNER JOIN`, silently dropping those 21 orphaned franchises. 
-- MAGIC
-- MAGIC - The correct approach uses a `LEFT JOIN` with `COALESCE` to surface all franchises, including those without a valid supplier.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Run the cell below to verify the correct result.
-- MAGIC
-- MAGIC     Confirm that **No Matching Supplier** shows `21` franchises.

-- COMMAND ----------

SELECT
    COALESCE(s.name, 'No Matching Supplier') AS supplier_name,
    COUNT(f.franchiseID) AS franchise_count
FROM sales_franchises_gold AS f
LEFT JOIN sales_suppliers_gold AS s
    ON f.supplierID = s.supplierID
GROUP BY
    s.name
ORDER BY
    franchise_count DESC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. In Genie, select **Benchmarks** > **+ Add benchmark**.
-- MAGIC
-- MAGIC 3. Enter the question: `How many franchises does each supplier serve?`
-- MAGIC
-- MAGIC 4. Run the cell below to generate the query with your catalog name.

-- COMMAND ----------

DECLARE OR REPLACE my_query STRING DEFAULT "";

SET VAR my_query = "
SELECT
    COALESCE(s.name, 'No Matching Supplier') AS supplier_name,
    COUNT(f.franchiseID) AS franchise_count
FROM " || my_catalog || ".genie_course_bakehouse.sales_franchises_gold AS f
LEFT JOIN " || my_catalog || ".genie_course_bakehouse.sales_suppliers_gold AS s
    ON f.supplierID = s.supplierID
GROUP BY
    s.name
ORDER BY
    franchise_count DESC
";

SELECT my_query;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Copy the output above and paste into the **Ground truth SQL answer** field.
-- MAGIC
-- MAGIC 6. Select **Add benchmark**.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### B4. Add Benchmark: What Are Total Sales by Region?
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Why This Benchmark?
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC - This tests whether Genie knows our **business-defined regions**. 
-- MAGIC
-- MAGIC - There is no `region` column in the data. 
-- MAGIC
-- MAGIC - Our business groups countries into three regions: 
-- MAGIC   - **APJ** (Japan, Australia)
-- MAGIC   - **AMER** (US, Canada)
-- MAGIC   - **EMEA** (Netherlands, France, Germany, Italy, Sweden). 
-- MAGIC
-- MAGIC #### Without a SQL expression or instruction defining this mapping, Genie will likely group by `country` instead, or invent its own region definitions.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Run the cell below to verify the correct result.
-- MAGIC
-- MAGIC     Confirm the results show 3 regions: **APJ**, **AMER**, and **EMEA**.

-- COMMAND ----------

SELECT
    CASE
        WHEN f.country IN ('Japan', 'Australia') THEN 'APJ'
        WHEN f.country IN ('US', 'Canada') THEN 'AMER'
        WHEN f.country IN ('Netherlands', 'France', 'Germany', 'Italy', 'Sweden') THEN 'EMEA'
        ELSE 'Other'
    END AS region,
    SUM(t.totalPrice) AS total_sales
FROM sales_franchises_gold AS f
JOIN sales_transactions_gold AS t
    ON f.franchiseID = t.franchiseID
GROUP BY
    region
ORDER BY
    total_sales DESC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. In Genie, select **Benchmark** > **+ Add benchmark**.
-- MAGIC
-- MAGIC 3. Enter the question: `What are total sales by region?`
-- MAGIC
-- MAGIC 4. Run the cell below to generate the query with your catalog name.

-- COMMAND ----------

DECLARE OR REPLACE my_query STRING DEFAULT "";

SET VAR my_query = "
SELECT
    CASE
        WHEN f.country IN ('Japan', 'Australia') THEN 'APJ'
        WHEN f.country IN ('US', 'Canada') THEN 'AMER'
        WHEN f.country IN ('Netherlands', 'France', 'Germany', 'Italy', 'Sweden') THEN 'EMEA'
        ELSE 'Other'
    END AS region,
    SUM(t.totalPrice) AS total_sales
FROM " || my_catalog || ".genie_course_bakehouse.sales_franchises_gold AS f
JOIN " || my_catalog || ".genie_course_bakehouse.sales_transactions_gold AS t
    ON f.franchiseID = t.franchiseID
GROUP BY region
ORDER BY total_sales DESC
";

SELECT my_query;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Copy the output above and paste into the **Ground truth SQL answer** field.
-- MAGIC
-- MAGIC 6. Select **Add benchmark**.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### B5. Add Benchmark: Count of Bad Reviews by Location?
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Why This Benchmark?
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC This benchmark tests multiple metadata challenges at once. 
-- MAGIC
-- MAGIC - The word "bad" is business language for the value `negative` in the `flag` column. Genie has no way to know this mapping without a column description or synonym. 
-- MAGIC
-- MAGIC - The column `ref` is a cryptic foreign key to `sales_franchises_gold.franchiseID` that Genie most likely cannot resolve without a description. 
-- MAGIC
-- MAGIC - Additionally, some franchise locations share the **same name** but have different `franchiseID` values. The ground truth groups by `ref` and `name` to keep them distinct.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Run the cell below to verify the correct result.
-- MAGIC
-- MAGIC     Notice the query groups by **ref** (the franchise ID) and **name** to distinguish between franchises that **share the same name but are in different cities**.

-- COMMAND ----------

SELECT
    r.ref,
    f.name AS franchise_name,
    f.city,
    COUNT(*) AS negative_review_count
FROM media_customer_reviews_gold r
JOIN sales_franchises_gold f ON r.ref = f.franchiseID
WHERE r.flag = 'negative'
GROUP BY r.ref, f.name, f.city
ORDER BY negative_review_count DESC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. In Genie, select **Benchmark** > **+ Add benchmark**.
-- MAGIC
-- MAGIC 3. Enter the question: `Count of bad reviews by locations?`
-- MAGIC
-- MAGIC 4. Run the cell below to generate the query with your catalog name.

-- COMMAND ----------

DECLARE OR REPLACE my_query STRING DEFAULT "";

SET VAR my_query = "
SELECT
    r.ref,
    f.name AS franchise_name,
    f.city,
    COUNT(*) AS negative_review_count
FROM " || my_catalog || ".genie_course_bakehouse.media_customer_reviews_gold r
JOIN " || my_catalog || ".genie_course_bakehouse.sales_franchises_gold f ON r.ref = f.franchiseID
WHERE r.flag = 'negative'
GROUP BY r.ref, f.name, f.city
ORDER BY negative_review_count DESC
";

SELECT my_query;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Copy the output above and paste into the **Ground truth SQL answer** field.
-- MAGIC
-- MAGIC 6. Select **Add benchmark**.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B6. Benchmark Summary
-- MAGIC
-- MAGIC You now have **6 benchmarks** that cover a range of question types and difficulty levels:
-- MAGIC
-- MAGIC <br></br>
-- MAGIC
-- MAGIC <div style="max-width: 1100px; margin: 0 auto;">
-- MAGIC
-- MAGIC | # | Benchmark Question | What It Tests | Why Genie Will Struggle | What Would Fix It |
-- MAGIC |---|-------------------|---------------|------------------------|-------------------|
-- MAGIC | 1 | *How many customers do we have?* | Simple count, the baseline | Minimal issues expected | Should already work |
-- MAGIC | 2 | *What are the top 5 franchise locations by total revenue?* | Multi-table join, revenue calculation | May not use `SUM(totalPrice)` or may merge same-name franchises | **Column descriptions** clarifying revenue and franchise name uniqueness |
-- MAGIC | 3 | *Who are our best customers?* | Ambiguous business term | "Best" is undefined and Genie must guess | **Text instruction** defining best = highest total spend, number of customers to return |
-- MAGIC | 4 | *How many franchises does each supplier serve?* | Data quality issue, orphaned foreign keys | Will `INNER JOIN`, dropping 21 of 48 franchises | **Example SQL** demonstrating `LEFT JOIN` + `COALESCE` |
-- MAGIC | 5 | *What are total sales by region?* | Business-defined grouping | No `region` column, will most likely group by country | **SQL expression** mapping countries to APJ/AMER/EMEA |
-- MAGIC | 6 | *Count of bad reviews by locations?* | Cryptic columns + business synonyms | `flag` ≠ "bad", `ref` ≠ franchise, same-name locations | **Column descriptions** + **synonyms** mapping bad→negative, ref→franchiseID |
-- MAGIC
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     This is Your Starting Point
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC These benchmarks represent your **baseline**. The questions Genie needs to answer correctly for this space to be useful.
-- MAGIC
-- MAGIC Right now, some of them will most likely fail because the Genie Agent has **no metadata, no instructions, and no example SQL logic (Queries, Joins or Expressions)**.
-- MAGIC
-- MAGIC As you work through the next demos, you will iteratively add context and re-run these benchmarks to measure progress.
-- MAGIC
-- MAGIC #### In production, it is important to collaborate with **subject matter experts** to define your benchmark questions and ground truth answers. 
-- MAGIC
-- MAGIC #### We have limited, simple benchmarks for training purposes.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## C. Run Benchmarks

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C1. Navigate to the Benchmarks Tab
-- MAGIC
-- MAGIC 1. In your Genie Agent, select **Benchmarks** at the top of the settings panel.
-- MAGIC
-- MAGIC 2. Select **Questions** and confirm you see all 6 benchmarks:
-- MAGIC
-- MAGIC    | # | Benchmark Question | Ground Truth SQL |
-- MAGIC    |---|-------------------|-----------------|
-- MAGIC    | 1 | How many customers do we have? | Yes |
-- MAGIC    | 2 | What are the top 5 franchise locations by total revenue? | Yes |
-- MAGIC    | 3 | Who are our best customers? | Yes |
-- MAGIC    | 4 | How many franchises does each supplier serve? | Yes |
-- MAGIC    | 5 | What are total sales by region? | Yes |
-- MAGIC    | 6 | Count of bad reviews by locations? | Yes |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### C2. Run All Benchmarks
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #f44336;
-- MAGIC   background: #ffebee;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Please Select Chat Mode</strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Please select the **Chat** button before running all benchmarks. We will be testing the **Chat** mode benchmarks in this course.
-- MAGIC
-- MAGIC #### Benchmark questions support two modes:
-- MAGIC
-- MAGIC - Chat mode: The default mode. Genie assesses accuracy by comparing its SQL-generated results against a provided SQL answer.
-- MAGIC
-- MAGIC - Agent mode: Executes benchmark questions using the same multi-step reasoning as Genie's Agent mode. An LLM judge grades the responses. You can provide an optional evaluation note to guide grading.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Select **Run all benchmarks** to execute all benchmark questions.
-- MAGIC
-- MAGIC 2. Genie will process each benchmark question as a **new conversation**.
-- MAGIC     - No prior thread context (memory) is carried over.
-- MAGIC
-- MAGIC 3. As the benchmarks are executing, continue on in this notebook. This may take a few minutes depending on the SQL warehouse.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #1976d2;
-- MAGIC   background: #e3f2fd;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Important: Benchmarks Run as New Conversations
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Each benchmark question is processed as a **brand new conversation**. 
-- MAGIC
-- MAGIC This means:
-- MAGIC
-- MAGIC - Genie does **not** carry over context from previous questions in the thread.
-- MAGIC - The only context Genie uses is the **space configuration**: table schemas, instructions, example SQL, and SQL expressions.
-- MAGIC - A question that worked correctly in your chat thread may **fail** as a benchmark if it relied on context from earlier questions.
-- MAGIC
-- MAGIC #### This is by design. Benchmarks test how well your **space configuration** supports each question independently.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C3. Review Benchmark Results
-- MAGIC
-- MAGIC 1. As a benchmark completes, review the results for each question.
-- MAGIC
-- MAGIC 2. For each benchmark, Genie shows:
-- MAGIC    - **Assessment** - Whether the benchmark passed or failed
-- MAGIC    - **Score reason** - Reason for the pass or fail
-- MAGIC    - **Question** - Question that was asked
-- MAGIC    - **Failure analysis** - Detailed reasoning on why the benchmark failed with the **SQL Differences**
-- MAGIC    - **Response** - The SQL that Genie produced for this run
-- MAGIC    - **Ground truth SQL answer** - If you provided ground truth SQL, Genie compares the **model output against the expected results (ground truth)**
-- MAGIC
-- MAGIC 3. Review the details of each result and note which benchmarks passed and which failed.
-- MAGIC    - Specifically focus on the **why** these failed. 
-- MAGIC
-- MAGIC 4. Leave the benchmark page open.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC The table below summarizes expected behavior at this stage **before any metadata, SQL logic or instructions have been added**:
-- MAGIC
-- MAGIC #### The results might vary. Our goal is to add enough context where we see correct and consistent Genie Agent results.
-- MAGIC
-- MAGIC   <table style="width: 100%; border-collapse: collapse; font-size: 11pt;">
-- MAGIC     <thead>
-- MAGIC       <tr style="background: #1B5162; color: white;">
-- MAGIC         <th style="padding: 10px; text-align: center; width: 40px;">#</th>
-- MAGIC         <th style="padding: 10px; text-align: left;">Benchmark Question</th>
-- MAGIC         <th style="padding: 10px; text-align: left;">Expected Behavior</th>
-- MAGIC         <th style="padding: 10px; text-align: left;">Likely Result</th>
-- MAGIC       </tr>
-- MAGIC     </thead>
-- MAGIC     <tbody>
-- MAGIC       <tr style="background: #f8d7da;">
-- MAGIC         <td style="padding: 10px; text-align: center;">1</td>
-- MAGIC         <td style="padding: 10px;"><em>How many customers do we have?</em></td>
-- MAGIC         <td style="padding: 10px;">Simple COUNT on <code>sales_customers_gold</code></td>
-- MAGIC         <td style="padding: 10px;"><strong>Likely fail</strong>, straightforward, unambiguous. However, when we added this benchmark it might have added additional information. We will see this later.</td>
-- MAGIC       </tr>
-- MAGIC       <tr style="background: #d4edda;">
-- MAGIC         <td style="padding: 10px; text-align: center;">2</td>
-- MAGIC         <td style="padding: 10px;"><em>What are the top 5 franchise locations by total revenue?</em></td>
-- MAGIC         <td style="padding: 10px;">JOIN franchises to transactions, SUM totalPrice</td>
-- MAGIC         <td style="padding: 10px;"><strong>May vary, should pass</strong> — depends on grouping and column selection</td>
-- MAGIC       </tr>
-- MAGIC       <tr style="background: #fff3cd;">
-- MAGIC         <td style="padding: 10px; text-align: center;">3</td>
-- MAGIC         <td style="padding: 10px;"><em>Who are our best customers?</em></td>
-- MAGIC         <td style="padding: 10px;">JOIN customers to transactions, SUM totalPrice, LIMIT 10</td>
-- MAGIC         <td style="padding: 10px;"><strong>May fail</strong> — "best" is ambiguous without instructions</td>
-- MAGIC       </tr>
-- MAGIC       <tr style="background: #f8d7da;">
-- MAGIC         <td style="padding: 10px; text-align: center;">4</td>
-- MAGIC         <td style="padding: 10px;"><em>How many franchises does each supplier serve?</em></td>
-- MAGIC         <td style="padding: 10px;">LEFT JOIN franchises to suppliers with COALESCE</td>
-- MAGIC         <td style="padding: 10px;"><strong>Likely fail</strong> — Genie will probably INNER JOIN, missing 21 franchises</td>
-- MAGIC       </tr>
-- MAGIC       <tr style="background: #f8d7da;">
-- MAGIC         <td style="padding: 10px; text-align: center;">5</td>
-- MAGIC         <td style="padding: 10px;"><em>What are total sales by region?</em></td>
-- MAGIC         <td style="padding: 10px;">CASE expression mapping countries to APJ/AMER/EMEA</td>
-- MAGIC         <td style="padding: 10px;"><strong>Likely fail</strong> — no region column exists; Genie will group by country</td>
-- MAGIC       </tr>
-- MAGIC       <tr style="background: #f8d7da;">
-- MAGIC         <td style="padding: 10px; text-align: center;">6</td>
-- MAGIC         <td style="padding: 10px;"><em>Count of bad reviews by locations?</em></td>
-- MAGIC         <td style="padding: 10px;">Filter <code>flag = 'negative'</code>, join <code>ref</code> to franchiseID, group by ref + name + city</td>
-- MAGIC         <td style="padding: 10px;"><strong>Likely fail</strong> — "bad" ≠ column value, <code>flag</code> and <code>ref</code> are cryptic</td>
-- MAGIC       </tr>
-- MAGIC     </tbody>
-- MAGIC   </table>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## D. (Optional, Benchmark Can Vary) Update a `Ground Truth` if Necessary
-- MAGIC
-- MAGIC 1. Select the benchmark `  How many customers do we have?`
-- MAGIC     - **NOTE:** This is the benchmark we added after asking Genie the question in the previous demonstration.
-- MAGIC
-- MAGIC 2. View the **Ground truth SQL answer**
-- MAGIC
-- MAGIC 3. View the ground truth here.  It might give a variety of additional information in the query that was not shown when we asked Genie the count of total customers in our original question:
-- MAGIC
-- MAGIC **Your Ground truth SQL answer might look like this**
-- MAGIC ```sql
-- MAGIC SELECT
-- MAGIC   COUNT(*) AS total_rows,
-- MAGIC   COUNT(DISTINCT customerID) AS distinct_customers,
-- MAGIC   COUNT(customerID) AS non_null_customers,
-- MAGIC   SUM(
-- MAGIC     CASE
-- MAGIC       WHEN customerID IS NULL THEN 1
-- MAGIC       ELSE 0
-- MAGIC     END
-- MAGIC   ) AS null_customers
-- MAGIC FROM
-- MAGIC   `labuser_YOURUSERNAME`.`genie_course_bakehouse`.`sales_customers_gold`
-- MAGIC ```
-- MAGIC
-- MAGIC **Results**
-- MAGIC | total_rows | distinct_customers | non_null_customers | null_customers |
-- MAGIC |------------|-------------------|--------------------|----------------|
-- MAGIC | 300        | 300               | 300                | 0              |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **If this benchmark failed and looks like the query above, you can update the ground truth to a simple query, see example below.**
-- MAGIC ```sql
-- MAGIC SELECT
-- MAGIC   COUNT(DISTINCT customerID) AS distinct_customers
-- MAGIC FROM
-- MAGIC   `labuser_YOURUSERNAME`.`genie_course_bakehouse`.`sales_customers_gold`
-- MAGIC ```
-- MAGIC
-- MAGIC 3. In the **Response - Model output** section select **Update ground truth** > **Update question**. 
-- MAGIC     - When this question is asked all we want to test is if it will query distinct customers. 
-- MAGIC     - In some scenarios it could add additional information we don't want in the **Ground truth SQL answer**.
-- MAGIC     - **NOTE:** After you update you might not see the updated **Ground truth SQL answer**. You can try refreshing the page. If not, it will update when we rerun the benchmark.
-- MAGIC
-- MAGIC 4. Select the checkmark next to `How many customers do we have?`.
-- MAGIC
-- MAGIC 5. Then select **Start new run** to run this **benchmark** again.
-- MAGIC
-- MAGIC 6. Confirm the test completes and is successful (if the test completes but you don't see results, refresh the page).
-- MAGIC
-- MAGIC 7. Lastly, select the **Evaluations** tab to view all evaluations. Confirm the latest single test passed:
-- MAGIC
-- MAGIC **Last run example**
-- MAGIC | Evaluation Name   | Execution Status | Accuracy       | Timestamp              | User             |
-- MAGIC |-------------------|------------------|----------------|------------------------|------------------|
-- MAGIC | Evaluation        | Completed        | 100% (1/1)     | Mar XX, 20XX, 18:28:58 | Peter Sty  |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## E. Conclusion
-- MAGIC
-- MAGIC In this demo, you:
-- MAGIC
-- MAGIC - Added additional benchmarks with ground truth SQL covering multi-table joins, ambiguous business terms, data quality issues, and business-defined groupings.
-- MAGIC - Ran all the benchmarks (including the baseline from the previous demo) to establish baseline accuracy.
-- MAGIC - Observed that Genie handles simple, unambiguous questions well but struggles with undefined business terms, complex join patterns, and business-defined concepts like region.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
-- MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
-- MAGIC <script>
-- MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
-- MAGIC </script>
