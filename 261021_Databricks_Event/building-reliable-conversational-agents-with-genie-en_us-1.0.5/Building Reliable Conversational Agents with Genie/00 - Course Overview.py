# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Building Reliable Conversational Agents with Genie
# MAGIC  
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This course teaches you how to design, build, and maintain a Databricks Genie Agent, a natural language interface that enables business users to ask questions about governed data and receive SQL-backed answers without writing code.
# MAGIC
# MAGIC You will learn how Genie Agents fits into the Databricks AI/BI product family and how it translates natural language into reliable SQL queries. The course focuses on what it takes to create a Genie Agent that delivers accurate, consistent, and trustworthy results.
# MAGIC
# MAGIC You will follow a complete end-to-end workflow, from understanding source data and defining benchmarks to configuring and refining a Genie Agent using the full set of Knowledge Store curation tools. These include metadata, synonyms, prompt matching, SQL logic, example queries, and text instructions.
# MAGIC
# MAGIC You will also learn how to share Genie Agents with business users through Genie One, understand how Unity Catalog governance is automatically enforced, and use monitoring and user feedback to continuously improve quality over time.
# MAGIC
# MAGIC By the end of the course, you will be able to create and manage a production-ready Genie Agent that delivers governed, self-service conversational analytics at scale.
# MAGIC
# MAGIC ## Terminal Objectives
# MAGIC - Explain how Genie Agents translates natural language into SQL, and when to use dashboards, Genie Agents, Genie Code, and the Genie One interface.
# MAGIC - Create and configure a Genie Agent using Unity Catalog tables, a SQL warehouse, and benchmark tests to evaluate accuracy.
# MAGIC - Apply an iterative build, test, observe, improve workflow using benchmarks and real Genie outputs.
# MAGIC - Curate the Knowledge Store with descriptions, synonyms, prompt-matching features, and example SQL to improve accuracy.
# MAGIC - Encode business logic using SQL through derived expressions, joins, queries and clear business instructions.
# MAGIC - Share Genie Agents and validate governance using Unity Catalog, including Genie permissions and ABAC policies.
# MAGIC - Monitor and continuously improve Genie using user feedback, and turn insights into new benchmarks and updates.
# MAGIC
# MAGIC
# MAGIC ##### Course update and version can be found in the `Version Info` file.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Prerequisites
# MAGIC
# MAGIC Before starting this course, learners should be comfortable with the following:
# MAGIC
# MAGIC - **General familiarity with the Databricks workspace** - You can navigate the workspace UI, attach compute resources, and run notebooks.
# MAGIC
# MAGIC - **Familiarity with Unity Catalog concepts** - You understand catalogs, schemas, and tables in Unity Catalog. Prior experience with permissions, tags, or column masks is helpful but not required.
# MAGIC
# MAGIC - **Intermediate SQL proficiency** - You can read and write SQL queries including SELECT, JOIN, GROUP BY, and aggregate functions.
# MAGIC
# MAGIC - **Access to a Databricks workspace** with the Databricks SQL entitlement and CAN USE permission on a serverless SQL warehouse.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Workspace Setup Information
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="border-left: 4px solid #f44336; background: #ffebee; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC <div>
# MAGIC <strong style="color: #c62828; font-size: 1.1em;">Prerequisites</strong>
# MAGIC <p style="margin: 8px 0 0 0; color: #333;">This content assumes you have:</p>
# MAGIC
# MAGIC - <strong>CAN USE access on at least one pro or serverless SQL warehouse.</strong> (2X-Small is sufficient)
# MAGIC - Access to the <strong>samples.bakehouse</strong> schema in Unity Catalog
# MAGIC - <strong>Unity Catalog</strong> enabled in your workspace
# MAGIC - Permission to <strong>create Genie</strong> in your workspace
# MAGIC </div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Results May Vary
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC This demo uses a live Genie Agent in Databricks. 
# MAGIC
# MAGIC Because Genie uses a large language model to generate SQL, responses may differ between runs or between users. The expected checkpoints shown in this notebook are representative examples, not guaranteed outputs.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B1. Databricks Provided Vocareum Workspace (Recommended)
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
# MAGIC - If you are running this notebook in a <strong>Databricks Academy provided Vocareum workspace</strong>, your Unity Catalog catalog is already created for you.
# MAGIC
# MAGIC - Your catalog name matches your Vocareum username and looks like: <strong>labuser12345</strong> (series of unique numbers)
# MAGIC
# MAGIC - If a <strong>Marketplace</strong> dataset is required, the share is already installed and available in the workspace.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B2. Databricks Free Edition or Outside Workspaces (*as is*)
# MAGIC
# MAGIC ##### Databricks Free Edition or Other Workspaces may work for this, but it is provided **as is** and support is not guaranteed.  
# MAGIC
# MAGIC Some features may not be available depending on the capabilities of Databricks Free Edition or your Workspace.
# MAGIC
# MAGIC Please read below to setup your environment
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
# MAGIC - If you are running this notebook in your own Databricks workspace or Databricks Free Edition, the setup will <strong>create a Unity Catalog catalog and schema for you</strong>. 
# MAGIC
# MAGIC - The <strong>Create Catalog</strong> permission is required.
# MAGIC
# MAGIC - The catalog name is derived from your Databricks username and follows this pattern: <strong>labuser_username</strong>
# MAGIC
# MAGIC <br></br>
# MAGIC #### Access Marketplace Data
# MAGIC
# MAGIC Marketplace data is not required.
# MAGIC
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Troubleshooting Setup - Your Workspace Can't Create Catalogs
# MAGIC   </strong>
# MAGIC <details>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC If you do not have permission to create a new catalog but already have one available, you can explicitly specify an existing catalog by updating the following:
# MAGIC
# MAGIC - In this notebook: `./Includes/Classroom-Setup-Common-SQL-WAREHOUSE` in Cell 2.
# MAGIC   - Specify your catalog in this statement: `DECLARE catalog_forced STRING DEFAULT 'NONE';`
# MAGIC
# MAGIC - In this notebook: `Classroom-Setup-Common-Python` in Cell 2.
# MAGIC   - Specify your catalog name in the argument here: `my_catalog = build_user_catalog(catalog_forced='YOUR_CATALOG_NAME')`
# MAGIC
# MAGIC   </div>
# MAGIC </details>
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
# MAGIC <li>Do not run in production environments. The setup scripts creates catalogs, schemas and pipelines in your workspace.</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## C. Course Agenda
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
# MAGIC       <th style="padding: 10px 14px; text-align: center; border: 1px solid #EEEDE9; width: 50px;">#</th>
# MAGIC       <th style="padding: 10px 14px; text-align: center; border: 1px solid #EEEDE9; width: 80px;">Type</th>
# MAGIC       <th style="padding: 10px 14px; text-align: left; border: 1px solid #EEEDE9;">Module Name</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">1</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Lecture</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Introduction to Genie Agents</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">2</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #fff3e0; color: #e65100; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Demo</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Bakehouse Setup and Data Exploration</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">3</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Demo</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Creating and Exploring a Genie Agent</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">4</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #fff3e0; color: #e65100; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Demo</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Adding Genie Benchmarks</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">5</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Lab</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Create an HR Genie Agent</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">6</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #fff3e0; color: #e65100; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Lecture</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Curating an Effective Genie Agent</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">7</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Demo</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Adding Metadata to the Knowledge Store</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">8</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #fff3e0; color: #e65100; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Demo</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Adding SQL Logic and Instructions to the Knowledge Store</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">9</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Demo</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Sharing and the End User Experience with Genie One</td>
# MAGIC     </tr><tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">10</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #fff3e0; color: #e65100; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Demo</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Monitoring Genie Conversations</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: white;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">11</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Lecture</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Summary and Next Steps</td>
# MAGIC     </tr>
# MAGIC     </tr><tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center; font-weight: 700; color: #1B5162;">12</td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9; text-align: center;"><span style="background: #fff3e0; color: #e65100; padding: 2px 8px; border-radius: 4px; font-weight: 600;">Lab</span></td>
# MAGIC       <td style="padding: 8px 14px; border: 1px solid #EEEDE9;">Improve the Knowledge Store for the HR Genie Agent</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ### Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
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
# MAGIC - Use Databricks Runtime version: **`Serverless SQL Warehouse`** for running all demo and lab notebooks.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
