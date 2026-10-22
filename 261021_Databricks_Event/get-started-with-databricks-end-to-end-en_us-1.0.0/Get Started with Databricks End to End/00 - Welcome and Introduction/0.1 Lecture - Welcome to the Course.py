# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Welcome to Databricks End-to-End
# MAGIC
# MAGIC ## Your complete introduction to the Databricks Data Intelligence Platform
# MAGIC
# MAGIC This course is a comprehensive, hands-on introduction to the Databricks Data Intelligence Platform. You will follow a single end-to-end journey that starts in the workspace and finishes with an introduction to AI and machine learning, covering the everyday skills you need to work with data on Databricks.
# MAGIC
# MAGIC The course covers:
# MAGIC
# MAGIC - Navigating the Databricks workspace, compute options, and the Lakehouse versus Genie experiences.
# MAGIC - Understanding and ingesting data with Unity Catalog, including file upload and the Catalog Explorer.
# MAGIC - Working in Databricks notebooks and using Genie Code to write and debug code.
# MAGIC - Querying data with SQL, managing saved queries, and building dashboards and visualizations.
# MAGIC - Exploring data in natural language with Genie Agents.
# MAGIC - An introduction to AI and machine learning with MLflow and the Data Science Agent.
# MAGIC
# MAGIC By the end of the course, you will be comfortable navigating Databricks, finding and governing data in Unity Catalog, writing SQL and notebook code with AI assistance, building dashboards, and exploring data with Genie.
# MAGIC
# MAGIC ## Course Objectives
# MAGIC
# MAGIC By the end of this course, you will be able to:
# MAGIC
# MAGIC - **Navigate** the Databricks workspace, compute options, and core UI.
# MAGIC - **Explain** how Unity Catalog governs data through its three-level namespace, and **ingest** data using file upload and the Catalog Explorer.
# MAGIC - **Use** Databricks notebooks and **apply** Genie Code to generate and debug code.
# MAGIC - **Write** SQL queries, **manage** saved queries, and **build** dashboards and visualizations.
# MAGIC - **Explore** data in natural language using Genie Agents.
# MAGIC - **Describe** how MLflow and the Data Science Agent support AI and machine learning workflows on Databricks.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Prerequisites
# MAGIC
# MAGIC This is an introductory course. To get the most out of it, you should have:
# MAGIC
# MAGIC - **Basic computer and web browser skills.** You can navigate a web application and work with tabs and menus.
# MAGIC - **A willingness to work with data.** No prior Databricks experience is required.
# MAGIC - **Helpful, but optional: basic SQL.** Familiarity with `SELECT` statements makes the SQL and dashboard modules easier, but the course introduces what you need as you go.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. The Sample Dataset
# MAGIC
# MAGIC Throughout the course, we will be using the Bakehouse dataset. the Bakehouse dataset is a curated sample bakery franchise business dataset, built around sales transactions and related business data. There are five tables in this dataset:
# MAGIC 1. sales_transactions - Core sales data
# MAGIC 2. sales_franchises - Store locations
# MAGIC 3. sales_customers - Customer information
# MAGIC 4. sales_suppliers - Supplier data
# MAGIC 5. media_customer_reviews - Customer feedback
# MAGIC
# MAGIC This dataset is perfect for learning about retail analytics, geographic analysis, customer behavior, sales trends, and multi-table joins. Many of these topics will be covered in this course.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## C. Workspace Setup Information
# MAGIC
# MAGIC Most of this course explores the read-only **`samples.bakehouse`** dataset, so there is very little to set up. A few hands-on modules create your own objects (schemas, tables, queries, and dashboards) in a personal catalog.
# MAGIC
# MAGIC <div style="border-left: 4px solid #f44336; background: #ffebee; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC <div>
# MAGIC <strong style="color: #c62828; font-size: 1.1em;">Prerequisites</strong>
# MAGIC <p style="margin: 8px 0 0 0; color: #333;">This content assumes you have:</p>
# MAGIC
# MAGIC - <strong>CAN USE access on Serverless Compute, or a serverless SQL warehouse (2X-Small is sufficient).</strong>
# MAGIC - <strong>Unity Catalog</strong> enabled in your workspace, including read access to the <strong>samples</strong> catalog.
# MAGIC - Permission to <strong>create objects in your own catalog</strong> for the hands-on exercises.
# MAGIC </div>
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C1. Databricks Provided Vocareum Workspace (Recommended)
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC - If you are running this course in a <strong>Databricks Academy provided Vocareum workspace</strong>, your Unity Catalog catalog is already created for you.
# MAGIC
# MAGIC - Your catalog name matches your Vocareum username and looks like: <strong>labuser12345</strong> (a series of unique numbers).
# MAGIC
# MAGIC - The shared <strong>samples.bakehouse</strong> dataset is available for the read-only exploration parts of the course.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C2. Databricks Free Edition or Other Workspaces (*as is*)
# MAGIC
# MAGIC ##### Databricks Free Edition or other workspaces may work for this course, but it is provided **as is** and support is not guaranteed.
# MAGIC
# MAGIC Some features may not be available depending on the capabilities of Databricks Free Edition or your workspace.
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC <div style="color:#333;">
# MAGIC
# MAGIC #### Catalog Information
# MAGIC
# MAGIC - If you are running this course in your own Databricks workspace or Databricks Free Edition, the hands-on setup will <strong>create a Unity Catalog catalog and schema for you</strong>.
# MAGIC
# MAGIC - The <strong>Create Catalog</strong> permission is required.
# MAGIC
# MAGIC - The catalog name is derived from your Databricks username and follows this pattern: <strong>labuser_username</strong>
# MAGIC
# MAGIC - The shared <strong>samples.bakehouse</strong> dataset is available by default for the read-only exploration parts of the course.
# MAGIC
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #f44336;
# MAGIC   background: #ffebee;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Do Not Run in Production Environments</strong>
# MAGIC
# MAGIC <div style="color:#333;">
# MAGIC <ul>
# MAGIC <li>Only run this course in <strong>development or sandbox workspaces</strong>.</li>
# MAGIC <li>Do not run it in production. The setup scripts create catalogs and schemas in your workspace.</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## D. Course Agenda
# MAGIC
# MAGIC The course is organized into folders. Each folder holds the notebooks for that topic. Work through them in order.
# MAGIC
# MAGIC <div style="max-width: 1200px; margin: 0 auto; font-family: sans-serif;">
# MAGIC <div style="background: #F9F7F4; border-radius: 10px; padding: 20px 24px; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC
# MAGIC <style>
# MAGIC .agenda-table td, .agenda-table th {
# MAGIC   font-size: 14pt !important;
# MAGIC }
# MAGIC </style>
# MAGIC
# MAGIC <table class="agenda-table" style="width: 100%; border-collapse: collapse; line-height: 1.5;">
# MAGIC   <thead>
# MAGIC     <tr style="background: #1B5162; color: white;">
# MAGIC       <th style="padding: 10px 14px; text-align: center; border: 1px solid #EEEDE9; width: 60px;">#</th>
# MAGIC       <th style="padding: 10px 14px; text-align: center; border: 1px solid #EEEDE9; width: 90px;">Type</th>
# MAGIC       <th style="padding: 10px 14px; text-align: left; border: 1px solid #EEEDE9;">Module</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">00</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #eceff1; color: #455a64; padding: 2px 10px; border-radius: 4px; font-weight: 600;">Folder</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Welcome &amp; Introduction</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">01</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #eceff1; color: #455a64; padding: 2px 10px; border-radius: 4px; font-weight: 600;">Folder</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">The Databricks Workspace</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">02</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #eceff1; color: #455a64; padding: 2px 10px; border-radius: 4px; font-weight: 600;">Folder</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Understanding &amp; Ingesting Data with Unity Catalog</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">03</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #eceff1; color: #455a64; padding: 2px 10px; border-radius: 4px; font-weight: 600;">Folder</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Notebooks &amp; Genie Code</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">04</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #eceff1; color: #455a64; padding: 2px 10px; border-radius: 4px; font-weight: 600;">Folder</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">SQL for Querying and Dashboards</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">05</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #eceff1; color: #455a64; padding: 2px 10px; border-radius: 4px; font-weight: 600;">Folder</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Genie Agents for Natural Language Analytics</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">06</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #eceff1; color: #455a64; padding: 2px 10px; border-radius: 4px; font-weight: 600;">Folder</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">AI/ML &amp; Data Science Agent</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">07</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #eceff1; color: #455a64; padding: 2px 10px; border-radius: 4px; font-weight: 600;">Folder</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Wrap Up</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Getting Help and Resources
# MAGIC
# MAGIC ### During the course
# MAGIC
# MAGIC - **Genie Code**: Use Genie Code inside your notebooks for code help and debugging.
# MAGIC
# MAGIC ### Additional resources
# MAGIC
# MAGIC - **Databricks Documentation**: [docs.databricks.com](https://docs.databricks.com/)
# MAGIC - **Community Forums**: [community.databricks.com](https://community.databricks.com/)
# MAGIC - **Databricks Academy**: Free training courses at [databricks.com/learn](https://www.databricks.com/learn)
# MAGIC
# MAGIC ### Community
# MAGIC
# MAGIC Join the Databricks community to:
# MAGIC
# MAGIC - Ask questions in the forums.
# MAGIC - Share your projects and solutions.
# MAGIC - Learn from others' experiences.
# MAGIC - Stay updated on new features.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
