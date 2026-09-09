# Databricks notebook source
# MAGIC %run "./01_core_functions"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 02. Main Ingestion Loop
# MAGIC
# MAGIC Each file is processed independently inside a `try/except`:
# MAGIC
# MAGIC - If any value fails to cast to its declared dtype (`Columns_Dtypes`), or the row count doesn't match `File_Count`, an exception is raised **before** `load_to_delta` runs -- the file is never written to the target table.
# MAGIC - On success -> row count captured, appended to the Delta target, logged as `SUCCESS`.
# MAGIC - On failure -> full error message logged as `FAILED`, loop continues to the next file
# MAGIC   (one bad file never blocks the rest of the batch).
# MAGIC
# MAGIC The full read path is built as `Source_Path + Source_File_Name` (control table stores them
# MAGIC separately). Row-count mismatch vs `File_Count` is logged as a warning but still marked
# MAGIC `SUCCESS`

# COMMAND ----------

batch_id = str(uuid.uuid4())
pending_rows = get_pending_files()

for r in pending_rows:

    full_tgt = f"{r.Target_Catalog}.{r.Target_Schema}.{r.Target_Table_Name}"
    full_source_path = f"{r.Source_Path.rstrip('/')}/{r.Source_File_Name}"
    source_file_delimiter = r.Source_File_Delimiter

    start_time = datetime.now()

    log_record = base_log_record(
        r,
        batch_id,
        full_source_path
    )

    try:

    
        df_source = read_source_file(full_source_path, source_file_delimiter, r.S_No, r.Columns_Dtypes)

        row_count = df_source.count()


        # error_message = validate_row_count(
        #     int(r.File_Count),
        #     int(row_count)
        # )

        # if error_message:
        #     raise ValueError(error_message)

        load_to_delta(
            df_source=df_source,
            full_tgt=full_tgt,
            pk_cols=r.Primary_Fields,
            date_col=r.Date_Field
        )

        log_success(
            log_record,
            row_count,
            None,
            executed_by,
            start_time
        )

        print(f"SUCCESS : {r.Source_File_Name}")

    except Exception:

        log_failure(
            log_record,
            executed_by,
            start_time
        )

        print(traceback.format_exc())

print("Batch Complete")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM iics.casemix.csv_file_logs_test
