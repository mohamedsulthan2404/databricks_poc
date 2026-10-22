# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Databricks Notebook Basics
# MAGIC
# MAGIC A **notebook** is where you write and run code in Databricks. It is made up of **cells**: code cells run code, and markdown cells hold formatted text like these instructions. In this lesson you will get to know the notebook interface, run Python and SQL, and document your work with markdown.
# MAGIC
# MAGIC ## Learning objectives
# MAGIC
# MAGIC By the end of this lesson, you should be able to:
# MAGIC
# MAGIC - **Navigate** the notebook interface and its sidebar tools.
# MAGIC - **Attach** a notebook to compute so you can run code.
# MAGIC - **Run** code cells in Python and SQL and view their output.
# MAGIC - **Create** and **edit** markdown cells, and **re-order** cells.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Notebook Interface
# MAGIC
# MAGIC Take a quick look around before you start. A notebook has a **toolbar** across the top and shortcut **sidebars** down the left and right edges.
# MAGIC
# MAGIC ### A1. Top toolbar
# MAGIC
# MAGIC 1. The toolbar runs across the top of the notebook. A few things to notice:
# MAGIC
# MAGIC 2. **Default language.** To the right of the menu bar, the **language dropdown** sets the notebook's default language: ![Language Dropdown](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/language-dropdown.png) This notebook's default is **Python**, which is why you use a `%sql` magic command later to run SQL in a single cell.
# MAGIC
# MAGIC 3. **Notebook format.** Open the **File** menu and point to **Notebook Format**. You will see this notebook is a **`.ipynb`** (Jupyter) file, the standard, portable notebook format.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### A2. Left sidebar
# MAGIC
# MAGIC - ![Table of Contents Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/toc.png) the notebook **table of contents**.
# MAGIC - ![Folder Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/folder.png) the **folder** structure of the workspace.
# MAGIC - ![Catalog Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/catalog.png) a list of available **catalogs**, schemas, and other assets.

# COMMAND ----------

# MAGIC %md
# MAGIC ### A3. Right sidebar
# MAGIC
# MAGIC - ![Experiments Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/experiments.png) create a workspace **experiment**.
# MAGIC - ![History Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/history.png) code **version history**.
# MAGIC - ![Variables Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/variables.png) a list of **variables** used in the notebook.
# MAGIC - ![Environment Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/environment-icon.png) view your **environment** configuration.
# MAGIC - ![Info Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/info.png) more **information** about the notebook.
# MAGIC - ![Genie Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/genie-icon.png) open **Genie Code**, the AI assistant that writes and explains code and diagnoses errors. We cover Genie Code later in the course.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## B. Attach to Compute
# MAGIC
# MAGIC Before you can run anything, a notebook needs **compute** attached. You saw this in the workspace tour, so here it is briefly.
# MAGIC
# MAGIC 1. In the upper-right corner of the notebook, between the **Run all** and **Schedule** buttons, click the **compute selector** dropdown.
# MAGIC 2. The list includes every compute resource you can access. Choose **Serverless**.
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">Serverless compute starts in seconds, so there is nothing to set up or wait for. Databricks Free Edition supports <b>Python</b> and <b>SQL</b>. R and Scala are available in paid editions.</div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Work with Code Cells
# MAGIC
# MAGIC Code cells run code, and the output appears directly below the cell.
# MAGIC
# MAGIC ### C1. Run a Python cell
# MAGIC
# MAGIC 1. Click the Python cell below to select it.
# MAGIC 2. Run it with the **Run** (&#9654;) icon in the cell's upper-left corner, or press **Shift + Enter**.
# MAGIC 3. Note the output that appears below the cell.

# COMMAND ----------

# This Python cell runs on the compute you attached.
print("Hello World")

print("2 + 2 =", 2 + 2)

# COMMAND ----------

# MAGIC %md
# MAGIC ### C2. Override the cell language with SQL
# MAGIC
# MAGIC As you saw in the toolbar, this notebook's default language is **Python**. You can still run another language in a single cell using a **magic command**. Starting a cell with **`%sql`** runs SQL.
# MAGIC
# MAGIC 1. Run the SQL cell below (**Shift + Enter**) and note the output.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT "Hello World" AS greeting, 2 + 2 AS simple_math

# COMMAND ----------

# MAGIC %md
# MAGIC ### C3. Add a cell and run all
# MAGIC
# MAGIC - **Add a cell:** hover just below a cell and click the **(+) Code** icon to insert a new code cell. Try typing `print("I added this cell")` and running it.
# MAGIC - **To run everything:** click **Run all** at the top of the notebook to run every cell in order.

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Work with Markdown Cells
# MAGIC
# MAGIC Markdown cells add formatted text and documentation to your notebook, like the instructions you are reading now.
# MAGIC
# MAGIC - **Create one:** hover above or below a cell and click the **(+) Text** icon. A new cell is added with `%md` at the top, which designates it as markdown.
# MAGIC - **Edit one:** double-click a markdown cell to edit it. Press **`Esc`** or run the cell to render it.
# MAGIC
# MAGIC Use the next cell to get to know markdown better.

# COMMAND ----------

# MAGIC %md
# MAGIC ### D1. Markdown example
# MAGIC
# MAGIC Double-click this cell to see the markdown behind it, then press **`Esc`** to render it again.
# MAGIC
# MAGIC # Title one
# MAGIC ## Title two
# MAGIC ### Title three
# MAGIC
# MAGIC This is text with a **bold** word in it.
# MAGIC
# MAGIC This is text with an *italicized* word in it.
# MAGIC
# MAGIC This is an ordered list:
# MAGIC 1. one
# MAGIC 1. two
# MAGIC 1. three
# MAGIC
# MAGIC This is an unordered list:
# MAGIC * apples
# MAGIC * peaches
# MAGIC * bananas
# MAGIC
# MAGIC Links: <a href="https://en.wikipedia.org/wiki/Markdown" target="_blank">Markdown - Wikipedia</a>
# MAGIC
# MAGIC And of course, tables:
# MAGIC
# MAGIC | name   | value |
# MAGIC |--------|-------|
# MAGIC | Yi     | 1     |
# MAGIC | Ali    | 2     |
# MAGIC | Selina | 3     |

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Re-order Cells
# MAGIC
# MAGIC You can move cells up or down to re-order them.
# MAGIC
# MAGIC - To the left of a cell, click and drag the ![Reorder Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/reorder-icon.png) up or down within the notebook to move the cell.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
