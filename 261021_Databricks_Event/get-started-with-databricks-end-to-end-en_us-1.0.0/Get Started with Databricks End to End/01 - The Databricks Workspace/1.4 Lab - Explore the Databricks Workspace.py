# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Lab - Explore the Databricks Workspace
# MAGIC ### Estimated Duration: ~10 minutes
# MAGIC
# MAGIC This lab is your chance to **practice on your own** everything you have seen so far in this module: navigating the workspace, switching between Lakehouse and Genie One, and working in a notebook with real data.
# MAGIC
# MAGIC Work through the tasks below at your own pace. The steps tell you **what** to do, not always exactly how, so you get comfortable finding your way around.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lab, you should be able to:
# MAGIC
# MAGIC - **Navigate** the workspace sidebar and open workspace assets.
# MAGIC - **Switch** between the Lakehouse UI and Genie One with the app switcher.
# MAGIC - **Run** Python, SQL, and markdown in a notebook, and analyze data with a DataFrame.
# MAGIC - **Build** a visualization from a query result.

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
# MAGIC ## A. Navigate the Workspace
# MAGIC
# MAGIC Practice moving around the workspace, like you did in the workspace tour.
# MAGIC
# MAGIC **On your own:**
# MAGIC
# MAGIC - Open the **left sidebar** and find **Workspace**, **Catalog**, and **Compute**.
# MAGIC
# MAGIC - In **Workspace**, browse to the folder that holds this notebook.
# MAGIC
# MAGIC - Open **Compute** and confirm you have a **Serverless** resource available.
# MAGIC
# MAGIC - Use the **search bar** at the top to search for this notebook by name.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Switch Between Lakehouse and Genie One
# MAGIC
# MAGIC You are currently in the **Lakehouse** workspace UI. Practice moving to **Genie One** and back.
# MAGIC
# MAGIC **On your own:**
# MAGIC
# MAGIC - Click the **app switcher** (the "waffle" icon, top-right).
# MAGIC
# MAGIC - Right-click **Genie One** and open it in a **new browser tab**, so you keep this lab open.
# MAGIC
# MAGIC - On the Genie One home page, find the **search bar** and the **left panel** of assets.
# MAGIC
# MAGIC - Switch back to this **Lakehouse** tab to continue.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Work in This Notebook
# MAGIC
# MAGIC Practice the notebook skills from the last lesson, this time against the real **samples.bakehouse** sales data.
# MAGIC
# MAGIC ### C1. Run Python and SQL
# MAGIC
# MAGIC 1. Run the **Python** cell below (**Shift + Enter**).
# MAGIC
# MAGIC 2. Run the **SQL** cell below it, and review the 10 rows of sales data returned.

# COMMAND ----------

# Run this Python cell
print("Hello from the workspace lab!")
print("5 * 4 =", 5 * 4)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Preview the bakehouse sales data
# MAGIC SELECT *
# MAGIC FROM samples.bakehouse.sales_transactions
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ### C2. Load the Data into a DataFrame
# MAGIC
# MAGIC Run the cell below. It loads the sales table into a DataFrame variable and previews it with `display()`. The `sales_df` variable stays available in the cells that follow.

# COMMAND ----------

# Load the sales data into a DataFrame and preview it
sales_df = spark.table("samples.bakehouse.sales_transactions")
display(sales_df.limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC ### C3. Aggregate and Visualize
# MAGIC
# MAGIC 1. Run the cell below to calculate total revenue by product.
# MAGIC
# MAGIC 2. Then build a chart from the result:
# MAGIC
# MAGIC    - Click the **+** icon above the results table and select **Visualization**.
# MAGIC    - Choose a **Bar** chart.
# MAGIC    - Set the **X column** to `product` and the **Y column** to `total_revenue`.
# MAGIC
# MAGIC **On your own:**
# MAGIC
# MAGIC - Add a **markdown cell** (`%md`) below the chart with a short heading and a bullet or two describing what you found.
# MAGIC
# MAGIC - Click **Run all** at the top to run the whole notebook top to bottom.

# COMMAND ----------

from pyspark.sql import functions as F

# Total revenue per product, highest first
product_revenue = (
    sales_df.groupBy("product")
    .agg(F.sum("totalPrice").alias("total_revenue"))
    .orderBy(F.desc("total_revenue"))
)

display(product_revenue)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lab, you:
# MAGIC
# MAGIC 1. Navigated the workspace sidebar and searched for assets.
# MAGIC 2. Switched between the Lakehouse UI and Genie One with the app switcher.
# MAGIC 3. Ran Python and SQL, loaded the bakehouse data into a DataFrame, and built a revenue-by-product chart.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
