-- Databricks notebook source
-- MAGIC %run ./Classroom-Setup-Common-SQL-WAREHOUSE

-- COMMAND ----------

-- MAGIC %run ./Classroom-Setup-0-REQUIRED-tables

-- COMMAND ----------

SELECT
  current_catalog() AS `Your Default Catalog`,
  current_schema() AS `Your Default Schema`
