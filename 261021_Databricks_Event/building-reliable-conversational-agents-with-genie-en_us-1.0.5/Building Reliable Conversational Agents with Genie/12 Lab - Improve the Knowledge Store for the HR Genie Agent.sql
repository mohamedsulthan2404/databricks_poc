-- Databricks notebook source
-- MAGIC %md
-- MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Lab - Improve the Knowledge Store for the HR Genie Agent
-- MAGIC
-- MAGIC #### Duration: ~20 Minutes
-- MAGIC
-- MAGIC ## Overview
-- MAGIC
-- MAGIC In the previous lab, you created an HR Genie Agent, added tables, and established baseline benchmarks. Some of those benchmarks likely failed because Genie was working with **table and column names only** — no metadata, no SQL logic, no instructions.
-- MAGIC
-- MAGIC In this lab, you will **iteratively improve** your HR Genie Agent using the same three-phase approach from the demonstrations:
-- MAGIC
-- MAGIC 1. **Metadata** — Table and column descriptions, synonyms, and prompt matching
-- MAGIC 2. **SQL Logic** — Joins, SQL expressions, and example SQL queries
-- MAGIC 3. **Instructions** — Text instructions defining business terms and default behaviors
-- MAGIC
-- MAGIC After each phase, you will re-run your benchmarks to measure progress. The goal is to get **all benchmarks passing**.
-- MAGIC
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lab, you will be able to:
-- MAGIC
-- MAGIC 1. **Add table and column descriptions** to Unity Catalog tables using `ALTER TABLE` SQL statements.
-- MAGIC 2. **Add column synonyms** in the Knowledge Store to map business terms to column names.
-- MAGIC 3. **Enable prompt matching** (format assistance and entity matching) on key categorical columns.
-- MAGIC 4. **Add a join** in the Knowledge Store to define table relationships.
-- MAGIC 5. **Add a SQL expression** to create a derived field for Genie.
-- MAGIC 6. **Add example SQL queries** to teach Genie complex query patterns.
-- MAGIC 7. **Add text instructions** to define ambiguous business terms and set default behaviors.
-- MAGIC 8. **Re-run benchmarks** after each phase and measure improvement.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #f44336;
-- MAGIC   background: #ffebee;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Prerequisites</strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Complete **Lab 05 - Create an HR Genie**. This lab builds on the HR Genie Agent and benchmarks you created in Lab 05.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## REQUIRED - SELECT A COMPUTE ENVIRONMENT
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #f44336;
-- MAGIC   background: #ffebee;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Select a Serverless SQL Warehouse</strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Before starting this notebook, select the required compute environment listed below.
-- MAGIC
-- MAGIC - **Serverless SQL Warehouse (2X-Small is sufficient)**
-- MAGIC   - Select **Compute** > **More** > **SQL Warehouse** > Select a SQL Warehouse you have access to.
-- MAGIC
-- MAGIC **NOTE:** This notebook was **developed and tested using Serverless SQL Warehouse**. Other compute options may work but are not guaranteed to behave the same or support all features demonstrated.
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## A. Review - Where You Left Off
-- MAGIC
-- MAGIC In **05 Lab - Create an HR Genie Agent**, you created an HR Genie Agent with 4 tables and added benchmarks.
-- MAGIC
-- MAGIC ##### Without any metadata or instructions, your results likely looked like this:
-- MAGIC
-- MAGIC <div style="margin: 16px 0;">
-- MAGIC   <strong style="display:block; margin-bottom:12px; font-size: 14pt; color: #0b2026;">
-- MAGIC     Expected Baseline Results (Results May Vary)
-- MAGIC   </strong>
-- MAGIC
-- MAGIC <style>
-- MAGIC table td, table th {
-- MAGIC   font-size: 14pt !important;
-- MAGIC }
-- MAGIC </style>
-- MAGIC
-- MAGIC <table style="width: 100%; border-collapse: collapse; line-height: 1.5;">
-- MAGIC   <thead>
-- MAGIC     <tr style="background: #1B5162; color: white;">
-- MAGIC       <th style="padding: 10px 14px; text-align: center; width: 40px; border: 1px solid #EEEDE9;">#</th>
-- MAGIC       <th style="padding: 10px 14px; text-align: left; border: 1px solid #EEEDE9;">Benchmark Question</th>
-- MAGIC       <th style="padding: 10px 14px; text-align: left; border: 1px solid #EEEDE9;">Likely Baseline Result</th>
-- MAGIC       <th style="padding: 10px 14px; text-align: left; border: 1px solid #EEEDE9;">Why</th>
-- MAGIC     </tr>
-- MAGIC   </thead>
-- MAGIC   <tbody>
-- MAGIC     <tr style="background: #E8F7EF;">
-- MAGIC       <td style="padding: 10px 14px; text-align: center; border: 1px solid #EEEDE9;">1</td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9;"><em>How many active employees do we have?</em></td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9; font-weight: 700; color: #00A972;">Passed</td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9;">Simple filter — column names are clear</td>
-- MAGIC     </tr>
-- MAGIC     <tr style="background: #E8F7EF;">
-- MAGIC       <td style="padding: 10px 14px; text-align: center; border: 1px solid #EEEDE9;">2</td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9;"><em>What is the average salary by department?</em></td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9; font-weight: 700; color: #00A972;">Passed</td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9;">Descriptive column names make the join obvious</td>
-- MAGIC     </tr>
-- MAGIC     <tr style="background: #FDECEA;">
-- MAGIC       <td style="padding: 10px 14px; text-align: center; border: 1px solid #EEEDE9;">3</td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9;"><em>Who are our most underpaid employees?</em></td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9; font-weight: 700; color: #98102A;">Failed</td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9;">"Underpaid" is ambiguous — Genie doesn't know it means <code>comp_ratio &lt; 1.0</code></td>
-- MAGIC     </tr>
-- MAGIC     <tr style="background: #FDECEA;">
-- MAGIC       <td style="padding: 10px 14px; text-align: center; border: 1px solid #EEEDE9;">4</td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9;"><em>Which managers have the highest attrition on their teams?</em></td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9; font-weight: 700; color: #98102A;">Failed</td>
-- MAGIC       <td style="padding: 10px 14px; border: 1px solid #EEEDE9;">"Attrition" isn't in the schema + requires three-table join</td>
-- MAGIC     </tr>
-- MAGIC   </tbody>
-- MAGIC </table>
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC Your goal in this lab is to **make all benchmarks pass** by iteratively adding context to the Knowledge Store using the three-phase approach from the demonstrations.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Classroom Setup
-- MAGIC
-- MAGIC 1. Run the cell below to set your default catalog and schema.

-- COMMAND ----------

-- MAGIC %run ./Includes/Classroom-Setup-lab-setup

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="max-width: 1200px; margin: 0 auto; font-family: sans-serif;">
-- MAGIC
-- MAGIC <div style="background: #F9F7F4; border-radius: 10px; padding: 22px 26px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); border-top: 6px solid #FF5F46;">
-- MAGIC
-- MAGIC   <img src="https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/icons/genie-code.png" style="height: 44px; margin-bottom: 10px;">
-- MAGIC
-- MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 12px;">
-- MAGIC     Need Help? Use Genie Code
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <div style="font-size: 15pt; color: #0b2026; line-height: 1.6; margin-bottom: 16px;">
-- MAGIC     Genie is an AI-powered assistant that can help you as you work through this lab.
-- MAGIC     Use it if you get stuck or want a little extra guidance.
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <div style="display: flex; gap: 10px;">
-- MAGIC     <a href="https://docs.databricks.com/aws/en/genie-code/" target="_blank" style="display: inline-block; background: #1B5162; color: white; font-size: 14pt; font-weight: 700; padding: 10px 22px; border-radius: 8px; text-decoration: none;">
-- MAGIC       AWS →
-- MAGIC     </a>
-- MAGIC     <a href="https://learn.microsoft.com/en-us/azure/databricks/genie-code/use-genie-code" target="_blank" style="display: inline-block; background: #1B5162; color: white; font-size: 14pt; font-weight: 700; padding: 10px 22px; border-radius: 8px; text-decoration: none;">
-- MAGIC       Azure →
-- MAGIC     </a>
-- MAGIC     <a href="https://docs.databricks.com/gcp/en/genie-code/" target="_blank" style="display: inline-block; background: #1B5162; color: white; font-size: 14pt; font-weight: 700; padding: 10px 22px; border-radius: 8px; text-decoration: none;">
-- MAGIC       GCP →
-- MAGIC     </a>
-- MAGIC   </div>
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## C. Step 1: Add Table and Column Metadata
-- MAGIC
-- MAGIC Metadata are the **easiest, highest-impact** change you can make. They tell Genie what each table contains, what each column means, and what values are valid.
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #1976d2;
-- MAGIC   background: #e3f2fd;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     What Good Metadata Includes
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC - **Table descriptions**: What does this table represent? When should Genie use it?
-- MAGIC - **Column descriptions**: What does this column mean? What are the valid values? How does it join to other tables?
-- MAGIC - **Primary/foreign key constraints**: Informational metadata that tells Genie how tables join. These are `NOT ENFORCED` — they are hints, not data-level constraints.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C1. Add Metadata Using `ALTER TABLE`
-- MAGIC
-- MAGIC The SQL below adds table descriptions, column descriptions, and primary/foreign key constraints to all four HR tables at once.
-- MAGIC
-- MAGIC 1. **Review the metadata** being added as the code executes. Pay attention to:
-- MAGIC    - How column descriptions clarify ambiguous terms (e.g., what does **comp_ratio** mean?)
-- MAGIC    - How join relationships are made explicit through foreign key constraints
-- MAGIC    - How valid values are listed for categorical columns like **status** and **reason_code**
-- MAGIC
-- MAGIC 2. **TO DO: Feel free to make any changes you see fit.**
-- MAGIC
-- MAGIC 3. Run the cell below.

-- COMMAND ----------

-- -----------------------------------------------------------
-- employees
-- -----------------------------------------------------------
COMMENT ON TABLE employees
  IS 'Employee profiles for the company. Each row represents one unique employee. Use employee_id to join with compensation, and manager_id to join with managers. The status column indicates whether the employee is currently Active, Resigned, or Terminated.';

ALTER TABLE employees
  ALTER COLUMN employee_id COMMENT 'Unique identifier for each employee (e.g., EMP-0001). Primary key. Join key to compensation.employee_id and resignations.employee_id.';
ALTER TABLE employees
  ALTER COLUMN first_name COMMENT 'Employee first name.';
ALTER TABLE employees
  ALTER COLUMN last_name COMMENT 'Employee last name.';
ALTER TABLE employees
  ALTER COLUMN department COMMENT 'Department the employee belongs to. Valid values: Engineering, Product, Operations, Finance, Marketing, Sales, Customer Success.';
ALTER TABLE employees
  ALTER COLUMN region COMMENT 'Geographic region where the employee is based. Valid values: West Coast, Southwest, Midwest, Northeast, Southeast.';
ALTER TABLE employees
  ALTER COLUMN hire_date COMMENT 'Date the employee was hired.';
ALTER TABLE employees
  ALTER COLUMN manager_id COMMENT 'Foreign key to managers.manager_id. Identifies the employee direct manager.';
ALTER TABLE employees
  ALTER COLUMN job_title COMMENT 'Employee job title (e.g., Senior Engineer, Staff Engineer, Product Manager).';
ALTER TABLE employees
  ALTER COLUMN job_level COMMENT 'Numeric job level. Higher numbers indicate more senior roles.';
ALTER TABLE employees
  ALTER COLUMN status COMMENT 'Current employment status. Valid values: Active (currently employed), Resigned (voluntarily left), Terminated (involuntarily separated). Use this column to filter for current vs. former employees.';

ALTER TABLE employees ALTER COLUMN employee_id SET NOT NULL;
ALTER TABLE employees ADD CONSTRAINT pk_employees PRIMARY KEY (employee_id) NOT ENFORCED;

-- -----------------------------------------------------------
-- managers (must come before employees FK)
-- -----------------------------------------------------------
COMMENT ON TABLE managers
  IS 'Manager profiles. Each row represents a manager with their department, region, team size, and performance rating. Use manager_id to join with employees.manager_id. Managers with a non-null end_date are no longer active.';

ALTER TABLE managers
  ALTER COLUMN manager_id COMMENT 'Unique identifier for each manager (e.g., MGR-001). Primary key. Join key to employees.manager_id.';
ALTER TABLE managers
  ALTER COLUMN manager_name COMMENT 'Full name of the manager.';
ALTER TABLE managers
  ALTER COLUMN department COMMENT 'Department the manager leads. Valid values match employees.department.';
ALTER TABLE managers
  ALTER COLUMN region COMMENT 'Geographic region where the manager is based. Valid values match employees.region.';
ALTER TABLE managers
  ALTER COLUMN team_size COMMENT 'Number of direct reports for this manager.';
ALTER TABLE managers
  ALTER COLUMN start_date COMMENT 'Date the manager started in this role.';
ALTER TABLE managers
  ALTER COLUMN end_date COMMENT 'Date the manager left this role. NULL means the manager is currently active.';
ALTER TABLE managers
  ALTER COLUMN performance_rating COMMENT 'Manager performance rating on a 1.0 to 5.0 scale. Higher is better.';

ALTER TABLE managers ALTER COLUMN manager_id SET NOT NULL;
ALTER TABLE managers ADD CONSTRAINT pk_managers PRIMARY KEY (manager_id) NOT ENFORCED;

-- -----------------------------------------------------------
-- compensation
-- -----------------------------------------------------------
COMMENT ON TABLE compensation
  IS 'Compensation details for each employee. Each row contains salary, market benchmark, and raise history. Use employee_id to join with the employees table. The comp_ratio column indicates whether an employee is paid above (> 1.0) or below (< 1.0) market rate.';

ALTER TABLE compensation
  ALTER COLUMN employee_id COMMENT 'Foreign key to employees.employee_id. Each employee has exactly one compensation record.';
ALTER TABLE compensation
  ALTER COLUMN base_salary COMMENT 'Current annual base salary in dollars.';
ALTER TABLE compensation
  ALTER COLUMN market_benchmark COMMENT 'Market benchmark salary in dollars for this role and level. Used to compare against base_salary.';
ALTER TABLE compensation
  ALTER COLUMN comp_ratio COMMENT 'Compensation ratio = base_salary / market_benchmark. A comp_ratio below 1.0 means the employee is paid below market rate (underpaid). A comp_ratio above 1.0 means paid above market rate. Use this column to identify underpaid employees.';
ALTER TABLE compensation
  ALTER COLUMN last_raise_date COMMENT 'Date of the employee most recent salary raise.';
ALTER TABLE compensation
  ALTER COLUMN last_raise_pct COMMENT 'Percentage of the most recent salary raise (e.g., 3.5 means a 3.5% raise).';

ALTER TABLE compensation ADD CONSTRAINT fk_compensation_employee FOREIGN KEY (employee_id) REFERENCES employees(employee_id) NOT ENFORCED;

-- -----------------------------------------------------------
-- resignations
-- -----------------------------------------------------------
COMMENT ON TABLE resignations
  IS 'Resignation records for employees who voluntarily left the company. Each row represents one resignation event. Use employee_id to join with employees to get employee details, and then employees.manager_id to join with managers for attrition analysis. Only employees with status = Resigned appear here.';

ALTER TABLE resignations
  ALTER COLUMN resignation_id COMMENT 'Unique identifier for each resignation record (e.g., RES-0001).';
ALTER TABLE resignations
  ALTER COLUMN employee_id COMMENT 'Foreign key to employees.employee_id. Identifies who resigned.';
ALTER TABLE resignations
  ALTER COLUMN resignation_date COMMENT 'Date the employee submitted their resignation.';
ALTER TABLE resignations
  ALTER COLUMN last_day COMMENT 'Employee final working day.';
ALTER TABLE resignations
  ALTER COLUMN reason_code COMMENT 'Primary reason for resignation. Valid values: Compensation, Career Growth, Manager Relationship, Personal, Relocation, Work-Life Balance.';
ALTER TABLE resignations
  ALTER COLUMN exit_survey_score COMMENT 'Exit survey satisfaction score on a 1.0 to 5.0 scale. Lower scores indicate more dissatisfaction.';

ALTER TABLE resignations ALTER COLUMN resignation_id SET NOT NULL;
ALTER TABLE resignations ADD CONSTRAINT pk_resignations PRIMARY KEY (resignation_id) NOT ENFORCED;
ALTER TABLE resignations ADD CONSTRAINT fk_resignations_employee FOREIGN KEY (employee_id) REFERENCES employees(employee_id) NOT ENFORCED;

-- Add FK from employees to managers (after managers PK exists)
ALTER TABLE employees ADD CONSTRAINT fk_employees_manager FOREIGN KEY (manager_id) REFERENCES managers(manager_id) NOT ENFORCED;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C2. Verify Descriptions
-- MAGIC
-- MAGIC 1. Run the cell below to confirm descriptions and constraints were added.

-- COMMAND ----------

DESCRIBE TABLE EXTENDED employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Open your **HR Genie Agent** in a new tab. Select **Configure** > **Sources** and confirm that:
-- MAGIC    - Table descriptions appear at the top of each table
-- MAGIC    - Column descriptions are visible for each column
-- MAGIC
-- MAGIC    **NOTE:** You may need to refresh your Genie page if it was already open.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## D. Step 2: Add Column Synonyms and Prompt Matching
-- MAGIC
-- MAGIC Beyond descriptions, the Knowledge Store supports **synonyms** and **prompt matching**.
-- MAGIC
-- MAGIC Both of these are configured in the Genie Agent UI.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D1. Add Synonyms to Key Columns
-- MAGIC
-- MAGIC Synonyms map **business language** to column names. 
-- MAGIC
-- MAGIC Think about how your stakeholders talk about the data. They might say "salary" when they mean `base_salary`, or "pay" when they mean `compensation`.
-- MAGIC
-- MAGIC In your HR Genie Agent, add synonyms to the following columns. For each one:
-- MAGIC
-- MAGIC 1. Select **Configure** > **Sources** > select the table.
-- MAGIC
-- MAGIC 2. Click the **pencil icon** next to the column.
-- MAGIC
-- MAGIC 3. Add a **Display Name** and **Synonyms**, then click **Save**.
-- MAGIC
-- MAGIC | Table | Column | Display Name | Synonyms |
-- MAGIC |-------|--------|-------------|----------|
-- MAGIC | `compensation` | `base_salary` | `Base Salary` | `salary, pay, annual salary, current salary` |
-- MAGIC | `compensation` | `comp_ratio` | `Comp Ratio` | `compensation ratio, pay ratio, market ratio, underpaid ratio` |
-- MAGIC | `resignations` | `reason_code` | `Resignation Reason` | `reason, exit reason, departure reason, why they left` |
-- MAGIC | `resignations` | `exit_survey_score` | `Exit Survey Score` | `exit score, satisfaction score, departure score` |
-- MAGIC
-- MAGIC **NOTE:** Feel free to add additional synonyms to other columns based on how you think stakeholders would phrase their questions.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### D2. Enable Prompt Matching
-- MAGIC
-- MAGIC For key categorical columns, confirm that **format assistance** is enabled and enable **entity matching** where appropriate.
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #1976d2;
-- MAGIC   background: #e3f2fd;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Prompt Matching Recap
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC - **Format assistance** — samples representative values so Genie understands data formats. Enabled by default on most columns.
-- MAGIC - **Entity matching** — builds a complete list of distinct values for categorical columns. Use selectively on high-signal columns users frequently reference.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC Good candidates for entity matching in the HR dataset:
-- MAGIC
-- MAGIC | Table | Column | Why |
-- MAGIC |-------|--------|-----|
-- MAGIC | `employees` | `status` | Users filter by Active, Resigned, Terminated |
-- MAGIC | `employees` | `department` | Users ask about specific departments |
-- MAGIC | `resignations` | `reason_code` | Users ask about resignation reasons by name |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC For each column above:
-- MAGIC 1. Select **Configure** > **Sources** > select the table > click the **pencil icon** next to the column.
-- MAGIC
-- MAGIC 2. Click **Advanced**.
-- MAGIC
-- MAGIC 3. Confirm **Format assistance** is **on**.
-- MAGIC
-- MAGIC 4. Confirm **Entity matching** is **on**.
-- MAGIC
-- MAGIC 5. Click **Save**.
-- MAGIC
-- MAGIC **NOTE:** By default Genie will automatically set these for you so yours might already be enabled.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## E. Run Benchmarks After Adding Metadata
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #1976d2;
-- MAGIC   background: #e3f2fd;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Test After Every Phase
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Each time you complete a phase of changes to your Genie Agent, re-run benchmarks to confirm:
-- MAGIC - Did the change **fix** the questions it was intended to fix?
-- MAGIC - Did the change **break** anything that was already working?
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC 1. In your HR Genie Agent, select **Benchmarks** > **Run all**.
-- MAGIC
-- MAGIC 2. Review the results. Did any previously failing benchmarks improve?
-- MAGIC
-- MAGIC 3. Take note of which benchmarks still need work.
-- MAGIC     - These will be addressed by **SQL Logic** and **Instructions** in the next phases.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## F. Step 3: Add SQL Logic to the Knowledge Store
-- MAGIC
-- MAGIC SQL logic addresses the benchmark failures that metadata alone could not fix. In this section, you will add:
-- MAGIC
-- MAGIC | What | Why |
-- MAGIC |------|-----|
-- MAGIC | **Joins** | Define table relationships explicitly so Genie connects tables correctly |
-- MAGIC | **SQL Expressions** | Create derived columns that do not exist in the data but can be computed |
-- MAGIC | **Example SQL Queries** | Teach Genie complex query patterns it is unlikely to generate on its own |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### F1. Add a Join
-- MAGIC
-- MAGIC While the foreign key constraints you added in the metadata phase give Genie join hints, explicitly defining joins in the Knowledge Store provides additional guidance. Especially for multi-table patterns.
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Benchmark This Helps
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC **Benchmark #4: Which managers have the highest attrition on their teams?** — This requires joining `resignations > employees > managers`. Defining the employees-to-managers join explicitly helps Genie find this path.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. In your HR Genie Agent, select **Configure** > **Examples**.
-- MAGIC
-- MAGIC 2. Select **Add** > **Join**.
-- MAGIC
-- MAGIC 3. Configure the join:
-- MAGIC    - **Left Table:** `employees`
-- MAGIC    - **Right Table:** `managers`
-- MAGIC    - **Join Condition:** `manager_id` on both tables
-- MAGIC    - **Relationship Type:** `Many to One`
-- MAGIC
-- MAGIC 4. Add the following to the **Instructions**: `Each employee has exactly one manager. Use this join when answering questions about manager performance, team composition, or attrition by manager. To calculate attrition by manager, join resignations to employees first (on employee_id), then employees to managers (on manager_id).`
-- MAGIC
-- MAGIC 5. Select **Save**.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### F2. Add a SQL Expression
-- MAGIC
-- MAGIC SQL expressions let you define **derived columns**. 
-- MAGIC
-- MAGIC These are values that do not exist in the data but can be computed from existing columns. Genie can use these expressions in generated SQL.
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Benchmark This Helps
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC **Benchmark #3: Who are our most underpaid employees?** — Our business categorizes employees by compensation status based on their `comp_ratio`. This expression creates a `compensation_status` field that maps comp_ratio values to business categories.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. In your HR Genie Agent, select **Configure** > **Examples**.
-- MAGIC
-- MAGIC 2. Select **Add** > **Field**.
-- MAGIC
-- MAGIC 3. **Name the Field:** `compensation_status`
-- MAGIC
-- MAGIC 4. Run the cell below to generate the SQL **Code** with your catalog name.

-- COMMAND ----------

DECLARE OR REPLACE my_query STRING DEFAULT "";

SET VAR my_query = "
CASE
    WHEN " || current_catalog() || ".genie_course_hr.compensation.comp_ratio < 0.9
      THEN 'Significantly Underpaid'
    WHEN " || current_catalog() || ".genie_course_hr.compensation.comp_ratio < 1.0
      THEN 'Slightly Underpaid'
    WHEN " || current_catalog() || ".genie_course_hr.compensation.comp_ratio <= 1.1
      THEN 'At Market'
    ELSE 'Above Market'
END
";

SELECT my_query;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Copy the output above and paste into the **Code** field.
-- MAGIC
-- MAGIC 6. Add the following:
-- MAGIC    - **Synonyms:** `pay status, comp status, salary status, underpaid status`
-- MAGIC    - **Instructions:** `When users ask about compensation categories, pay bands, or underpaid status, use this expression. Employees with comp_ratio below 1.0 are considered underpaid. SCOPE_TABLES: Use with compensation and employees tables.`
-- MAGIC
-- MAGIC 7. Select **Save**.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### F3. Add Example SQL Queries
-- MAGIC
-- MAGIC Example SQL queries teach Genie **query patterns** that it is unlikely to generate on its own. Genie uses these as trusted templates when similar questions are asked.
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #1976d2;
-- MAGIC   background: #e3f2fd;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Think of Example Queries as Teaching Patterns
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC One good example query can improve answers for many similar questions. Genie uses them in two ways:
-- MAGIC - It can **use the query directly** when a question matches
-- MAGIC - Or **learn from it** to generate similar queries for related questions
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC #### F3a. Add Example Query: Who are our most underpaid employees?
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Benchmark This Fixes
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC **Benchmark #3: Who are our most underpaid employees?** — Genie does not know that "underpaid" means `comp_ratio < 1.0`. This query teaches the exact pattern.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. In your HR Genie Agent, select **Configure** > **Examples**.
-- MAGIC
-- MAGIC 2. Select **Add** > **Example Query**.
-- MAGIC
-- MAGIC 3. Enter the question: `Who are our most underpaid employees?`
-- MAGIC
-- MAGIC 4. Run the cell below to generate the query with your catalog name, then paste it as the SQL query.

-- COMMAND ----------

DECLARE OR REPLACE my_query STRING DEFAULT "";

SET VAR my_query = "
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.department,
    e.job_title,
    c.base_salary,
    c.market_benchmark,
    c.comp_ratio
FROM " || current_catalog() || ".genie_course_hr.employees e
JOIN " || current_catalog() || ".genie_course_hr.compensation c
    ON e.employee_id = c.employee_id
WHERE c.comp_ratio < 1.0
ORDER BY c.comp_ratio ASC
LIMIT 10
";

SELECT my_query;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Copy the output above and paste into the **SQL query** field.
-- MAGIC
-- MAGIC 6. Select **Preview** to verify the results look correct.
-- MAGIC
-- MAGIC 7. Expand **Usage Guidance** and add: `When users ask about underpaid employees, use comp_ratio < 1.0 as the filter. Return the most underpaid first (lowest comp_ratio). Default to top 10 unless specified otherwise.`
-- MAGIC
-- MAGIC 8. Select **Save**.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC #### F3b. Add Example Query: Which managers have the highest attrition?
-- MAGIC
-- MAGIC This teaches Genie the **three-table join** pattern needed to connect resignations to managers through employees.
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Benchmark This Fixes
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC **Benchmark #4: Which managers have the highest attrition on their teams?** — This requires joining `resignations > employees > managers`. Genie is unlikely to discover this three-table join on its own.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. In your HR Genie Agent, select **Configure** > **Examples**.
-- MAGIC
-- MAGIC 2. Select **Add** > **Example Query**.
-- MAGIC
-- MAGIC 3. Enter the question: `Which managers have the highest attrition on their teams?`
-- MAGIC
-- MAGIC 4. Run the cell below to generate the query with your catalog name, then paste it as the SQL query.

-- COMMAND ----------

DECLARE OR REPLACE my_query STRING DEFAULT "";

SET VAR my_query = "
SELECT
    m.manager_name,
    m.department,
    m.region,
    COUNT(r.resignation_id) AS attrition_count
FROM " || current_catalog() || ".genie_course_hr.resignations r
JOIN " || current_catalog() || ".genie_course_hr.employees e
    ON r.employee_id = e.employee_id
JOIN " || current_catalog() || ".genie_course_hr.managers m
    ON e.manager_id = m.manager_id
GROUP BY
    m.manager_name,
    m.department,
    m.region
ORDER BY attrition_count DESC
LIMIT 10
";

SELECT my_query;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Copy the output above and paste into the **SQL query** field.
-- MAGIC
-- MAGIC 6. Select **Preview** to verify the results look correct.
-- MAGIC
-- MAGIC 7. Expand **Usage Guidance** and add: `Attrition means the count of resignations per manager. Resignations do not link directly to managers — always join through the employees table. Return top 10 by default.`
-- MAGIC
-- MAGIC 8. Select **Save**.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## G. Run Benchmarks After Adding SQL Logic
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #1976d2;
-- MAGIC   background: #e3f2fd;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Checkpoint: Phase 2 Complete
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC You have now added a join, a SQL expression, and two example SQL queries. Re-run benchmarks to see the impact:
-- MAGIC - Did the "underpaid" and "attrition" benchmarks improve?
-- MAGIC - Did anything that was already passing break?
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC 1. In your HR Genie Agent, select **Benchmarks** > **Run all**.
-- MAGIC
-- MAGIC 2. Review results. The "underpaid" and "attrition" benchmarks should show significant improvement.
-- MAGIC
-- MAGIC 3. If benchmarks are still failing, consider:
-- MAGIC    - Does the SQL expression need adjustments?
-- MAGIC    - Are the example queries using fully qualified table names?
-- MAGIC    - You can also try **Knowledge Mining**: 
-- MAGIC       - In **Benchmarks** > **Evaluations**
-- MAGIC       - select your latest evaluation
-- MAGIC       - select a failed benchmark
-- MAGIC       - click **Review proposed fixes**.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## H. Step 4: Add Text Instructions - Final Touch
-- MAGIC
-- MAGIC Text instructions define **business terms** and **default behaviors** that cannot be expressed in SQL or metadata alone. 
-- MAGIC
-- MAGIC Use them for what metadata and SQL logic cannot handle.
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     What Still Needs Defining?
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Even with SQL logic in place, Genie may benefit from explicit behavioral guidance:
-- MAGIC - **"Underpaid"** — Reinforce the definition: `comp_ratio < 1.0`
-- MAGIC - **"Attrition"** — Reinforce the join path: `resignations → employees → managers`
-- MAGIC - **Formatting** — Should currency be rounded? How many results by default?
-- MAGIC - **Counting** — Should Genie use `COUNT(*)` or `COUNT(DISTINCT ...)`?
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### H1. Add Text Instructions
-- MAGIC
-- MAGIC 1. In your HR Genie Agent, select **Configure** > **Instructions**.
-- MAGIC
-- MAGIC 2. Add text instructions that reinforce your SQL logic and address general behaviors. Consider including:
-- MAGIC    - A definition for **"underpaid"** (hint: `comp_ratio < 1.0`)
-- MAGIC    - A definition for **"attrition"** (hint: count of resignations per manager, joined through employees)
-- MAGIC    - Formatting rules (e.g., round salary values to 2 decimal places)
-- MAGIC    - Default row limits (e.g., return top 10 unless specified otherwise)
-- MAGIC    - Counting behavior (e.g., use `COUNT(*)` unless the user asks for distinct values)
-- MAGIC
-- MAGIC 3. Select **Save**.
-- MAGIC
-- MAGIC **NOTE:** View the suggestion solution for ideas, or try your own.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC
-- MAGIC ##### SUGGESTED SOLUTIONS — TEXT INSTRUCTIONS
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary>Click to expand suggested text instructions</summary>
-- MAGIC
-- MAGIC <br/>
-- MAGIC
-- MAGIC **NOTE:** These are suggestions. Your instructions may differ and still be effective. The key is that your instructions give Genie enough context to answer the benchmark questions correctly.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC **Suggested Text Instructions**
-- MAGIC
-- MAGIC ```
-- MAGIC - Underpaid Definition
-- MAGIC     - "Underpaid" employees are those with a comp_ratio below 1.0
-- MAGIC     - This means their base_salary is less than the market_benchmark
-- MAGIC     - When asked about underpaid employees, filter on comp_ratio < 1.0 and order by comp_ratio ASC
-- MAGIC     - Return the top 10 most underpaid employees by default unless specified otherwise
-- MAGIC     - Include: employee_id, first_name, last_name, department, job_title, base_salary, market_benchmark, comp_ratio
-- MAGIC
-- MAGIC - Attrition Definition
-- MAGIC     - "Attrition" means the count of resignations
-- MAGIC     - To find attrition by manager, join resignations to employees (on employee_id), then employees to managers (on manager_id)
-- MAGIC     - Resignations do not link directly to managers — always join through the employees table
-- MAGIC     - When asked about manager attrition, return manager_name, department, region, and resignation count
-- MAGIC     - Order by resignation count descending, return top 10 by default
-- MAGIC
-- MAGIC - Formatting
-- MAGIC     - Round all salary and currency values to 2 decimal places
-- MAGIC     - Format using US dollars
-- MAGIC
-- MAGIC - General Rules
-- MAGIC     - When counting rows, use COUNT(*) unless the user asks for distinct values
-- MAGIC     - Return top 10 results by default when ranking or listing "top" items
-- MAGIC ```
-- MAGIC
-- MAGIC </details>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #1976d2;
-- MAGIC   background: #e3f2fd;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Best Practice
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Keep text instructions **short and specific**. Avoid duplicating what is already defined in column descriptions, SQL expressions, or example queries. Instructions are for behavior and edge cases only.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## I. Run Final Benchmarks
-- MAGIC
-- MAGIC 1. In your HR Genie Agent, select **Benchmarks** > **Run all**.
-- MAGIC
-- MAGIC 2. Review your final results. The goal is that **all benchmarks pass**.
-- MAGIC
-- MAGIC 3. If some benchmarks still fail, consider:
-- MAGIC    - Are your instructions specific enough?
-- MAGIC    - Try **Knowledge Mining**: In **Benchmarks** > **Evaluations**, select your latest evaluation > select a failed benchmark > click **Review proposed fixes**. Review the suggested knowledge snippets and accept any that look correct.
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #ff9800;
-- MAGIC   background: #fff3e0;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
-- MAGIC     Results May Vary
-- MAGIC   </strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC Even with all three phases complete, Genie may not match your ground truth SQL exactly. 
-- MAGIC
-- MAGIC The goal is **directional improvement**.
-- MAGIC
-- MAGIC Are the results closer to what you expect? Over time, you refine further by adding more examples, adjusting instructions, and reviewing user feedback through Monitoring.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #7b1fa2;
-- MAGIC   background: #f3e5f5;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#4a148c; margin-bottom:6px; font-size: 1.1em;">Continue Practicing</strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC
-- MAGIC This was a simple starter Genie Agent. There is much more you can do to improve accuracy and consistency. 
-- MAGIC
-- MAGIC Continue building by adding additional benchmarks, refining SQL logic, enhancing metadata, and expanding your test coverage.
-- MAGIC
-- MAGIC Treat your Genie Agent like a product. Iterate, test, and improve over time.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## J. BONUS - Agent Mode in Genie Agents
-- MAGIC Agent mode is designed for deeper, multi-step investigation.
-- MAGIC
-- MAGIC The questions should be open-ended and analytical rather than single-query answers.
-- MAGIC
-- MAGIC - Agent mode in Genie Agents:
-- MAGIC [AWS](https://docs.databricks.com/aws/en/genie/agent-mode) |
-- MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-code/agent-mode) |
-- MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/agent-mode)
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Navigate to your Genie Agent.
-- MAGIC
-- MAGIC 2. Select **Agent** (instead of **Chat**)
-- MAGIC
-- MAGIC 3. Ask the following questions (or anything else you can think of) and view the results:
-- MAGIC
-- MAGIC 1. `Investigate what's driving employee resignations. Are there patterns by department, manager, or compensation?`
-- MAGIC    - Forces the agent to explore across all four tables, including resignation reasons, compensation ratios of resigned employees, manager performance ratings, and department-level breakdowns. This requires multi-step analysis rather than a single query.
-- MAGIC
-- MAGIC 2. `Which departments have the biggest compensation equity problems, and who are the most at-risk employees?`
-- MAGIC    - The agent would need to analyze compensation ratio distributions by department, identify underpaid clusters, cross-reference job levels and tenure, and surface specific employees. This requires iterative exploration across multiple dimensions.
-- MAGIC
-- MAGIC 3. `Compare attrition patterns between high-performing and low-performing managers. What do you find?`
-- MAGIC    - The agent needs to join manager performance ratings to employee and resignation data, segment managers into groups, and compare resignation counts, exit survey scores, and reason codes. This is a hypothesis-driven investigation, not a simple retrieval task.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## K. Conclusion
-- MAGIC
-- MAGIC In this lab, you improved your HR Genie Agent using the three-phase approach:
-- MAGIC
-- MAGIC **Phase 1 — Metadata:**
-- MAGIC - Added **table and column descriptions** to give Genie context about your HR data.
-- MAGIC - Added **synonyms** to bridge the gap between stakeholder language and column names.
-- MAGIC - Enabled **prompt matching** on key categorical columns.
-- MAGIC
-- MAGIC **Phase 2 — SQL Logic:**
-- MAGIC - Added a **join** to define the employees-to-managers relationship.
-- MAGIC - Added a **SQL expression** to create a `compensation_status` field.
-- MAGIC - Added **example SQL queries** to teach Genie complex patterns (underpaid employees and manager attrition).
-- MAGIC
-- MAGIC **Phase 3 — Instructions:**
-- MAGIC - Added **text instructions** to define ambiguous business terms like "underpaid" and "attrition" and set default behaviors.
-- MAGIC
-- MAGIC You **re-ran benchmarks** after each phase to measure improvement and catch regressions.
-- MAGIC
-- MAGIC You have now completed the full Genie curation lifecycle: from raw tables to a fully curated, benchmarked Genie Agent.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
-- MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
-- MAGIC <script>
-- MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
-- MAGIC </script>
