-- Databricks notebook source
-- MAGIC %md
-- MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC # Demo - Bakehouse Setup and Data Exploration
-- MAGIC
-- MAGIC ## Overview
-- MAGIC
-- MAGIC Before creating a Genie Agent, you need to understand the data it will use. 
-- MAGIC
-- MAGIC In this short demo, you will quickly explore the **bakehouse** dataset, a fictional bakery franchise business.
-- MAGIC
-- MAGIC During exploration you need to familiarize yourself with the tables, their relationships, and a key data quality issue. This context will help you make better decisions when configuring and curating Genie in the next demo.
-- MAGIC
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this demo, you will be able to:
-- MAGIC
-- MAGIC 1. **Identify the tables** in the bakehouse dataset and understand what each one contains.
-- MAGIC 2. **Understand the relationships** between tables using primary and foreign keys.
-- MAGIC 3. **Identify a data quality issue** - Specifically orphaned foreign keys between franchises and suppliers.

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
-- MAGIC 1. Run the cell below to initialize your environment. This setup step will:
-- MAGIC     - Assume that you have **permission to create a catalog**
-- MAGIC     - Create a catalog named **labuser_YOUR_USER_NAME**
-- MAGIC     - Create a schema named **genie_course_bakehouse**
-- MAGIC     - Create the necessary tables (copies the **samples.bakehouse** data to your catalog with minor modifications)

-- COMMAND ----------

-- MAGIC %run ./Includes/Classroom-Setup-creating-genie-agent

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Run the cell below to view the tables in your **labuser_YOUR_USER_NAME.genie_course_bakehouse** schema.
-- MAGIC
-- MAGIC     Confirm the following 5 tables exist:
-- MAGIC
-- MAGIC     - **media_customer_reviews_gold**
-- MAGIC     - **sales_customers_gold**
-- MAGIC     - **sales_franchises_gold**
-- MAGIC     - **sales_suppliers_gold**
-- MAGIC     - **sales_transactions_gold**

-- COMMAND ----------

SHOW TABLES IN genie_course_bakehouse;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #1976d2;
-- MAGIC   background: #e3f2fd;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Information
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC For this course, we assume a data pipeline is already running and producing the **gold tables** required for Genie.
-- MAGIC
-- MAGIC These tables represent curated, analytics-ready data that Genie will use to answer questions.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Understanding the Bakehouse Dataset
-- MAGIC
-- MAGIC Before creating a Genie Agent, it is important to understand the data that the space will use.
-- MAGIC
-- MAGIC > The **bakehouse** dataset represents a fictional bakery franchise business with locations around the world. It includes data on customers, franchise locations, suppliers, sales transactions, and customer reviews.
-- MAGIC
-- MAGIC | Table | Description | Rows |
-- MAGIC |-------|-------------|------|
-- MAGIC | **sales_customers_gold** | Customer profiles including name, email, location, and demographics | 300 |
-- MAGIC | **sales_franchises_gold** | Bakery franchise locations with city, country, size, and geographic coordinates | 48 |
-- MAGIC | **sales_suppliers_gold** | Ingredient suppliers with location and approval status | 27 |
-- MAGIC | **sales_transactions_gold** | Sales transactions including product, quantity, price, and payment method | 3,333 |
-- MAGIC | **media_customer_reviews_gold** | Customer reviews with free-text feedback and a sentiment label | 204 |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B1. Preview the Tables
-- MAGIC Run the queries below to quickly preview each table and understand the data you will be working with.
-- MAGIC
-- MAGIC 1. View the **sales_customers_gold** table.
-- MAGIC
-- MAGIC     Notice it contains:
-- MAGIC       - a **customerID** column
-- MAGIC       - general customer information such as name, contact details, and location

-- COMMAND ----------

-- Preview the sales_customers table
SELECT *
FROM sales_customers_gold;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. View the **sales_franchises_gold** table.
-- MAGIC
-- MAGIC     Notice it contains:
-- MAGIC       - a **franchiseID** column
-- MAGIC       - location details such as city, district, zip code, and country
-- MAGIC       - franchise attributes such as size and supplier relationships (**supplierID** column)

-- COMMAND ----------

-- Preview the sales_franchises table
SELECT *
FROM sales_franchises_gold;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. View the **sales_suppliers_gold** table.
-- MAGIC
-- MAGIC     Notice it contains:
-- MAGIC       - a **supplierID** column
-- MAGIC       - supplier details such as name, ingredient, and location
-- MAGIC       - operational attributes such as size and approval status

-- COMMAND ----------

-- Preview the sales_suppliers table
SELECT *
FROM sales_suppliers_gold;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. View the **sales_transactions_gold** table.
-- MAGIC
-- MAGIC     Notice it contains:
-- MAGIC       - a **transactionID** column
-- MAGIC       - relationships to customers and franchises through **customerID** and **franchiseID**
-- MAGIC       - transactional details such as product, quantity, pricing, and total amount
-- MAGIC       - payment information such as payment method and card number

-- COMMAND ----------

-- Preview the sales_transactions table
SELECT *
FROM sales_transactions_gold;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. View the **media_customer_reviews_gold** table.
-- MAGIC
-- MAGIC     Notice it contains:
-- MAGIC       - a **review** column with unstructured text data
-- MAGIC       - a **ref** column linking reviews to specific locations (**sales_franchises_gold.franchiseID**)
-- MAGIC       - a **review_date** for when the review was created
-- MAGIC       - a **flag** classification indicating positive, negative, or mixed feedback
-- MAGIC         - Created for you using the `ai_analyze_sentiment` function:
-- MAGIC         [AWS](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_analyze_sentiment) |
-- MAGIC         [Azure](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_analyze_sentiment) |
-- MAGIC         [GCP](https://docs.databricks.com/gcp/en/sql/language-manual/functions/ai_analyze_sentiment)
-- MAGIC

-- COMMAND ----------

SELECT *
FROM media_customer_reviews_gold;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 6. Join the **sales_franchises_gold** and **sales_suppliers_gold** tables to find if all franchises have a supplier documented.

-- COMMAND ----------

SELECT
  f.franchiseID,
  COUNT(s.supplierID) AS supplier_count
FROM sales_franchises_gold f
LEFT JOIN sales_suppliers_gold s 
  ON f.supplierID = s.supplierID
GROUP BY f.franchiseID

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
-- MAGIC     Warning
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Notice that not all **franchises** have an associated **supplier** in this synthetic data.
-- MAGIC
-- MAGIC **Summary Counts**
-- MAGIC
-- MAGIC | has_valid_supplier | count |
-- MAGIC |-------------------|-------|
-- MAGIC | No                | 21    |
-- MAGIC | Yes               | 27    |
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

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
-- MAGIC     A Note on Data Exploration
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC In production scenarios, it is important to **thoroughly explore and profile your data** before building a Genie Agent. 
-- MAGIC
-- MAGIC Understanding distributions, nulls, edge cases, and business logic embedded in the data.
-- MAGIC
-- MAGIC For this training, we have done a **brief, focused exploration**. Just enough to understand the tables and one key data quality issue before moving on to Genie.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## C. Genie Agent Project Architecture Overview
-- MAGIC <br></br>
-- MAGIC <div style="max-width: 1280px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
-- MAGIC
-- MAGIC <!-- TITLE BAR -->
-- MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 20px 28px; margin-bottom: 18px;">
-- MAGIC   <div style="font-size: 22pt; font-weight: 700; margin-bottom: 6px;">Genie Project Architecture</div>
-- MAGIC   <div style="font-size: 15pt; font-weight: 400; line-height: 1.45; opacity: 0.95;">Let&rsquo;s view the project architecture for Genie. The goal is to link all of our Unity Catalog tables to a Genie Agent where consumers can <b>ask questions in natural language to obtain results.</b></div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- BEST PRACTICE CALLOUT -->
-- MAGIC <div style="background: #FFF6F4; border-left: 4px solid #FF5F46; border-radius: 6px; padding: 12px 18px; margin-bottom: 22px; font-size: 14pt; line-height: 1.5;">
-- MAGIC   <span style="font-size: 12pt; font-weight: 700; letter-spacing: 1.5px; color: #B83A24; text-transform: uppercase; display: block; margin-bottom: 4px;">Best Practice</span>
-- MAGIC   It&rsquo;s best for a <b>data domain expert</b> to set up a Genie Agent with <b>stakeholder involvement</b>.
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- FAN-IN/FAN-OUT ARCHITECTURE -->
-- MAGIC <div style="display: grid; grid-template-columns: 1.35fr auto 1fr auto 0.85fr; gap: 0; align-items: center;">
-- MAGIC
-- MAGIC   <!-- LEFT COLUMN: SOURCE TABLES -->
-- MAGIC   <div>
-- MAGIC     <div style="font-size: 12pt; font-weight: 700; letter-spacing: 2px; color: #1B5162; text-transform: uppercase; text-align: center; margin-bottom: 12px;">Unity Catalog Tables</div>
-- MAGIC     <div style="display: flex; flex-direction: column; gap: 10px;">
-- MAGIC     <div style="background: #FFFFFF; border: 2px solid #1B5162; border-left: 6px solid #1B5162; border-radius: 8px; padding: 10px 14px; box-shadow: 0 1px 4px rgba(27,49,57,0.06);">
-- MAGIC       <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
-- MAGIC         <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1B5162" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5v6c0 1.66 4.03 3 9 3s9-1.34 9-3V5"></path><path d="M3 11v6c0 1.66 4.03 3 9 3s9-1.34 9-3v-6"></path></svg>
-- MAGIC         <div style="font-family: monospace; font-size: 14pt; font-weight: 700; color: #0b2026;">sales_customers_gold</div>
-- MAGIC       </div>
-- MAGIC       <div style="font-size: 14pt; color: #5A6F77; font-style: italic; line-height: 1.35; padding-left: 30px;">Customer profiles and locations</div>
-- MAGIC     </div>
-- MAGIC     <div style="background: #FFFFFF; border: 2px solid #1B5162; border-left: 6px solid #1B5162; border-radius: 8px; padding: 10px 14px; box-shadow: 0 1px 4px rgba(27,49,57,0.06);">
-- MAGIC       <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
-- MAGIC         <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1B5162" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5v6c0 1.66 4.03 3 9 3s9-1.34 9-3V5"></path><path d="M3 11v6c0 1.66 4.03 3 9 3s9-1.34 9-3v-6"></path></svg>
-- MAGIC         <div style="font-family: monospace; font-size: 14pt; font-weight: 700; color: #0b2026;">sales_franchises_gold</div>
-- MAGIC       </div>
-- MAGIC       <div style="font-size: 14pt; color: #5A6F77; font-style: italic; line-height: 1.35; padding-left: 30px;">Franchise locations and size</div>
-- MAGIC     </div>
-- MAGIC     <div style="background: #FFFFFF; border: 2px solid #1B5162; border-left: 6px solid #1B5162; border-radius: 8px; padding: 10px 14px; box-shadow: 0 1px 4px rgba(27,49,57,0.06);">
-- MAGIC       <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
-- MAGIC         <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1B5162" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5v6c0 1.66 4.03 3 9 3s9-1.34 9-3V5"></path><path d="M3 11v6c0 1.66 4.03 3 9 3s9-1.34 9-3v-6"></path></svg>
-- MAGIC         <div style="font-family: monospace; font-size: 14pt; font-weight: 700; color: #0b2026;">sales_suppliers_gold</div>
-- MAGIC       </div>
-- MAGIC       <div style="font-size: 14pt; color: #5A6F77; font-style: italic; line-height: 1.35; padding-left: 30px;">Ingredient suppliers</div>
-- MAGIC     </div>
-- MAGIC     <div style="background: #FFFFFF; border: 2px solid #1B5162; border-left: 6px solid #1B5162; border-radius: 8px; padding: 10px 14px; box-shadow: 0 1px 4px rgba(27,49,57,0.06);">
-- MAGIC       <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
-- MAGIC         <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1B5162" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5v6c0 1.66 4.03 3 9 3s9-1.34 9-3V5"></path><path d="M3 11v6c0 1.66 4.03 3 9 3s9-1.34 9-3v-6"></path></svg>
-- MAGIC         <div style="font-family: monospace; font-size: 14pt; font-weight: 700; color: #0b2026;">sales_transactions_gold</div>
-- MAGIC       </div>
-- MAGIC       <div style="font-size: 14pt; color: #5A6F77; font-style: italic; line-height: 1.35; padding-left: 30px;">Sales transactions and revenue</div>
-- MAGIC     </div>
-- MAGIC     <div style="background: #FFFFFF; border: 2px solid #1B5162; border-left: 6px solid #1B5162; border-radius: 8px; padding: 10px 14px; box-shadow: 0 1px 4px rgba(27,49,57,0.06);">
-- MAGIC       <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
-- MAGIC         <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1B5162" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5v6c0 1.66 4.03 3 9 3s9-1.34 9-3V5"></path><path d="M3 11v6c0 1.66 4.03 3 9 3s9-1.34 9-3v-6"></path></svg>
-- MAGIC         <div style="font-family: monospace; font-size: 14pt; font-weight: 700; color: #0b2026;">media_customer_reviews_gold</div>
-- MAGIC       </div>
-- MAGIC       <div style="font-size: 14pt; color: #5A6F77; font-style: italic; line-height: 1.35; padding-left: 30px;">Reviews and sentiment</div>
-- MAGIC     </div>
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <!-- LEFT ARROW BUNDLE -->
-- MAGIC   <div style="display: flex; flex-direction: column; align-items: center; padding: 0 14px;">
-- MAGIC     <div style="font-size: 32pt; color: #618794; line-height: 1;">&rarr;</div>
-- MAGIC     <div style="font-size: 12pt; color: #618794; font-style: italic; margin-top: 4px; text-align: center; max-width: 90px;">governed data</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <!-- CENTER: GENIE HUB -->
-- MAGIC   <div style="background: #F9F7F4; border: 3px solid #FF5F46; border-radius: 14px; padding: 22px 18px; box-shadow: 0 6px 20px rgba(255,95,70,0.18); text-align: center; position: relative;">
-- MAGIC     <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #FF5F46; color: white; font-size: 11pt; font-weight: 700; letter-spacing: 1.5px; padding: 3px 14px; border-radius: 12px;">GENIE AGENT</div>
-- MAGIC     <div style="margin: 10px 0 14px 0;">
-- MAGIC       
-- MAGIC     </div>
-- MAGIC     <div style="font-size: 16pt; font-weight: 700; color: #0b2026; line-height: 1.3; margin-bottom: 10px;">Ask questions in<br>natural language</div>
-- MAGIC     <div style="background: #FFFFFF; border: 1.5px dashed #FF5F46; border-radius: 18px 18px 18px 4px; padding: 8px 14px; font-size: 13pt; font-style: italic; color: #5A6F77; text-align: left; margin-top: 12px;">
-- MAGIC       &ldquo;What were our top 5 selling products last quarter?&rdquo;
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <!-- RIGHT ARROW BUNDLE -->
-- MAGIC   <div style="display: flex; flex-direction: column; align-items: center; padding: 0 14px;">
-- MAGIC     <div style="font-size: 32pt; color: #618794; line-height: 1;">&rarr;</div>
-- MAGIC     <div style="font-size: 12pt; color: #618794; font-style: italic; margin-top: 4px; text-align: center; max-width: 90px;">answers &amp; charts</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <!-- RIGHT COLUMN: CONSUMERS -->
-- MAGIC   <div>
-- MAGIC     <div style="font-size: 12pt; font-weight: 700; letter-spacing: 2px; color: #00A972; text-transform: uppercase; text-align: center; margin-bottom: 12px;">Consumers</div>
-- MAGIC     <div style="display: flex; flex-direction: column; gap: 12px;">
-- MAGIC     <div style="background: #FFFFFF; border: 2px solid #00A972; border-left: 6px solid #00A972; border-radius: 8px; padding: 14px 16px; display: flex; align-items: center; gap: 12px; box-shadow: 0 1px 4px rgba(27,49,57,0.06);">
-- MAGIC       <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#00A972" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
-- MAGIC       <div style="font-size: 15pt; font-weight: 700; color: #0b2026;">Analysts</div>
-- MAGIC     </div>
-- MAGIC     <div style="background: #FFFFFF; border: 2px solid #00A972; border-left: 6px solid #00A972; border-radius: 8px; padding: 14px 16px; display: flex; align-items: center; gap: 12px; box-shadow: 0 1px 4px rgba(27,49,57,0.06);">
-- MAGIC       <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#00A972" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
-- MAGIC       <div style="font-size: 15pt; font-weight: 700; color: #0b2026;">Business Users</div>
-- MAGIC     </div>
-- MAGIC     <div style="background: #FFFFFF; border: 2px solid #00A972; border-left: 6px solid #00A972; border-radius: 8px; padding: 14px 16px; display: flex; align-items: center; gap: 12px; box-shadow: 0 1px 4px rgba(27,49,57,0.06);">
-- MAGIC       <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#00A972" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
-- MAGIC       <div style="font-size: 15pt; font-weight: 700; color: #0b2026;">Franchise Managers</div>
-- MAGIC     </div>
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- BOTTOM BAND: foundation note -->
-- MAGIC <div style="margin-top: 24px; background: linear-gradient(135deg, #1B5162 0%, #0b2026 100%); color: #ffffff; border-radius: 8px; padding: 14px 22px; text-align: center;">
-- MAGIC   <div style="font-size: 11pt; letter-spacing: 2.5px; text-transform: uppercase; color: #B7CDD5; font-weight: 700; margin-bottom: 4px;">Foundation</div>
-- MAGIC   <div style="font-size: 14pt; color: #ffffff;">Unity Catalog &middot; one governed copy of your data &middot; permissions enforced end to end</div>
-- MAGIC </div>
-- MAGIC
-- MAGIC </div>

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
-- MAGIC     Metric Views as a Source for Genie Agents are Recommended
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Instead of referencing tables directly in Genie, **it's recommended that you use Metric Views**. However, to keep this course focused on **Genie**, we will reference tables directly.
-- MAGIC
-- MAGIC **Learning metric views in depth is outside the scope of this course.**
-- MAGIC
-- MAGIC **Metric Views** are recommended as a source for Genie Agents because they centralize business metrics, dimensions, joins, and aggregations, helping produce more accurate and consistent answers. The same governed semantic definitions can also be reused across other Databricks experiences, such as alerts and more.
-- MAGIC
-- MAGIC <div style="width: 100%; max-width: 1200px; margin: 16px auto; font-family: sans-serif;">
-- MAGIC
-- MAGIC <div style="background: #1B5162; color: white; border-radius: 8px 8px 4px 4px; padding: 20px 24px; text-align: center; margin-bottom: 16px;">
-- MAGIC <div style="font-size: 20pt; font-weight: 700; margin-bottom: 8px;">What are Databricks Metric Views?</div>
-- MAGIC <div style="font-size: 14pt; font-weight: 400; line-height: 1.5; opacity: 0.95;">A governed semantic layer that standardizes how business metrics and dimensions are defined
-- MAGIC across your organization, built from joins, filters, and aggregations, plus metadata for AI and BI.</div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <svg viewBox="0 110 1200 650" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" style="width: 100%; height: auto; display: block; background: #FFFFFF; border-radius: 10px;">
-- MAGIC <defs>
-- MAGIC <marker id="mvo-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#5E7077"/></marker>
-- MAGIC </defs>
-- MAGIC <rect x="20" y="120" width="780" height="400" rx="10" fill="#F9F7F4" stroke="#EEEDE9" stroke-width="1"/>
-- MAGIC <text x="410" y="150" text-anchor="middle" font-size="17" font-weight="700" fill="#1B5162" letter-spacing="2">HOW A METRIC VIEW WORKS</text>
-- MAGIC <text x="130" y="180" text-anchor="middle" font-size="16" font-weight="700" fill="#0b2026">1. Curate your data</text>
-- MAGIC <text x="130" y="202" text-anchor="middle" font-size="14" fill="#5E7077">Tables in Unity Catalog</text>
-- MAGIC <rect x="50" y="218" width="160" height="80" rx="6" fill="#FFFFFF" stroke="#1B5162" stroke-width="1.5"/>
-- MAGIC <text x="130" y="244" text-anchor="middle" font-size="15" font-weight="700" fill="#0b2026">Fact tables</text>
-- MAGIC <text x="130" y="268" text-anchor="middle" font-size="14" fill="#5E7077">events, transactions,</text>
-- MAGIC <text x="130" y="286" text-anchor="middle" font-size="14" fill="#5E7077">orders</text>
-- MAGIC <rect x="50" y="308" width="160" height="80" rx="6" fill="#FFFFFF" stroke="#1B5162" stroke-width="1.5"/>
-- MAGIC <text x="130" y="334" text-anchor="middle" font-size="15" font-weight="700" fill="#0b2026">Dimension tables</text>
-- MAGIC <text x="130" y="358" text-anchor="middle" font-size="14" fill="#5E7077">customers, products,</text>
-- MAGIC <text x="130" y="376" text-anchor="middle" font-size="14" fill="#5E7077">dates</text>
-- MAGIC <rect x="50" y="398" width="160" height="80" rx="6" fill="#FFFFFF" stroke="#1B5162" stroke-width="1.5"/>
-- MAGIC <text x="130" y="424" text-anchor="middle" font-size="15" font-weight="700" fill="#0b2026">Source filters</text>
-- MAGIC <text x="130" y="448" text-anchor="middle" font-size="14" fill="#5E7077">scope and quality</text>
-- MAGIC <text x="130" y="466" text-anchor="middle" font-size="14" fill="#5E7077">rules</text>
-- MAGIC <line x1="216" y1="326" x2="248" y2="326" stroke="#5E7077" stroke-width="2" marker-end="url(#mvo-arr)"/>
-- MAGIC <text x="380" y="180" text-anchor="middle" font-size="16" font-weight="700" fill="#0b2026">2. Define your metric view</text>
-- MAGIC <text x="380" y="202" text-anchor="middle" font-size="14" fill="#5E7077">Data, joins, filters, dimensions</text>
-- MAGIC <rect x="252" y="218" width="256" height="216" rx="10" fill="none" stroke="#4299E0" stroke-width="1.5" stroke-opacity="0.35"/>
-- MAGIC <rect x="258" y="224" width="244" height="204" rx="8" fill="#F4FAFF" stroke="#4299E0" stroke-width="2.5"/>
-- MAGIC <text x="380" y="250" text-anchor="middle" font-size="18" font-weight="700" fill="#1B5162" letter-spacing="1">METRIC VIEW</text>
-- MAGIC <rect x="266" y="266" width="72" height="28" rx="14" fill="#D8EBFB" stroke="#4299E0" stroke-width="1"/>
-- MAGIC <text x="302" y="285" text-anchor="middle" font-size="14" fill="#1B5162" font-weight="700">JOINS</text>
-- MAGIC <rect x="344" y="266" width="72" height="28" rx="14" fill="#D8EBFB" stroke="#4299E0" stroke-width="1"/>
-- MAGIC <text x="380" y="285" text-anchor="middle" font-size="14" fill="#1B5162" font-weight="700">FILTERS</text>
-- MAGIC <rect x="422" y="266" width="72" height="28" rx="14" fill="#D8EBFB" stroke="#4299E0" stroke-width="1"/>
-- MAGIC <text x="458" y="285" text-anchor="middle" font-size="14" fill="#1B5162" font-weight="700">FIELDS</text>
-- MAGIC <rect x="264" y="304" width="88" height="28" rx="14" fill="#D8EBFB" stroke="#4299E0" stroke-width="1"/>
-- MAGIC <text x="308" y="323" text-anchor="middle" font-size="14" fill="#1B5162" font-weight="700">MEASURES</text>
-- MAGIC <rect x="358" y="304" width="140" height="28" rx="14" fill="#D8EBFB" stroke="#4299E0" stroke-width="1"/>
-- MAGIC <text x="428" y="323" text-anchor="middle" font-size="14" fill="#1B5162" font-weight="700">AGENTIC METADATA</text>
-- MAGIC <text x="380" y="372" text-anchor="middle" font-size="14" fill="#5E7077">Defined once, reused</text>
-- MAGIC <text x="380" y="392" text-anchor="middle" font-size="14" fill="#5E7077">across consumers</text>
-- MAGIC <line x1="510" y1="326" x2="544" y2="326" stroke="#5E7077" stroke-width="2" marker-end="url(#mvo-arr)"/>
-- MAGIC <text x="652" y="180" text-anchor="middle" font-size="16" font-weight="700" fill="#0b2026">3. Use everywhere</text>
-- MAGIC <text x="652" y="202" text-anchor="middle" font-size="14" fill="#5E7077">One source of truth</text>
-- MAGIC <rect x="552" y="218" width="200" height="48" rx="6" fill="#FFFFFF" stroke="#00A972" stroke-width="1.5"/>
-- MAGIC <text x="652" y="240" text-anchor="middle" font-size="15" font-weight="700" fill="#0b2026">Dashboards</text>
-- MAGIC <text x="652" y="258" text-anchor="middle" font-size="14" fill="#5E7077">AI/BI Dashboards</text>
-- MAGIC <rect x="552" y="274" width="200" height="48" rx="6" fill="#FFFFFF" stroke="#00A972" stroke-width="1.5"/>
-- MAGIC <text x="652" y="296" text-anchor="middle" font-size="15" font-weight="700" fill="#0b2026">Genie</text>
-- MAGIC <text x="652" y="314" text-anchor="middle" font-size="14" fill="#5E7077">Code, Agents, One</text>
-- MAGIC <rect x="552" y="330" width="200" height="48" rx="6" fill="#FFFFFF" stroke="#00A972" stroke-width="1.5"/>
-- MAGIC <text x="652" y="352" text-anchor="middle" font-size="15" font-weight="700" fill="#0b2026">Notebooks and SQL</text>
-- MAGIC <text x="652" y="370" text-anchor="middle" font-size="14" fill="#5E7077">ad hoc analysis</text>
-- MAGIC <rect x="552" y="386" width="200" height="48" rx="6" fill="#FFFFFF" stroke="#00A972" stroke-width="1.5"/>
-- MAGIC <text x="652" y="408" text-anchor="middle" font-size="15" font-weight="700" fill="#0b2026">APIs and Integrations</text>
-- MAGIC <text x="652" y="426" text-anchor="middle" font-size="14" fill="#5E7077">downstream tools</text>
-- MAGIC <rect x="820" y="120" width="360" height="400" rx="10" fill="#F9F7F4" stroke="#EEEDE9" stroke-width="1"/>
-- MAGIC <text x="1000" y="150" text-anchor="middle" font-size="17" font-weight="700" fill="#1B5162" letter-spacing="2">AGENTIC METADATA</text>
-- MAGIC <text x="1000" y="180" text-anchor="middle" font-size="14" fill="#5E7077">Metric views ship with rich metadata,</text>
-- MAGIC <text x="1000" y="200" text-anchor="middle" font-size="14" fill="#5E7077">so agents and dashboards understand</text>
-- MAGIC <text x="1000" y="220" text-anchor="middle" font-size="14" fill="#5E7077">your business terms correctly.</text>
-- MAGIC <rect x="840" y="240" width="320" height="60" rx="6" fill="#FFFFFF" stroke="#4299E0" stroke-width="1.5"/>
-- MAGIC <rect x="840" y="240" width="6" height="60" fill="#4299E0"/>
-- MAGIC <text x="858" y="266" font-size="16" font-weight="700" fill="#0b2026">Display names</text>
-- MAGIC <text x="858" y="288" font-size="14" fill="#5E7077">Friendly labels for metrics and dimensions.</text>
-- MAGIC <rect x="840" y="308" width="320" height="60" rx="6" fill="#FFFFFF" stroke="#4299E0" stroke-width="1.5"/>
-- MAGIC <rect x="840" y="308" width="6" height="60" fill="#4299E0"/>
-- MAGIC <text x="858" y="334" font-size="16" font-weight="700" fill="#0b2026">Formatting</text>
-- MAGIC <text x="858" y="356" font-size="14" fill="#5E7077">Auto-applied currency and date formats.</text>
-- MAGIC <rect x="840" y="376" width="320" height="60" rx="6" fill="#FFFFFF" stroke="#4299E0" stroke-width="1.5"/>
-- MAGIC <rect x="840" y="376" width="6" height="60" fill="#4299E0"/>
-- MAGIC <text x="858" y="402" font-size="16" font-weight="700" fill="#0b2026">Comments</text>
-- MAGIC <text x="858" y="424" font-size="14" fill="#5E7077">Plain-language descriptions for context.</text>
-- MAGIC <rect x="840" y="444" width="320" height="60" rx="6" fill="#FFFFFF" stroke="#4299E0" stroke-width="1.5"/>
-- MAGIC <rect x="840" y="444" width="6" height="60" fill="#4299E0"/>
-- MAGIC <text x="858" y="470" font-size="16" font-weight="700" fill="#0b2026">Synonyms</text>
-- MAGIC <text x="858" y="492" font-size="14" fill="#5E7077">Alternative terms for the same concept.</text>
-- MAGIC <rect x="20" y="540" width="1160" height="180" rx="10" fill="#F9F7F4" stroke="#EEEDE9" stroke-width="1"/>
-- MAGIC <text x="600" y="570" text-anchor="middle" font-size="17" font-weight="700" fill="#1B5162" letter-spacing="2">KEY BENEFITS</text>
-- MAGIC <circle cx="160" cy="620" r="30" fill="#00A972"/>
-- MAGIC <text x="160" y="630" text-anchor="middle" font-size="24" font-weight="700" fill="#FFFFFF">&#10003;</text>
-- MAGIC <text x="160" y="672" text-anchor="middle" font-size="16" font-weight="700" fill="#0b2026">Trusted and Consistent</text>
-- MAGIC <text x="160" y="694" text-anchor="middle" font-size="14" fill="#5E7077">one definition, everywhere</text>
-- MAGIC <circle cx="380" cy="620" r="30" fill="#1B5162"/>
-- MAGIC <text x="380" y="627" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">FAST</text>
-- MAGIC <text x="380" y="672" text-anchor="middle" font-size="16" font-weight="700" fill="#0b2026">Save Time</text>
-- MAGIC <text x="380" y="694" text-anchor="middle" font-size="14" fill="#5E7077">no more rebuilding logic</text>
-- MAGIC <circle cx="600" cy="620" r="30" fill="#4299E0"/>
-- MAGIC <text x="600" y="627" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">AI</text>
-- MAGIC <text x="600" y="672" text-anchor="middle" font-size="16" font-weight="700" fill="#0b2026">AI-Ready</text>
-- MAGIC <text x="600" y="694" text-anchor="middle" font-size="14" fill="#5E7077">Genie picks the right field</text>
-- MAGIC <circle cx="820" cy="620" r="30" fill="#FFAB00"/>
-- MAGIC <text x="820" y="630" text-anchor="middle" font-size="26" font-weight="700" fill="#FFFFFF">&#9733;</text>
-- MAGIC <text x="820" y="672" text-anchor="middle" font-size="16" font-weight="700" fill="#0b2026">Better Decisions</text>
-- MAGIC <text x="820" y="694" text-anchor="middle" font-size="14" fill="#5E7077">trustworthy metrics</text>
-- MAGIC <circle cx="1040" cy="620" r="30" fill="#FF5F46"/>
-- MAGIC <text x="1040" y="627" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">UC</text>
-- MAGIC <text x="1040" y="672" text-anchor="middle" font-size="16" font-weight="700" fill="#0b2026">Scale with Governance</text>
-- MAGIC <text x="1040" y="694" text-anchor="middle" font-size="14" fill="#5E7077">UC permissions and lineage</text>
-- MAGIC <text x="600" y="744" text-anchor="middle" font-size="14" font-style="italic" fill="#5E7077">Metric views bring together governed data, business logic, and rich metadata.</text>
-- MAGIC </svg>
-- MAGIC
-- MAGIC <div style="background: #1B5162; color: #FFFFFF; border-radius: 4px 4px 8px 8px; padding: 14px 24px; text-align: center; font-size: 14pt; margin-top: 12px;">
-- MAGIC <div style="margin-bottom: 10px;">
-- MAGIC <strong style="font-weight: 700;">Unity Catalog Metric Views docs</strong>&nbsp;&nbsp;
-- MAGIC <a href="https://docs.databricks.com/aws/en/metric-views/" target="_blank" style="color: #FFFFFF; font-weight: 700; text-decoration: underline; margin: 0 4px;">AWS</a> |
-- MAGIC <a href="https://learn.microsoft.com/en-us/azure/databricks/metric-views/" target="_blank" style="color: #FFFFFF; font-weight: 700; text-decoration: underline; margin: 0 4px;">Azure</a> |
-- MAGIC <a href="https://docs.databricks.com/gcp/en/metric-views/" target="_blank" style="color: #FFFFFF; font-weight: 700; text-decoration: underline; margin: 0 4px;">GCP</a>
-- MAGIC </div>
-- MAGIC <div style="border-top: 1px solid rgba(255,255,255,0.25); padding-top: 10px;">
-- MAGIC Want to go deeper? Check out the <a href="https://www.databricks.com/training/catalog/building-semantic-models-in-databricks-with-uc-metric-views-4962" target="_blank" style="color: #FFFFFF; font-weight: 700; text-decoration: underline;">Building Semantic Models in Databricks with UC Metric Views</a> Databricks training.
-- MAGIC </div>
-- MAGIC </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC **NOTE:** In this course, we focus on building and curating a Genie Agent directly. In production, many teams layer Genie on top of metric views to ensure consistent business semantics.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## D. Conclusion
-- MAGIC
-- MAGIC In this demo, you:
-- MAGIC
-- MAGIC 1. Previewed all five bakehouse gold tables and identified their key columns.
-- MAGIC 2. Reviewed the relationships between tables using primary and foreign keys.
-- MAGIC 3. Discovered that **21 out of 48 franchises** have a `supplierID` that does not match any record in the suppliers table. This is a data quality issue that can affect how Genie generates joins.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
-- MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
-- MAGIC <script>
-- MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
-- MAGIC </script>
