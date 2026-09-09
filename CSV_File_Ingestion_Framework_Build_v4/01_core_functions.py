# Databricks notebook source
# MAGIC %run "./00_config"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 01. Core Functions
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Metadata
# MAGIC - Reads `Is_Active = 1` rows from the control table (optionally filtered by
# MAGIC   `DataMart`), builds the full source path, and excludes any file already logged as `success`
# MAGIC   in the log table for the same target (unless `force_reload = True`)

# COMMAND ----------

def get_pending_files():
    # control_df = spark.table(control_table).filter(col("Is_Active") == 1)
    control_df = spark.table(control_table).filter(col("S_No") == 12)

    if datamart_filter is not None:
        control_df = control_df.filter(col("DataMart") == datamart_filter)

    control_df = control_df.dropDuplicates(
        ["Target_Catalog", "Target_Schema", "Target_Table_Name", "Source_Path", "Source_File_Name"]
    )

    if force_reload:
        return control_df.collect()

    succeeded_df = (spark.table(log_table)
                    .filter(col("status") == "SUCCESS")
                    .select("file_name", "tgt_catalog", "tgt_schema", "tgt_table")
                    .distinct())

    pending_df = (control_df.join(
                      succeeded_df,
                      (control_df.Source_File_Name == succeeded_df.file_name) &
                      (control_df.Target_Catalog == succeeded_df.tgt_catalog) &
                      (control_df.Target_Schema == succeeded_df.tgt_schema) &
                      (control_df.Target_Table_Name == succeeded_df.tgt_table),
                      "left_anti"))

    return pending_df.collect()


# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Source Data
# MAGIC This function reads the source CSV file and appends the `loaded_at` timestamp.
# MAGIC
# MAGIC If the control table row has a `Columns_Dtypes` JSON mapping (`{"COL":"dtype"}`), it's used to build an explicit schema instead of `inferSchema` -- this avoids inferSchema mistakes like turning ID columns into numeric types or misreading dates. Falls back to `inferSchema` when `Columns_Dtypes` is not set.
# MAGIC
# MAGIC When an explicit schema is used, the reader runs in `FAILFAST` mode: if any value in the CSV can't be cast to its declared dtype (e.g. a text string in a `date` column), Spark raises immediately instead of silently writing `null` (Spark's `PERMISSIVE` default). This exception surfaces on the first action that scans the file (`.count()` in `02_main`), is caught by the batch loop's `try/except`, logged as `FAILED` with the traceback, and the batch moves on to the next file -- the mismatched file is never written to the target table.
# MAGIC

# COMMAND ----------

# Maps the dtype strings used in Columns_Dtypes to Spark types.
DTYPE_MAP = {
    "string":    StringType(),
    "int":       IntegerType(),
    "integer":   IntegerType(),
    "bigint":    LongType(),
    "long":      LongType(),
    "double":    DoubleType(),
    "float":     DoubleType(),
    "date":      DateType(),
    "timestamp": TimestampType(),
}


def build_schema(columns_dtypes_json):

    dtype_dict = json.loads(columns_dtypes_json)

    fields = []
    for col_name, dtype_str in dtype_dict.items():
        dtype_str = dtype_str.strip().lower()

        if dtype_str.startswith("decimal"):
            precision, scale = (
                dtype_str.replace("decimal(", "").replace(")", "").split(",")
            )
            spark_type = DecimalType(int(precision), int(scale))
        else:
            spark_type = DTYPE_MAP.get(dtype_str, StringType())

        fields.append(StructField(col_name, spark_type, True))

    return StructType(fields)


def read_source_file(source_path, source_file_delimiter, file_s_no, columns_dtypes=None):

    reader = spark.read.option("header", True)

    if columns_dtypes:
        schema = build_schema(columns_dtypes)
        reader = (
            reader
            # .option("dateFormat", "dd-MM-yyyy")
            .schema(schema)
            .option("enforceSchema", False)  # validates header names/order against the schema instead of silently trusting position
            .option("mode", "FAILFAST")      # raise immediately if any value can't be cast to its declared dtype, instead of silently writing null (PERMISSIVE default)
        )
    else:
        reader = reader.option("inferSchema", True)  # fallback when no explicit dtype map is configured

    if source_file_delimiter == "|":
        reader = (
            reader
            .option("sep", "|")
            .option("quote", '"')
        )

    df = reader.csv(source_path)


    return df.withColumns(
        {
             "_s_no___c": lit(file_s_no),
            "_loaded_at___c": current_timestamp(),
           
        }
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Data into Delta Table
# MAGIC
# MAGIC This function performs the following:
# MAGIC
# MAGIC - Checks whether the target table exists
# MAGIC - Creates a Delta table if it does not exist
# MAGIC - Appends data when no primary key is configured
# MAGIC - Performs Delta MERGE when primary keys are available
# MAGIC - Updates existing records only when the source date is newer

# COMMAND ----------

def load_to_delta(df_source, full_tgt, pk_cols, date_col):

    table_exists = spark.catalog.tableExists(full_tgt)

    if not table_exists:

        (
            df_source.write
            .format("delta")
            .mode("overwrite")
            .saveAsTable(full_tgt)
        )

        print(f"Created table : {full_tgt}")
        return

    if not pk_cols:

        (
            df_source.write
            .format("delta")
            .mode("append")
            .saveAsTable(full_tgt)
        )

        print(f"Appended into : {full_tgt}")
        return

    if isinstance(pk_cols, str):
        pk_cols = [c.strip() for c in pk_cols.split(",") if c.strip()]

    merge_condition = " AND ".join(
        f"tgt.{c} = src.{c}" for c in pk_cols
        )

    delta_table = DeltaTable.forName(spark, full_tgt)

    merge = (
        delta_table.alias("tgt")
        .merge(df_source.alias("src"), merge_condition)
    )

    if date_col and date_col in df_source.columns:
        merge = merge.whenMatchedUpdateAll(
            condition=f"src.{date_col} > tgt.{date_col}"
        )
    else:
        merge = merge.whenMatchedUpdateAll()

    (
        merge
        .whenNotMatchedInsertAll()
        .execute()
    )

    print(f"Merged into : {full_tgt}")

# COMMAND ----------

# MAGIC %md
# MAGIC # Validate Row Count
# MAGIC
# MAGIC Compares the expected row count from the control table with the actual row count from the source file.
# MAGIC
# MAGIC Returns an error message if the counts do not match.

# COMMAND ----------

def validate_row_count(expected, actual):

    if expected is None:
        return None

    if expected != actual:
        return (
            f"Row Count Mismatch. "
            f"Expected={expected}, Actual={actual}"
        )

    return None

# COMMAND ----------

# MAGIC %md
# MAGIC ## Log
# MAGIC - Uses an explicit schema (`log_schema`) rather than type inference
# MAGIC - Appends log rows immediately (failure won't break the process).

# COMMAND ----------

def write_log(record: dict):

    ordered = {field.name: record.get(field.name) for field in log_schema.fields}
    log_df = spark.createDataFrame([Row(**ordered)], schema=log_schema)
    log_df.write.format("delta").mode("append").saveAsTable(log_table)

# COMMAND ----------

# MAGIC %md
# MAGIC - `base_log_record()` - maps control-table columns to the log-table's internal fields.__
# MAGIC

# COMMAND ----------

def base_log_record(r, batch_id, full_source_path):
    return {
        "log_id": str(uuid.uuid4()),
        "batch_id": batch_id,
        "s_no": r["S_No"],
        "datamart": r["DataMart"],
        "file_name": r["Source_File_Name"],
        "source_path": full_source_path,
        "tgt_catalog": r["Target_Catalog"],
        "tgt_schema": r["Target_Schema"],
        "tgt_table": r["Target_Table_Name"],
        "expected_count": int(r["File_Count"]),
    }

# COMMAND ----------

# MAGIC %md
# MAGIC ## Log Successful Execution
# MAGIC
# MAGIC Writes a SUCCESS record into the ingestion log table.
# MAGIC
# MAGIC Logged details include:
# MAGIC
# MAGIC - Batch ID
# MAGIC - File Name
# MAGIC - Start Time
# MAGIC - End Time
# MAGIC - Duration
# MAGIC - Row Count
# MAGIC - Status
# MAGIC - Executed By

# COMMAND ----------

def log_success(log_record, row_count, error_message,
                executed_by, start_time):

    end_time = datetime.now()

    log_record.update({
        "row_count": row_count,
        "status": "SUCCESS",
        "error_message": error_message,
        "executed_by": executed_by,
        "start_time": start_time,
        "end_time": end_time,
        "loaded_at": end_time,
        "duration_sec": (end_time - start_time).total_seconds()
    })

    write_log(log_record)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Log Failed Execution
# MAGIC
# MAGIC Captures exception details and writes a FAILED record into the ingestion log.
# MAGIC
# MAGIC Logged details include:
# MAGIC
# MAGIC - Error Message
# MAGIC - Execution Duration
# MAGIC - Start Time
# MAGIC - End Time
# MAGIC - Status

# COMMAND ----------

def log_failure(log_record, executed_by, start_time):

    end_time = datetime.now()

    log_record.update({
        "row_count": None,
        "status": "FAILED",
        "error_message": traceback.format_exc()[:4000],
        "executed_by": executed_by,
        "start_time": start_time,
        "end_time": end_time,
        "loaded_at": end_time,
        "duration_sec": (end_time - start_time).total_seconds()
    })

    write_log(log_record)
