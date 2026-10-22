-- Databricks notebook source
-- MAGIC %md
-- MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Lab - Catalog Explorer Navigation
-- MAGIC ### Estimated Duration: ~7-10 minutes
-- MAGIC In this demo, you inspect data objects in Unity Catalog using the Catalog Explorer. Once you can navigate the Catalog Explorer, you can find any dataset, see who owns it, and trace how it is used.

-- COMMAND ----------

-- DBTITLE 1,Learning Objectives
-- MAGIC %md
-- MAGIC ## Learning objectives
-- MAGIC
-- MAGIC By the end of this lesson, you should be able to:
-- MAGIC
-- MAGIC - **Navigate** the Catalog Explorer to locate catalogs, schemas, and tables in Unity Catalog.
-- MAGIC - **Review** and manage object details, including permissions and metadata.
-- MAGIC - **Add** AI-generated descriptions and column comments to improve data discovery.
-- MAGIC - **Visualize** data lineage at both the table and column levels.
-- MAGIC - **Query** tables using natural language through Genie in the Catalog Explorer.
-- MAGIC - **Explore** table history, insights, and quality monitoring features.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## A. Classroom Setup
-- MAGIC
-- MAGIC No Classroom Setup
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. The Catalog Explorer
-- MAGIC
-- MAGIC All of the data objects you create are available to you in the Catalog Explorer. You can view and change permissions, change object ownership, examine lineage, and a whole lot more.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B1. Navigate the Catalog Explorer
-- MAGIC
-- MAGIC 1. Open the Catalog Explorer by right-clicking on **Catalog** in the far left sidebar menu and selecting **Open Link in New Tab**. 
-- MAGIC     - This keeps these instructions open while you work.
-- MAGIC
-- MAGIC 2. Along the left side of the Catalog Explorer is the **Schema Browser**, which lets you navigate between the objects you have access privileges to. 
-- MAGIC
-- MAGIC 3. On the right side is the main Catalog Explorer interface.
-- MAGIC
-- MAGIC 4. **SELECT COMPUTE FOR CATALOG EXPLORER:** 
-- MAGIC     - On the **Schema Browser** on the left select a SQL warehouse.
-- MAGIC     
-- MAGIC     ![Compute](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/catalog-explorer-compute.png)
-- MAGIC
-- MAGIC 5. Click your **labuser_UNIQUE_ID** catalog in the schema browser.
-- MAGIC
-- MAGIC     You will see a list of at least two schemas in the catalog:
-- MAGIC     - **example** - this schema was created for you in the classroom setup.
-- MAGIC     - **information_schema** - this schema is created when the catalog is created and contains a wealth of metadata. The contents of this schema are beyond the scope of this course.
-- MAGIC
-- MAGIC     > The Catalog Explorer has more tabs than we can cover here. We will focus on **Details** and **Permissions**, the two tabs you will use most often.
-- MAGIC
-- MAGIC 6. Click the **Details** tab (just below the name of the catalog).
-- MAGIC
-- MAGIC     > The **Details** tab is common to nearly every object in Unity Catalog and provides more information about the object involved. In this case, you get information about your **labuser_UNIQUE_ID** catalog.
-- MAGIC
-- MAGIC 7. Click the **Permissions** tab.
-- MAGIC
-- MAGIC     > You can grant and revoke privileges using this interface. The same tab exists for most objects in Databricks.
-- MAGIC
-- MAGIC 8. Click the **example** schema in the schema browser.
-- MAGIC
-- MAGIC     > Note the list of table names in this schema and the tabs along the top (including **Details** and **Permissions**, discussed earlier). Since schemas can hold more than just tables, note that you can view **Volumes**, **Models**, and **Functions**, too.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B2. Tables in the Catalog Explorer
-- MAGIC
-- MAGIC In this course, we focus on the table object in the Catalog Explorer.
-- MAGIC
-- MAGIC 1. Click the **patient_info** table.
-- MAGIC
-- MAGIC 2. Let's explore the features of **Catalog Explorer** for a table.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## C. Add AI-Generated Descriptions and Comments
-- MAGIC
-- MAGIC When you open a table in Catalog Explorer, Databricks automatically generates a suggested description using AI. Review it for accuracy before accepting. The description of a table (or other object) is used in many places throughout your Lakehouse.
-- MAGIC
-- MAGIC - **Discovery and search** - Descriptions make tables easier to find. When you search for data in Catalog Explorer or use AI-powered search, Databricks indexes descriptions to help match your intent with relevant tables.
-- MAGIC
-- MAGIC - **AI-powered features** - Genie Agents and AI assistants use table and column descriptions to understand your data semantics. When you ask questions in natural language, these descriptions help the AI generate accurate queries and provide better recommendations.
-- MAGIC
-- MAGIC - **Documentation and collaboration** - Descriptions serve as inline documentation for your team. Anyone browsing the Catalog Explorer can quickly understand what a table contains and how it should be used, without needing to examine the data or contact the table owner.
-- MAGIC
-- MAGIC - **Governance and compliance** - Descriptions can indicate data sensitivity, usage policies, or compliance requirements. Combined with tags, they help data stewards understand what data exists and how it should be handled.
-- MAGIC
-- MAGIC 1. Select **Overview** to go back to the main **patient_info** table.
-- MAGIC
-- MAGIC 2. Accept the suggested table description by clicking **Accept**.
-- MAGIC
-- MAGIC     > Beyond table descriptions, column comments help users understand individual fields, their formats, and expected values. With the button labeled **AI Generate**, Databricks can generate comments for your columns.
-- MAGIC
-- MAGIC 3. In the column details section select **AI Generate**.
-- MAGIC
-- MAGIC     The Data Intelligence Platform proposes comments for each column in your table.
-- MAGIC
-- MAGIC 4. Click **Save all** to accept all suggested comments.
-- MAGIC
-- MAGIC **NOTE:** Always review generated AI output. For training, we will leave as is.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## D. Understand Data Lineage
-- MAGIC
-- MAGIC Data lineage in Databricks tracks the complete lifecycle of your data through Unity Catalog, showing where data originates, how it transforms, and where it is consumed. It captures dependencies at both the table and column level, mapping relationships between tables, views, notebooks, jobs, dashboards, pipelines, and ML models.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D1. View Data Lineage in Catalog Explorer
-- MAGIC
-- MAGIC 1. Click the **Lineage** tab to see upstream and downstream dependencies listed.
-- MAGIC
-- MAGIC 2. Click **See lineage graph** to open an interactive visual representation showing:
-- MAGIC     - Upstream sources (where data originates)
-- MAGIC     - Downstream consumers (where data is used)
-- MAGIC     - Connected notebooks, jobs, dashboards, and pipelines
-- MAGIC
-- MAGIC 3. Explore column-level lineage: click any column name to see which source columns map to it.
-- MAGIC
-- MAGIC 4. Close the lineage graph by clicking the **X** in the upper-right corner.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## E. Query a Table Using Natural Language
-- MAGIC
-- MAGIC You can query a table directly, using natural language, from within the Catalog Explorer. This is done using Genie.
-- MAGIC
-- MAGIC 1. Click the **Sample data** tab.
-- MAGIC
-- MAGIC     This tab shows the first rows of the table, so you can see the data it contains. You can also query the table using Genie.
-- MAGIC
-- MAGIC 2. Enter the following query:
-- MAGIC
-- MAGIC     > What is the average heart rate per device?
-- MAGIC
-- MAGIC     Genie shows you the SQL it generated, so you can review it before running.
-- MAGIC
-- MAGIC 3. Click **Yes** to allow Genie to run the query.
-- MAGIC
-- MAGIC     After the query runs, you will see the results displayed right in the Catalog Explorer.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## F. Explore Other Table Information
-- MAGIC
-- MAGIC There are other tabs along the top where you can view and manage metadata about this table:
-- MAGIC
-- MAGIC - **Overview** - On the right, you have information about the table, tags, its description, and you can add a row filtering function if you wish. On the left, you get information about each column in the table.
-- MAGIC
-- MAGIC - **Sample data** - This tab shows the first rows of the table.
-- MAGIC
-- MAGIC - **Details** - You get the same information here as you would by running `DESCRIBE EXTENDED <table_name>`.
-- MAGIC
-- MAGIC - **Permissions** - The UI gives you the ability to manage table permissions. You can `GRANT` and `REVOKE` permissions here.
-- MAGIC
-- MAGIC - **History** - The Delta Lake transaction log is on this tab. You can get this programmatically by running `DESCRIBE HISTORY <table_name>`.
-- MAGIC
-- MAGIC - **Lineage** - Provides a list and a graph of upstream and downstream dependencies.
-- MAGIC
-- MAGIC - **Insights** - The Databricks Data Intelligence Platform provides these insights, so you can see how your data object is being used.
-- MAGIC
-- MAGIC - **Quality** - This tab gives you the ability to monitor this table for data quality.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
-- MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
-- MAGIC <script>
-- MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
-- MAGIC </script>
