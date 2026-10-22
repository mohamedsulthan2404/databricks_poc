# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Ingesting Data via File Upload
# MAGIC
# MAGIC One of the simplest ways to bring data into Databricks is to upload it directly from your local machine. In this lesson, you upload a CSV file, create a Unity Catalog table from it, and explore the result.
# MAGIC
# MAGIC ## Learning objectives
# MAGIC
# MAGIC By the end of this lesson, you should be able to:
# MAGIC
# MAGIC - **Upload** a CSV file from your local machine into Databricks.
# MAGIC - **Create** a Unity Catalog table from the uploaded file.
# MAGIC - **Configure** column names and data types during the upload.
# MAGIC - **Explore** the table using both the Catalog UI and SQL.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - Select a Compute Environment
# MAGIC
# MAGIC <div style="border-left: 4px solid #FF5F46; background: rgba(255,95,70,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#98102A; margin-bottom:6px; font-size:15pt;">Select Serverless Compute</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC
# MAGIC Before starting this notebook, select the required compute environment listed below.
# MAGIC
# MAGIC - **Serverless Compute, Version 5**
# MAGIC
# MAGIC ![Serverless Select](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/select-compute.png)
# MAGIC
# MAGIC <br></br>
# MAGIC How to select an environment version:
# MAGIC [AWS](https://docs.databricks.com/aws/en/compute/serverless/dependencies#-select-an-environment-version) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies#-select-an-environment-version) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/compute/serverless/dependencies#-select-an-environment-version)
# MAGIC
# MAGIC **NOTE:** This notebook requires **SQL and Python**, and was tested using **Serverless V5**. All-purpose compute may work but is not guaranteed to behave the same or support all features demonstrated.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Classroom Setup
# MAGIC
# MAGIC 1. Run the cell below. 
# MAGIC     - It will create or use your personal catalog named **labuser_UNIQUE_ID**.
# MAGIC     - Create the **example** schema if necessary.
# MAGIC     - Sets your default catalog to **labuser_UNIQUE_ID** and the default schema to **example**.

# COMMAND ----------

# DBTITLE 1,Setup
# MAGIC %run ../Includes/Classroom-Setup-catalog-schema-setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Download the CSV File
# MAGIC
# MAGIC In the same folder as this notebook, there is a data file named **cust_service_data.csv**. Download it so you can upload it in the next section.
# MAGIC
# MAGIC 1. If it is not already open, click the ![Workspace Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/workspace-icon.png "Workspace Icon") **Workspace** icon just to the right of the left navigation bar.
# MAGIC
# MAGIC 2. Hover over the **cust_service_data.csv** file and click the three-dot (kebab) menu to the right of the file name.
# MAGIC
# MAGIC 3. Click **Download**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Create a Table from the File
# MAGIC
# MAGIC Now create a table by uploading the file you just downloaded.
# MAGIC
# MAGIC 1. Right-click **Catalog** in the left navigation bar and select **Open Link in New Tab**. 
# MAGIC     - This keeps this notebook open while you work.
# MAGIC
# MAGIC 2. In the new tab, open your **labuser_UNIQUE_ID** catalog, then the **example** schema.
# MAGIC
# MAGIC 3. In the upper-right corner, click **Create** > **Table**.
# MAGIC
# MAGIC 4. Drag the **cust_service_data.csv** file you downloaded onto the drop zone.
# MAGIC
# MAGIC 5. Click the downward-facing arrow to the right of the **interaction_id** column name and select **Exclude column**. 
# MAGIC     - The column is grayed out and will not be included in the table.
# MAGIC     
# MAGIC 6. Name the table **cust_service_data**.
# MAGIC
# MAGIC 7. Click **Create table**.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC   
# MAGIC Databricks pre-selects your **labuser_UNIQUE_ID** catalog and **example** schema (because you navigated to them), fills in a table name based on the file name, and infers the column names and data types from the file. You can change a column name or type by clicking it. The inferred values here are correct, so you can leave them as they are.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Explore the Data

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### D1. Explore with the Catalog Explorer UI
# MAGIC
# MAGIC 1. In the Catalog tab you opened, confirm you are in your **labuser_UNIQUE_ID** catalog and **example** schema.
# MAGIC
# MAGIC 2. Click the **cust_service_data** table to view its columns, sample data, and details.
# MAGIC
# MAGIC     **NOTE:** We will cover the **Catalog Explorer** in more detail in the next lesson.

# COMMAND ----------

# MAGIC %md
# MAGIC ### D2. Explore with SQL
# MAGIC
# MAGIC You can also read the table right here in the notebook. 
# MAGIC
# MAGIC 1. Run the cell below to view the **cust_service_data** table you just created.

# COMMAND ----------

# DBTITLE 1,SQL Query Table
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM cust_service_data

# COMMAND ----------

# DBTITLE 1,Python Query Table
## Python equivalent
df = spark.table("cust_service_data")

display(df)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
