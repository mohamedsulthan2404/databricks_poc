# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Lab - Use a Genie Agent
# MAGIC ### Estimated Duration: ~20-30 minutes
# MAGIC
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC In this short hands-on lab, you use a **Genie Agent** to analyze the `bakehouse` data using natural language. You ask a question, refine it for a better answer, and then ask a more powerful question that spans multiple tables. This lab takes about 10 minutes.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lab, you will be able to:
# MAGIC
# MAGIC 1. **Ask** a business question in a Genie Agent and interpret the result.
# MAGIC 2. **Refine** a question to get a more precise answer.
# MAGIC 3. **Ask** a question that Genie answers by joining multiple tables.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - Created Genie Agent
# MAGIC
# MAGIC <div style="border-left: 4px solid #FF5F46; background: rgba(255,95,70,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#98102A; margin-bottom:6px; font-size:15pt;">Prerequisites</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC
# MAGIC
# MAGIC Completion of the previous notebook, which creates the Bakehouse Genie Agent used in this lab.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Ask a Basic Question
# MAGIC
# MAGIC Open your **Bakehouse** Genie Agent and ask the following questions, one at a time. After each answer, click **Show code** to see the SQL Genie generated.
# MAGIC
# MAGIC 1. Ask a simple aggregation:
# MAGIC
# MAGIC    > *What is the total revenue?*
# MAGIC
# MAGIC    You should get a single number ($66,471). Notice how Genie sums the totalPrice column.
# MAGIC
# MAGIC 2. Break the total down by category:
# MAGIC
# MAGIC    > *Show me revenue by product*
# MAGIC
# MAGIC    Genie groups by product and returns one row per product, listing all 6 bakehouse products.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Refine for Better Results
# MAGIC
# MAGIC Your first question does not always give you exactly what you want. Refining it makes Genie's response more precise.
# MAGIC
# MAGIC 1. Start with a broad request:
# MAGIC
# MAGIC    > *Show me sales*
# MAGIC
# MAGIC    This is generic and returns raw transaction records, which are hard to scan.
# MAGIC
# MAGIC 2. Refine it to be specific about aggregation and sorting:
# MAGIC
# MAGIC    > *Show me total sales by product, ordered from highest to lowest*
# MAGIC
# MAGIC    Compare the two results. The refined question returns summarized, sorted data with the top products first, which is much easier to act on.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Ask a More Powerful Question
# MAGIC
# MAGIC Genie remembers context within a conversation and can join tables for you automatically.
# MAGIC
# MAGIC 1. Ask a question, then a one of the follow-up questions below that depends on it:
# MAGIC
# MAGIC    > *Which product has the highest revenue?*
# MAGIC
# MAGIC    > *Show me all transactions for that product*
# MAGIC
# MAGIC    Genie remembers which product you meant from the previous question and filters to it, without you naming it again.
# MAGIC
# MAGIC 2. Ask a question that needs two tables:
# MAGIC
# MAGIC    > *Show me transactions with customer names*
# MAGIC
# MAGIC    Genie joins **sales_transactions** to **sales_customers** on its own. You did not have to specify the join. Click **Show code** to confirm the join in the generated SQL.

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
# MAGIC     Tips
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC - **Rephrase** if a result is unexpected. Genie understands many ways of asking the same thing.
# MAGIC - **Check the SQL** with **Show code** to confirm Genie interpreted your question the way you intended.
# MAGIC - **Refine** by adding a filter ("over $20"), a time frame ("in May 2024"), or a sort order to narrow any answer.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. View the Genie Agent in Genie One
# MAGIC
# MAGIC 1. Open Genie One in a new tab.
# MAGIC
# MAGIC 2. Select **Agents** from the left navigation pane.
# MAGIC
# MAGIC 3. Browse the **Agents** available to you under **MCPs**.
# MAGIC    - You should see the **Genie Agent** you created.
# MAGIC    - Depending on your workspace and the permissions granted on other published **Genie Agents**, you may see additional agents.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lab, you:
# MAGIC
# MAGIC 1. Asked a basic aggregation and grouping question in a Genie Agent.
# MAGIC 2. Refined a broad question into a precise, sorted answer.
# MAGIC 3. Used a follow-up question and a multi-table question that Genie answered by joining tables automatically.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
