# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Building Dashboards from Queries
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC In this demonstration, you build an interactive AI/BI Dashboard on the `samples.bakehouse` data. You create a new dashboard, use **Genie Code** with a natural language prompt to generate the visualizations, review the datasets Genie Code creates, and publish and share the finished dashboard.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lesson, you will be able to:
# MAGIC
# MAGIC 1. **Create** a new Databricks AI/BI Dashboard.
# MAGIC 2. **Use** Genie Code with a natural language prompt to generate dashboard visualizations.
# MAGIC 3. **Publish** a dashboard and manage sharing permissions for workspace and account users.

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
# MAGIC     Sample Data
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC This demo uses the `samples.bakehouse` dataset. Open each tool in a new tab so you can keep these instructions visible while you work.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Using the Sample Data
# MAGIC
# MAGIC You use the `bakehouse` sample dataset in the `samples` catalog. This dataset simulates a bakery franchise business with sales transactions, customer data, and franchise information.
# MAGIC
# MAGIC **Dataset location:**
# MAGIC
# MAGIC - **Catalog**: `samples`
# MAGIC - **Schema**: `bakehouse`
# MAGIC
# MAGIC This lesson uses the following tables as the source data for the dashboard visualizations:
# MAGIC
# MAGIC - **sales_transactions**: transaction-level sales data including products, prices, quantities, and payment information.
# MAGIC - **sales_customers**: customer demographic and contact information.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Create a New Dashboard
# MAGIC
# MAGIC 1. Right-click **Dashboards** in the left navigation bar and open the link in a new tab.
# MAGIC
# MAGIC 2. In the new tab, click **Create dashboard** in the upper-right corner.
# MAGIC
# MAGIC 3. At the top of the screen, click the dashboard name and change it to **FIRST_NAME_LAST_INITIALS_Bakehouse Dashboard**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Use Genie Code to Fill the Dashboard with Visualizations
# MAGIC
# MAGIC You can describe the dashboard you want in plain language, and **Genie Code** builds the visualizations and queries for you. This is faster than building each chart by hand, and you can edit the result afterward.
# MAGIC
# MAGIC 1. Copy the prompt below and enter it into the **Genie Code** input field.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='✓ Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Create a dashboard that uses the data found in the catalog, samples, and the schema, bakehouse. Include a counter based on the sum of the totalPrice column in the sales_transactions table. Also, create a combo chart that combines the data in sales_transactions and sales_customers. Create a bar chart with product on the x-axis and average totalPrice on the y-axis. Create a scatterplot of the sales_transactions data. Finally, there should be a text box at the top of the dashboard that says, "Bakehouse Main Dashboard".</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC Genie Code shows its thinking and progress in the **Genie Code** pane. The process can take a few minutes. Note a couple of things:
# MAGIC
# MAGIC 1. For this demo, if Genie Code asks for permission to run code, click **Allow**.
# MAGIC
# MAGIC 2. Genie Code detects and corrects errors as part of its normal process. If you see errors in the Genie Code panel, give it some time to note, correct, and implement the corrections.

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Review the Dashboard Data
# MAGIC
# MAGIC With a brand-new dashboard, you normally associate the dashboard with data before designing the display, but Genie Code has already done this for you. Take a look at the data sources it created.
# MAGIC
# MAGIC At the top of the dashboard screen, you have two tabs, **Data** and **Untitled page**.
# MAGIC
# MAGIC - **Data**: defines the datasets used in the dashboard. Datasets are bundled with dashboards when you share, import, or export them using the UI or API.
# MAGIC
# MAGIC - **Untitled page**: the dashboard canvas where you create visualizations and construct your dashboard. Each item on the canvas is called a **widget**. Widgets come in three types: visualizations, text boxes, and filters.
# MAGIC
# MAGIC 1. You start on the **Untitled page** tab. 
# MAGIC
# MAGIC 2. Select the **Data** tab to see the data sources.
# MAGIC
# MAGIC 3. Here you can see the data sources **Genie Code** used for the dashboard.
# MAGIC
# MAGIC 4. Click their names in the left column, under **Datasets**, to view their contents, measures, and dimensions. You can add additional datasets if you wish.

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Publishing and Sharing
# MAGIC
# MAGIC When your dashboard is complete, you can publish it and share it with others. When you publish a dashboard, the default setting is **Share data permission**.

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
# MAGIC     Data permission options
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC - **Share data permission**: viewers use your data permissions to access the data and power the queries behind the dashboard. This enables a shared cache, which can improve performance.
# MAGIC - **Individual data permission**: each viewer uses their own data permissions to run queries. This can lead to more frequent refresh operations, and viewers need access to both the underlying tables and the SQL warehouse to see the visualizations.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC To publish your dashboard, complete the following steps:
# MAGIC
# MAGIC 1. Click **Publish** in the upper-right corner of your dashboard.
# MAGIC
# MAGIC 2. In the **Publish** dialog, you will see two data permission options. Select **Share data permission**.
# MAGIC
# MAGIC 3. Optionally, notify viewers via email and describe your changes in the text field.
# MAGIC
# MAGIC 4. Click **Publish** in the lower-right corner of the dialog. The **Sharing** dialog opens afterward. If it does not open, select **Share** next to **Publish** at the top of the dashboard.
# MAGIC
# MAGIC    - Use the text field to search for individual users, or share the dashboard with a preconfigured group like **Admins** or **All workspace users**. From this window, you can grant leveled privileges like **Can Manage** or **Can Edit**. See <a href="https://docs.databricks.com/en/security/auth-authz/access-control/index.html#lakeview" target="_blank">Dashboard ACLs</a> for details on permissions.
# MAGIC    - The bottom of the **Sharing** dialog controls view access. Use this setting to share with all account users.
# MAGIC
# MAGIC 5. Under **Sharing settings**, choose **Anyone in my account can view** from the drop-down, then close the **Sharing** dialog. This makes the dashboard visible to every user in your Databricks account. For sensitive data, use **Specific users** instead.
# MAGIC
# MAGIC 6. Use the context icon at the top of the dashboard, next to the dashboard name, to switch between **Edit Draft** and **View Published** versions of your dashboard.

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
# MAGIC     Draft vs published
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC When you edit your draft dashboard, viewers of the published dashboard do not see your changes until you republish. The published dashboard includes visualizations built on queries that refresh as new data arrives. When dashboards are refreshed, they update with new data automatically and do not need to be republished.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this demo, you:
# MAGIC
# MAGIC 1. Created a new AI/BI Dashboard on the `samples.bakehouse` data.
# MAGIC 2. Used Genie Code with a natural language prompt to generate the dashboard visualizations.
# MAGIC 3. Reviewed the datasets Genie Code created on the **Data** tab.
# MAGIC 4. Published the dashboard and set sharing permissions for account users.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
