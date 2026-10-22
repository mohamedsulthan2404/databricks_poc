# Databricks notebook source
# DBTITLE 1,Setup
# MAGIC %run ./Classroom-Setup-Common-Python

# COMMAND ----------

# DBTITLE 1,Create or Use Catalog
#####################
# CREATE USER OR SET USER CATALOG
#####################
my_catalog = build_user_catalog(catalog_forced=None)
spark.sql(f'USE CATALOG {my_catalog}')

# COMMAND ----------

# DBTITLE 1,Create Schema
schema_name = "example"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
spark.sql(f'USE SCHEMA {schema_name}')

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create table
# MAGIC CREATE OR REPLACE TABLE patient_info (
# MAGIC   device_id  INT,
# MAGIC   mrn        STRING,
# MAGIC   name       STRING,
# MAGIC   time       TIMESTAMP,
# MAGIC   heartrate  DOUBLE
# MAGIC );
# MAGIC INSERT OVERWRITE patient_info VALUES
# MAGIC   (23,'40580129','Nicholas Spears','2020-02-01T00:01:58.000+0000',54.0122153343),
# MAGIC   (17,'52804177','Lynn Russell','2020-02-01T00:02:55.000+0000',92.5136468131),
# MAGIC   (37,'65300842','Samuel Hughes','2020-02-01T00:08:58.000+0000',52.1354807863),
# MAGIC   (23,'40580129','Nicholas Spears','2020-02-01T00:16:51.000+0000',54.6477014191),
# MAGIC   (17,'52804177','Lynn Russell','2020-02-01T00:18:08.000+0000',95.033344842),
# MAGIC   (37,'65300842','Samuel Hughes','2020-02-01T00:23:58.000+0000',57.3391541312),
# MAGIC   (23,'40580129','Nicholas Spears','2020-02-01T00:31:58.000+0000',56.6165053697),
# MAGIC   (17,'52804177','Lynn Russell','2020-02-01T00:32:56.000+0000',94.8134313932),
# MAGIC   (37,'65300842','Samuel Hughes','2020-02-01T00:38:54.000+0000',56.2469995332),
# MAGIC   (23,'40580129','Nicholas Spears','2020-02-01T00:46:57.000+0000',54.8372685558),
# MAGIC   (23,'40580129',NULL,'2020-02-01T00:01:58.000+0000',54.0122153343),
# MAGIC   (17,'52804177',NULL,'2020-02-01T00:02:55.000+0000',92.5136468131),
# MAGIC   (37,'65300842',NULL,'2020-02-01T00:08:58.000+0000',1000052.1354807863),
# MAGIC   (23,'40580129',NULL,'2020-02-01T00:16:51.000+0000',54.6477014191),
# MAGIC   (17,'52804177','Lynn Russell','2020-02-01T00:18:08.000+0000',9),
# MAGIC   (37,'65300842','Samuel Hughes','2020-02-01T00:23:58.000+0000',7),
# MAGIC   (23,'40580129','Nicholas Spears','2020-02-01T00:31:58.000+0000',6),
# MAGIC   (17,'52804177','Lynn Russell','2020-02-01T00:32:56.000+0000',5),
# MAGIC   (37,'65300842','Samuel Hughes','2020-02-01T00:38:54.000+0000',9000),
# MAGIC   (23,'40580129','Nicholas Spears','2020-02-01T00:46:57.000+0000',66),
# MAGIC   (23,'40580129',NULL,'2020-02-01T00:01:58.000+0000',54.0122153343),
# MAGIC   (17,'52804177',NULL,'2020-02-01T00:02:55.000+0000',92.5136468131),
# MAGIC   (37,'65300842',NULL,'2020-02-01T00:08:58.000+0000',1000052.1354807863),
# MAGIC   (23,'40580129',NULL,'2020-02-01T00:16:51.000+0000',54.6477014191),
# MAGIC   (17,'52804177','Lynn Russell','2020-02-01T00:18:08.000+0000',98),
# MAGIC   (37,'65300842','Samuel Hughes','2020-02-01T00:23:58.000+0000',90),
# MAGIC   (23,'40580129','Nicholas Spears','2020-02-01T00:31:58.000+0000',60),
# MAGIC   (17,'52804177','Lynn Russell','2020-02-01T00:32:56.000+0000',50),
# MAGIC   (37,'65300842','Samuel Hughes','2020-02-01T00:38:54.000+0000',30),
# MAGIC   (23,'40580129','Nicholas Spears','2020-02-01T00:46:57.000+0000',80);
# MAGIC
# MAGIC
# MAGIC -- Create view
# MAGIC CREATE OR REPLACE VIEW vw_gold AS (
# MAGIC SELECT 
# MAGIC     mrn, 
# MAGIC     name, 
# MAGIC     MEAN(heartrate) 
# MAGIC     avg_heartrate, 
# MAGIC     DATE_TRUNC("DD", time) AS date
# MAGIC FROM patient_info
# MAGIC GROUP BY mrn, name, DATE_TRUNC("DD", time)
# MAGIC );

# COMMAND ----------

# DBTITLE 1,Display Values
display_config_values(
    [
        ("Your Default Catalog Name", my_catalog),
        ("Your Default Schema Name", schema_name)
    ]
)


# COMMAND ----------

compute_validation(recommend_dbr_classic_version=None, recommended_serverless_version=5)
