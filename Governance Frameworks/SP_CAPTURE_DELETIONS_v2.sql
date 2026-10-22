-- ONE-TIME MIGRATION (audit table structure changed):
-- DROP TABLE IF EXISTS moh_raz.raz_casemix_transformed.t_ft_cs_deletion_aud;
-- DELETE FROM moh_raz.raz_casemix_transformed.t_ft_cs_deletion_aud_control;  -- reprocess all versions

CREATE OR REPLACE PROCEDURE moh_raz.raz_casemix_stg.SP_CAPTURE_DELETIONS()
LANGUAGE SQL
SQL SECURITY INVOKER
MODIFIES SQL DATA
AS
BEGIN
    -- VARIABLES
    DECLARE v_last_version     BIGINT DEFAULT 0;
    DECLARE v_start_version    BIGINT DEFAULT 1;
    DECLARE v_current_version  BIGINT DEFAULT 1;
    DECLARE v_source_table     STRING;
    DECLARE v_col_array        ARRAY<STRING>;
    DECLARE v_expr_1           STRING;
    DECLARE v_expr_2           STRING;
    DECLARE v_sql              STRING;

    -- Control table (one row per source table)
    CREATE TABLE IF NOT EXISTS moh_raz.raz_casemix_transformed.t_ft_cs_deletion_aud_control
    (
        catalog_name            STRING,
        schema_name             STRING,
        table_name              STRING,
        capture_columns         STRING,
        last_processed_version  BIGINT,
        is_active               INT,
        updated_at              TIMESTAMP
    )
    USING DELTA;

    -- Output table 1 (transformed)
    CREATE TABLE IF NOT EXISTS moh_raz.raz_casemix_transformed.t_ft_cs_deletion_aud
    (
        catalog_name             STRING,
        schema_name              STRING,
        table_name               STRING,
        healthcare_facility      STRING,
        patient_account_number   STRING,
        deleted_by               STRING,
        deleted_at               TIMESTAMP
    )
    USING DELTA;

    -- Output table 2 (stg) - same structure
    CREATE TABLE IF NOT EXISTS moh_raz.raz_casemix_stg.css_deletion_audit
    (
        catalog_name             STRING,
        schema_name              STRING,
        table_name               STRING,
        healthcare_facility      STRING,
        patient_account_number   STRING,
        deleted_by               STRING,
        deleted_at               TIMESTAMP
    )
    USING DELTA;

    -- Loop over every active entry in the lookup table
    FOR rec AS
        SELECT
            `catalog`  AS c_catalog,
            `schema`   AS c_schema,
            `table`    AS c_table,
            `columns`  AS c_columns
        FROM moh_raz.raz_casemix_transformed.css_deletion_lookup
        WHERE is_active = 1
        ORDER BY s_no
    DO

        -- 1. Fully qualified source table
        SET v_source_table = CONCAT(
            '`', rec.c_catalog, '`.`', rec.c_schema, '`.`', rec.c_table, '`'
        );

        -- 2. Last processed version for this table
        SET v_last_version = COALESCE(
            (
                SELECT MAX(last_processed_version)
                FROM moh_raz.raz_casemix_transformed.t_ft_cs_deletion_aud_control
                WHERE catalog_name = rec.c_catalog
                  AND schema_name  = rec.c_schema
                  AND table_name   = rec.c_table
                  AND is_active    = 1
            ),
            0
        );

        -- 3. Next version to process
        SET v_start_version = v_last_version + 1;

        -- 4. Latest Delta version of the source table
        SET v_sql = CONCAT(
            'SELECT COALESCE(MAX(version), -1) ',
            'FROM (DESCRIBE HISTORY ', v_source_table, ')'
        );
        EXECUTE IMMEDIATE v_sql INTO v_current_version;

        -- 5. Process only when there are new versions
        IF v_current_version >= v_start_version THEN

            -- 6. Map lookup columns by position to the output columns
            --    1st column -> healthcare_facility
            --    2nd column -> patient_account_number
            SET v_col_array = SPLIT(rec.c_columns, ',');

            SET v_expr_1 = CONCAT('CAST(c.`', TRIM(v_col_array[0]), '` AS STRING)');

            SET v_expr_2 = CASE
                WHEN SIZE(v_col_array) > 1
                THEN CONCAT('CAST(c.`', TRIM(v_col_array[1]), '` AS STRING)')
                ELSE 'CAST(NULL AS STRING)'
            END;

            -- 7. Build a temp view with the deleted rows (read the change feed once)
            SET v_sql = CONCAT(
                'CREATE OR REPLACE TEMPORARY VIEW v_deletions_tmp AS ',
                'SELECT ',
                CHR(39), rec.c_catalog, CHR(39), ' AS catalog_name, ',
                CHR(39), rec.c_schema,  CHR(39), ' AS schema_name, ',
                CHR(39), rec.c_table,   CHR(39), ' AS table_name, ',
                v_expr_1, ' AS healthcare_facility, ',
                v_expr_2, ' AS patient_account_number, ',
                'h.userName AS deleted_by, ',
                'c._commit_timestamp AS deleted_at ',
                'FROM table_changes(',
                CHR(39), v_source_table, CHR(39), ', ',
                CAST(v_start_version AS STRING), ', ',
                CAST(v_current_version AS STRING),
                ') c ',
                'LEFT JOIN (DESCRIBE HISTORY ', v_source_table, ') h ',
                'ON c._commit_version = h.version ',
                'WHERE c._change_type = ', CHR(39), 'delete', CHR(39)
            );
            EXECUTE IMMEDIATE v_sql;

            -- 8. Write the same rows to both output tables
            INSERT INTO moh_raz.raz_casemix_transformed.t_ft_cs_deletion_aud
                (catalog_name, schema_name, table_name,
                 healthcare_facility, patient_account_number,
                 deleted_by, deleted_at)
            SELECT catalog_name, schema_name, table_name,
                   healthcare_facility, patient_account_number,
                   deleted_by, deleted_at
            FROM v_deletions_tmp;

            INSERT INTO moh_raz.raz_casemix_stg.css_deletion_audit
                (catalog_name, schema_name, table_name,
                 healthcare_facility, patient_account_number,
                 deleted_by, deleted_at)
            SELECT catalog_name, schema_name, table_name,
                   healthcare_facility, patient_account_number,
                   deleted_by, deleted_at
            FROM v_deletions_tmp;

            -- 9. Update control table
            MERGE INTO moh_raz.raz_casemix_transformed.t_ft_cs_deletion_aud_control AS tgt
            USING
            (
                SELECT
                    rec.c_catalog     AS catalog_name,
                    rec.c_schema      AS schema_name,
                    rec.c_table       AS table_name,
                    rec.c_columns     AS capture_columns,
                    v_current_version AS last_processed_version
            ) AS src
            ON  tgt.catalog_name = src.catalog_name
            AND tgt.schema_name  = src.schema_name
            AND tgt.table_name   = src.table_name
            AND tgt.is_active    = 1
            WHEN MATCHED THEN
                UPDATE SET
                    tgt.capture_columns        = src.capture_columns,
                    tgt.last_processed_version = src.last_processed_version,
                    tgt.updated_at             = current_timestamp()
            WHEN NOT MATCHED THEN
                INSERT
                (
                    catalog_name, schema_name, table_name, capture_columns,
                    last_processed_version, is_active, updated_at
                )
                VALUES
                (
                    src.catalog_name, src.schema_name, src.table_name, src.capture_columns,
                    src.last_processed_version, 1, current_timestamp()
                );

        END IF;

    END FOR;

END;

-- Run it:
-- CALL moh_raz.raz_casemix_stg.SP_CAPTURE_DELETIONS();