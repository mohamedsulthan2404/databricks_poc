# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Create Final Demonstration Genie Agent
# MAGIC
# MAGIC This notebook will create the final demonstration Genie Agent after going through each notebook. If you'd lke the final output, run all cells is this notebook.
# MAGIC
# MAGIC It will create a **Genie agent** in your workspaced named: `labuser_UNIQUE_ID - Final Solution Bakehouse Agent`

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - DATA SETUP AND TABLE/COLUMN METADATA
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #f44336;
# MAGIC   background: #ffebee;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Data Setup</strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Before starting this notebook, make sure you ran the **02 Demo - Bakehouse Setup and Data Exploration** notebook once to set up the course data.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - SELECT A COMPUTE ENVIRONMENT
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #f44336;
# MAGIC   background: #ffebee;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Select Serverless Compute</strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Before starting this notebook, select the required compute environment listed below.
# MAGIC
# MAGIC - **Serverless Compute, Version 5**
# MAGIC
# MAGIC ![Serverless Select](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/select-serverless.png)
# MAGIC <br></br>
# MAGIC   - How to select an environment version:
# MAGIC [AWS](https://docs.databricks.com/aws/en/compute/serverless/dependencies#-select-an-environment-version) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies#-select-an-environment-version) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/compute/serverless/dependencies#-select-an-environment-version)
# MAGIC
# MAGIC **NOTE:**  This notebook requires **SQL and Python, and was tested using Serverless V5**. All purpose compute may work but is not guaranteed to behave the same or support all features demonstrated.
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Run the cell below to create the necessary values.

# COMMAND ----------

# MAGIC %run ./Includes/create-genie-agent

# COMMAND ----------

# MAGIC %md
# MAGIC Run the cell below to create the Genie Agent. Wait 1-2 minutes for the Genie Agent to appear in the UI.

# COMMAND ----------

# =====================================================================
# Build the Bakehouse Genie Agemt
# =====================================================================

def build_bakehouse_space(
    *,
    title: str = f"{my_catalog} - Final Solution Bakehouse Agent",
    description: str = "Final demonstration Genie Agent.",
    warehouse_name: str = "shared_warehouse",
) -> str:
    """Create the Bakehouse Genie Agent using the variables defined above."""
    return create_genie_space(
        title=title,
        description=description,
        warehouse_name=warehouse_name,
        table_identifiers=TABLE_IDENTIFIERS,
        sample_questions=SAMPLE_QUESTIONS,
        general_instructions=SPACE_INSTRUCTIONS,
        sql_examples=SQL_EXAMPLES,
        sql_expressions=SQL_EXPRESSIONS,
        benchmarks=BENCHMARKS,
    )

build_bakehouse_space()

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
