-- Databricks notebook source
-- MAGIC %run ./Classroom-Setup-Common-SQL-WAREHOUSE

-- COMMAND ----------

SELECT
  current_catalog() AS `Your Default Catalog`,
  current_schema() AS `Your Default Schema`
