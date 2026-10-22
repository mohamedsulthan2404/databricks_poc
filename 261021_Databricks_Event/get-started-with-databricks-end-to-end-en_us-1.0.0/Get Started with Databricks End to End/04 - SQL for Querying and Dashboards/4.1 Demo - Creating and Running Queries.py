# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Creating and Running Queries
# MAGIC
# MAGIC In this demonstration, you write SQL queries using the Databricks SQL Editor.
# MAGIC
# MAGIC ## Learning objectives
# MAGIC
# MAGIC By the end of this lesson, you should be able to:
# MAGIC
# MAGIC - **Open** the SQL Editor.
# MAGIC - **Run** a query against the bakehouse data.
# MAGIC - **Save** and rerun a query.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. The Databricks SQL Editor
# MAGIC
# MAGIC The SQL Editor is a dedicated environment for writing and running SQL queries. Use it when you want a focused SQL workspace, separate from notebooks. You might prefer this editor, especially if you have experience with one in another SQL development environment. In Databricks, the SQL Editor gives you a more developer-focused experience with specific features.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <!-- TITLE BAR -->
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 20px 28px; margin-bottom: 18px;">
# MAGIC   <div style="font-size: 22pt; font-weight: 700; margin-bottom: 6px;">The Databricks SQL Editor</div>
# MAGIC   <div style="font-size: 15pt; font-weight: 400; line-height: 1.45; opacity: 0.95;">A unified, streamlined place to write and run SQL, separate from notebooks, for exploring data, building visualizations, and developing queries.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- FEATURE GRID: ROW 1 -->
# MAGIC <div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; margin-bottom: 24px;">
# MAGIC
# MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #4299E0;">
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">AI assistant &amp; Quick Fix</div>
# MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55;">Genie helps you write and optimize SQL, and <b>Quick Fix</b> resolves common typos and syntax errors in seconds.</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #00A972;">
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">Multiple statement results</div>
# MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55;">Run several SQL statements at once and page through each result set in a single view.</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #FF5F46;">
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">AI-generated filters</div>
# MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55;">Filter your results with plain language, no need to rewrite or rerun the query.</div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- FEATURE GRID: ROW 2 -->
# MAGIC <div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; margin-bottom: 22px;">
# MAGIC
# MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #FFAB00;">
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">Inline history</div>
# MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55;">Jump back to past results and compare run times and statuses without re-executing a query.</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #98102A;">
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">Real-time collaboration</div>
# MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55;">Co-edit a query with teammates, see who is active, and leave inline comments right in the code.</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #4299E0;">
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">Built for productivity</div>
# MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55;">Split-screen editing, code folding, a command palette, custom themes, parameters, and Git support.</div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- NOTE -->
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 0;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">When to use it</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">Reach for the SQL Editor when you want a focused, developer-style SQL workspace. If you have used a SQL editor in another tool, this will feel familiar. You can still write SQL in notebooks, however the SQL Editor just gives SQL its own dedicated home.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Open and Use the SQL Editor

# COMMAND ----------

# MAGIC %md
# MAGIC ### B1. Opening and using the SQL editor
# MAGIC
# MAGIC 1. In the far left sidebar menu, right click on **SQL Editor** and open the link in a new tab. This will take you to the SQL editor.
# MAGIC
# MAGIC 2. Click the **SQL Query** button under the *Create New* section.
# MAGIC     - Or click the **plus icon (`+`)** next to *New tab* and select **New Query** to start a fresh SQL editor session.
# MAGIC
# MAGIC 3. Copy the directions below and paste them into the query editor. Then follow those instructions.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">SQL Editor Steps</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='✓ Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">
# MAGIC ------------------------------------
# MAGIC -- Demonstration Directions
# MAGIC ------------------------------------
# MAGIC
# MAGIC
# MAGIC
# MAGIC -- 1. Ensure that the "New SQL editor" option is turned on at the top of the screen.
# MAGIC     -- a. Click on the kebab menu (⋮)
# MAGIC     -- b. At the bottom it should say "New SQL editor ON"
# MAGIC
# MAGIC -- 2. At the top right, drop open "Connect", and select "shared_warehouse" if necessary.
# MAGIC     -- You may need to click "More..."
# MAGIC
# MAGIC -- 3. In the dropdown above, select your default catalog and schema:
# MAGIC     -- Select the "samples" catalog
# MAGIC     -- Select the "bakehouse" schema
# MAGIC     -- This will manually set the default catalog and schema for this query.
# MAGIC
# MAGIC -- 4. Highlight the SELECT statement below and click the "Run selected" button above.
# MAGIC     -- You may need to select "Start new session" if asked.
# MAGIC     -- Confirm in the results section below that your default catalog is "samples" and your current schema is "bakehouse".
# MAGIC
# MAGIC SELECT current_catalog(), current_schema();
# MAGIC
# MAGIC -- 5. Highlight the SELECT statement below and click the "Run selected" button above.
# MAGIC     -- Confirm that the results show 10 rows from the "sales_customers" table.
# MAGIC
# MAGIC SELECT *
# MAGIC FROM sales_customers
# MAGIC LIMIT 10;
# MAGIC
# MAGIC -- 6. Highlight both SELECT statements below and click the "Run selected" button above.
# MAGIC
# MAGIC SELECT *
# MAGIC FROM sales_customers
# MAGIC LIMIT 10;
# MAGIC
# MAGIC SELECT *
# MAGIC FROM sales_transactions
# MAGIC LIMIT 10;
# MAGIC
# MAGIC -- 7. Check the output window below. It should display 'Results n of 2'.
# MAGIC     -- Click the forward or backward arrow to view the other result. When running multiple queries with results, you can scroll through the output.
# MAGIC
# MAGIC -- 8. Click the dropdown next to 'Table' on either of the results below.
# MAGIC     -- You will see multiple options to download or copy the results.
# MAGIC
# MAGIC -- 9. Click the '+' icon next to either of the results below.
# MAGIC     -- This allows you to create visualizations based on the SQL results. The same thing can be done in a Databricks notebook.
# MAGIC
# MAGIC -- 10. By default, the SQL editor is configured to return only 1000 rows. This can speed up development.
# MAGIC     -- We need to configure the editor to return all results.
# MAGIC     --  a. Click the "Run all" dropdown and uncheck "LIMIT 1000"
# MAGIC     --  b. Now, select and run the query below to view rows in the "sales_transactions" table.
# MAGIC     -- The query returns 3,333 rows.
# MAGIC
# MAGIC SELECT *
# MAGIC FROM sales_transactions;
# MAGIC
# MAGIC -- 11. We will then filter the results using natural language filters generated by AI. Complete the following:
# MAGIC --  a. Click the filter icon in the results output below (on the far right of the output section).
# MAGIC --  b. In the filter popup, type 'totalPrice less than 50'.
# MAGIC --  c. Notice that the results are filtered using natural language, and 3200 rows are shown.
# MAGIC
# MAGIC -- 12. Save the query:
# MAGIC -- The first time you save a query, you can simply give the query a name.
# MAGIC -- Once a query has been saved once, you save changes to the query by clicking "Save" in the upper-right.
# MAGIC     --  a. Give the query a name by clicking in the query's current name (in the tab at the top of the query editor)
# MAGIC     -- The query is saved to your home folder.
# MAGIC     --  b. Click the "Save" button in the upper-right corner to save future changes to the query.
# MAGIC
# MAGIC -- 13. To share a query, click the "Share" command at the top right. Close the share.
# MAGIC
# MAGIC -- 14. Run the query below and view the results.
# MAGIC SELECT
# MAGIC   paymentMethod, count(*) AS total_transactions
# MAGIC FROM sales_transactions
# MAGIC GROUP BY paymentMethod;
# MAGIC
# MAGIC --  a. Notice that the filter you set earlier is still shown. Select the 'X' to remove the filter.
# MAGIC   </pre>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
