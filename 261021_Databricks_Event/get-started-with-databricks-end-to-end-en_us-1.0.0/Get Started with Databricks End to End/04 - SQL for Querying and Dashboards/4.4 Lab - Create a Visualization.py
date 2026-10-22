# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Lab: Create a visualization for your Bakehouse dashboard
# MAGIC ### Estimated Duration: ~5-10 minutes
# MAGIC
# MAGIC ## Learning objectives
# MAGIC
# MAGIC In this lab, you'll practice creating a new visualization and adding it to the **Bakehouse Dashboard** you created in the previous lesson. This hands-on exercise will reinforce your understanding of:
# MAGIC
# MAGIC * Creating datasets from SQL queries
# MAGIC * Configuring visualizations
# MAGIC * Adding visualizations to an existing dashboard
# MAGIC * Formatting and styling charts

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - Created AI/BI Dashboard
# MAGIC
# MAGIC <div style="border-left: 4px solid #FF5F46; background: rgba(255,95,70,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#98102A; margin-bottom:6px; font-size:15pt;">Prerequisites</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC
# MAGIC
# MAGIC You must complete the previous demonstration to update and publish the dashboard used in this demonstration.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ## A. Add a simple counter visualization
# MAGIC *This is a simple example for training purposes*.
# MAGIC
# MAGIC Let's add a counter visualization to the dashboard. This will be a simple counter, similar to the counter that Genie created for us. You'll build this one by hand so you understand how datasets, visualizations, and the canvas connect, knowledge you'll need when Genie's output isn't quite right.
# MAGIC
# MAGIC
# MAGIC 1. In the **Data** tab, select the **Add SQL dataset** option. 
# MAGIC
# MAGIC 2. Enter the following query into the query editing space:
# MAGIC
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='✓ Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">
# MAGIC   SELECT count(*) AS Total_Customers 
# MAGIC   FROM samples.bakehouse.sales_customers;</pre>
# MAGIC </div>
# MAGIC
# MAGIC
# MAGIC 3. Click **Run** to execute the query.
# MAGIC
# MAGIC 4. Right-click the query in the **Datasets** list and select **Rename**, or use the kebab menu, to rename the query as **Count Total Customers**.
# MAGIC
# MAGIC 5. Return to the **Untitled page** canvas tab.
# MAGIC
# MAGIC 6. At the bottom of the screen you have a toolbar for moving objects, adding a visualization, adding a text box, and adding a filter. 
# MAGIC     - Select the Genie Code icon on the left. 
# MAGIC
# MAGIC 7. In Genie's input field, enter the following:
# MAGIC
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='✓ Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">
# MAGIC Add a counter to the top of the dashboard, just below the "Bakehouse Main Dashboard" text box. The counter should show the count of total customers, based on the Count Total Customers dataset. Label the counter "Total Customers."</pre>
# MAGIC </div>
# MAGIC
# MAGIC 8. In the **Configuration Panel** on the right (between the canvas and Genie), click the kebab menu (⋮), and change the font color to the color of your choice
# MAGIC
# MAGIC > This is a simple visualization but lets you get a feel for manually working with Visualizations on dashboards. You can adjust the placement and size of the visualization by dragging the edges or click-holding while hovering over the visualization box.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Position Your widget and publish
# MAGIC
# MAGIC ### Position and resize
# MAGIC
# MAGIC Organize your dashboard for the best viewing experience:
# MAGIC
# MAGIC 1. **Move the widget**: Click and drag the visualization to reposition it
# MAGIC    * Try placing it near your other sales-related visualizations
# MAGIC    * Consider visual flow - group related metrics together
# MAGIC
# MAGIC 2. **Resize the widget**: Drag the edges or corners to adjust the size
# MAGIC    * Make it large enough to read comfortably
# MAGIC    * But not so large that it dominates the dashboard
# MAGIC
# MAGIC 3. **Rearrange other widgets** if needed to create a balanced layout
# MAGIC
# MAGIC ### Test your visualization
# MAGIC
# MAGIC Before republishing, verify everything works correctly:
# MAGIC 1. Click **Refresh** on the counter. 
# MAGIC 1. Confirm the number matches your earlier query result. 
# MAGIC
# MAGIC ### Republish your dashboard
# MAGIC
# MAGIC Now that the counter is ready, republish the dashboard to make the changes live:
# MAGIC
# MAGIC 1. Click the **Publish** button in the top right corner
# MAGIC 1. Click **Publish** to make your changes live
# MAGIC 1. Click the published version (**View published**) and confirm the new counter shows up.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. View the AI/BI Dashboard in Genie One
# MAGIC
# MAGIC 1. Open Genie One in a new tab.
# MAGIC
# MAGIC 2. Select **Dashboards** from the left navigation pane.
# MAGIC
# MAGIC 3. Browse the dashboards available to you.
# MAGIC    - You should see the dashboard you published.
# MAGIC    - Depending on your workspace and the permissions granted on other published dashboards, you may see additional dashboards.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
