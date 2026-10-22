-- Databricks notebook source
-- Create safe function for catalog name
CREATE OR REPLACE TEMPORARY FUNCTION safe_uc_name(value STRING)
RETURNS STRING
RETURN
  COALESCE(
    NULLIF(
      REGEXP_REPLACE(
        REGEXP_REPLACE(
          LOWER(TRIM(value)),
          '[^a-z0-9_]',
          '_'
        ),
        '_+',
        '_'
      ),
      ''
    ),
    'user'
  );


-- Create temp view of all available catalogs
CREATE OR REPLACE TEMPORARY VIEW list_of_catalogs AS
SELECT LOWER(catalog_name) AS catalog_names
FROM system.information_schema.catalogs;

-- COMMAND ----------

-- Start SQL scripting block to create and or set catalog based on Workspace
BEGIN

-- =========================================
-- 1. Declare variables
-- =========================================

  -- Leave catalog_forced as NONE to use the default labuser_yourusername catalog. 
  -- IF you already have a catalog you want to use instead, replace NONE with your catalog name.
  DECLARE catalog_forced STRING DEFAULT 'NONE';   -- <--- Modify to force a catalog


  DECLARE user_email STRING;
  DECLARE user_name STRING;
  -- Make the user name safe as a catalog name
  DECLARE safe_user_name STRING;
  -- Set's the vocareum catalog name 'labuser1234123423'
  DECLARE vocareum_catalog_name STRING DEFAULT 'NA';
  -- Catalog name to use outside of Vocareum
  DECLARE catalog_name STRING DEFAULT 'NA';
  -- Flag to determine if the catalog already exists
  DECLARE catalog_already_exists BOOLEAN DEFAULT FALSE;
  -- Create catalog statement to run
  DECLARE create_catalog_statement STRING DEFAULT '';
  -- View to create the catalog name as view to use outside of this script
  DECLARE create_view_with_catalog_name STRING DEFAULT '';


-- =========================================
-- 2. Capture current user
-- =========================================
  SET user_email = current_user();
  SET user_name = SPLIT(user_email, '@')[0];
  SET safe_user_name = (SELECT safe_uc_name(SPLIT(current_user(), '@')[0]));

-- ==================================================================================
-- 3. Determine Vocareum or Non Vocareum Workspace and set and/or create catalog (Non Vocareum)
-- ==================================================================================
  -- Check to see if the user is in Vocareum by email address then setting the catalog name to the labuser name.
  IF (LOWER(user_email) LIKE '%@vocareum.com')
    THEN 
      SET vocareum_catalog_name = safe_user_name;
      
      -- Check existence using the temp view of catalogs
      IF EXISTS (
        SELECT 1
        FROM list_of_catalogs
        WHERE catalog_names = LOWER(vocareum_catalog_name)
      ) THEN  

        -- Document the catalog already exists
        SET catalog_already_exists = TRUE;

        -- Create Temp View to Store the SQL Variable Value for Global Use
        SET create_view_with_catalog_name = CONCAT(
              "CREATE OR REPLACE TEMP VIEW catalog_name_vw AS ",
              "SELECT '", vocareum_catalog_name, "' AS catalog_name"
            );


      END IF; 

  -- If Vocareum check fails, setup assuming you are in another Workspace like Free Edition. Create a catalog using labuser_username
  ELSE

    -- Checks to see if a catalog is forced to be used. Will use that but the catalog has to exist already. 
    IF catalog_forced != 'NONE' THEN

      -- Use the forced catalog by the user
      SET catalog_name = catalog_forced;

      -- Tests to confirm the catalog exists. Error is returned if it doesn't.
      USE CATALOG IDENTIFIER(catalog_name);

      -- Document the catalog already exists
      SET catalog_already_exists = TRUE;

      -- Create Temp View to Store the SQL Variable Value for Global Use
      SET create_view_with_catalog_name = CONCAT(
        "CREATE OR REPLACE TEMP VIEW catalog_name_vw AS ",
        "SELECT '", catalog_name, "' AS catalog_name"
      );

    -- If catalog is not forced, create default catalog for learner
    ELSE

      -- Limit the user's name to 19 characters. THis is done because there is a limit to the catalog.schema.object name (64 characters). For someone with a long name this could cause issus. Using 19 because that is the general size of the vocareum user name
      SET catalog_name = CONCAT('labuser_', LEFT(safe_user_name,19));

      -- Create Temp View to Store the SQL Variable Value for Global Use
      SET create_view_with_catalog_name = CONCAT(
        "CREATE OR REPLACE TEMP VIEW catalog_name_vw AS ",
        "SELECT '", catalog_name, "' AS catalog_name"
      );

      -- Check existence using the temp view of catalogs
      IF EXISTS (
        SELECT 1
        FROM list_of_catalogs
        WHERE catalog_names = LOWER(catalog_name)
      ) 
        THEN 
        
          -- Document if the catalog already exists
          SET catalog_already_exists = TRUE;
      
      ELSE 
        -- Otherwise, create the catalog for the user
        SET create_catalog_statement = CONCAT(
          'CREATE CATALOG IF NOT EXISTS ',
          catalog_name
        );

        -- Create the catalog
        EXECUTE IMMEDIATE create_catalog_statement;
        
        -- Document if the catalog didn't exist
        SET catalog_already_exists = FALSE;

      END IF;

    END IF;

  END IF;

  -- Create the temp view with the catalog name
  EXECUTE IMMEDIATE create_view_with_catalog_name;


-- ===================================================================
-- 4. Return Final Script Results (Workspace Assumed and Catalog Name
-- ===================================================================
  SELECT
    CASE
      WHEN vocareum_catalog_name <> 'NA' THEN 'Vocareum Workspace'
      ELSE 'Non Vocareum Workspace'
    END AS Workspace,
    CASE
      WHEN vocareum_catalog_name <> 'NA' THEN vocareum_catalog_name
      ELSE catalog_name
    END AS `User Catalog Name`,
    CASE
      WHEN catalog_already_exists = TRUE THEN 'Catalog Already Exists'
      ELSE 'Catalog Created'
    END AS `Catalog Status`;
END;

-- COMMAND ----------

-- Create the global SQL variable with the catalog name using the temp view
DECLARE OR REPLACE my_catalog STRING;
SET VAR my_catalog = (SELECT catalog_name FROM catalog_name_vw);


-- Set default catalog to user's labuser catalog
USE CATALOG IDENTIFIER(my_catalog);


--Create lab schema for learner

DECLARE OR REPLACE my_schema STRING;
SET VAR my_schema = 'genie_course_bakehouse';

CREATE SCHEMA IF NOT EXISTS IDENTIFIER(my_schema);
USE SCHEMA IDENTIFIER(my_schema);

-- COMMAND ----------

CREATE OR REPLACE PROCEDURE copy_table(
  source_catalog STRING,
  source_schema STRING,
  target_catalog STRING,
  target_schema STRING,
  table_name STRING,
  delete_first BOOLEAN DEFAULT FALSE
)
LANGUAGE SQL
SQL SECURITY INVOKER
COMMENT 'Copies a single table from a source catalog.schema to a target catalog.schema. Creates target table with _gold suffix. Skips if the target table already exists. Set delete_first to TRUE to drop the target table before copying.'
BEGIN
  DECLARE source STRING;
  DECLARE target STRING;
  DECLARE target_table_name STRING;

  -- Append _gold to target table name
  SET target_table_name = table_name || '_gold';

  SET source = source_catalog || '.' || source_schema || '.' || table_name;
  SET target = target_catalog || '.' || target_schema || '.' || target_table_name;

  IF delete_first THEN
    EXECUTE IMMEDIATE 'DROP TABLE IF EXISTS ' || target;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM system.information_schema.tables
    WHERE table_catalog = target_catalog
      AND table_schema = target_schema
      AND table_name = target_table_name
  ) THEN
    EXECUTE IMMEDIATE 'CREATE TABLE ' || target || ' AS SELECT * FROM ' || source;
  END IF;
END;

-- COMMAND ----------

CREATE OR REPLACE PROCEDURE setup_all_tables(
  source_catalog STRING,
  source_schema STRING,
  target_catalog STRING,
  target_schema STRING,
  tables ARRAY<STRING>,
  delete_all BOOLEAN DEFAULT FALSE
)
LANGUAGE SQL
SQL SECURITY INVOKER
COMMENT 'Copies multiple tables from a source catalog.schema to a target catalog.schema. Calls copy_table for each table in the array and returns a log of all actions. Target tables are created with a _gold suffix. Set delete_all to TRUE to drop and recreate all tables.'
BEGIN
  DECLARE log STRING DEFAULT '';
  DECLARE i INT DEFAULT 0;
  DECLARE t STRING;
  DECLARE target STRING;
  DECLARE target_table_name STRING;

  WHILE i < SIZE(tables) DO
    SET t = tables[i];
    SET target_table_name = t || '_gold';
    SET target = target_catalog || '.' || target_schema || '.' || target_table_name;

    IF delete_all THEN
      CALL copy_table(source_catalog, source_schema, target_catalog, target_schema, t, TRUE);
      SET log = log || 'Dropped and recreated ' || target || '\n';
    ELSE
      IF EXISTS (
        SELECT 1 FROM system.information_schema.tables
        WHERE table_catalog = target_catalog
          AND table_schema = target_schema
          AND table_name = target_table_name
      ) THEN
        SET log = log || 'Skipped ' || target || ' - already exists.\n';
      ELSE
        CALL copy_table(source_catalog, source_schema, target_catalog, target_schema, t, FALSE);
        SET log = log || 'Created ' || target || '\n';
      END IF;
    END IF;

    SET i = i + 1;
  END WHILE;

  SELECT log AS status;
END;

-- COMMAND ----------

DROP VIEW IF EXISTS catalog_name_vw;
DROP VIEW IF EXISTS list_of_catalogs;
