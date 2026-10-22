# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Navigating the Databricks Workspace
# MAGIC
# MAGIC This notebook is a guided tour of the Databricks Workspace UI: the homepage, your user settings, the left sidebar, search and the **+ New** menu, how to organize your assets, and the different types of compute. A few things look different in Databricks Free Edition, and we will flag those as we go.
# MAGIC
# MAGIC ## Learning objectives
# MAGIC
# MAGIC By the end of this lesson, you should be able to:
# MAGIC
# MAGIC - **Navigate** the Databricks Workspace homepage.
# MAGIC - **Access** and **configure** your user settings.
# MAGIC - **Use** the left sidebar to find features across SQL, data engineering, and AI/ML.
# MAGIC - **Use** intelligent search, **Recents**, and the **+ New** menu to find and create assets.
# MAGIC - **Organize** workspace assets with folders and files.
# MAGIC - **Identify** the different types of Databricks compute.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #FFAB00; background: rgba(255,171,0,0.12); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#0b2026; margin-bottom:6px; font-size:15pt;">NOTE - Open Links in a New Tab</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC
# MAGIC  Keep this notebook open as your directions. When you click a link below, open it in a new browser tab so you don't lose your place: 
# MAGIC
# MAGIC - Right-click and choose *Open link in new tab*.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. The Workspace Homepage
# MAGIC
# MAGIC 1. Right click the **Databricks logo** at the top left and select **Open Link in a New Tab**
# MAGIC    - You'll be taken to a screen that says **Welcome to Databricks**.
# MAGIC
# MAGIC 2. This page contains some helpful resources:
# MAGIC    - **Suggested**
# MAGIC       - These are objects you've recently opened or worked on, including notebooks, data tables, pipelines, and more.
# MAGIC    - **Favorites**
# MAGIC       - This is a list of objects you have "favorited" by selecting the Star icon next to its name.
# MAGIC
# MAGIC 3. Select **Workspace** in the main navigation bar to get your user files.
# MAGIC
# MAGIC 4. Close the browser tab.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Locate and Configure User Settings
# MAGIC
# MAGIC 1. At the top right, click your **user icon** (a letter from your username) and select **Settings**.
# MAGIC
# MAGIC 2. **Settings** opens to **User Settings**, which has five sections:
# MAGIC
# MAGIC    - **Profile**: your display name and the group(s) you belong to.
# MAGIC    - **Preferences**: **Language** (General) and **Interface Theme** (Appearance). Change these if you wish.
# MAGIC    - **Developer**: **Access Tokens**, **SQL Query Snippets**, and **Editor Settings** (General, Code Editor, Experimental Features, SQL Format).
# MAGIC    - **Linked Accounts**: Git integration. Link a Git account and select a **Personal Access Token** for a provider such as GitHub.
# MAGIC    - **Notifications**: manage **Model Registry**, **Comment**, **Account-level**, and **Promotional** email notifications.
# MAGIC
# MAGIC **NOTE:** Admins also see a **Workspace admin** menu. Those options are not covered in this content.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. The Main Navigation Sidebar
# MAGIC
# MAGIC No matter where you are in Databricks, the sidebar stays with you, organized by what you're trying to do: explore data, write code, run jobs, build dashboards, manage models.
# MAGIC
# MAGIC ### Showing and hiding the main navigation bar
# MAGIC
# MAGIC 1. Click the ![Sidebar Show Hide Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/sidebar-show-hide-icon.png) in the upper-left corner of the workspace. Clicking this icon will reveal or hide the left sidebar navigation. When it is hidden, you can reveal the navigation panel by hovering over the ![Sidebar Show Hide Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/sidebar-show-hide-icon.png) icon.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C1. Main Sidebar Groups (Common Tasks) High Level Overview
# MAGIC
# MAGIC The sidebar is broken up into functional groups. At the top are common tasks.
# MAGIC
# MAGIC These tasks consist of the following:
# MAGIC <br></br>
# MAGIC <div class="acc-wrap">
# MAGIC <style>
# MAGIC .acc-wrap { max-width: 900px; margin: 0 auto; font-family: sans-serif; --accent: #1B5162; --tint: rgba(27,81,98,0.08); }
# MAGIC .acc-wrap * { box-sizing: border-box; }
# MAGIC .acc-item { border: 2px solid #EEEDE9; border-radius: 8px; margin-bottom: 8px; overflow: hidden; transition: border-color 0.2s; }
# MAGIC .acc-item.open { border-color: var(--accent); }
# MAGIC .acc-header { display: flex; align-items: center; gap: 14px; padding: 14px 18px; cursor: pointer; user-select: none; background: #F9F7F4; transition: background 0.15s; }
# MAGIC .acc-item.open .acc-header { background: var(--tint); }
# MAGIC .acc-summary { flex: 1; font-size: 15pt; font-weight: 600; color: #0b2026; }
# MAGIC .acc-chevron { font-size: 14pt; color: #5E7077; transition: transform 0.25s; }
# MAGIC .acc-item.open .acc-chevron { transform: rotate(180deg); color: var(--accent); }
# MAGIC .acc-body { max-height: 0; opacity: 0; overflow: hidden; transition: max-height 0.3s ease, opacity 0.25s ease, padding 0.25s ease; padding: 0 18px 0 18px; font-size: 14pt; line-height: 1.7; color: #0b2026; }
# MAGIC .acc-item.open .acc-body { max-height: 600px; opacity: 1; padding: 4px 18px 18px 18px; }
# MAGIC .acc-body ul { margin: 8px 0 0; padding-left: 20px; }
# MAGIC .acc-body li { margin-bottom: 8px; }
# MAGIC </style>
# MAGIC
# MAGIC <div id="acc-container"></div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <script>
# MAGIC var ACC_DATA = [
# MAGIC   { summary: '+ New', detail: 'The fastest way to create things. Instead of hunting for the right page, use <strong>+ New</strong> to spin up a notebook, query, job, dashboard, and more from one menu.' },
# MAGIC   { summary: 'Learn', detail: 'Built-in tutorials and guided learning content. Appears in <strong>Databricks Free Edition</strong> only. On Vocareum or other workspaces you will not see it.' },
# MAGIC   { summary: 'Workspace', detail: 'Your file browser. The notebooks, folders, and libraries you create live here, organized much like files on your computer.' },
# MAGIC   { summary: 'Recents', detail: 'A shortcut back to whatever you opened last. Handy when you are jumping between a few notebooks and do not want to dig through the Workspace tree.' },
# MAGIC   { summary: 'Catalog', detail: 'The home for your data in Unity Catalog. Browse catalogs, schemas, tables, and views, preview data, and manage who can access what.' },
# MAGIC   { summary: 'Jobs & Pipelines', detail: 'Where you schedule and monitor work. Build <strong>Lakeflow Jobs</strong> to orchestrate tasks and <strong>Spark Declarative Pipelines</strong> for declarative data pipelines.' },
# MAGIC   { summary: 'Compute', detail: 'Create and manage the compute that runs your code. In this course you will mostly use Serverless, so you will not spend much time here.' },
# MAGIC   { summary: 'Discover (Beta)', detail: 'A searchable catalog of assets you have access to. Still in Beta, so expect it to keep evolving.' },
# MAGIC   { summary: 'Marketplace', detail: 'A place to get sample datasets, quick starts, and other helpful content you can bring into your workspace to explore.' }
# MAGIC ];
# MAGIC
# MAGIC (function() {
# MAGIC   var container = document.getElementById('acc-container');
# MAGIC   ACC_DATA.forEach(function(item, i) {
# MAGIC     var div = document.createElement('div');
# MAGIC     div.className = 'acc-item';
# MAGIC     div.innerHTML =
# MAGIC       '<div class="acc-header" onclick="toggleAcc(' + i + ')">'
# MAGIC       + '<div class="acc-summary">' + item.summary + '</div>'
# MAGIC       + '<div class="acc-chevron">&#9660;</div>'
# MAGIC       + '</div>'
# MAGIC       + '<div class="acc-body">'
# MAGIC       + '<div>' + item.detail + '</div>'
# MAGIC       + '</div>';
# MAGIC     container.appendChild(div);
# MAGIC   });
# MAGIC })();
# MAGIC
# MAGIC function toggleAcc(idx) {
# MAGIC   var items = document.querySelectorAll('.acc-item');
# MAGIC   items.forEach(function(el, i) {
# MAGIC     el.classList.toggle('open', i === idx && !el.classList.contains('open'));
# MAGIC   });
# MAGIC }
# MAGIC </script>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### C2. Task-Specific Groups
# MAGIC
# MAGIC Below the common tasks, the sidebar also groups tools by specialty: **SQL**, **Data Engineering**, and **AI/ML**. You will explore some of these areas in a later section where you use it, so we will not tour them all here.

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Search and the "+ New" Button

# COMMAND ----------

# MAGIC %md
# MAGIC ### D1. Intelligent Search
# MAGIC
# MAGIC Search helps you quickly find notebooks, queries, dashboards, tables, and more across your workspace. It is fuzzy, so partial names and keywords still surface the right results.
# MAGIC
# MAGIC **Finding assets through the search bar:**
# MAGIC - Click the **search bar** at the top-center (or press **Cmd/Ctrl + P**).
# MAGIC - Type the name of a table or notebook.
# MAGIC - Select a result from the dropdown, or press **Enter** to see all matches.
# MAGIC - Use filters to narrow results by type, such as **Notebooks**, **Dashboards**, or **Tables**.
# MAGIC
# MAGIC **Finding recent files and folders:**
# MAGIC - On the left sidebar, right click on **Recents** and open in a new tab.
# MAGIC - Select the file, notebook, or table you want to revisit.
# MAGIC
# MAGIC For more, see the **Search for workspace objects** docs: [AWS](https://docs.databricks.com/aws/en/search/) | [Azure](https://learn.microsoft.com/en-us/azure/databricks/search/) | [GCP](https://docs.databricks.com/gcp/en/search/).

# COMMAND ----------

# MAGIC %md
# MAGIC ### D2. The '+ New' Menu
# MAGIC
# MAGIC **+ New** at the top of the sidebar is the quickest way to create something. The options a new user reaches for most are:
# MAGIC
# MAGIC - **Notebook** - Interactive document for writing and running code in Python, SQL, Scala, or R. (Scala and R are not available in Databricks Free Edition.)
# MAGIC - **Query** - A SQL query you can save, share, and schedule.
# MAGIC - **Dashboard** - A visual report of charts, tables, and insights from your data.
# MAGIC - **Genie Agent** - Ask questions about your data in natural language.
# MAGIC - **Job** - An automated workflow that runs notebooks, queries, or code on a schedule.
# MAGIC
# MAGIC The menu also has more advanced options such as **ETL Pipeline**, **Experiment**, **Model**, **App**, and (under **More**) **File**, **Git folder**, **SQL Warehouse**, and **Serving Endpoint**. **Cluster** (under **More**) is not available in Databricks Free Edition.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC
# MAGIC New notebooks and files are saved to your home folder (**Workspace > Users > your email**) by default. You can move them afterward.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## E. Navigate Workspace Assets and Objects
# MAGIC
# MAGIC 1. View the Workspace browser sidebar (Not the main navigation bar). 
# MAGIC
# MAGIC ![The workspace browser](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/workspace_sidebar.png)
# MAGIC
# MAGIC 2. This is the file tree you are looking at right now, where your notebooks, files, and folders live.
# MAGIC     - You can create, open, and organize your files right here, in whatever folder you are in.
# MAGIC
# MAGIC 3. Here you can also view:
# MAGIC     - **Notebook Table of Contents**
# MAGIC     - **Folders and Files**
# MAGIC     - **Catalogs and Schemas**
# MAGIC
# MAGIC
# MAGIC 4. In the workspace browser sidebar, select the **Folder** icon > click the kebab (**⋮**) icon.
# MAGIC
# MAGIC 5. Then choose **Create**. 
# MAGIC     - Notice you have a variety of options.
# MAGIC     - This will create the asset directly in this location.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Tip</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC
# MAGIC Creating from the main navigation sidebar's **+ New** menu saves to your home folder. 
# MAGIC
# MAGIC Creating from the workspace browser saves it right where you are.
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## F. Compute Overview
# MAGIC
# MAGIC Compute is what runs your code. Databricks offers a few types, each suited to different work.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### F1. Understanding compute and runtimes in Databricks
# MAGIC
# MAGIC Databricks offers various types of compute for different tasks:
# MAGIC
# MAGIC <br></br>
# MAGIC <div class="rc-wrap">
# MAGIC <style>
# MAGIC .rc-wrap { width: 100%; display: flex; flex-direction: column; align-items: center; gap: 18px; font-family: sans-serif; }
# MAGIC .rc-wrap * { box-sizing: border-box; }
# MAGIC .rc-hint { width: 100%; max-width: 1100px; text-align: center; font-size: 14pt; color: #5E7077; font-style: italic; }
# MAGIC .rc-hint strong { color: #FF5F46; font-style: normal; font-weight: 700; }
# MAGIC .rc-row { display: block; white-space: nowrap; font-size: 0; width: 100%; max-width: 1100px; }
# MAGIC .rc-box { display: inline-block; width: 23%; margin-right: 2%; min-height: 90px; background: #F9F7F4; border-top: 8px solid transparent; border-left: 2px solid transparent; border-right: 2px solid transparent; border-bottom: 2px solid transparent; border-radius: 8px; padding: 16px 14px; text-align: center; cursor: pointer; user-select: none; vertical-align: top; transition: transform 0.12s; box-shadow: 0 2px 8px rgba(27,49,57,0.06); white-space: normal; }
# MAGIC .rc-box:last-child { margin-right: 0; }
# MAGIC .rc-box:hover { transform: translateY(-2px); }
# MAGIC .rc-box.active { background: #fff; border-left-color: var(--pc); border-right-color: var(--pc); border-bottom-color: var(--pc); }
# MAGIC .rc-label { display: block; font-weight: 700; font-size: 14pt; letter-spacing: 2px; text-transform: uppercase; line-height: 1.2; pointer-events: none; }
# MAGIC .rc-title { display: block; font-size: 14pt; color: #0b2026; line-height: 1.3; margin-top: 6px; pointer-events: none; }
# MAGIC .rc-detail-wrap { overflow: hidden; max-height: 0; opacity: 0; transition: max-height 0.35s ease, opacity 0.28s ease, margin-top 0.28s ease; margin-top: 0; width: 100%; max-width: 1100px; }
# MAGIC .rc-detail-wrap.open { max-height: 700px; opacity: 1; margin-top: 12px; }
# MAGIC .rc-detail-card { background: #F9F7F4; border-radius: 10px; padding: 22px 26px; border-top: 7px solid #ccc; box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
# MAGIC .rc-detail-title { font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 12px; line-height: 1.3; }
# MAGIC .rc-detail-body { font-size: 14pt; color: #0b2026; line-height: 1.55; }
# MAGIC .rc-detail-body ul { margin: 0; padding-left: 22px; }
# MAGIC .rc-detail-body li { margin-bottom: 8px; }
# MAGIC .rc-detail-body li:last-child { margin-bottom: 0; }
# MAGIC </style>
# MAGIC
# MAGIC <div class="rc-hint">For more detail, <strong>click each card below</strong>.</div>
# MAGIC
# MAGIC <div class="rc-row">
# MAGIC   <span class="rc-box" data-id="0" onclick="rcSelect(0)" style="--pc:#4299E0; border-top-color:#4299E0;">
# MAGIC     <span class="rc-label" style="color:#4299E0;">Serverless</span>
# MAGIC     <span class="rc-title">Databricks manages it for you</span>
# MAGIC   </span><span class="rc-box" data-id="1" onclick="rcSelect(1)" style="--pc:#00A972; border-top-color:#00A972;">
# MAGIC     <span class="rc-label" style="color:#00A972;">All-Purpose</span>
# MAGIC     <span class="rc-title">Interactive clusters you configure</span>
# MAGIC   </span><span class="rc-box" data-id="2" onclick="rcSelect(2)" style="--pc:#FF5F46; border-top-color:#FF5F46;">
# MAGIC     <span class="rc-label" style="color:#FF5F46;">SQL Warehouse</span>
# MAGIC     <span class="rc-title">Compute for SQL and BI</span>
# MAGIC   </span><span class="rc-box" data-id="3" onclick="rcSelect(3)" style="--pc:#FFAB00; border-top-color:#FFAB00;">
# MAGIC     <span class="rc-label" style="color:#FFAB00;">Jobs Compute</span>
# MAGIC     <span class="rc-title">Runs scheduled jobs</span>
# MAGIC   </span>
# MAGIC </div>
# MAGIC
# MAGIC <div class="rc-detail-wrap" id="rc-detail-wrap">
# MAGIC   <div class="rc-detail-card" id="rc-detail-card"></div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #FFAB00; background: rgba(255,171,0,0.12); padding: 14px 18px; border-radius: 4px; margin: 16px auto; max-width: 1100px; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#0b2026; margin-bottom:6px; font-size:15pt;">NOTE - Compute Availability</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC     Databricks Free Edition includes only <strong>Serverless</strong> and <strong>SQL Warehouses</strong>. Also, depending on your organization, you may not have permission to create compute and can only use what's provided.<br><br>
# MAGIC     To create compute, select <strong>Compute</strong> in the main navigation bar.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="max-width: 1100px; margin: 8px auto 0; font-size: 14pt; color: #5E7077; font-family: sans-serif;">
# MAGIC   For more on compute, see the docs: <a href="https://docs.databricks.com/aws/en/compute/">AWS</a> | <a href="https://learn.microsoft.com/en-us/azure/databricks/compute/">Azure</a> | <a href="https://docs.databricks.com/gcp/en/compute/">GCP</a>.
# MAGIC </div>
# MAGIC
# MAGIC <script>
# MAGIC var REVEAL = [
# MAGIC   { title: "Serverless Compute (Recommended for Python & SQL Workloads)", color: "#4299E0", text: "<ul><li><strong>Runs:</strong> your notebooks, SQL, jobs, and pipelines, with no setup.</li><li><strong>Best for:</strong> everyday work using SQL or Python. Databricks manages the infrastructure, and this is what you use in this course.</li></ul>" },
# MAGIC   { title: "All-Purpose Compute", color: "#00A972", text: "<ul><li><strong>Runs:</strong> interactive notebooks in Python, SQL, Scala, or R on a cluster you size and configure.</li><li><strong>Best for:</strong> hands-on, exploratory work when you need a classic cluster.</li></ul>" },
# MAGIC   { title: "SQL Warehouses (Recommended for SQL Workloads)", color: "#FF5F46", text: "<ul><li><strong>Runs:</strong> SQL queries only.</li><li><strong>Best for:</strong> SQL analytics, BI, and dashboards.</li></ul>" },
# MAGIC   { title: "Jobs Compute", color: "#FFAB00", text: "<ul><li><strong>Runs:</strong> your code as part of an automated job.</li><li><strong>Best for:</strong> scheduled, production jobs at the lowest cost.</li></ul>" }
# MAGIC ];
# MAGIC var rcCurrent = null;
# MAGIC function rcSelect(id) {
# MAGIC   var wrap = document.getElementById('rc-detail-wrap');
# MAGIC   var card = document.getElementById('rc-detail-card');
# MAGIC   var d = REVEAL[id];
# MAGIC   document.querySelectorAll('.rc-box').forEach(function(b) {
# MAGIC     b.classList.toggle('active', parseInt(b.dataset.id) === id && rcCurrent !== id);
# MAGIC   });
# MAGIC   if (rcCurrent === id) { wrap.classList.remove('open'); rcCurrent = null; return; }
# MAGIC   rcCurrent = id;
# MAGIC   card.style.borderTopColor = d.color;
# MAGIC   card.innerHTML = '<div class="rc-detail-title" style="color:' + d.color + ';">' + d.title + '</div><div class="rc-detail-body">' + d.text + '</div>';
# MAGIC   wrap.classList.add('open');
# MAGIC }
# MAGIC </script>
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
