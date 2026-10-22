# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Managing Queries
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC In this demonstration, you organize the queries you save in the Databricks SQL Editor. You save a query to the workspace, arrange your saved queries into folders, tag them, and use query history to find and revisit previous runs.
# MAGIC
# MAGIC All examples use the `samples.bakehouse` dataset.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lesson, you will be able to:
# MAGIC
# MAGIC 1. **Save** a query to the workspace and give it a descriptive name.
# MAGIC 2. **Organize** queries into folders and apply tags.
# MAGIC 3. **Use** query history to review and recover past runs.

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
# MAGIC     Work in the SQL Editor
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC All examples use the `samples.bakehouse` dataset. Run these queries in the SQL Editor, and open it in a new tab so you can keep these instructions visible while you work.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Create and Save a Query
# MAGIC
# MAGIC You start by writing a query, running it, and saving it to the workspace so you can find it again later.

# COMMAND ----------

# MAGIC %md
# MAGIC 1. In the far left sidebar, right-click **SQL Editor** and open the link in a new tab.
# MAGIC
# MAGIC 2. Create a new query.
# MAGIC
# MAGIC 3. In the SQL Editor, set the query context at the top:
# MAGIC
# MAGIC    - **Catalog**: `samples`
# MAGIC    - **Schema**: `bakehouse`
# MAGIC
# MAGIC 4. Copy the query below and paste it into the editor.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Customer Purchase Summary Query</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='✓ Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">-- Customer Purchase Summary
# MAGIC SELECT
# MAGIC   c.customerID,
# MAGIC   c.first_name,
# MAGIC   c.last_name,
# MAGIC   c.state,
# MAGIC   COUNT(t.transactionID) AS total_purchases,
# MAGIC   SUM(t.totalPrice) AS total_spent,
# MAGIC   AVG(t.totalPrice) AS avg_transaction_value
# MAGIC FROM samples.bakehouse.sales_customers c
# MAGIC JOIN samples.bakehouse.sales_transactions t
# MAGIC   ON c.customerID = t.customerID
# MAGIC GROUP BY c.customerID, c.first_name, c.last_name, c.state
# MAGIC ORDER BY total_spent DESC
# MAGIC LIMIT 50;</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC 5. Click **Run** to execute the query, and review the results.
# MAGIC
# MAGIC 6. Save the query to the workspace by giving it a name (`bakehouse_query_YOUR_INITIALS`). 
# MAGIC     - Click the query's current name in the tab at the top of the query editor and enter a descriptive name.

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
# MAGIC     Best practices for query names
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC - Use descriptive names. The SQL Editor's query list shows the name, and teammates searching for your work will see it too.
# MAGIC - Include the purpose or audience, for example `Finance - Revenue Report`.
# MAGIC - Use consistent naming conventions across your team.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Organizing Queries
# MAGIC
# MAGIC By default, queries are saved in your **Home** folder. Folders and tags help you and your team find them as the number of saved queries grows.

# COMMAND ----------

# MAGIC %md
# MAGIC ### B1. Create Folders for Organization
# MAGIC
# MAGIC 1. In the left sidebar, right-click **Workspace** and open the link in a new tab.
# MAGIC
# MAGIC 2. Click **Home** in the upper-left. You will see the query you saved above.
# MAGIC
# MAGIC 3. Click the **Create** button in the upper-right and select **Folder**.
# MAGIC
# MAGIC 4. Name the folder, for example `Bakehouse Analytics`. You are taken into the new folder.
# MAGIC
# MAGIC 5. Go back to your Home folder by clicking **Home** in the upper-left.
# MAGIC
# MAGIC 6. Drag and drop your saved query into the folder.
# MAGIC
# MAGIC 7. You can create nested folders for deeper organization, similar to any computer's file system:
# MAGIC
# MAGIC    - `Marketing Reports` then `Customer Segmentation`
# MAGIC    - `Sales Analytics` then `Daily Reports`, `Monthly Reports`

# COMMAND ----------

# MAGIC %md
# MAGIC ### B2. Add Tags to Queries
# MAGIC
# MAGIC 1. Open your saved query.
# MAGIC
# MAGIC 2. Click the **three dots (⋮)** menu at the top of the query editor. 
# MAGIC
# MAGIC 3. Select the (⋮) > **File** > **Edit query tags**.
# MAGIC
# MAGIC 4. Save tags such as:
# MAGIC
# MAGIC    - `customer-analytics`
# MAGIC    - `sales`
# MAGIC    - `monthly-report`
# MAGIC    - `executive-dashboard`
# MAGIC

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
# MAGIC     Best practices for organizing queries
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC
# MAGIC - Group queries by department (Marketing, Finance, Sales).
# MAGIC - Group by frequency (Daily, Weekly, Monthly).
# MAGIC - Group by data domain (Customers, Products, Transactions).
# MAGIC - Use tags for cross-cutting concerns (urgent, deprecated, production).
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Query History
# MAGIC
# MAGIC Query history lets you revisit past runs of a query without re-executing it.

# COMMAND ----------

# MAGIC %md
# MAGIC ### C1. Access Query History
# MAGIC
# MAGIC 1. Open and run any saved query in the SQL Editor.
# MAGIC
# MAGIC 2. In the upper-right of the results section, click the **Open Execution History** icon to see information about past runs.
# MAGIC
# MAGIC     ![History](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/query-execution-history.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### C2. Review Past Query Results
# MAGIC
# MAGIC 1. In the Query History panel, click any past execution.
# MAGIC
# MAGIC 2. From there you can:
# MAGIC
# MAGIC    - **View the results** from that specific run.
# MAGIC    - **See the exact query** that was executed, which is useful if the query has since been modified.
# MAGIC    - **Download historical results** from past runs.
# MAGIC    - **Check execution details** such as duration and rows returned.

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
# MAGIC     Query history use cases
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC
# MAGIC - **Debugging**: Compare results from different runs to identify when data changed.
# MAGIC - **Audit**: Track who ran queries and when.
# MAGIC - **Performance**: Identify slow queries by comparing execution times.
# MAGIC - **Recovery**: Access results from a previous run without re-executing.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

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
# MAGIC     Result Retention
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Query results are retained for 30 days by default.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this demo, you:
# MAGIC
# MAGIC 1. Created and saved a query to the workspace with a descriptive name.
# MAGIC 2. Organized saved queries into folders and applied tags to make them easy to find.
# MAGIC 3. Used query history to review and recover the results of past runs.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
