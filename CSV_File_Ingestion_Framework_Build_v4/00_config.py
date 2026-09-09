# Databricks notebook source
# MAGIC %md
# MAGIC # CSV to Delta Ingestion Framework - Batch Process

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

catalog        = "iics"
schema         = "casemix"
control_table  = f"{catalog}.{schema}.csv_file_control_test"
log_table      = f"{catalog}.{schema}.csv_file_logs_test"

# Optional
force_reload   = False # set True to reprocess every file regardless of status
datamart_filter = "healthcare_test" # for parallel executions

#executing user
executed_by = spark.sql("SELECT current_user()").first()[0]

print(f"Control table  : {control_table}")
print(f"Log table      : {log_table}")
print(f"Force reload   : {force_reload}")
print(f"DataMart filter: {datamart_filter}")
print(f"executed_by: {executed_by}")

# COMMAND ----------

# spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
# spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Required Libraries

# COMMAND ----------

from datetime import datetime
from pyspark.sql.functions import (
    col, row_number, desc, current_user, 
    lit, current_timestamp, md5, concat_ws
    )
# from pyspark.sql.window import Window
from pyspark.sql.types import (
    StructType, StructField, StringType, 
    LongType, TimestampType, DoubleType,
    IntegerType, DateType, DecimalType
    )
from pyspark.sql import Row
from delta.tables import DeltaTable
import traceback
import uuid
import json

# COMMAND ----------

# MAGIC %md
# MAGIC ## Control Table
# MAGIC Pattern: Control table + Log table -> the log table drives fault-tolerant retries.
# MAGIC Re-running this notebook automatically skips any file already marked success and
# MAGIC reprocesses everything else (if failed)
# MAGIC
# MAGIC
# MAGIC **Control table schema:**
# MAGIC
# MAGIC | Column | Meaning |
# MAGIC |---|---|
# MAGIC | S_No | Serial Number |
# MAGIC | DataMart | Data Domain |
# MAGIC | Target_Catalog | Delta target catalog |
# MAGIC | Target_Schema | Delta target schema |
# MAGIC | Target_Table_Name | Delta target table |
# MAGIC | Source_Path | folder path (e.g. `s3://bucket/.../iics_test/`)|
# MAGIC | Source_File_Name | file name |
# MAGIC | Source_File_Format | file format |
# MAGIC | Primary_Fields | primary keys |
# MAGIC | Date_Field | date fields |
# MAGIC | File_Type | file type |
# MAGIC | File_Count | expected row count for that file |
# MAGIC | Is_Active | 1 = Active, 0 = Inactive|
# MAGIC | Columns_Dtypes | JSON string mapping each source column to its Spark dtype, e.g. `{"CASE_SURR_ID":"int","CASE_TYPE":"string","DISCH_DATE":"date"}`. Used to build an explicit read schema instead of `inferSchema`. Key order must match the CSV's column order. Leave NULL to fall back to `inferSchema`. |
# MAGIC
# MAGIC The full source path used for reading is `Source_Path + Source_File_Name` + (add File_Format if needed).
# MAGIC

# COMMAND ----------

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {control_table} (
    S_No INT,
    DataMart STRING,
    Target_Catalog STRING,
    Target_Schema STRING,
    Target_Table_Name STRING,
    Source STRING,
    Source_Path STRING,
    Source_File_Name STRING,
    Source_File_Format STRING,
    Source_File_Delimiter STRING,
    Primary_Fields STRING,
    Date_Field STRING,
    File_Type STRING,
    File_Count BIGINT,
    Columns_Dtypes STRING,
    Is_Active INT
)
USING DELTA
""")

# COMMAND ----------

# Safety net for control tables created before Columns_Dtypes existed.
# CREATE TABLE IF NOT EXISTS above won't add the column to an already-existing table.
try:
    spark.sql(f"ALTER TABLE {control_table} ADD COLUMNS (Columns_Dtypes STRING)")
    print("Columns_Dtypes column added")
except Exception as e:
    print("Columns_Dtypes already present (or ALTER not needed):", str(e)[:200])

# COMMAND ----------

existing_rows = spark.table(control_table).count()

if existing_rows == 0:
    spark.sql(f"""
INSERT INTO {control_table}
VALUES
(1, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test/', 'case_data_003.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000,'{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',1),
(2, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test/', 'case_data_004.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000,'{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',1),
(3, 'healthcare_test', 'iics', 'casemix', 'healthcare_merge_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/merge_test/', 'case_data_003.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000,'{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(4, 'healthcare_test', 'iics', 'casemix', 'healthcare_merge_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/merge_test/', 'case_data_004.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000, '{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(5, 'healthcare_test', 'iics', 'casemix', 'healthcare_merge_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/merge_test/', 'case_data_005.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000, '{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(6, 'healthcare_test', 'iics', 'casemix', 'healthcare_error_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/error_test/', 'case_data_003.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000, '{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(7, 'healthcare_test', 'iics', 'casemix', 'healthcare_error_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/error_test/', 'case_data_004.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000, '{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(8, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test/', 'case_data_005.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 1000000, '{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(9, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test/', 'case_data_006.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 1000000,'{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(10, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test/', 'case_data_007.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 1000000, '{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(11, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test_1', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test_1/', 'case_data_005.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000, '{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(12, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test_1', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test_1/', 'case_data_006.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000, '{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(13, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test_1', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test_1/', 'case_data_007.csv', 'csv',NULL, 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10, '{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(14, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test_1', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test_1/', 'case_data_008.csv', 'csv','|', 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000,'{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(15, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test_1', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test_1/', 'case_data_009.csv', 'csv','|', 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000,'{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0),
(16, 'healthcare_test', 'iics', 'casemix', 'healthcare_ingestion_test_1', 's3', 's3://cittabase-s3-test/Databricks-poc/moh_test/ingestion_test_1/', 'case_data_010.csv', 'csv','|', 'CASE_SURR_ID', 'DH_UPDATED_DATE', 'data', 10000,'{{"CASE_SURR_ID": "int", "PATIENT_SURR_ID": "int", "CASE_TYPE": "string", "HEALTHCARE_FACILITY": "string", "PATIENT_AC_NO": "string", "DIAG_CODE": "string", "DIAG_TYPE": "string", "MDC": "string", "DRG": "string", "DISCH_DATE": "date", "LOS": "int", "HTP": "double", "LTP": "double", "DH_CREATED_DATE": "date", "DH_UPDATED_DATE": "date", "ORDER_NUMBER": "string", "PRFX": "string", "ARE": "string", "ARCL": "string", "DRG_ICD10": "string", "MDC_ICD10": "string", "DIAG_CODE_ICD10": "string", "PATIENT_ACC_SURR_ID": "int"}}',0)
""")
    print(f"Control table seeded with 16 rows.")
else:
    print(f"Control table already has {existing_rows} row(s) - skipping seed insert to avoid duplicates.")


# COMMAND ----------

# MAGIC %md
# MAGIC ## Log Table Configs

# COMMAND ----------

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {log_table} (
  log_id          STRING,
  batch_id        STRING,
  s_no            STRING,
  datamart        STRING,
  file_name       STRING,
  source_path     STRING,
  tgt_catalog     STRING,
  tgt_schema      STRING,
  tgt_table       STRING,
  row_count       BIGINT,
  expected_count  BIGINT,
  status          STRING,
  error_message   STRING,
  executed_by     STRING,
  start_time      TIMESTAMP,
  end_time        TIMESTAMP,
  loaded_at       TIMESTAMP,
  duration_sec    DOUBLE
) USING DELTA
""")

print("Log Table Created")

# COMMAND ----------

log_schema = StructType([
    StructField("log_id",         StringType(),    True),
    StructField("batch_id",       StringType(),    True),
    StructField("s_no",           StringType(),    True),
    StructField("datamart",       StringType(),    True),
    StructField("file_name",      StringType(),    True),
    StructField("source_path",    StringType(),    True),
    StructField("tgt_catalog",    StringType(),    True),
    StructField("tgt_schema",     StringType(),    True),
    StructField("tgt_table",      StringType(),    True),
    StructField("row_count",      LongType(),      True),
    StructField("expected_count", LongType(),      True),
    StructField("status",         StringType(),    True),
    StructField("error_message",  StringType(),    True),
    StructField("executed_by",    StringType(),    True),
    StructField("start_time",     TimestampType(), True),
    StructField("end_time",       TimestampType(), True),
    StructField("loaded_at",      TimestampType(), True),
    StructField("duration_sec",   DoubleType(),    True),
])
