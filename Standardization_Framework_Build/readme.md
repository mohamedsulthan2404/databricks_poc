## **Standardization Framework: Bronze -> Silver layer**
### **Author:** Mohamed Sulthan (mohamedsulthan.m@cittabase.com)
### **Created Date:** 2026-07-10 (YYYY-MM-DD)
### **Last Modified Date:** 2026-07-10 (YYYY-MM-DD)
### **Last Modified By:** Mohamed Sulthan (mohamedsulthan.m@cittabase.com)

### OVERVIEW
**This framework standardizes raw Bronze tables into governed Silver tables using a fully metadata-driven approach. Column mappings, target data types, default values, and column order are all defined in a central control table (METADATA_TABLE) rather than hardcoded per pipeline, so onboarding a new source table only requires adding metadata rows - no notebook changes**

### NOTEBOOKS
### 1. 00_Config
- Shared imports (re, uuid, datetime, pyspark.sql.functions)
- parameters (METADATA_TABLE, DEBUG, WRITE_MODE),
- exposed as widgets. Validates that the metadata control table exists.

### 2. 01_functions
####   Reusable helper functions used across the framework:
- snake_case()          : standardizes column naming convention
- get_metadata()         : looks up active column mappings for a table
- trim_string_columns()  : trims whitespace, converts blanks to NULL
- add_audit_columns()    : adds lineage/audit columns (_source_,_ingestion_timestamp, _batch_id)
- deduplicate()          : removes duplicates, key on primary key(s)
- log()                  : timestamped logging

### 3. 02_standardization_engine
### Core pipeline logic (standardize_table):
- Load metadata mapping
- Read Bronze table            
- Standardize column names
- Rename / fill / cast / 
- Cleanse strings
- Add audit columns
- Deduplicate
- Write to Silver (Delta, schema evolution enabled)

### 4. 03_run_pipeline
###   Orchestration entry point. Two modes, controlled via widget:
- single_table        : standardize one named source table
- all_active_tables    : reads all active tables from METADATA_TABLE and standardizes each, sharing one batch_id. Failures are logged per-table; a summary is raised at the end if any table failed.

### EXECUTION ORDER
- 00_Config -> 01_functions -> 02_standardization_engine -> 03_run_pipeline

### FURTHER ENHANCEMENTS
- Data Quality Checks
- Buisness Rules (client/project specifications)
- Notebook Optimization