# Databricks notebook source
# DBTITLE 1,Setup
# MAGIC %run ./Classroom-Setup-Common-Python

# COMMAND ----------

# DBTITLE 1,Create or Use Catalog
#####################
# CREATE USER OR SET USER CATALOG
#####################
my_catalog = build_user_catalog(catalog_forced=None)

# COMMAND ----------

# DBTITLE 1,Display Values
display_config_values(
    [
        ("Your Catalog Name", my_catalog)
    ]
)


# COMMAND ----------

compute_validation(recommend_dbr_classic_version=None, recommended_serverless_version=5)
