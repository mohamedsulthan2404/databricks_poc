# Databricks notebook source
from pyspark.sql import functions as F

# COMMAND ----------

max_trigger_per_trigger = 50000
src_path = "/Volumes/iics/casemix/history/json_stress_test/"
check_point_path = "/Volumes/iics/casemix/history/json_stress_test_v2_checkpoint/"
catalog = "iics"
schema = "casemix"
table = "json_stress_test_v2"

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table if exists iics.casemix.json_stress_test_v2

# COMMAND ----------

m = F.col("_metadata")

raw = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "text")
    .option("wholetext", "true")
    .option("cloudFiles.maxFilesPerTrigger", max_trigger_per_trigger)
    .load(src_path)
)

name_dt = F.regexp_extract(m["file_name"], r"_(\d{8})_\d{6}\.[A-Za-z]+$", 1)
dt_file = F.when(name_dt != "", name_dt).otherwise(None)

df = (
    raw.select(
        F.lit("/Volumes/iics/casemix/history/json_stress_test/").alias("file_path"),
        m["file_name"].alias("file_name"),
        F.col("value").alias("json_original_data"),
        F.expr("try_parse_json(value)").alias("json_data_for_parsing"),
        (m["file_size"] / 1024.0).alias("file_size_kb"),
        m["file_modification_time"].alias("file_modified_date"),
        dt_file.alias("dt_data_file"),
    )
    .withColumn("dt_data_file_date", F.to_date("dt_data_file", "yyyyMMdd"))
    .withColumn("data_year",  F.year("dt_data_file_date"))
    .withColumn("data_month", F.month("dt_data_file_date"))
    .withColumn("loaded_at",  F.current_timestamp())
)

q = (
    df.writeStream.format("delta")
    .option("checkpointLocation", check_point_path)
    .trigger(availableNow=True)
    .toTable(f"{catalog}.{schema}.{table}")
)

q.awaitTermination()

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM iics.casemix.json_stress_test_v2 limit 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM iics.casemix.json_stress_test_v2 limit 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM iics.casemix.json_stress_test_v2 LIMIT 10
