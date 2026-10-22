-- Databricks notebook source
-- MAGIC %md
-- MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Demo - Unity Catalog Foundations
-- MAGIC
-- MAGIC Databricks organizes objects in a three-level namespace: catalog &rarr; schema &rarr; object. In this demo, you create and manage catalogs, schemas, tables, and views using SQL.
-- MAGIC
-- MAGIC ## Learning objectives
-- MAGIC
-- MAGIC By the end of this demo, you should be able to:
-- MAGIC
-- MAGIC - **Explain** the three-level namespace introduced by Unity Catalog.
-- MAGIC - **Create** and manage catalogs, schemas, tables, and views in Unity Catalog.
-- MAGIC - **Execute** SQL commands to set defaults and inspect the objects you create.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## REQUIRED - Select a Compute Environment
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #FF5F46; background: rgba(255,95,70,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
-- MAGIC   <strong style="display:block; color:#98102A; margin-bottom:6px; font-size:15pt;">Select Serverless Compute</strong>
-- MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
-- MAGIC
-- MAGIC Before starting this notebook, select the required compute environment listed below.
-- MAGIC
-- MAGIC - **Serverless Compute, Version 5**
-- MAGIC
-- MAGIC ![Serverless Select](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/select-compute.png)
-- MAGIC
-- MAGIC <br></br>
-- MAGIC How to select an environment version:
-- MAGIC [AWS](https://docs.databricks.com/aws/en/compute/serverless/dependencies#-select-an-environment-version) |
-- MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies#-select-an-environment-version) |
-- MAGIC [GCP](https://docs.databricks.com/gcp/en/compute/serverless/dependencies#-select-an-environment-version)
-- MAGIC
-- MAGIC **NOTE:** This notebook requires **SQL and Python**, and was tested using **Serverless V5**. All-purpose compute may work but is not guaranteed to behave the same or support all features demonstrated.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## A. The Databricks Three-Level Namespace

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
-- MAGIC
-- MAGIC <!-- TITLE BAR -->
-- MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 20px 28px; margin-bottom: 18px;">
-- MAGIC   <div style="font-size: 22pt; font-weight: 700; margin-bottom: 6px;">How Unity Catalog Addresses Your Data</div>
-- MAGIC   <div style="font-size: 15pt; font-weight: 400; line-height: 1.45; opacity: 0.95;">Traditional SQL used two levels to find a table. Unity Catalog adds one more, a <b>catalog</b>, at the top.</div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- TWO-LEVEL vs THREE-LEVEL COMPARISON -->
-- MAGIC <div style="font-size: 0; width: 100%; margin-bottom: 22px;">
-- MAGIC
-- MAGIC   <!-- Two-level card -->
-- MAGIC   <div style="display: inline-block; width: 40%; margin-right: 2%; vertical-align: top; box-sizing: border-box; background: #F9F7F4; border-radius: 12px; border-top: 8px solid #C2C2C2; box-shadow: 0 2px 8px rgba(27,49,57,0.05); padding: 18px 20px 20px 20px;">
-- MAGIC     <div style="font-size: 12pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #5A6F77; margin-bottom: 10px;">Traditional &middot; Two levels</div>
-- MAGIC     <div style="font-family: Menlo, Consolas, monospace; font-size: 15pt; color: #0b2026; background: #FFFFFF; border: 1px solid #EEEDE9; border-radius: 6px; padding: 12px 14px; text-align: center;"><span style="color:#618794; font-weight:700;">database</span><span style="color:#B0B0B0;">.</span><span style="color:#618794; font-weight:700;">table</span></div>
-- MAGIC     <div style="font-size: 13pt; color: #5E7077; line-height: 1.5; margin-top: 12px;">A database name and an object name. That is as deep as it goes.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <!-- Three-level card -->
-- MAGIC   <div style="display: inline-block; width: 58%; vertical-align: top; box-sizing: border-box; background: #F9F7F4; border-radius: 12px; border-top: 8px solid #FF3621; box-shadow: 0 2px 8px rgba(27,49,57,0.08); padding: 18px 20px 20px 20px;">
-- MAGIC     <div style="font-size: 12pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #98102A; margin-bottom: 10px;">Unity Catalog &middot; Three levels</div>
-- MAGIC     <div style="font-family: Menlo, Consolas, monospace; font-size: 15pt; color: #0b2026; background: #FFFFFF; border: 1px solid #EEEDE9; border-radius: 6px; padding: 12px 14px; text-align: center;"><span style="color:#2272B4; font-weight:700;">catalog</span><span style="color:#B0B0B0;">.</span><span style="color:#00A972; font-weight:700;">schema</span><span style="color:#B0B0B0;">.</span><span style="color:#FF5F46; font-weight:700;">object</span></div>
-- MAGIC     <div style="font-size: 13pt; color: #5E7077; line-height: 1.5; margin-top: 12px;">A <b style="color:#2272B4;">catalog</b> at the top, a <b style="color:#00A972;">schema</b> inside it, and the <b style="color:#FF5F46;">object</b> you actually query.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- NESTED CONTAINMENT: catalog > schema > object -->
-- MAGIC <div style="font-size: 12pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #1B5162; margin-bottom: 12px;">Each level lives inside the one above it</div>
-- MAGIC
-- MAGIC <!-- Catalog container -->
-- MAGIC <div style="position: relative; border: 3px solid #2272B4; border-radius: 14px; background: rgba(34,114,180,0.05); padding: 40px 20px 20px 20px; margin-bottom: 8px;">
-- MAGIC   <div style="position: absolute; top: -14px; left: 20px; background: #2272B4; color: #ffffff; font-size: 11pt; font-weight: 700; letter-spacing: 1.5px; padding: 3px 14px; border-radius: 10px;">CATALOG &middot; sales</div>
-- MAGIC
-- MAGIC   <!-- Schema container -->
-- MAGIC   <div style="position: relative; border: 3px solid #00A972; border-radius: 12px; background: rgba(0,169,114,0.06); padding: 40px 18px 18px 18px;">
-- MAGIC     <div style="position: absolute; top: -14px; left: 18px; background: #00A972; color: #ffffff; font-size: 11pt; font-weight: 700; letter-spacing: 1.5px; padding: 3px 14px; border-radius: 10px;">SCHEMA &middot; orders</div>
-- MAGIC
-- MAGIC     <!-- Objects -->
-- MAGIC     <div style="font-size: 0;">
-- MAGIC       <span style="display: inline-block; vertical-align: top; background: #FFFFFF; border: 2px solid #FF5F46; border-radius: 8px; padding: 10px 16px; margin: 0 10px 0 0; font-size: 13pt; font-weight: 600; color: #0b2026;">tables<span style="display: inline-block; background: rgba(255,95,70,0.10); border: 1px solid #FF5F46; border-radius: 6px; padding: 2px 9px; margin-left: 8px; font-size: 10.5pt; font-weight: 600; color: #98102A;">views</span></span><span style="display: inline-block; vertical-align: top; background: #FFFFFF; border: 2px solid #FF5F46; border-radius: 8px; padding: 10px 16px; margin: 0 10px 0 0; font-size: 13pt; font-weight: 600; color: #0b2026;">volume</span><span style="display: inline-block; vertical-align: top; background: #FFFFFF; border: 2px solid #FF5F46; border-radius: 8px; padding: 10px 16px; margin: 0 10px 0 0; font-size: 13pt; font-weight: 600; color: #0b2026;">function</span><span style="display: inline-block; vertical-align: top; background: #FFFFFF; border: 2px solid #FF5F46; border-radius: 8px; padding: 10px 16px; margin: 0; font-size: 13pt; font-weight: 600; color: #0b2026;">model</span>
-- MAGIC     </div>
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- Full path readout -->
-- MAGIC <div style="text-align: center; font-family: Menlo, Consolas, monospace; font-size: 16pt; margin: 14px 0 22px 0;"><span style="color:#2272B4; font-weight:700;">sales</span><span style="color:#B0B0B0;">.</span><span style="color:#00A972; font-weight:700;">orders</span><span style="color:#B0B0B0;">.</span><span style="color:#FF5F46; font-weight:700;">transactions</span></div>
-- MAGIC
-- MAGIC <!-- WHY CATALOGS + USE -->
-- MAGIC <div style="font-size: 0; width: 100%;">
-- MAGIC
-- MAGIC   <!-- Why catalogs -->
-- MAGIC   <div style="display: inline-block; width: 58%; margin-right: 2%; vertical-align: top; box-sizing: border-box; background: #F9F7F4; border-radius: 10px; padding: 16px 18px 18px 18px; box-shadow: 0 2px 8px rgba(27,49,57,0.05);">
-- MAGIC     <div style="font-size: 14pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">Why a top-level catalog?</div>
-- MAGIC     <div style="font-size: 13.5pt; color: #0b2026; line-height: 1.55;">Catalogs are how teams carve up data at the highest level:</div>
-- MAGIC     <ul style="font-size: 13.5pt; color: #0b2026; line-height: 1.55; margin: 6px 0 0 0; padding-left: 20px;">
-- MAGIC       <li style="margin-bottom: 5px;">By <b>business unit</b>: sales, marketing, HR</li>
-- MAGIC       <li style="margin-bottom: 5px;">By <b>environment</b>: dev, staging, prod</li>
-- MAGIC       <li>As <b>sandboxes</b> for temporary datasets</li>
-- MAGIC     </ul>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <!-- USE shortcut -->
-- MAGIC   <div style="display: inline-block; width: 40%; vertical-align: top; box-sizing: border-box; background: #F9F7F4; border-radius: 10px; padding: 16px 18px 18px 18px; box-shadow: 0 2px 8px rgba(27,49,57,0.05);">
-- MAGIC     <div style="font-size: 14pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">Skip the full path with <code>USE</code></div>
-- MAGIC     <div style="font-size: 13pt; color: #5E7077; line-height: 1.5; margin-bottom: 8px;">Set a default catalog and schema so you can reference objects by name alone.</div>
-- MAGIC     <div style="font-family: Menlo, Consolas, monospace; font-size: 12.5pt; color: #0b2026; background: #FFFFFF; border: 1px solid #EEEDE9; border-radius: 6px; padding: 10px 12px; line-height: 1.6;">USE CATALOG sales;<br>USE SCHEMA orders;</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC ##### EXPAND FOR ADDITIONAL NOTES
-- MAGIC
-- MAGIC <details>
-- MAGIC
-- MAGIC ### How Unity Catalog addresses your data
-- MAGIC
-- MAGIC - The whole visual is about one idea: **where does a table live, and how do you name it.**
-- MAGIC - Traditional SQL used a **two-level** namespace, `database.table`. You had a database, and objects inside it. That was the deepest you could go.
-- MAGIC - Unity Catalog adds a **third level on top**, the **catalog**. So the full address is now `catalog.schema.object`.
-- MAGIC
-- MAGIC ### The three levels, top to bottom
-- MAGIC
-- MAGIC - **Catalog** — the top-tier container. Think of it as the biggest bucket you organize data into.
-- MAGIC - **Schema** — sits inside a catalog and groups related objects together. (You may hear "schema" and "database" used interchangeably; in Unity Catalog they are the same thing.)
-- MAGIC - **Object** — the thing you actually query or manage: a table, view, volume, function, or model.
-- MAGIC
-- MAGIC The nested boxes in the visual show this literally: the object lives inside the schema, and the schema lives inside the catalog. You reference any object by its full three-part path, for example `sales.orders.transactions`.
-- MAGIC
-- MAGIC ### Why the extra level helps
-- MAGIC
-- MAGIC - A catalog gives teams a clean way to carve up data at the highest level. Common patterns:
-- MAGIC   - **By business unit** — separate sales, marketing, and HR data.
-- MAGIC   - **By environment** — keep dev, staging, and prod apart (SDLC).
-- MAGIC   - **As sandboxes** — a throwaway space for temporary datasets.
-- MAGIC - You can have as many catalogs as you want, and each can hold as many schemas as you want.
-- MAGIC
-- MAGIC ### Writing less with USE
-- MAGIC
-- MAGIC - Typing `catalog.schema.object` every time gets tedious. The `USE` statements set a default catalog and schema:
-- MAGIC   - `USE CATALOG sales;`
-- MAGIC   - `USE SCHEMA orders;`
-- MAGIC - After that, you can reference an object by its name alone (for example `transactions`), and Databricks fills in the rest. You only need the full path when you want something outside your current defaults.
-- MAGIC
-- MAGIC </details>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Classroom Setup
-- MAGIC
-- MAGIC 1. Run the cell below. 
-- MAGIC     - It will create or use your personal catalog named **labuser_UNIQUE_ID**.

-- COMMAND ----------

-- DBTITLE 1,Setup
-- MAGIC %run ../Includes/Classroom-Setup-basic-catalog-setup

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## C. Create Data Containers and Objects
-- MAGIC
-- MAGIC In this section, let's explore how to create data containers and objects. This can be done in the UI or by using SQL and Python. We will focus on SQL.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C1. Catalogs

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Run the cell below to view available catalogs in your workspace.
-- MAGIC
-- MAGIC     Confirm you see a catalog named **labuser_YOUR_UNIQUE_ID**.
-- MAGIC         
-- MAGIC     - This was created for you in the previous classroom setup script.

-- COMMAND ----------

-- DBTITLE 1,Display Catalogs
SHOW CATALOGS;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. To create a catalog, you use the `CREATE CATALOG <catalog_name>` statement, as shown in the next code cell.
-- MAGIC
-- MAGIC     - **NOTE**: the `IF NOT EXISTS` keywords prevent an error if the catalog name already exists.
-- MAGIC     - The statement in the next cell is **commented out**, because in most training environments you will not have permission to create a catalog (see below). Your personal catalog was already created for you in the classroom setup.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #FF5F46; background: rgba(255,95,70,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
-- MAGIC   <strong style="display:block; color:#98102A; margin-bottom:6px; font-size:15pt;">Creating Catalogs May Be Restricted</strong>
-- MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
-- MAGIC
-- MAGIC Depending on your workspace, running the `CREATE CATALOG` statement might fail because you do not have permission to create catalogs:
-- MAGIC
-- MAGIC - In the **Databricks Academy** provided workspace (Vocareum), you **cannot** create catalogs.
-- MAGIC - In **Databricks Free Edition**, you do have the ability to create catalogs.
-- MAGIC - In your **organization's** workspace, you might not have permission either.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- DBTITLE 1,(Optional) Create Catalog
-- CREATE CATALOG IF NOT EXISTS ENTER_CATALOG_NAME;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Before setting your own default, run the cell below to see the **current** default catalog and schema.
-- MAGIC     - Setting a default catalog and schema lets you reference objects by name alone, so you can avoid writing the full three-level namespace every time.

-- COMMAND ----------

-- DBTITLE 1,Display Default Catalog and Schema
SELECT current_catalog() AS `Default Catalog`, current_schema() AS `Default Schema`

-- COMMAND ----------

-- DBTITLE 1,Py - Display Default Catalog and Schema
-- MAGIC %python
-- MAGIC # Python equivalent
-- MAGIC print("Default Catalog:", spark.catalog.currentCatalog())
-- MAGIC print("Default Schema: ", spark.catalog.currentDatabase())

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. A catalog named **labuser_UNIQUE_ID** has already been created for you for training purposes. 
-- MAGIC
-- MAGIC     Run the cell below to print your personal catalog name.

-- COMMAND ----------

-- DBTITLE 1,View Classroom Catalog Name
-- MAGIC %python
-- MAGIC ## Run this cell to get your classroom catalog name
-- MAGIC print(my_catalog)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Copy the catalog name printed above and paste it into the `USE CATALOG` statement below, replacing `ADD_CATALOG_NAME`. 
-- MAGIC
-- MAGIC     Then run the cell to set it as your default catalog.

-- COMMAND ----------

-- DBTITLE 1,Set Default Catalog
USE CATALOG ADD_CATALOG_NAME;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 6. Inspect the current catalog at any time using the `current_catalog()` function.
-- MAGIC     - If you set your catalog in the previous step, your default catalog is now your **labuser_UNIQUE_ID** catalog.

-- COMMAND ----------

-- DBTITLE 1,View Default Catalog
SELECT current_catalog()

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C2. Creating and Using a Schema

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. In the following code cell, we will:
-- MAGIC     * Create a schema named **example** within your **labuser_UNIQUE_ID** catalog set as the default above
-- MAGIC     * Select the **example** schema as the default schema
-- MAGIC     * Verify that our default schema is, indeed, **example**

-- COMMAND ----------

-- DBTITLE 1,Create Schema
-- Create a new schema
CREATE SCHEMA IF NOT EXISTS example;

-- Make our newly created schema the default
USE SCHEMA example;

-- Verify the current default schema
SELECT current_catalog(), current_schema();

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Manually view the catalog and schema without leaving this notebook by using the Workspace sidebar:
-- MAGIC    - Select the ![Schema Browser Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/schema-browser-icon.png "Schema Browser Icon") icon on the left.
-- MAGIC
-- MAGIC    - Expand your **labuser_UNIQUE_ID** catalog.
-- MAGIC
-- MAGIC    - Expand the **example** schema you created (if you don't see it, select the refresh icon ![refresh-icon.png](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/refresh-icon.png "Refresh Icon")).
-- MAGIC
-- MAGIC    - Leave the schema browser open on the left.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C3. Tables
-- MAGIC
-- MAGIC With all the necessary containers in place, let's turn our attention to creating some data objects.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC 1. Let's create a table named **patient_info**. For this example, we'll fill the table with a simple mock dataset containing synthetic patient heart rate data shortly.
-- MAGIC
-- MAGIC     Note the following:
-- MAGIC     * We only need to specify the table name when creating the table. We don't need to specify the containing catalog or schema because we already selected defaults earlier with the `USE` statements.
-- MAGIC     * The table will be a Unity Catalog managed table.
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
-- MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
-- MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">Creating other types of tables is possible, but beyond the scope of this course.</div>
-- MAGIC </div>

-- COMMAND ----------

-- DBTITLE 1,Create a Table
-- Create an empty silver table
CREATE OR REPLACE TABLE patient_info (
  device_id  INT,
  mrn        STRING,
  name       STRING,
  time       TIMESTAMP,
  heartrate  DOUBLE
);

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Run the `SHOW TABLES` statement to view tables in your current default catalog (**labuser_UNIQUE_ID**) and the schema you set earlier. 
-- MAGIC
-- MAGIC     In the results, you should see the table named **patient_info** in the **example** schema (database).

-- COMMAND ----------

-- DBTITLE 1,View Tables
SHOW TABLES;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Populate the **patient_info** table with some sample data.

-- COMMAND ----------

-- DBTITLE 1,Insert Records in a Table
INSERT OVERWRITE patient_info VALUES
  (23,'40580129','Nicholas Spears','2020-02-01T00:01:58.000+0000',54.0122153343),
  (17,'52804177','Lynn Russell','2020-02-01T00:02:55.000+0000',92.5136468131),
  (37,'65300842','Samuel Hughes','2020-02-01T00:08:58.000+0000',52.1354807863),
  (23,'40580129','Nicholas Spears','2020-02-01T00:16:51.000+0000',54.6477014191),
  (17,'52804177','Lynn Russell','2020-02-01T00:18:08.000+0000',95.033344842),
  (37,'65300842','Samuel Hughes','2020-02-01T00:23:58.000+0000',57.3391541312),
  (23,'40580129','Nicholas Spears','2020-02-01T00:31:58.000+0000',56.6165053697),
  (17,'52804177','Lynn Russell','2020-02-01T00:32:56.000+0000',94.8134313932),
  (37,'65300842','Samuel Hughes','2020-02-01T00:38:54.000+0000',56.2469995332),
  (23,'40580129','Nicholas Spears','2020-02-01T00:46:57.000+0000',54.8372685558),
  (23,'40580129',NULL,'2020-02-01T00:01:58.000+0000',54.0122153343),
  (17,'52804177',NULL,'2020-02-01T00:02:55.000+0000',92.5136468131),
  (37,'65300842',NULL,'2020-02-01T00:08:58.000+0000',1000052.1354807863),
  (23,'40580129',NULL,'2020-02-01T00:16:51.000+0000',54.6477014191),
  (17,'52804177','Lynn Russell','2020-02-01T00:18:08.000+0000',9),
  (37,'65300842','Samuel Hughes','2020-02-01T00:23:58.000+0000',7),
  (23,'40580129','Nicholas Spears','2020-02-01T00:31:58.000+0000',6),
  (17,'52804177','Lynn Russell','2020-02-01T00:32:56.000+0000',5),
  (37,'65300842','Samuel Hughes','2020-02-01T00:38:54.000+0000',9000),
  (23,'40580129','Nicholas Spears','2020-02-01T00:46:57.000+0000',66),
  (23,'40580129',NULL,'2020-02-01T00:01:58.000+0000',54.0122153343),
  (17,'52804177',NULL,'2020-02-01T00:02:55.000+0000',92.5136468131),
  (37,'65300842',NULL,'2020-02-01T00:08:58.000+0000',1000052.1354807863),
  (23,'40580129',NULL,'2020-02-01T00:16:51.000+0000',54.6477014191),
  (17,'52804177','Lynn Russell','2020-02-01T00:18:08.000+0000',98),
  (37,'65300842','Samuel Hughes','2020-02-01T00:23:58.000+0000',90),
  (23,'40580129','Nicholas Spears','2020-02-01T00:31:58.000+0000',60),
  (17,'52804177','Lynn Russell','2020-02-01T00:32:56.000+0000',50),
  (37,'65300842','Samuel Hughes','2020-02-01T00:38:54.000+0000',30),
  (23,'40580129','Nicholas Spears','2020-02-01T00:46:57.000+0000',80);

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Execute queries on the created table to examine its contents, ensuring that the data is correctly stored and accessible for analysis purposes.

-- COMMAND ----------

-- DBTITLE 1,View Table
-- View the rows inside the patient_info table
SELECT * 
FROM patient_info;

-- COMMAND ----------

-- DBTITLE 1,Py - View Table
-- MAGIC %python
-- MAGIC # Python equivalent
-- MAGIC df = spark.table("patient_info")
-- MAGIC
-- MAGIC display(df)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C4. Creating and Managing Views
-- MAGIC
-- MAGIC 1. Let's create a **vw_gold** view that presents an aggregated version of the **patient_info** table data by averaging heart rate data per patient on a daily basis. 
-- MAGIC
-- MAGIC     In the following cell, we will:
-- MAGIC     - Create the view
-- MAGIC     - Query the view

-- COMMAND ----------

-- DBTITLE 1,Create View
-- Create a gold view
CREATE OR REPLACE VIEW vw_gold AS (
  SELECT 
    mrn, 
    name, 
    MEAN(heartrate) AS avg_heartrate, 
    DATE_TRUNC("DD", time) AS date
  FROM patient_info
  WHERE name IS NOT NULL
  GROUP BY mrn, name, DATE_TRUNC("DD", time)
);


-- View the rows inside the gold view
SELECT * 
FROM vw_gold;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC # Python equivalent (creates a temp view)
-- MAGIC
-- MAGIC from pyspark.sql import functions as F
-- MAGIC
-- MAGIC # Build the gold aggregation with the DataFrame API
-- MAGIC gold_df = (
-- MAGIC     spark.table("patient_info")
-- MAGIC     .where(F.col("name").isNotNull())
-- MAGIC     .groupBy("mrn", "name", F.date_trunc("DD", F.col("time")).alias("date"))
-- MAGIC     .agg(F.mean("heartrate").alias("avg_heartrate"))
-- MAGIC     .select("mrn", "name", "avg_heartrate", "date")
-- MAGIC )
-- MAGIC
-- MAGIC # Register it as a temporary view (session-scoped, not a persistent Unity Catalog view)
-- MAGIC gold_df.createOrReplaceTempView("vw_gold_py")
-- MAGIC
-- MAGIC # View the rows
-- MAGIC display(gold_df)
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Use the `SHOW VIEWS` statement to display all available views. 
-- MAGIC
-- MAGIC     Run the cell and view the results. 
-- MAGIC     
-- MAGIC     Notice that we have a view named **vw_gold**, and a temporary view named **vw_gold_py**.

-- COMMAND ----------

-- DBTITLE 1,Show Views
SHOW VIEWS;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D.  View Objects in the Workspace Sidebar
-- MAGIC
-- MAGIC 1. View the new objects without leaving this notebook by using the schema browser:
-- MAGIC    - If it's not already open, select the ![Schema Browser Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/schema-browser-icon.png "Schema Browser Icon") (schema browser icon) icon on the left.
-- MAGIC
-- MAGIC    - If the schema browser is already open, you may need to refresh it by clicking ![refresh-icon.png](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/refresh-icon.png "Refresh Icon") (refresh icon)
-- MAGIC
-- MAGIC    - Expand your **labuser_UNIQUE_ID** catalog.
-- MAGIC
-- MAGIC    - Expand the **example** schema you created.
-- MAGIC
-- MAGIC    Note the table(s) and view are both displayed (The temporary view is not shown).

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
-- MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
-- MAGIC <script>
-- MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
-- MAGIC </script>
