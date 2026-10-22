# Databricks notebook source
!pip install "mlflow-skinny==3.8.1"

# COMMAND ----------

# DBTITLE 1,Setup
# MAGIC %run ./Classroom-Setup-Common-Python

# COMMAND ----------

# DBTITLE 1,Create or Use Catalog
#####################
# CREATE USER OR SET USER CATALOG
#####################
my_catalog = build_user_catalog(catalog_forced=None)

# COMMAND ----------

# DBTITLE 1,Set Default Catalog and Schema
# Create the catalog, schema, and volume if they don't exist already
spark.sql(f"USE CATALOG {my_catalog}")

# COMMAND ----------

# DBTITLE 1,Create Schema

#####################
# User Schema
#####################
my_schema = 'ai_ml_ds'
spark.sql(f'CREATE SCHEMA IF NOT EXISTS {my_schema}')
spark.sql(f"USE SCHEMA {my_schema}")

# COMMAND ----------

# DBTITLE 1,User Name
username = spark.sql("SELECT current_user()").first()[0]

# COMMAND ----------

# DBTITLE 1,Display Values
display_config_values(
    [
        ("Your Catalog Name", my_catalog),
        ("Your Schema Name", my_schema),
        ("User Name", username)
    ]
)


# COMMAND ----------

compute_validation(recommend_dbr_classic_version=None, recommended_serverless_version=5)
