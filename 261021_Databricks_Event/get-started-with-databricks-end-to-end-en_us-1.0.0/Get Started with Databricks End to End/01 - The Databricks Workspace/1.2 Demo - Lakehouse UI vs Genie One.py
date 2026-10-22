# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Lakehouse UI vs Genie One
# MAGIC
# MAGIC Databricks has several experiences, but the two most people use for data and analytics are the full **Lakehouse workspace UI** you have been touring and **Genie One**, a simplified interface built for business users. This lesson explains the difference, who sees which one, and how to move between them.
# MAGIC
# MAGIC ## Learning objectives
# MAGIC
# MAGIC By the end of this lesson, you should be able to:
# MAGIC
# MAGIC - **Explain** what Genie One is and how it differs from the Lakehouse workspace UI.
# MAGIC - **Switch** between the Lakehouse workspace UI and Genie One using the app switcher.
# MAGIC - **Navigate** the Genie One home page, **open** shared assets, and **ask** a question in natural language.
# MAGIC - **Describe** how entitlements determine which interface a user sees.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## A. Lakehouse vs Genie One
# MAGIC
# MAGIC 1. Click the app switcher icon (![App Switcher](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/app-switcher.png)) to move between Databricks experiences.
# MAGIC   - The two we will focus on here are:
# MAGIC     - **Lakehouse (the workspace where we are)**
# MAGIC     - **Genie One**
# MAGIC
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC <div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap;">
# MAGIC
# MAGIC   <div style="flex: 1; min-width: 260px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); border-top: 8px solid #1B5162; padding: 18px 20px;">
# MAGIC     <div style="font-size: 18pt; font-weight: 700; color: #1B5162;">Lakehouse <span style="font-size: 11pt; font-weight: 700; letter-spacing: 1px; background: #1B5162; color: #fff; padding: 2px 10px; border-radius: 12px; vertical-align: middle; margin-left: 6px;">YOU ARE HERE</span></div>
# MAGIC     <div style="font-size: 14pt; color: #5A6F77; font-style: italic; margin: 4px 0 10px;">Analytics &amp; AI on large-scale data</div>
# MAGIC     <ul style="margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55;">
# MAGIC       <li style="margin-bottom: 8px;">The full platform and workspace for building: notebooks, pipelines, SQL, dashboards, and ML.</li>
# MAGIC       <li>Built for technical users.</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="flex: 1; min-width: 260px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); border-top: 8px solid #FF5F46; padding: 18px 20px;">
# MAGIC     <div style="font-size: 18pt; font-weight: 700; color: #FF5F46;">Genie One (Consumers)</div>
# MAGIC     <div style="font-size: 14pt; color: #5A6F77; font-style: italic; margin: 4px 0 10px;">Business insights from data and AI</div>
# MAGIC     <ul style="margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55;">
# MAGIC       <li style="margin-bottom: 8px;">A simplified, consumer-style view to find assets and ask questions in plain language.</li>
# MAGIC       <li>Built for business users.</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <div style="font-size: 14pt; color: #5E7077; font-style: italic; text-align: center; margin-top: 14px;">The switcher also includes Lakebase Postgres and Databricks Apps. Outside the scope of this course.</div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. What Is Genie One?
# MAGIC
# MAGIC Genie One is a simplified, business-user-friendly interface that provides a single, intuitive entry point to interact with data and AI in Databricks. 
# MAGIC
# MAGIC Unlike the full Lakehouse workspace UI, Genie One allows users to focus on what matters most: getting access to their data quickly and efficiently. 
# MAGIC
# MAGIC Genie One streamlines the Databricks experience with a chat interface that can access your data, and a search interface to help you find the assets that you need when you need them.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B1. Genie One Overview
# MAGIC <br></br>
# MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <!-- TITLE BAR -->
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 20px 28px; margin-bottom: 18px;">
# MAGIC   <div style="font-size: 22pt; font-weight: 700; margin-bottom: 6px;">What Genie One Brings Together</div>
# MAGIC   <div style="font-size: 15pt; font-weight: 400; line-height: 1.45; opacity: 0.95;">Genie One is the simplified home where business users work with data and AI, with no compute, queries, models, or notebooks to manage. It brings your assets into one place.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- GENIE ONE CONTAINER -->
# MAGIC <div style="position: relative; border: 3px solid #FF3621; border-radius: 18px; padding: 46px 24px 24px 24px; background: rgba(255,54,33,0.05);">
# MAGIC
# MAGIC   <!-- Container label -->
# MAGIC   <div style="position: absolute; top: -16px; left: 50%; transform: translateX(-50%); background: #FF3621; color: #ffffff; font-size: 13pt; font-weight: 700; letter-spacing: 2px; padding: 5px 22px; border-radius: 14px; white-space: nowrap;">GENIE ONE</div>
# MAGIC
# MAGIC   <!-- Row of 3 product cards -->
# MAGIC   <div style="display: block; white-space: nowrap; font-size: 0; width: 100%;">
# MAGIC
# MAGIC     <div style="display: inline-block; vertical-align: top; width: 32%; margin-right: 2%; white-space: normal; background: #F9F7F4; border-radius: 12px; border-top: 8px solid #FF3621; padding: 18px 18px 20px 18px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); box-sizing: border-box;">
# MAGIC       <div style="font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 4px;">AI/BI Dashboards</div>
# MAGIC       <div style="font-size: 13pt; color: #5E7077; line-height: 1.5;">Curated charts and KPIs to track and analyze the metrics that matter.</div>
# MAGIC     </div><div style="display: inline-block; vertical-align: top; width: 32%; margin-right: 2%; white-space: normal; background: #F9F7F4; border-radius: 12px; border-top: 8px solid #FF3621; padding: 18px 18px 20px 18px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); box-sizing: border-box;">
# MAGIC       <div style="font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 4px;">Genie Agents</div>
# MAGIC       <div style="font-size: 13pt; color: #5E7077; line-height: 1.5;">Ask questions about your data in plain natural language and get answers.</div>
# MAGIC     </div><div style="display: inline-block; vertical-align: top; width: 32%; white-space: normal; background: #F9F7F4; border-radius: 12px; border-top: 8px solid #FF3621; padding: 18px 18px 20px 18px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); box-sizing: border-box;">
# MAGIC       <div style="font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 4px;">Databricks Apps</div>
# MAGIC       <div style="font-size: 13pt; color: #5E7077; line-height: 1.5;">Interactive, purpose-built analytics and workflow applications.</div>
# MAGIC     </div>
# MAGIC
# MAGIC   </div>
# MAGIC
# MAGIC   <!-- Capability strip: what you can do in Genie One -->
# MAGIC   <div style="margin-top: 20px; padding-top: 16px; border-top: 1px dashed rgba(255,54,33,0.35);">
# MAGIC     <div style="font-size: 11pt; font-weight: 700; letter-spacing: 2px; color: #98102A; text-transform: uppercase; margin-bottom: 10px;">All in one place, you can</div>
# MAGIC     <div style="font-size: 0; width: 100%;">
# MAGIC       <span style="display: inline-block; background: #FFFFFF; border: 1.5px solid #FF3621; border-radius: 8px; padding: 10px 16px; margin: 0 10px 10px 0; font-size: 13pt; font-weight: 600; color: #0b2026;">Ask questions in natural language</span><span style="display: inline-block; background: #FFFFFF; border: 1.5px solid #FF3621; border-radius: 8px; padding: 10px 16px; margin: 0 10px 10px 0; font-size: 13pt; font-weight: 600; color: #0b2026;">Search assets by name</span><span style="display: inline-block; background: #FFFFFF; border: 1.5px solid #FF3621; border-radius: 8px; padding: 10px 16px; margin: 0 10px 10px 0; font-size: 13pt; font-weight: 600; color: #0b2026;">Schedule chat tasks</span><span style="display: inline-block; background: #FFFFFF; border: 1.5px solid #FF3621; border-radius: 8px; padding: 10px 16px; margin: 0 10px 10px 0; font-size: 13pt; font-weight: 600; color: #0b2026;">Draft &amp; share documents</span><span style="display: inline-block; background: #FFFFFF; border: 1.5px solid #FF3621; border-radius: 8px; padding: 10px 16px; margin: 0 10px 10px 0; font-size: 13pt; font-weight: 600; color: #0b2026;">Take action with agents &amp; apps</span><span style="display: inline-block; background: #FFFFFF; border: 1.5px solid #FF3621; border-radius: 8px; padding: 10px 16px; margin: 0 10px 10px 0; font-size: 13pt; font-weight: 600; color: #0b2026;">Work anywhere: mobile, Slack, Teams</span><span style="display: inline-block; background: #FFFFFF; border: 1.5px solid #FF3621; border-radius: 8px; padding: 10px 16px; margin: 0 10px 10px 0; font-size: 13pt; font-weight: 600; color: #0b2026;">Trust every answer, governed by Unity Catalog</span>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- CLOSING CALL-OUT: positioning + consumer view -->
# MAGIC <div style="background: linear-gradient(135deg, #1B5162 0%, #0b2026 100%); color: #ffffff; border-radius: 10px; padding: 22px 28px; margin-top: 18px; text-align: center;">
# MAGIC   <div style="font-size: 18pt; font-weight: 800; line-height: 1.25; margin-bottom: 6px;">AI that works for you, grounded in your data</div>
# MAGIC   <div style="font-size: 14.5pt; font-weight: 400; line-height: 1.45; color: #E5EEF1;">Ask questions, take action, and drive real outcomes with AI that knows your business.</div>
# MAGIC   <div style="font-size: 12.5pt; color: #B7CDD5; margin-top: 12px;">The simplified <b style="color:#FF5F46;">Consumer view</b> of Databricks &mdash; built for business users, available for a single workspace or across your whole account.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC ### What Genie One Brings Together
# MAGIC
# MAGIC - Genie One is the simplified Databricks UI for business users. It is a single entry point for working with data and AI, without having to navigate technical concepts like compute, queries, models, or notebooks.
# MAGIC - The visual is a containment metaphor on purpose. The big outer box is Genie One, and everything a consumer needs lives inside it. The message is "one home for all of this," not "a tool that links to other tools."
# MAGIC
# MAGIC ### The three assets inside
# MAGIC
# MAGIC - **AI/BI Dashboards** — curated charts and KPIs. Business users view and interact with them to track key performance indicators and analyze metrics.
# MAGIC - **Genie Agents** — ask questions about your data in natural language and get answers back, no SQL required.
# MAGIC - **Databricks Apps** — interactive, purpose-built analytics and workflow applications, including custom apps your teams build.
# MAGIC
# MAGIC ### All in one place, you can
# MAGIC
# MAGIC - **Ask questions in natural language** — a unified, full-screen chat that spans your dashboards and agents, with follow-ups and root-cause analysis, no SQL required.
# MAGIC - **Search assets by name** to jump straight to what you need, and favorite or browse them by domain and business context.
# MAGIC - **Schedule chat tasks** so recurring questions run on their own and post results back as a thread, with email notifications when they run.
# MAGIC - **Draft and share documents** straight from a chat conversation, edit them in a canvas pane, share by link, and track version history.
# MAGIC - **Take action with agents and apps** — move from insight to action with Genie Agents and Databricks Apps, no code required.
# MAGIC - **Work anywhere** — chat and view dashboards from the iOS and Android app, or natively in Slack and Microsoft Teams with @mentions.
# MAGIC - **Trust every answer** — responses respect Unity Catalog row- and column-level security and source permissions, and you can verify the data behind an answer with citations.
# MAGIC
# MAGIC ### A couple of deeper capabilities
# MAGIC
# MAGIC - **Connect 50+ external tools** — pull in context from sources like Google Drive, SharePoint, GitHub, Glean, and Atlassian.
# MAGIC - **Citations** — click the citation icons in a response to verify the knowledge sources and underlying data.
# MAGIC
# MAGIC ### Who it is for
# MAGIC
# MAGIC - Designed for business users, who need at minimum Consumer access.
# MAGIC - Works at the workspace level for a single workspace, or at the account level for a unified view across all workspaces in your Databricks account.
# MAGIC - When you open an asset it launches in the familiar experience for that object type, and whether it opens read-only or with an Edit draft button depends on your privileges, covered next.
# MAGIC
# MAGIC </details>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### B2. Opening and Interacting with Assets in Genie One
# MAGIC
# MAGIC 1. Click the app switcher icon (![App Switcher](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/app-switcher.png)).
# MAGIC
# MAGIC 2. Right click on **Genie One** and select **Open Link in New Tab**.
# MAGIC
# MAGIC 3. The Genie One home page is the central hub for business users. It is organized into several key areas:
# MAGIC
# MAGIC     - **Search bar** allows you to do two things:
# MAGIC         1. **Search** to quickly locate assets
# MAGIC         2. **Ask** ask questions about your data
# MAGIC
# MAGIC     - **Quick links** (in the left panel), a hub for assets such as dashboards, Genie Agents, and apps.
# MAGIC
# MAGIC     **The Genie One interface is an AI-powered chat over your whole data estate that queries all the data you have access to and finds answers to your questions.**
# MAGIC
# MAGIC 4. For example, select **Dashboards**.
# MAGIC     - Depending on your workspace, you might see dashboards if available.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Opening an asset in Genie One</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC
# MAGIC When you click an asset in Genie One, it opens in the familiar experience for that object type (for example, a dashboard opens in the dashboard viewer).
# MAGIC
# MAGIC An asset opens in different ways depending on whether you have edit privileges on it:
# MAGIC
# MAGIC - If you have **viewing rights only**, the asset opens within Genie One.
# MAGIC - If you have **authoring privileges**, you will see an **Edit draft** button to open the asset in the full Lakehouse workspace UI for editing.
# MAGIC
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B3. Ask Genie One a Question
# MAGIC
# MAGIC **Chat** in Genie One is a unified, full-screen, natural-language interface where business users can ask questions about their data. 
# MAGIC
# MAGIC In this step, you will ask Genie One a question about the **samples.nyctaxi.trips** sample data and watch it find the answer for you.
# MAGIC
# MAGIC 1. Select **+ New Chat**.
# MAGIC
# MAGIC 2. Ask **Genie One** the question below. Click **Copy**, then paste it into the chat and send it.
# MAGIC     - Every Databricks workspace comes with a set of ready-to-use sample tables in the **samples** catalog, so you can try Chat right away, no setup or SQL required.
# MAGIC
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='✓ Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">What is the average taxi fare by hour of the day?</pre>
# MAGIC </div>
# MAGIC
# MAGIC 3. While it runs, watch how Genie One works. It finds the right table, picks the columns it needs, and writes and runs the query for you.
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">The data does not store an "average fare by hour" anywhere. Genie One reads the raw trip records, groups them by the hour of pickup, and calculates the average for you, all from a plain-language question.</div>
# MAGIC </div>
# MAGIC
# MAGIC 4. View the results. Genie One returns the answer along with a chart, an explanation of how it got there, and the sources it used. 
# MAGIC
# MAGIC 5. From here, you can ask a follow-up question to dig deeper.
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## C. Genie One Permissions and Entitlements
# MAGIC
# MAGIC <br></br>
# MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <!-- TITLE BAR -->
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 20px 28px; margin-bottom: 18px;">
# MAGIC   <div style="font-size: 22pt; font-weight: 700; margin-bottom: 6px;">How You Get Into Genie One</div>
# MAGIC   <div style="font-size: 15pt; font-weight: 400; line-height: 1.45; opacity: 0.95;">What a user can see and do in a workspace is controlled by their <b>entitlements</b>. To use Genie One, you need just one.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- HERO: CONSUMER ACCESS -->
# MAGIC <div style="background: #F9F7F4; border-radius: 14px; border-top: 10px solid #FF3621; box-shadow: 0 4px 16px rgba(27,49,57,0.10); padding: 24px 28px; margin-bottom: 18px;">
# MAGIC
# MAGIC   <div style="font-size: 12pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #98102A; margin-bottom: 6px;">Your key to Genie One</div>
# MAGIC   <div style="font-size: 26pt; font-weight: 800; color: #FF3621; line-height: 1.1;">Consumer access</div>
# MAGIC   <div style="font-size: 15pt; color: #5E7077; line-height: 1.5; margin-top: 8px;">The one entitlement a business user needs. With it, you log in and land right on the <b>Genie One</b> home page. It is for <b>using</b> data, not building it, and every interaction is governed by <b>Unity Catalog</b>, so you only ever see what you are allowed to.</div>
# MAGIC
# MAGIC   <div style="font-size: 12pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #1B5162; margin: 20px 0 12px 0; padding-top: 16px; border-top: 1px solid #EEEDE9;">What it lets you do</div>
# MAGIC   <div style="font-size: 0;">
# MAGIC     <div style="display: inline-block; width: 50%; vertical-align: top; box-sizing: border-box; padding-right: 12px; margin-bottom: 12px; font-size: 15pt; color: #0b2026;"><span style="color:#00A972; font-weight:700;">&#10003;</span>&nbsp; View and interact with <b>dashboards</b></div><div style="display: inline-block; width: 50%; vertical-align: top; box-sizing: border-box; padding-right: 12px; margin-bottom: 12px; font-size: 15pt; color: #0b2026;"><span style="color:#00A972; font-weight:700;">&#10003;</span>&nbsp; Chat with <b>Genie Agents</b></div><div style="display: inline-block; width: 50%; vertical-align: top; box-sizing: border-box; padding-right: 12px; font-size: 15pt; color: #0b2026;"><span style="color:#00A972; font-weight:700;">&#10003;</span>&nbsp; Open and use <b>Databricks Apps</b></div><div style="display: inline-block; width: 50%; vertical-align: top; box-sizing: border-box; padding-right: 12px; font-size: 15pt; color: #0b2026;"><span style="color:#00A972; font-weight:700;">&#10003;</span>&nbsp; See only data <b>shared with you</b></div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- SECONDARY: the other two, muted gray accent -->
# MAGIC <div style="font-size: 13pt; color: #5E7077; margin-bottom: 10px;">Two other entitlements exist for people who <b>build</b> data and AI. You do not need these for Genie One.</div>
# MAGIC <div style="font-size: 0; margin-bottom: 18px;">
# MAGIC   <div style="display: inline-block; width: 49%; margin-right: 2%; vertical-align: top; box-sizing: border-box; background: #F9F7F4; border-radius: 10px; border-top: 8px solid #C2C2C2; box-shadow: 0 2px 8px rgba(27,49,57,0.05); padding: 16px 18px;">
# MAGIC     <div style="font-size: 15pt; font-weight: 700; color: #5A6F77;">Workspace access</div>
# MAGIC     <div style="font-size: 13pt; color: #618794; line-height: 1.5; margin-top: 4px;">Notebooks, jobs, models, and pipelines.</div>
# MAGIC   </div><div style="display: inline-block; width: 49%; vertical-align: top; box-sizing: border-box; background: #F9F7F4; border-radius: 10px; border-top: 8px solid #C2C2C2; box-shadow: 0 2px 8px rgba(27,49,57,0.05); padding: 16px 18px;">
# MAGIC     <div style="font-size: 15pt; font-weight: 700; color: #5A6F77;">Databricks SQL access</div>
# MAGIC     <div style="font-size: 13pt; color: #618794; line-height: 1.5; margin-top: 4px;">SQL dashboards, queries, and SQL warehouses.</div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- KEEP IT SIMPLE -->
# MAGIC <div style="border-left: 4px solid #FFAB00; background: rgba(255,171,0,0.12); padding: 14px 18px; border-radius: 4px; margin: 0 0 12px 0;">
# MAGIC   <strong style="display:block; color:#B37A00; margin-bottom:6px; font-size:15pt;">Keep it simple</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">For the simplified Genie One experience, <b>Consumer access should be a user's only entitlement</b>. Adding another one moves them into the full Databricks workspace UI instead.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- HOW YOU GET IT -->
# MAGIC <div style="font-size: 13pt; color: #5E7077; font-style: italic; text-align: center;">A workspace admin turns on Consumer access under <b>Settings &rarr; Identity and access &rarr; Users</b>.</div>
# MAGIC
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
