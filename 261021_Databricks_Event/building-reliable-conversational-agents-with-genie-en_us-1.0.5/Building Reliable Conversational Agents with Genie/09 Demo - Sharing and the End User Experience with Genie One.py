# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Sharing and the End User Experience with Genie
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC You have built and curated a Genie Agent through descriptions, SQL logic, instructions, and benchmarks. Before end users can interact with your Genie, you need to understand **permissions**, **share** the space, and see what the experience looks like from the **end-user perspective**.
# MAGIC
# MAGIC In this demo, you will first review permissions and share your Genie Agent. Then you will switch to the **end-user role** by opening **Genie** (formerly Databricks One), asking natural language questions, and rating responses to simulate real-world feedback. Finally, you will see how **Unity Catalog governance** automatically protects data even when accessed through your Genie Agent.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this demo, you will be able to:
# MAGIC
# MAGIC 1. **Understand the required permissions** to create or edit a Genie Agent (entitlements, compute, data, ACLs).
# MAGIC 2. **Describe the four Genie ACL levels** (CAN VIEW, CAN RUN, CAN EDIT, CAN MANAGE) and their capabilities.
# MAGIC 3. **Share a Genie Agent** with users or groups and select the appropriate permission level.
# MAGIC 4. **Access a Genie Agent through Genie** as an end user would.
# MAGIC 5. **Ask natural language questions** and rate responses using thumbs up, thumbs down, and request review.
# MAGIC 6. **Observe that Genie respects Unity Catalog governance**, including ABAC column masks, without any Genie-specific configuration.
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #f44336;
# MAGIC   background: #ffebee;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Prerequisites</strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Complete **all previous demonstrations** before proceeding. This demo builds on the Genie Agent you have curated with metadata, SQL logic, instructions, and benchmarks.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - SELECT A COMPUTE ENVIRONMENT
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #f44336;
# MAGIC   background: #ffebee;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Select a Serverless SQL Warehouse</strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Before starting this notebook, select the required compute environment listed below.
# MAGIC
# MAGIC - **Serverless SQL Warehouse (2X-Small is sufficient)**
# MAGIC   - Select **Compute** > **More** > **SQL Warehouse** > Select a SQL Warehouse you have access to.
# MAGIC
# MAGIC **NOTE:** This notebook was **developed and tested using Serverless SQL Warehouse**. Other compute options may work but are not guaranteed to behave the same or support all features demonstrated.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Classroom Setup
# MAGIC
# MAGIC 1. Run the cell below to set your default catalog and schema.
# MAGIC     - This assumes you have already run the setup from a prior demo and your tables exist in **labuser_YOUR_USER_NAME.genie_course_bakehouse**.

# COMMAND ----------

# MAGIC %run ./Includes/Classroom-Setup-consuming-monitoring

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## B. Genie Agent Authoring Checklist
# MAGIC
# MAGIC We are now on step **6** of the authoring checklist: testing with real user interactions and iterating based on feedback.
# MAGIC
# MAGIC <br></br>
# MAGIC <!--
# MAGIC   Focus variant of the Genie Agent Authoring Checklist.
# MAGIC   Each step card shows its full-color inline styles AND a commented "ACTIVE" version for the dimmed cards.
# MAGIC   To bring a dimmed step back to color: swap the dimmed <div> opening with the line marked "ACTIVE", and restore the inner number/title colors.
# MAGIC -->
# MAGIC
# MAGIC <div style="max-width: 1280px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <!-- 6-STEP FLOW -->
# MAGIC <div style="display: grid; grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr; gap: 0; align-items: stretch;">
# MAGIC
# MAGIC   <!-- STEP 1 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #2574B5; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">1</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Start with purpose<br>and questions</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 2 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #02A36F; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">2</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Select a minimal<br>data slice</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 3 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #F8A805; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">3</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Add metadata<br>and synonyms</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 4 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #FF5F46; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">4</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Encode business<br>logic in SQL</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 5 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #98182A; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">5</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Add light global<br>text instructions</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #C2C2C2; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC
# MAGIC   <!-- STEP 6 (active) -->
# MAGIC   <div style="background: #F9F7F4; border: 3px solid #1C3037; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #1C3037; line-height: 1; margin-bottom: 8px;">6</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Test, benchmark,<br>and iterate with users</div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Genie Permissions Overview

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C1. Required Permissions to Create or Edit a Genie Agent
# MAGIC
# MAGIC In this course you created your own Genie and had the required permissions to do so in this Workspace.
# MAGIC
# MAGIC **To create or edit a Genie in your own Workspace**, you must have the following permissions and entitlements:
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div class="four-pane">
# MAGIC
# MAGIC <style>
# MAGIC
# MAGIC .req-row {
# MAGIC     display: flex;
# MAGIC     justify-content: center;
# MAGIC     gap: 16px;
# MAGIC     flex-wrap: nowrap;
# MAGIC     max-width: 1100px;
# MAGIC     margin: 0 auto;
# MAGIC }
# MAGIC
# MAGIC .req-box {
# MAGIC     flex: 1 1 0;
# MAGIC     min-height: 165px;
# MAGIC     background: #F9F7F4;
# MAGIC     border-radius: 8px;
# MAGIC     box-shadow: 0 2px 8px rgba(27,49,57,0.06);
# MAGIC     padding: 14px 12px;
# MAGIC     text-align: center;
# MAGIC     position: relative;
# MAGIC     box-sizing: border-box;
# MAGIC }
# MAGIC
# MAGIC .req-box::before {
# MAGIC     content: "";
# MAGIC     position: absolute;
# MAGIC     top: 0;
# MAGIC     left: 0;
# MAGIC     width: 100%;
# MAGIC     height: 8px;
# MAGIC     border-radius: 8px 8px 0 0;
# MAGIC }
# MAGIC
# MAGIC .entitlement::before { background: #2574B5; }
# MAGIC .compute::before { background: #02A36F; }
# MAGIC .data::before { background: #F8A805; }
# MAGIC .acl::before { background: #98182A; }
# MAGIC
# MAGIC .req-title {
# MAGIC     font-size: 17pt;
# MAGIC     font-weight: 700;
# MAGIC     color: #0b2026;
# MAGIC     line-height: 1.3;
# MAGIC     margin-top: 8px;
# MAGIC     margin-bottom: 10px;
# MAGIC }
# MAGIC
# MAGIC .req-text {
# MAGIC     font-size: 15pt;
# MAGIC     color: #333;
# MAGIC     line-height: 1.45;
# MAGIC }
# MAGIC
# MAGIC .req-note {
# MAGIC     margin-top: 10px;
# MAGIC     font-size: 14pt;
# MAGIC     color: #5E7077;
# MAGIC     line-height: 1.35;
# MAGIC }
# MAGIC
# MAGIC </style>
# MAGIC
# MAGIC <div class="req-row">
# MAGIC
# MAGIC <div class="req-box entitlement">
# MAGIC   <div class="req-title">Databricks SQL Entitlement</div>
# MAGIC   <div class="req-text">
# MAGIC     Must have the <strong>Databricks SQL</strong> workspace entitlement.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div class="req-box compute">
# MAGIC   <div class="req-title">SQL Warehouse Access</div>
# MAGIC   <div class="req-text">
# MAGIC     Must have <strong>CAN USE</strong> on at least one <strong>pro</strong> or <strong>serverless SQL warehouse</strong>.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div class="req-box data">
# MAGIC   <div class="req-title">Data Access</div>
# MAGIC   <div class="req-text">
# MAGIC     Must have <strong>SELECT</strong> privileges on the data used in the space.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div class="req-box acl">
# MAGIC   <div class="req-title">Genie Agent ACLs</div>
# MAGIC   <div class="req-text">
# MAGIC     Must have at least <strong>CAN EDIT</strong> on the Genie Agent.
# MAGIC   </div>
# MAGIC   <div class="req-note">
# MAGIC     Space creators automatically get <strong>CAN MANAGE</strong> on spaces they create.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C2. Genie Agents Access Control Lists (ACLs) Overview
# MAGIC
# MAGIC After you create a Genie Agent, you need to share it with users so they can access and interact with it.
# MAGIC
# MAGIC Databricks groups Genie ACLs into four permission levels
# MAGIC
# MAGIC #### Select each card and view the details
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <style>
# MAGIC .perm-row { display: block; white-space: nowrap; font-size: 0; width: 100%; box-sizing: border-box; }
# MAGIC .perm-box {
# MAGIC   display: inline-block;
# MAGIC   width: 23.5%;
# MAGIC   margin-right: 2%;
# MAGIC   min-height: 100px;
# MAGIC   background: #F9F7F4;
# MAGIC   border-top: 8px solid transparent;
# MAGIC   border-left: 2px solid transparent;
# MAGIC   border-right: 2px solid transparent;
# MAGIC   border-bottom: 2px solid transparent;
# MAGIC   border-radius: 8px;
# MAGIC   padding: 14px 10px;
# MAGIC   text-align: center;
# MAGIC   box-sizing: border-box;
# MAGIC   cursor: pointer;
# MAGIC   user-select: none;
# MAGIC   vertical-align: top;
# MAGIC   transition: transform 0.12s;
# MAGIC }
# MAGIC .perm-box:last-child { margin-right: 0; }
# MAGIC .perm-box:hover { transform: translateY(-2px); }
# MAGIC .perm-box.active {
# MAGIC   background: #fff;
# MAGIC   border-left-color: var(--pc);
# MAGIC   border-right-color: var(--pc);
# MAGIC   border-bottom-color: var(--pc);
# MAGIC }
# MAGIC .perm-title {
# MAGIC   display: block;
# MAGIC   font-size: 14pt;
# MAGIC   font-weight: 700;
# MAGIC   color: #0b2026;
# MAGIC   line-height: 1.3;
# MAGIC   white-space: normal;
# MAGIC   pointer-events: none;
# MAGIC }
# MAGIC .detail-wrap {
# MAGIC   overflow: hidden;
# MAGIC   max-height: 0;
# MAGIC   opacity: 0;
# MAGIC   transition: max-height 0.35s ease, opacity 0.28s ease, margin-top 0.28s ease;
# MAGIC   margin-top: 0;
# MAGIC }
# MAGIC .detail-wrap.open {
# MAGIC   max-height: 700px;
# MAGIC   opacity: 1;
# MAGIC   margin-top: 12px;
# MAGIC }
# MAGIC .detail-card {
# MAGIC   background: #F9F7F4;
# MAGIC   border-radius: 10px;
# MAGIC   padding: 20px;
# MAGIC   box-sizing: border-box;
# MAGIC   border-top: 7px solid #ccc;
# MAGIC }
# MAGIC .can-block {
# MAGIC   border-left: 4px solid;
# MAGIC   border-radius: 0 6px 6px 0;
# MAGIC   padding: 10px 12px;
# MAGIC   margin-bottom: 12px;
# MAGIC }
# MAGIC </style>
# MAGIC
# MAGIC <div style="background: #F8F9FC; border: 3px solid #1B5162; border-radius: 10px; padding: 24px; box-sizing: border-box;">
# MAGIC
# MAGIC   <div class="perm-row">
# MAGIC     <span class="perm-box active" data-id="0" onclick="selectPerm(0)" style="--pc:#5E7077; border-top-color:#5E7077;">
# MAGIC       <span class="perm-title">NO PERMISSIONS</span>
# MAGIC     </span><span class="perm-box" data-id="1" onclick="selectPerm(1)" style="--pc:#2574B5; border-top-color:#2574B5;">
# MAGIC       <span class="perm-title">CAN VIEW / CAN RUN</span>
# MAGIC     </span><span class="perm-box" data-id="2" onclick="selectPerm(2)" style="--pc:#F8A805; border-top-color:#F8A805;">
# MAGIC       <span class="perm-title">CAN EDIT</span>
# MAGIC     </span><span class="perm-box" data-id="3" onclick="selectPerm(3)" style="--pc:#00A972; border-top-color:#00A972;">
# MAGIC       <span class="perm-title">CAN MANAGE</span>
# MAGIC     </span>
# MAGIC   </div>
# MAGIC
# MAGIC   <div class="detail-wrap" id="detail-wrap">
# MAGIC     <div class="detail-card" id="detail-card"></div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <script>
# MAGIC var PERMS = [
# MAGIC   {
# MAGIC     title: "NO PERMISSIONS",
# MAGIC     color: "#5E7077",
# MAGIC     roleBg: "#F1F3F4",
# MAGIC     can: ["No access to the Genie Agent", "Cannot open or use the space"],
# MAGIC     cannot: [],
# MAGIC     role: "User not yet shared on the space, anyone outside the intended audience"
# MAGIC   },
# MAGIC   {
# MAGIC     title: "CAN VIEW / CAN RUN",
# MAGIC     color: "#2574B5",
# MAGIC     roleBg: "#EEF4FB",
# MAGIC     can: ["See the space in the Genie list", "Ask Genie questions", "Provide response feedback"],
# MAGIC     cannot: ["Edit instructions or sample questions", "Add or remove included tables", "Monitor the space", "Modify permissions or delete the space"],
# MAGIC     role: "Business user, analyst, stakeholder"
# MAGIC   },
# MAGIC   {
# MAGIC     title: "CAN EDIT",
# MAGIC     color: "#F8A805",
# MAGIC     roleBg: "#FFF4DB",
# MAGIC     can: ["Everything CAN VIEW / CAN RUN can do", "Add or edit Genie instructions", "Add or edit sample questions", "Add or remove included tables"],
# MAGIC     cannot: ["Monitor the space", "Modify permissions", "Delete the space", "View other users' conversations"],
# MAGIC     role: "Space builder, subject matter expert, analytics developer"
# MAGIC   },
# MAGIC   {
# MAGIC     title: "CAN MANAGE",
# MAGIC     color: "#00A972",
# MAGIC     roleBg: "rgba(0,169,114,0.10)",
# MAGIC     can: ["Everything CAN EDIT can do", "Monitor the space", "Modify permissions", "Delete the space", "View other users' conversations"],
# MAGIC     cannot: [],
# MAGIC     role: "Space curator or owner, data or analytics team lead"
# MAGIC   }
# MAGIC ];
# MAGIC
# MAGIC var current = null;
# MAGIC
# MAGIC function selectPerm(id) {
# MAGIC   var wrap = document.getElementById('detail-wrap');
# MAGIC   var card = document.getElementById('detail-card');
# MAGIC   var p = PERMS[id];
# MAGIC
# MAGIC   document.querySelectorAll('.perm-box').forEach(function(b) {
# MAGIC     b.classList.toggle('active', parseInt(b.dataset.id) === id && current !== id);
# MAGIC   });
# MAGIC
# MAGIC   if (current === id) {
# MAGIC     wrap.classList.remove('open');
# MAGIC     current = null;
# MAGIC     return;
# MAGIC   }
# MAGIC
# MAGIC   current = id;
# MAGIC
# MAGIC   var canHtml = p.can.map(function(c) { return '<li style="margin-bottom:4px;">' + c + '</li>'; }).join('');
# MAGIC
# MAGIC   var cannotHtml = '';
# MAGIC   if (p.cannot.length > 0) {
# MAGIC     cannotHtml = '<div class="can-block" style="background:rgba(254,55,34,0.08);border-color:#FE3722;">'
# MAGIC       + '<div style="font-weight:700;font-size:15pt;margin-bottom:4px;">What they cannot do</div>'
# MAGIC       + '<ul style="font-size:15pt;margin:0;padding-left:16px;">'
# MAGIC       + p.cannot.map(function(c) { return '<li style="margin-bottom:4px;">' + c + '</li>'; }).join('')
# MAGIC       + '</ul></div>';
# MAGIC   }
# MAGIC
# MAGIC   card.style.borderTopColor = p.color;
# MAGIC   card.innerHTML =
# MAGIC     '<div style="font-size:20pt;font-weight:700;margin-bottom:12px;color:#0b2026;">' + p.title + '</div>'
# MAGIC     + '<div class="can-block" style="background:rgba(0,0,0,0.03);border-color:' + p.color + ';">'
# MAGIC     + '<div style="font-weight:700;font-size:15pt;margin-bottom:4px;">What they can do</div>'
# MAGIC     + '<ul style="font-size:15pt;margin:0;padding-left:16px;">' + canHtml + '</ul>'
# MAGIC     + '</div>'
# MAGIC     + cannotHtml
# MAGIC     + '<div class="can-block" style="background:' + p.roleBg + ';border-color:' + p.color + ';margin-bottom:0;">'
# MAGIC     + '<div style="font-weight:700;font-size:15pt;margin-bottom:4px;">Typical role</div>'
# MAGIC     + '<div style="font-size:15pt;color:#555;">' + p.role + '</div>'
# MAGIC     + '</div>';
# MAGIC
# MAGIC   wrap.classList.add('open');
# MAGIC }
# MAGIC </script>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Genie ACLs
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC *For more information view the Genie Agent ACLs documentation:
# MAGIC [AWS](https://docs.databricks.com/aws/en/security/auth/access-control/#genie-agent-acls) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/security/auth/access-control/#genie-agent) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/security/auth/access-control/#genie-agent-acls)*
# MAGIC
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### C3. Sharing Your Genie Agent
# MAGIC
# MAGIC Before end users can access your Genie, you need to share it with them.
# MAGIC
# MAGIC 1. In your Genie Agent, select **Share** (top-right corner).
# MAGIC
# MAGIC 2. Here you can add a user or group and select the appropriate permission level (No need to add any users).
# MAGIC
# MAGIC 3. Close the pop up.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="font-size: 22pt; font-weight: 700; color: #0b2026; margin-bottom: 6px;">Curator vs. Consumer</div>
# MAGIC <div style="width: 400px; height: 4px; background: #1B5162; margin-bottom: 24px; border-radius: 2px;"></div>
# MAGIC
# MAGIC <div style="display: flex; gap: 24px;">
# MAGIC
# MAGIC <!-- Curator Card -->
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 24px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #1B5162; border-radius: 8px 8px 0 0;"></div>
# MAGIC
# MAGIC   <!-- Image placeholder -->
# MAGIC   <img src="https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/icons/curator.png" style="width: 20%; display: block; margin: 8px 0 18px 0;">
# MAGIC
# MAGIC   <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 16px;">Curator (You)</div>
# MAGIC
# MAGIC   <ul style="font-size: 14pt; line-height: 1.6; padding-left: 20px; margin: 0;">
# MAGIC     <li style="margin-bottom: 12px;"><strong>Access</strong> — Workspace, full configuration</li>
# MAGIC     <li style="margin-bottom: 12px;"><strong>Sees</strong> — Knowledge Store, Benchmarks, Monitoring</li>
# MAGIC     <li style="margin-bottom: 12px;"><strong>Goal</strong> — Improve accuracy and coverage</li>
# MAGIC     <li><strong>Feedback</strong> — Reviews SQL, adjusts instructions</li>
# MAGIC   </ul>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Consumer Card -->
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 24px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #00A972; border-radius: 8px 8px 0 0;"></div>
# MAGIC
# MAGIC   <!-- Image placeholder -->
# MAGIC   <img src="https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/icons/people-blue.png" style="width: 20%; display: block; margin: 8px 0 18px 0;">
# MAGIC
# MAGIC   <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 16px;">Consumer (Business User)</div>
# MAGIC
# MAGIC   <ul style="font-size: 14pt; line-height: 1.6; padding-left: 20px; margin: 0;">
# MAGIC     <li style="margin-bottom: 12px;"><strong>Access</strong> — Genie, ask questions only</li>
# MAGIC     <li style="margin-bottom: 12px;"><strong>Sees</strong> — Chat interface with results</li>
# MAGIC     <li style="margin-bottom: 12px;"><strong>Goal</strong> — Get answers to business questions</li>
# MAGIC     <li><strong>Feedback</strong> — Rates responses, thumbs up/down, request review</li>
# MAGIC   </ul>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Training Note
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC For this training, you already have **CAN MANAGE** access on your space.
# MAGIC
# MAGIC In production, most of your business users would have **CAN VIEW/CAN RUN**.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## D. The End User Experience with Genie
# MAGIC
# MAGIC Now that you understand permissions and sharing, let's see what the experience looks like from the **end-user perspective**.
# MAGIC
# MAGIC **Your business users will typically not interact with their Genie Agent through the full Lakehouse UI.**
# MAGIC
# MAGIC They will access it through **Genie One**, a simplified experience designed for data consumers who need answers, not configuration.
# MAGIC
# MAGIC - What is Genie One?
# MAGIC     [AWS](https://docs.databricks.com/aws/en/genie-ui/genie) |
# MAGIC     [Azure](https://learn.microsoft.com/en-us/azure/databricks/genie-one/) |
# MAGIC     [GCP](https://docs.databricks.com/gcp/en/genie-ui/genie)
# MAGIC
# MAGIC - Chat in Genie One (*Public Preview at the time of this course release*):
# MAGIC     [AWS](https://docs.databricks.com/aws/en/genie-ui/genie-chat) |
# MAGIC     [Azure](https://learn.microsoft.com/en-us/azure/databricks/genie-ui/genie-chat) |
# MAGIC     [GCP](https://docs.databricks.com/gcp/en/genie-ui/genie-chat)
# MAGIC
# MAGIC - Consumer access provides a streamlined, read-only experience for business users to discover and consume dashboards, Genie Agents, and Databricks Apps shared with them using Genie One.  
# MAGIC     [AWS](https://docs.databricks.com/aws/en/ai-bi/consumers/) |
# MAGIC     [Azure](https://learn.microsoft.com/en-us/azure/databricks/ai-bi/consumers/) |
# MAGIC     [GCP](https://docs.databricks.com/gcp/en/ai-bi/consumers/)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### D1. Genie One Overview (formerly Databricks One)
# MAGIC
# MAGIC <br></br>
# MAGIC <div style="max-width: 1120px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <!-- TITLE BAR -->
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 16px 24px; margin-bottom: 18px;">
# MAGIC   <div style="font-size: 21pt; font-weight: 700; margin-bottom: 6px;">How Business Users Get Answers in Genie One</div>
# MAGIC   <div style="font-size: 14pt; font-weight: 400; line-height: 1.45; opacity: 0.95;">Genie One is the consumer home. A business user can <b>open a shared asset directly</b>, or <b>ask a question in Chat</b>, which routes to the right source. Either way, answers stay permission-gated and grounded in governed <b>Unity Catalog</b> data.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- BUSINESS USERS -->
# MAGIC <div style="text-align: center;">
# MAGIC   <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#618794" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin:0 8px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#618794" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin:0 8px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#618794" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin:0 8px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
# MAGIC   <div style="font-size: 14pt; font-weight: 700; margin-top: 6px;">Business users</div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="text-align: center; margin: 8px 0;"><div style="font-size: 12pt; color: #618794; font-style: italic;">sign in to Genie One</div><div style="font-size: 30pt; color: #618794; line-height: 1;">&darr;</div></div>
# MAGIC
# MAGIC <!-- GENIE ONE HOME (container) -->
# MAGIC <div style="background: #F8F9FC; border: 2.5px solid #1B5162; border-radius: 16px; padding: 18px 20px;">
# MAGIC   <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
# MAGIC     <svg style="height:62px;width:auto;display:inline-block;vertical-align:middle;flex-shrink:0;" viewBox="0 0 803 200" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M81.7909 159.789C75.0244 159.789 69.5392 166.599 69.5392 175H126.368C126.368 166.599 120.883 159.789 114.116 159.789H81.7909Z" fill="#FF5F46"/> <path d="M179.614 80.7871C167.525 100.208 149.376 126.933 141.272 133.79C133.167 140.647 121.149 153.009 93.2907 153.009C73.7741 153.009 56.9864 140.474 49.5352 122.498C49.5353 122.519 49.5356 122.54 49.5358 122.561C48.4799 119.938 45.9132 118.085 42.9121 118.085C38.969 118.085 35.7721 121.282 35.7721 125.225C35.7722 126.15 35.9484 126.997 36.2689 127.752C37.984 131.793 42.5469 131.965 42.5469 144.569C42.5469 143.103 42.5469 146.404 42.5469 144.569C30.6947 144.569 21.0865 134.96 21.0863 123.108C21.0863 111.256 30.6945 101.647 42.5469 101.647H45.4249V101.644H79.5153C82.062 101.644 84.5067 102.722 86.0978 104.71C88.8856 108.194 91.0222 111.438 92.5969 114.114C94.056 116.594 98.4255 116.618 99.8699 114.13C101.393 111.506 103.416 108.337 105.98 104.929C107.573 102.813 110.103 101.644 112.752 101.644H125.427C143.951 101.644 154.105 92.7623 159.289 86.3612C161.972 83.049 165.782 80.7871 170.045 80.7871H179.614Z" fill="#FABFBA"/> <path d="M96.3843 111.768C96.3842 87.8629 77.3194 68.4739 53.768 68.3843C77.3196 68.2949 96.3845 48.9049 96.3845 25C96.3845 25 96.3845 25 96.3845 25C96.3845 48.9602 115.538 68.3838 139.165 68.3838C115.538 68.3838 96.3844 87.8075 96.3843 111.768Z" fill="#FF5F46"/> <path d="M274.824 139.867C267.307 139.867 260.701 138.158 255.006 134.742C249.388 131.325 245.022 126.579 241.909 120.505C238.796 114.355 237.239 107.18 237.239 98.9793C237.239 90.855 238.834 83.6798 242.023 77.4537C245.212 71.1516 249.767 66.2543 255.69 62.7615C261.688 59.1929 268.787 57.4086 276.988 57.4086C286.251 57.4086 293.92 59.6485 299.994 64.1283C306.144 68.5321 310.13 74.6823 311.952 82.5788H296.577C295.438 78.6306 293.198 75.5555 289.857 73.3535C286.516 71.1516 282.189 70.0507 276.874 70.0507C271.483 70.0507 266.851 71.2276 262.979 73.5813C259.182 75.8592 256.259 79.2 254.209 83.6039C252.235 87.9318 251.248 93.0949 251.248 99.0932C251.248 105.092 252.235 110.255 254.209 114.583C256.259 118.911 259.144 122.213 262.865 124.491C266.585 126.693 270.951 127.794 275.962 127.794C283.403 127.794 289.022 125.706 292.819 121.53C296.615 117.354 298.855 111.925 299.538 105.243H278.924V94.8792H313.319V138.5H300.791L299.652 127.566C297.906 130.148 295.894 132.388 293.616 134.286C291.338 136.108 288.642 137.513 285.529 138.5C282.492 139.411 278.924 139.867 274.824 139.867ZM351.07 139.867C345.375 139.867 340.364 138.652 336.036 136.222C331.708 133.717 328.33 130.224 325.9 125.744C323.47 121.264 322.255 116.101 322.255 110.255C322.255 104.18 323.432 98.8654 325.786 94.3097C328.216 89.7541 331.594 86.1854 335.922 83.6039C340.326 81.0223 345.413 79.7315 351.184 79.7315C356.803 79.7315 361.7 80.9843 365.876 83.49C370.052 85.9956 373.279 89.3744 375.557 93.6264C377.835 97.8024 378.974 102.51 378.974 107.749C378.974 108.508 378.974 109.344 378.974 110.255C378.974 111.166 378.898 112.115 378.746 113.102H332.05V104.332H365.193C365.041 100.156 363.636 96.8913 360.979 94.5375C358.321 92.1078 355.018 90.893 351.07 90.893C348.261 90.893 345.679 91.5384 343.325 92.8291C340.972 94.1199 339.111 96.0561 337.745 98.6377C336.378 101.143 335.695 104.332 335.695 108.205V111.507C335.695 115.076 336.34 118.151 337.631 120.733C338.997 123.314 340.82 125.288 343.098 126.655C345.451 127.946 348.071 128.591 350.956 128.591C354.145 128.591 356.765 127.908 358.815 126.541C360.941 125.175 362.497 123.352 363.484 121.074H377.379C376.316 124.643 374.57 127.87 372.14 130.755C369.71 133.565 366.711 135.805 363.143 137.475C359.574 139.069 355.55 139.867 351.07 139.867ZM388.176 138.5V81.0982H400.248L401.273 90.6652C403.02 87.3243 405.525 84.6669 408.79 82.6927C412.055 80.7186 415.928 79.7315 420.407 79.7315C425.039 79.7315 428.987 80.7186 432.252 82.6927C435.517 84.5909 438.023 87.4003 439.769 91.1208C441.591 94.8412 442.503 99.4729 442.503 105.016V138.5H428.835V106.268C428.835 101.485 427.772 97.8024 425.646 95.2209C423.52 92.6393 420.369 91.3485 416.193 91.3485C413.46 91.3485 410.992 91.9939 408.79 93.2847C406.664 94.5755 404.956 96.4737 403.665 98.9793C402.45 101.409 401.843 104.37 401.843 107.863V138.5H388.176ZM454.064 138.5V81.0982H467.731V138.5H454.064ZM460.898 71.9868C458.392 71.9868 456.304 71.2275 454.634 69.709C453.039 68.1145 452.242 66.1783 452.242 63.9005C452.242 61.5467 453.039 59.6485 454.634 58.2059C456.304 56.6873 458.392 55.928 460.898 55.928C463.404 55.928 465.454 56.6873 467.048 58.2059C468.719 59.6485 469.554 61.5467 469.554 63.9005C469.554 66.1783 468.719 68.1145 467.048 69.709C465.454 71.2275 463.404 71.9868 460.898 71.9868ZM506.987 139.867C501.292 139.867 496.281 138.652 491.953 136.222C487.625 133.717 484.246 130.224 481.817 125.744C479.387 121.264 478.172 116.101 478.172 110.255C478.172 104.18 479.349 98.8654 481.703 94.3097C484.133 89.7541 487.511 86.1854 491.839 83.6039C496.243 81.0223 501.33 79.7315 507.101 79.7315C512.72 79.7315 517.617 80.9843 521.793 83.49C525.969 85.9956 529.196 89.3744 531.474 93.6264C533.752 97.8024 534.891 102.51 534.891 107.749C534.891 108.508 534.891 109.344 534.891 110.255C534.891 111.166 534.815 112.115 534.663 113.102H487.967V104.332H521.11C520.958 100.156 519.553 96.8913 516.896 94.5375C514.238 92.1078 510.935 90.893 506.987 90.893C504.178 90.893 501.596 91.5384 499.242 92.8291C496.889 94.1199 495.028 96.0561 493.662 98.6377C492.295 101.143 491.612 104.332 491.612 108.205V111.507C491.612 115.076 492.257 118.151 493.548 120.733C494.914 123.314 496.737 125.288 499.015 126.655C501.368 127.946 503.988 128.591 506.873 128.591C510.062 128.591 512.682 127.908 514.732 126.541C516.858 125.175 518.414 123.352 519.401 121.074H533.296C532.233 124.643 530.487 127.87 528.057 130.755C525.627 133.565 522.628 135.805 519.06 137.475C515.491 139.069 511.467 139.867 506.987 139.867Z" fill="#0B2026"/> <rect x="572" y="58" width="230.131" height="84" rx="42" fill="#0B2026"/> <path d="M689.673 113.164C687.292 113.164 685.183 112.634 683.345 111.574C681.53 110.489 680.104 108.993 679.067 107.084C678.03 105.151 677.511 102.912 677.511 100.367C677.511 97.8447 678.03 95.6293 679.067 93.7202C680.104 91.7875 681.53 90.2791 683.345 89.195C685.183 88.1108 687.292 87.5687 689.673 87.5687C692.1 87.5687 694.233 88.1108 696.072 89.195C697.91 90.2791 699.336 91.7875 700.349 93.7202C701.363 95.6293 701.87 97.8447 701.87 100.367C701.87 102.912 701.363 105.151 700.349 107.084C699.336 108.993 697.91 110.489 696.072 111.574C694.233 112.634 692.1 113.164 689.673 113.164ZM689.708 109.346C691.287 109.346 692.666 108.993 693.844 108.286C695.023 107.555 695.93 106.518 696.567 105.175C697.203 103.831 697.521 102.229 697.521 100.367C697.521 98.5047 697.203 96.902 696.567 95.5585C695.93 94.2151 695.023 93.1899 693.844 92.4828C692.666 91.7522 691.287 91.3869 689.708 91.3869C688.129 91.3869 686.75 91.7522 685.572 92.4828C684.393 93.1899 683.474 94.2151 682.814 95.5585C682.178 96.902 681.86 98.5047 681.86 100.367C681.86 102.229 682.178 103.831 682.814 105.175C683.474 106.518 684.393 107.555 685.572 108.286C686.75 108.993 688.129 109.346 689.708 109.346ZM710.257 112.74V87.9929H714.5L726.414 105.882V87.9929H730.656V112.74H726.414L714.5 94.8868V112.74H710.257ZM739.875 112.74V87.9929H755.855V91.4222H744.118V98.5282H754.794V101.887H744.118V109.311H755.855V112.74H739.875Z" fill="white"/> <path d="M653.736 87.0215V112.958L636.745 122.691V86.0166H631.61L620.711 90.8662V97.8281L627.844 95.8877V124.126L608.347 112.958V87.0215L631.042 74.0215L653.736 87.0215Z" fill="#FF3621"/> </svg>
# MAGIC     <span style="font-size: 15pt; color: #5A6F77;">the consumer home &middot; two ways to get answers</span>
# MAGIC   </div>
# MAGIC   <div style="display: flex; gap: 16px; margin-top: 12px; align-items: stretch; flex-wrap: nowrap;">
# MAGIC     <div style="flex: 1 1 0; min-width: 0; background: #FFFFFF; border-radius: 10px; padding: 16px 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06); box-sizing: border-box;">
# MAGIC       <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #FF5F46; border-radius: 10px 10px 0 0;"></div>
# MAGIC       <div style="font-size: 15pt; font-weight: 700; margin: 8px 0 10px 0;">1. Open a shared asset directly</div>
# MAGIC       <div style="display: flex; flex-direction: column; gap: 8px;"><div style="background:#F9F7F4; border:2px solid #1B5162; border-radius:8px; padding:10px 14px; display:flex; align-items:center;"><svg style="height:34px;width:auto;display:inline-block;vertical-align:middle;flex-shrink:0;" viewBox="0 0 1104 200" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M174.975 25.0001L107.787 25.0001L107.787 81.2499L174.975 81.2499L174.975 25.0001Z" fill="#FABFBA"/> <path d="M107.812 175L174.999 175L174.999 93.7499L107.812 93.7499L107.812 175Z" fill="#FF5F46"/> <path d="M92.1865 24.9999L24.9991 24.9999L24.999 118.75L92.1865 118.75L92.1865 24.9999Z" fill="#FF5F46"/> <path d="M25.0254 175L92.2129 175L92.2129 132.031L25.0254 132.031L25.0254 175Z" fill="#FABFBA"/> <path d="M234.76 137.5L263.022 60.22H277.816L306.078 137.5H292.058L270.309 75.676L248.56 137.5H234.76ZM247.346 119.284L250.878 108.796H288.966L292.499 119.284H247.346ZM313.397 137.5V60.22H326.645V137.5H313.397ZM333.682 149.423L361.392 51.94H374.309L346.599 149.423H333.682ZM387.093 137.5V60.22H417.343C422.789 60.22 427.315 61.0664 430.922 62.7592C434.602 64.452 437.362 66.8072 439.202 69.8248C441.042 72.7688 441.962 76.1912 441.962 80.092C441.962 83.9928 441.115 87.268 439.423 89.9176C437.73 92.5672 435.485 94.5912 432.688 95.9896C429.965 97.388 426.984 98.2344 423.746 98.5288L425.402 97.3144C428.861 97.388 431.952 98.308 434.675 100.074C437.472 101.841 439.68 104.159 441.299 107.03C442.919 109.826 443.728 112.954 443.728 116.414C443.728 120.462 442.735 124.105 440.747 127.343C438.834 130.508 436 133.01 432.247 134.85C428.493 136.617 423.893 137.5 418.447 137.5H387.093ZM400.341 126.681H416.459C420.802 126.681 424.187 125.65 426.616 123.59C429.045 121.529 430.259 118.658 430.259 114.978C430.259 111.298 429.008 108.391 426.506 106.257C424.003 104.049 420.581 102.945 416.239 102.945H400.341V126.681ZM400.341 92.8984H415.466C419.735 92.8984 422.973 91.9416 425.181 90.028C427.389 88.0408 428.493 85.3176 428.493 81.8584C428.493 78.4728 427.389 75.8232 425.181 73.9096C422.973 71.9224 419.698 70.9288 415.355 70.9288H400.341V92.8984ZM453.104 137.5V60.22H466.352V137.5H453.104ZM502.22 137.5V60.22H527.17C536.149 60.22 543.546 61.8024 549.36 64.9672C555.248 68.132 559.591 72.6216 562.388 78.436C565.258 84.1768 566.693 91.0216 566.693 98.9704C566.693 106.772 565.258 113.58 562.388 119.394C559.591 125.135 555.248 129.588 549.36 132.753C543.546 135.918 536.149 137.5 527.17 137.5H502.22ZM515.468 126.239H526.508C533.205 126.239 538.468 125.172 542.295 123.038C546.196 120.83 548.956 117.702 550.575 113.654C552.268 109.532 553.114 104.638 553.114 98.9704C553.114 93.2296 552.268 88.3352 550.575 84.2872C548.956 80.1656 546.196 77.0008 542.295 74.7928C538.468 72.5112 533.205 71.3704 526.508 71.3704H515.468V126.239ZM594.423 138.825C589.859 138.825 586.069 138.052 583.051 136.506C580.034 134.961 577.789 132.9 576.317 130.324C574.845 127.748 574.109 124.951 574.109 121.934C574.109 118.401 574.992 115.346 576.759 112.77C578.599 110.194 581.285 108.207 584.818 106.809C588.351 105.337 592.693 104.601 597.845 104.601H611.866C611.866 101.657 611.461 99.228 610.651 97.3144C609.842 95.3272 608.591 93.8552 606.898 92.8984C605.205 91.9416 603.034 91.4632 600.384 91.4632C597.367 91.4632 594.791 92.1624 592.656 93.5608C590.522 94.8856 589.197 96.9464 588.682 99.7432H575.655C576.096 95.7688 577.421 92.3832 579.629 89.5864C581.837 86.716 584.744 84.508 588.351 82.9624C592.031 81.3432 596.042 80.5336 600.384 80.5336C605.61 80.5336 610.063 81.4536 613.743 83.2936C617.423 85.06 620.219 87.636 622.133 91.0216C624.12 94.3336 625.114 98.3448 625.114 103.055V137.5H613.853L612.528 128.558C611.792 130.03 610.835 131.391 609.658 132.642C608.554 133.894 607.266 134.998 605.794 135.954C604.322 136.838 602.629 137.537 600.715 138.052C598.875 138.567 596.778 138.825 594.423 138.825ZM597.403 128.337C599.538 128.337 601.415 127.969 603.034 127.233C604.727 126.423 606.162 125.319 607.339 123.921C608.591 122.449 609.547 120.83 610.21 119.063C610.872 117.297 611.314 115.42 611.535 113.433V113.212H599.28C596.704 113.212 594.57 113.543 592.877 114.206C591.184 114.794 589.97 115.678 589.234 116.855C588.498 118.033 588.13 119.394 588.13 120.94C588.13 122.486 588.498 123.81 589.234 124.914C589.97 126.018 591.037 126.865 592.435 127.454C593.834 128.042 595.49 128.337 597.403 128.337ZM658.147 138.825C653.216 138.825 648.911 138.052 645.231 136.506C641.624 134.887 638.754 132.679 636.619 129.882C634.559 127.012 633.344 123.737 632.976 120.057H646.224C646.592 121.602 647.255 123.038 648.211 124.362C649.168 125.614 650.456 126.607 652.075 127.343C653.768 128.079 655.755 128.447 658.037 128.447C660.245 128.447 662.048 128.153 663.447 127.564C664.845 126.902 665.875 126.055 666.538 125.025C667.2 123.994 667.531 122.89 667.531 121.713C667.531 119.946 667.053 118.585 666.096 117.628C665.139 116.671 663.741 115.935 661.901 115.42C660.135 114.831 658 114.279 655.498 113.764C652.848 113.249 650.272 112.623 647.77 111.887C645.341 111.078 643.133 110.084 641.146 108.906C639.232 107.729 637.687 106.22 636.509 104.38C635.405 102.54 634.853 100.295 634.853 97.6456C634.853 94.4072 635.699 91.5 637.392 88.924C639.159 86.348 641.661 84.324 644.899 82.852C648.211 81.3064 652.149 80.5336 656.712 80.5336C663.189 80.5336 668.341 82.0424 672.168 85.06C676.069 88.004 678.351 92.1624 679.013 97.5352H666.427C666.059 95.4744 665.029 93.892 663.336 92.788C661.643 91.6104 659.399 91.0216 656.602 91.0216C653.731 91.0216 651.523 91.5736 649.978 92.6776C648.506 93.708 647.77 95.1064 647.77 96.8728C647.77 97.9768 648.211 99.0072 649.095 99.964C650.051 100.847 651.413 101.62 653.179 102.282C654.946 102.871 657.117 103.46 659.693 104.049C663.815 104.858 667.458 105.815 670.623 106.919C673.787 108.023 676.29 109.642 678.13 111.777C679.97 113.911 680.89 116.929 680.89 120.83C680.963 124.362 680.043 127.49 678.13 130.214C676.29 132.937 673.677 135.071 670.291 136.617C666.906 138.089 662.858 138.825 658.147 138.825ZM690.433 137.5V58.012H703.681V90.4696C705.521 87.452 708.023 85.06 711.188 83.2936C714.353 81.4536 717.922 80.5336 721.897 80.5336C726.46 80.5336 730.324 81.4904 733.489 83.404C736.653 85.244 739.045 88.004 740.665 91.684C742.357 95.2904 743.204 99.8168 743.204 105.263V137.5H730.066V106.478C730.066 101.694 729.036 98.0504 726.975 95.548C724.988 93.0456 721.933 91.7944 717.812 91.7944C715.162 91.7944 712.77 92.4568 710.636 93.7816C708.501 95.0328 706.809 96.8728 705.557 99.3016C704.306 101.657 703.681 104.564 703.681 108.023V137.5H690.433ZM785.76 138.825C782.816 138.825 780.166 138.42 777.811 137.61C775.456 136.874 773.395 135.844 771.628 134.519C769.862 133.121 768.39 131.538 767.212 129.772L765.777 137.5H753.964V58.012H767.212V90.028C768.979 87.3048 771.371 85.06 774.388 83.2936C777.406 81.4536 781.16 80.5336 785.649 80.5336C790.875 80.5336 795.475 81.8216 799.449 84.3976C803.497 86.9 806.662 90.3592 808.944 94.7752C811.299 99.1176 812.476 104.122 812.476 109.79C812.476 115.31 811.336 120.278 809.054 124.694C806.772 129.11 803.608 132.569 799.56 135.071C795.585 137.574 790.985 138.825 785.76 138.825ZM783 127.343C786.091 127.343 788.851 126.607 791.28 125.135C793.708 123.59 795.585 121.529 796.91 118.953C798.308 116.303 799.008 113.212 799.008 109.679C799.008 106.22 798.308 103.166 796.91 100.516C795.585 97.8664 793.708 95.8056 791.28 94.3336C788.851 92.8616 786.091 92.1256 783 92.1256C779.835 92.1256 777.038 92.8616 774.609 94.3336C772.254 95.8056 770.377 97.8664 768.979 100.516C767.654 103.166 766.992 106.22 766.992 109.679C766.992 113.212 767.654 116.303 768.979 118.953C770.377 121.529 772.254 123.59 774.609 125.135C777.038 126.607 779.835 127.343 783 127.343ZM847.968 138.825C842.669 138.825 837.885 137.61 833.616 135.182C829.421 132.679 826.109 129.257 823.68 124.914C821.325 120.498 820.147 115.457 820.147 109.79C820.147 103.975 821.362 98.8968 823.791 94.5544C826.219 90.1384 829.531 86.716 833.727 84.2872C837.995 81.7848 842.779 80.5336 848.079 80.5336C853.378 80.5336 858.125 81.7848 862.32 84.2872C866.589 86.716 869.901 90.1016 872.256 94.444C874.685 98.7864 875.899 103.865 875.899 109.679C875.899 115.494 874.685 120.572 872.256 124.914C869.827 129.257 866.479 132.679 862.21 135.182C858.015 137.61 853.267 138.825 847.968 138.825ZM847.968 127.454C850.618 127.454 853.01 126.791 855.144 125.466C857.352 124.142 859.119 122.154 860.443 119.505C861.768 116.855 862.431 113.58 862.431 109.679C862.431 105.778 861.768 102.54 860.443 99.964C859.192 97.3144 857.463 95.3272 855.255 94.0024C853.12 92.6776 850.728 92.0152 848.079 92.0152C845.503 92.0152 843.111 92.6776 840.903 94.0024C838.695 95.3272 836.928 97.3144 835.603 99.964C834.279 102.54 833.616 105.778 833.616 109.679C833.616 113.58 834.279 116.855 835.603 119.505C836.928 122.154 838.658 124.142 840.792 125.466C843 126.791 845.392 127.454 847.968 127.454ZM904.103 138.825C899.54 138.825 895.75 138.052 892.732 136.506C889.714 134.961 887.47 132.9 885.998 130.324C884.526 127.748 883.79 124.951 883.79 121.934C883.79 118.401 884.673 115.346 886.439 112.77C888.279 110.194 890.966 108.207 894.498 106.809C898.031 105.337 902.374 104.601 907.526 104.601H921.546C921.546 101.657 921.142 99.228 920.332 97.3144C919.522 95.3272 918.271 93.8552 916.578 92.8984C914.886 91.9416 912.714 91.4632 910.065 91.4632C907.047 91.4632 904.471 92.1624 902.337 93.5608C900.202 94.8856 898.878 96.9464 898.362 99.7432H885.335C885.777 95.7688 887.102 92.3832 889.31 89.5864C891.518 86.716 894.425 84.508 898.031 82.9624C901.711 81.3432 905.722 80.5336 910.065 80.5336C915.29 80.5336 919.743 81.4536 923.423 83.2936C927.103 85.06 929.9 87.636 931.814 91.0216C933.801 94.3336 934.794 98.3448 934.794 103.055V137.5H923.534L922.209 128.558C921.473 130.03 920.516 131.391 919.338 132.642C918.234 133.894 916.946 134.998 915.474 135.954C914.002 136.838 912.31 137.537 910.396 138.052C908.556 138.567 906.458 138.825 904.103 138.825ZM907.084 128.337C909.218 128.337 911.095 127.969 912.714 127.233C914.407 126.423 915.842 125.319 917.02 123.921C918.271 122.449 919.228 120.83 919.89 119.063C920.553 117.297 920.994 115.42 921.215 113.433V113.212H908.961C906.385 113.212 904.25 113.543 902.558 114.206C900.865 114.794 899.65 115.678 898.914 116.855C898.178 118.033 897.81 119.394 897.81 120.94C897.81 122.486 898.178 123.81 898.914 124.914C899.65 126.018 900.718 126.865 902.116 127.454C903.514 128.042 905.17 128.337 907.084 128.337ZM945.638 137.5V81.8584H957.451L958.665 92.236C959.99 89.8072 961.646 87.7464 963.633 86.0536C965.62 84.2872 967.939 82.9256 970.588 81.9688C973.311 81.012 976.292 80.5336 979.531 80.5336V94.5544H974.894C972.686 94.5544 970.588 94.8488 968.601 95.4376C966.614 95.9528 964.884 96.836 963.412 98.0872C962.014 99.2648 960.91 100.921 960.1 103.055C959.291 105.116 958.886 107.729 958.886 110.894V137.5H945.638ZM1009.75 138.825C1004.6 138.825 999.997 137.574 995.949 135.071C991.901 132.569 988.736 129.11 986.455 124.694C984.247 120.278 983.143 115.273 983.143 109.679C983.143 104.086 984.283 99.1176 986.565 94.7752C988.847 90.3592 992.011 86.9 996.059 84.3976C1000.18 81.8216 1004.82 80.5336 1009.97 80.5336C1014.17 80.5336 1017.81 81.3432 1020.9 82.9624C1024.06 84.508 1026.57 86.716 1028.41 89.5864V58.012H1041.65V137.5H1029.73L1028.41 129.441C1027.23 131.06 1025.79 132.606 1024.1 134.078C1022.41 135.476 1020.38 136.617 1018.03 137.5C1015.67 138.383 1012.91 138.825 1009.75 138.825ZM1012.51 127.343C1015.67 127.343 1018.47 126.607 1020.9 125.135C1023.33 123.59 1025.21 121.492 1026.53 118.842C1027.85 116.193 1028.52 113.138 1028.52 109.679C1028.52 106.22 1027.85 103.166 1026.53 100.516C1025.21 97.8664 1023.33 95.8056 1020.9 94.3336C1018.47 92.8616 1015.67 92.1256 1012.51 92.1256C1009.49 92.1256 1006.77 92.8616 1004.34 94.3336C1001.91 95.8056 999.997 97.8664 998.599 100.516C997.274 103.166 996.611 106.22 996.611 109.679C996.611 113.138 997.274 116.193 998.599 118.842C999.997 121.492 1001.91 123.59 1004.34 125.135C1006.77 126.607 1009.49 127.343 1012.51 127.343ZM1075.27 138.825C1070.34 138.825 1066.03 138.052 1062.35 136.506C1058.75 134.887 1055.88 132.679 1053.74 129.882C1051.68 127.012 1050.47 123.737 1050.1 120.057H1063.35C1063.71 121.602 1064.38 123.038 1065.33 124.362C1066.29 125.614 1067.58 126.607 1069.2 127.343C1070.89 128.079 1072.88 128.447 1075.16 128.447C1077.37 128.447 1079.17 128.153 1080.57 127.564C1081.97 126.902 1083 126.055 1083.66 125.025C1084.32 123.994 1084.65 122.89 1084.65 121.713C1084.65 119.946 1084.18 118.585 1083.22 117.628C1082.26 116.671 1080.86 115.935 1079.02 115.42C1077.26 114.831 1075.12 114.279 1072.62 113.764C1069.97 113.249 1067.39 112.623 1064.89 111.887C1062.46 111.078 1060.26 110.084 1058.27 108.906C1056.35 107.729 1054.81 106.22 1053.63 104.38C1052.53 102.54 1051.98 100.295 1051.98 97.6456C1051.98 94.4072 1052.82 91.5 1054.51 88.924C1056.28 86.348 1058.78 84.324 1062.02 82.852C1065.33 81.3064 1069.27 80.5336 1073.83 80.5336C1080.31 80.5336 1085.46 82.0424 1089.29 85.06C1093.19 88.004 1095.47 92.1624 1096.14 97.5352H1083.55C1083.18 95.4744 1082.15 93.892 1080.46 92.788C1078.77 91.6104 1076.52 91.0216 1073.72 91.0216C1070.85 91.0216 1068.65 91.5736 1067.1 92.6776C1065.63 93.708 1064.89 95.1064 1064.89 96.8728C1064.89 97.9768 1065.33 99.0072 1066.22 99.964C1067.17 100.847 1068.54 101.62 1070.3 102.282C1072.07 102.871 1074.24 103.46 1076.82 104.049C1080.94 104.858 1084.58 105.815 1087.74 106.919C1090.91 108.023 1093.41 109.642 1095.25 111.777C1097.09 113.911 1098.01 116.929 1098.01 120.83C1098.09 124.362 1097.17 127.49 1095.25 130.214C1093.41 132.937 1090.8 135.071 1087.41 136.617C1084.03 138.089 1079.98 138.825 1075.27 138.825Z" fill="#1B3139"/> </svg></div><div style="background:#F9F7F4; border:2px solid #1B5162; border-radius:8px; padding:10px 14px; display:flex; align-items:center;"><svg style="height:34px;width:auto;display:inline-block;vertical-align:middle;flex-shrink:0;" viewBox="0 0 881 200" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M81.7909 159.789C75.0244 159.789 69.5392 166.599 69.5392 175H126.368C126.368 166.599 120.883 159.789 114.116 159.789H81.7909Z" fill="#FF5F46"/> <path d="M179.614 80.7871C167.525 100.208 149.376 126.933 141.272 133.79C133.167 140.647 121.149 153.009 93.2907 153.009C73.7741 153.009 56.9864 140.474 49.5352 122.498C49.5353 122.519 49.5356 122.54 49.5358 122.561C48.4799 119.938 45.9132 118.085 42.9121 118.085C38.969 118.085 35.7721 121.282 35.7721 125.225C35.7722 126.15 35.9484 126.997 36.2689 127.752C37.984 131.793 42.5469 131.965 42.5469 144.569C42.5469 143.103 42.5469 146.404 42.5469 144.569C30.6947 144.569 21.0865 134.96 21.0863 123.108C21.0863 111.256 30.6945 101.647 42.5469 101.647H45.4249V101.644H79.5153C82.062 101.644 84.5067 102.722 86.0978 104.71C88.8856 108.194 91.0222 111.438 92.5969 114.114C94.056 116.594 98.4255 116.618 99.8699 114.13C101.393 111.506 103.416 108.337 105.98 104.929C107.573 102.813 110.103 101.644 112.752 101.644H125.427C143.951 101.644 154.105 92.7623 159.289 86.3612C161.972 83.049 165.782 80.7871 170.045 80.7871H179.614Z" fill="#FABFBA"/> <path d="M96.3843 111.768C96.3842 87.8629 77.3194 68.4739 53.768 68.3843C77.3196 68.2949 96.3845 48.9049 96.3845 25C96.3845 25 96.3845 25 96.3845 25C96.3845 48.9602 115.538 68.3838 139.165 68.3838C115.538 68.3838 96.3844 87.8075 96.3843 111.768Z" fill="#FF5F46"/> <path d="M274.824 139.867C267.307 139.867 260.701 138.158 255.006 134.742C249.388 131.325 245.022 126.579 241.909 120.505C238.796 114.355 237.239 107.18 237.239 98.9793C237.239 90.855 238.834 83.6798 242.023 77.4537C245.212 71.1516 249.767 66.2543 255.69 62.7615C261.688 59.1929 268.787 57.4086 276.988 57.4086C286.251 57.4086 293.92 59.6485 299.994 64.1283C306.144 68.5321 310.13 74.6823 311.952 82.5788H296.577C295.438 78.6306 293.198 75.5555 289.857 73.3535C286.516 71.1516 282.189 70.0507 276.874 70.0507C271.483 70.0507 266.851 71.2276 262.979 73.5813C259.182 75.8592 256.259 79.2 254.209 83.6039C252.235 87.9318 251.248 93.0949 251.248 99.0932C251.248 105.092 252.235 110.255 254.209 114.583C256.259 118.911 259.144 122.213 262.865 124.491C266.585 126.693 270.951 127.794 275.962 127.794C283.403 127.794 289.022 125.706 292.819 121.53C296.615 117.354 298.855 111.925 299.538 105.243H278.924V94.8792H313.319V138.5H300.791L299.652 127.566C297.906 130.148 295.894 132.388 293.616 134.286C291.338 136.108 288.642 137.513 285.529 138.5C282.492 139.411 278.924 139.867 274.824 139.867ZM351.07 139.867C345.375 139.867 340.364 138.652 336.036 136.222C331.708 133.717 328.33 130.224 325.9 125.744C323.47 121.264 322.255 116.101 322.255 110.255C322.255 104.18 323.432 98.8654 325.786 94.3097C328.216 89.7541 331.594 86.1854 335.922 83.6039C340.326 81.0223 345.413 79.7315 351.184 79.7315C356.803 79.7315 361.7 80.9843 365.876 83.49C370.052 85.9956 373.279 89.3744 375.557 93.6264C377.835 97.8024 378.974 102.51 378.974 107.749C378.974 108.508 378.974 109.344 378.974 110.255C378.974 111.166 378.898 112.115 378.746 113.102H332.05V104.332H365.193C365.041 100.156 363.636 96.8913 360.979 94.5375C358.321 92.1078 355.018 90.893 351.07 90.893C348.261 90.893 345.679 91.5384 343.325 92.8291C340.972 94.1199 339.111 96.0561 337.745 98.6377C336.378 101.143 335.695 104.332 335.695 108.205V111.507C335.695 115.076 336.34 118.151 337.631 120.733C338.997 123.314 340.82 125.288 343.098 126.655C345.451 127.946 348.071 128.591 350.956 128.591C354.145 128.591 356.765 127.908 358.815 126.541C360.941 125.175 362.497 123.352 363.484 121.074H377.379C376.316 124.643 374.57 127.87 372.14 130.755C369.71 133.565 366.711 135.805 363.143 137.475C359.574 139.069 355.55 139.867 351.07 139.867ZM388.176 138.5V81.0982H400.248L401.273 90.6652C403.02 87.3243 405.525 84.6669 408.79 82.6927C412.055 80.7186 415.928 79.7315 420.407 79.7315C425.039 79.7315 428.987 80.7186 432.252 82.6927C435.517 84.5909 438.023 87.4003 439.769 91.1208C441.591 94.8412 442.503 99.4729 442.503 105.016V138.5H428.835V106.268C428.835 101.485 427.772 97.8024 425.646 95.2209C423.52 92.6393 420.369 91.3485 416.193 91.3485C413.46 91.3485 410.992 91.9939 408.79 93.2847C406.664 94.5755 404.956 96.4737 403.665 98.9793C402.45 101.409 401.843 104.37 401.843 107.863V138.5H388.176ZM454.064 138.5V81.0982H467.731V138.5H454.064ZM460.898 71.9868C458.392 71.9868 456.304 71.2275 454.634 69.709C453.039 68.1145 452.242 66.1783 452.242 63.9005C452.242 61.5467 453.039 59.6485 454.634 58.2059C456.304 56.6873 458.392 55.928 460.898 55.928C463.404 55.928 465.454 56.6873 467.048 58.2059C468.719 59.6485 469.554 61.5467 469.554 63.9005C469.554 66.1783 468.719 68.1145 467.048 69.709C465.454 71.2275 463.404 71.9868 460.898 71.9868ZM506.987 139.867C501.292 139.867 496.281 138.652 491.953 136.222C487.625 133.717 484.246 130.224 481.817 125.744C479.387 121.264 478.172 116.101 478.172 110.255C478.172 104.18 479.349 98.8654 481.703 94.3097C484.133 89.7541 487.511 86.1854 491.839 83.6039C496.243 81.0223 501.33 79.7315 507.101 79.7315C512.72 79.7315 517.617 80.9843 521.793 83.49C525.969 85.9956 529.196 89.3744 531.474 93.6264C533.752 97.8024 534.891 102.51 534.891 107.749C534.891 108.508 534.891 109.344 534.891 110.255C534.891 111.166 534.815 112.115 534.663 113.102H487.967V104.332H521.11C520.958 100.156 519.553 96.8913 516.896 94.5375C514.238 92.1078 510.935 90.893 506.987 90.893C504.178 90.893 501.596 91.5384 499.242 92.8291C496.889 94.1199 495.028 96.0561 493.662 98.6377C492.295 101.143 491.612 104.332 491.612 108.205V111.507C491.612 115.076 492.257 118.151 493.548 120.733C494.914 123.314 496.737 125.288 499.015 126.655C501.368 127.946 503.988 128.591 506.873 128.591C510.062 128.591 512.682 127.908 514.732 126.541C516.858 125.175 518.414 123.352 519.401 121.074H533.296C532.233 124.643 530.487 127.87 528.057 130.755C525.627 133.565 522.628 135.805 519.06 137.475C515.491 139.069 511.467 139.867 506.987 139.867Z" fill="#0B2026"/> <rect x="572" y="58" width="308.12" height="84" rx="42" fill="#0B2026"/> <path d="M672.51 113.74L682.313 86.9347H687.444L697.247 113.74H692.384L684.84 92.2958L677.296 113.74H672.51ZM676.875 107.422L678.1 103.784H691.312L692.537 107.422H676.875ZM715.676 114.2C713.149 114.2 710.928 113.625 709.013 112.477C707.124 111.328 705.656 109.732 704.609 107.69C703.563 105.622 703.039 103.209 703.039 100.452C703.039 97.7207 703.575 95.3082 704.648 93.2148C705.72 91.0959 707.252 89.4493 709.243 88.275C711.26 87.0751 713.647 86.4752 716.404 86.4752C719.518 86.4752 722.097 87.2283 724.139 88.7345C726.207 90.2152 727.547 92.283 728.16 94.9381H722.99C722.607 93.6105 721.854 92.5766 720.731 91.8363C719.608 91.0959 718.152 90.7258 716.365 90.7258C714.553 90.7258 712.996 91.1215 711.694 91.9129C710.417 92.6787 709.434 93.802 708.745 95.2827C708.081 96.7379 707.749 98.4738 707.749 100.491C707.749 102.507 708.081 104.243 708.745 105.699C709.434 107.154 710.404 108.264 711.655 109.03C712.906 109.77 714.374 110.141 716.059 110.141C718.561 110.141 720.45 109.439 721.727 108.034C723.003 106.63 723.756 104.805 723.986 102.558H717.055V99.0738H728.619V113.74H724.407L724.024 110.064C723.437 110.932 722.76 111.685 721.995 112.323C721.229 112.936 720.322 113.408 719.276 113.74C718.255 114.047 717.055 114.2 715.676 114.2ZM738.172 113.74V86.9347H755.481V90.6492H742.767V98.3462H754.332V101.984H742.767V110.026H755.481V113.74H738.172ZM764.906 113.74V86.9347H769.501L782.406 106.311V86.9347H787.001V113.74H782.406L769.501 94.4019V113.74H764.906ZM803.229 113.74V90.6492H795.341V86.9347H815.675V90.6492H807.786V113.74H803.229ZM832.683 114.2C830.742 114.2 829.019 113.855 827.513 113.166C826.007 112.477 824.832 111.494 823.99 110.217C823.148 108.941 822.714 107.422 822.688 105.66H827.551C827.551 106.554 827.756 107.358 828.164 108.073C828.598 108.762 829.185 109.311 829.925 109.719C830.691 110.128 831.61 110.332 832.683 110.332C833.602 110.332 834.393 110.192 835.057 109.911C835.746 109.605 836.269 109.183 836.627 108.647C837.01 108.086 837.201 107.435 837.201 106.694C837.201 105.852 836.997 105.162 836.589 104.626C836.206 104.065 835.67 103.592 834.98 103.209C834.291 102.827 833.5 102.495 832.606 102.214C831.713 101.907 830.768 101.588 829.772 101.257C827.653 100.542 826.058 99.6354 824.986 98.5377C823.913 97.4144 823.377 95.9209 823.377 94.0573C823.377 92.5 823.747 91.1597 824.488 90.0365C825.228 88.9132 826.262 88.0452 827.59 87.4325C828.943 86.7943 830.5 86.4752 832.261 86.4752C834.048 86.4752 835.606 86.7943 836.933 87.4325C838.286 88.0707 839.346 88.9642 840.112 90.1131C840.903 91.2363 841.311 92.5894 841.337 94.1722H836.435C836.41 93.5084 836.231 92.8957 835.899 92.3341C835.567 91.7469 835.082 91.2746 834.444 90.9172C833.831 90.5343 833.078 90.3428 832.185 90.3428C831.419 90.3173 830.73 90.4449 830.117 90.7258C829.53 90.981 829.058 91.364 828.7 91.8746C828.368 92.3596 828.202 92.9723 828.202 93.7127C828.202 94.4275 828.355 95.0274 828.662 95.5125C828.994 95.972 829.466 96.3677 830.079 96.6996C830.691 97.0059 831.406 97.2995 832.223 97.5803C833.04 97.8611 833.934 98.1675 834.904 98.4994C836.231 98.9334 837.431 99.4695 838.503 100.108C839.601 100.72 840.469 101.525 841.107 102.52C841.745 103.516 842.065 104.805 842.065 106.388C842.065 107.766 841.707 109.056 840.992 110.256C840.278 111.43 839.231 112.387 837.852 113.128C836.474 113.842 834.75 114.2 832.683 114.2Z" fill="white"/> <path d="M632.893 74.0239C632.893 74.0239 632.893 74.02 632.893 74.0221L634.136 80.6146C635.485 87.7644 641.078 93.3568 648.228 94.7065L654.82 95.9495C654.82 97.6494 654.82 102.901 654.82 102.901L648.228 104.144C641.078 105.494 635.485 111.086 634.136 118.236L632.893 124.829C631.193 124.829 625.941 124.829 625.941 124.829L624.698 118.236C623.348 111.086 617.756 105.494 610.606 104.144L604.014 102.901C604.014 102.901 604.015 97.6494 604.015 95.9495H604.014L610.606 94.7065C617.756 93.3568 623.348 87.7644 624.698 80.6146L625.941 74.0221C625.941 74.0221 631.193 74.0239 632.893 74.0239Z" fill="#FF3621"/> </svg></div><div style="background:#F9F7F4; border:2px solid #1B5162; border-radius:8px; padding:10px 14px; display:flex; align-items:center;"><svg style="height:40px;width:auto;display:inline-block;vertical-align:middle;flex-shrink:0;" viewBox="0 0 852 300" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M32 40C32 35.5817 35.5817 32 40 32H117.75C122.168 32 125.75 35.5817 125.75 40V117.75C125.75 122.168 122.168 125.75 117.75 125.75H40C35.5817 125.75 32 122.168 32 117.75V40Z" fill="#FABFBA"/> <path d="M158.562 40C158.562 35.5817 162.144 32 166.562 32H244.312C248.731 32 252.312 35.5817 252.312 40V117.75C252.312 122.168 248.731 125.75 244.313 125.75H166.563C162.144 125.75 158.562 122.168 158.562 117.75V40Z" fill="#FF5F46"/> <path d="M32 171.25C32 166.832 35.5817 163.25 40 163.25H117.75C122.168 163.25 125.75 166.832 125.75 171.25V249C125.75 253.418 122.168 257 117.75 257H40C35.5817 257 32 253.418 32 249V171.25Z" fill="#FF5F46"/> <path d="M158.562 171.25C158.562 166.832 162.144 163.25 166.562 163.25H244.312C248.731 163.25 252.312 166.832 252.312 171.25V249C252.312 253.418 248.731 257 244.313 257H166.563C162.144 257 158.562 253.418 158.562 249V171.25Z" fill="#FABFBA"/> <path d="M340.501 138V60.72H360.373C369.352 60.72 376.749 62.3024 382.563 65.4672C388.451 68.5584 392.794 73.0112 395.59 78.8256C398.461 84.5664 399.896 91.4848 399.896 99.5808C399.896 107.53 398.461 114.374 395.59 120.115C392.794 125.856 388.451 130.272 382.563 133.363C376.749 136.454 369.352 138 360.373 138H340.501ZM349.774 130.272H360.152C367.586 130.272 373.51 129.058 377.926 126.629C382.342 124.126 385.507 120.594 387.421 116.03C389.334 111.394 390.291 105.91 390.291 99.5808C390.291 93.104 389.334 87.5472 387.421 82.9104C385.507 78.2736 382.342 74.704 377.926 72.2016C373.51 69.6992 367.586 68.448 360.152 68.448H349.774V130.272ZM427.945 139.325C423.529 139.325 419.849 138.515 416.905 136.896C413.961 135.203 411.753 132.995 410.281 130.272C408.809 127.475 408.073 124.494 408.073 121.33C408.073 117.502 409.029 114.264 410.943 111.614C412.93 108.891 415.69 106.83 419.223 105.432C422.756 104.034 426.877 103.334 431.588 103.334H446.05C446.05 99.5808 445.609 96.4528 444.725 93.9504C443.842 91.448 442.407 89.5712 440.42 88.32C438.433 87.0688 435.783 86.4432 432.471 86.4432C429.159 86.4432 426.325 87.2896 423.97 88.9824C421.615 90.6016 420.143 93.0304 419.554 96.2688H410.06C410.501 92.4416 411.789 89.24 413.924 86.664C416.058 84.0144 418.745 82.0272 421.983 80.7024C425.295 79.304 428.791 78.6048 432.471 78.6048C437.697 78.6048 442.002 79.5616 445.388 81.4752C448.773 83.3152 451.276 85.928 452.895 89.3136C454.514 92.6256 455.324 96.5632 455.324 101.126V138H447.044L446.492 128.064C445.756 129.61 444.799 131.082 443.621 132.48C442.517 133.805 441.193 134.982 439.647 136.013C438.101 137.043 436.335 137.853 434.348 138.442C432.434 139.03 430.3 139.325 427.945 139.325ZM429.269 131.486C431.698 131.486 433.943 130.934 436.004 129.83C438.065 128.726 439.831 127.254 441.303 125.414C442.849 123.501 444.026 121.366 444.836 119.011C445.645 116.656 446.05 114.19 446.05 111.614V110.51H432.361C428.901 110.51 426.068 110.952 423.86 111.835C421.725 112.718 420.18 113.97 419.223 115.589C418.266 117.134 417.788 118.901 417.788 120.888C417.788 123.022 418.229 124.899 419.113 126.518C419.996 128.064 421.284 129.278 422.977 130.162C424.743 131.045 426.841 131.486 429.269 131.486ZM488.345 138C485.033 138 482.163 137.485 479.734 136.454C477.305 135.424 475.429 133.694 474.104 131.266C472.853 128.763 472.227 125.414 472.227 121.219V87.768H462.07V79.9296H472.227L473.441 65.4672H481.501V79.9296H497.95V87.768H481.501V121.219C481.501 124.678 482.2 127.034 483.598 128.285C484.997 129.462 487.462 130.051 490.995 130.051H497.729V138H488.345ZM525.467 139.325C521.051 139.325 517.371 138.515 514.427 136.896C511.483 135.203 509.275 132.995 507.803 130.272C506.331 127.475 505.595 124.494 505.595 121.33C505.595 117.502 506.552 114.264 508.466 111.614C510.453 108.891 513.213 106.83 516.746 105.432C520.279 104.034 524.4 103.334 529.111 103.334H543.573C543.573 99.5808 543.131 96.4528 542.248 93.9504C541.365 91.448 539.93 89.5712 537.943 88.32C535.955 87.0688 533.306 86.4432 529.994 86.4432C526.682 86.4432 523.848 87.2896 521.493 88.9824C519.138 90.6016 517.666 93.0304 517.077 96.2688H507.583C508.024 92.4416 509.312 89.24 511.447 86.664C513.581 84.0144 516.267 82.0272 519.506 80.7024C522.818 79.304 526.314 78.6048 529.994 78.6048C535.219 78.6048 539.525 79.5616 542.911 81.4752C546.296 83.3152 548.799 85.928 550.418 89.3136C552.037 92.6256 552.847 96.5632 552.847 101.126V138H544.567L544.015 128.064C543.279 129.61 542.322 131.082 541.144 132.48C540.04 133.805 538.715 134.982 537.17 136.013C535.624 137.043 533.858 137.853 531.871 138.442C529.957 139.03 527.823 139.325 525.467 139.325ZM526.792 131.486C529.221 131.486 531.466 130.934 533.527 129.83C535.587 128.726 537.354 127.254 538.826 125.414C540.371 123.501 541.549 121.366 542.359 119.011C543.168 116.656 543.573 114.19 543.573 111.614V110.51H529.883C526.424 110.51 523.591 110.952 521.383 111.835C519.248 112.718 517.703 113.97 516.746 115.589C515.789 117.134 515.311 118.901 515.311 120.888C515.311 123.022 515.752 124.899 516.635 126.518C517.519 128.064 518.807 129.278 520.499 130.162C522.266 131.045 524.363 131.486 526.792 131.486ZM593.781 139.325C590.248 139.325 587.194 138.81 584.618 137.779C582.115 136.675 579.981 135.314 578.214 133.694C576.522 132.075 575.123 130.493 574.019 128.947L573.246 138H564.856V58.512H574.13V89.0928C575.896 85.6336 578.509 83.0208 581.968 81.2544C585.427 79.488 589.291 78.6048 593.56 78.6048C598.859 78.6048 603.496 79.8928 607.47 82.4688C611.445 85.0448 614.536 88.6144 616.744 93.1776C618.952 97.6672 620.056 102.856 620.056 108.744C620.056 114.558 618.952 119.784 616.744 124.421C614.536 129.058 611.445 132.701 607.47 135.35C603.57 138 599.006 139.325 593.781 139.325ZM592.566 131.266C596.026 131.266 599.08 130.382 601.73 128.616C604.453 126.776 606.587 124.2 608.133 120.888C609.752 117.502 610.562 113.528 610.562 108.965C610.562 104.402 609.752 100.464 608.133 97.152C606.587 93.7664 604.453 91.1904 601.73 89.424C599.08 87.584 596.026 86.664 592.566 86.664C588.886 86.664 585.685 87.584 582.962 89.424C580.238 91.1904 578.141 93.7664 576.669 97.152C575.197 100.464 574.461 104.402 574.461 108.965C574.461 113.528 575.197 117.502 576.669 120.888C578.141 124.2 580.238 126.776 582.962 128.616C585.685 130.382 588.886 131.266 592.566 131.266ZM630.221 138V79.9296H638.611L639.273 90.528C640.598 87.8784 642.328 85.6704 644.462 83.904C646.597 82.1376 649.173 80.8128 652.19 79.9296C655.281 79.0464 658.741 78.6048 662.568 78.6048V88.32H656.827C654.619 88.32 652.485 88.6144 650.424 89.2032C648.363 89.792 646.486 90.7488 644.793 92.0736C643.174 93.3984 641.886 95.2016 640.929 97.4832C639.973 99.7648 639.494 102.635 639.494 106.094V138H630.221ZM670.809 138V79.9296H680.083V138H670.809ZM675.446 68.8896C673.606 68.8896 672.06 68.3008 670.809 67.1232C669.631 65.872 669.043 64.3264 669.043 62.4864C669.043 60.6464 669.631 59.1744 670.809 58.0704C672.06 56.8928 673.606 56.304 675.446 56.304C677.212 56.304 678.721 56.8928 679.972 58.0704C681.223 59.1744 681.849 60.6464 681.849 62.4864C681.849 64.3264 681.223 65.872 679.972 67.1232C678.721 68.3008 677.212 68.8896 675.446 68.8896ZM718.304 139.325C713.005 139.325 708.295 138.074 704.173 135.571C700.051 132.995 696.813 129.426 694.458 124.862C692.103 120.299 690.925 115 690.925 108.965C690.925 102.856 692.103 97.5568 694.458 93.0672C696.813 88.504 700.051 84.9712 704.173 82.4688C708.295 79.8928 713.005 78.6048 718.304 78.6048C724.928 78.6048 730.448 80.3712 734.864 83.904C739.354 87.4368 742.224 92.184 743.475 98.1456H733.981C733.171 94.4656 731.295 91.632 728.351 89.6448C725.48 87.584 722.095 86.5536 718.194 86.5536C714.808 86.5536 711.754 87.4 709.031 89.0928C706.381 90.7856 704.283 93.288 702.738 96.6C701.192 99.912 700.419 104.034 700.419 108.965C700.419 112.645 700.861 115.92 701.744 118.79C702.627 121.587 703.842 123.942 705.387 125.856C707.007 127.696 708.883 129.094 711.018 130.051C713.226 131.008 715.618 131.486 718.194 131.486C720.843 131.486 723.235 131.045 725.37 130.162C727.578 129.205 729.418 127.843 730.89 126.077C732.435 124.31 733.466 122.213 733.981 119.784H743.475C742.298 125.598 739.427 130.309 734.864 133.915C730.375 137.522 724.855 139.325 718.304 139.325ZM787.762 138L761.377 106.646L786.217 79.9296H797.588L769.215 109.958L769.325 103.334L799.575 138H787.762ZM753.649 138V58.512H762.922V138H753.649ZM823.817 139.325C818.592 139.325 814.249 138.552 810.79 137.006C807.405 135.387 804.829 133.179 803.062 130.382C801.296 127.512 800.229 124.2 799.861 120.446H809.355C809.649 122.434 810.312 124.274 811.342 125.966C812.446 127.586 814.029 128.91 816.089 129.941C818.15 130.971 820.763 131.486 823.928 131.486C826.43 131.486 828.565 131.118 830.331 130.382C832.097 129.573 833.422 128.469 834.305 127.07C835.262 125.672 835.741 124.053 835.741 122.213C835.741 119.784 835.189 117.907 834.085 116.582C833.054 115.184 831.509 114.154 829.448 113.491C827.461 112.755 824.958 112.203 821.941 111.835C818.702 111.394 815.832 110.768 813.329 109.958C810.827 109.149 808.693 108.082 806.926 106.757C805.233 105.432 803.945 103.776 803.062 101.789C802.179 99.8016 801.737 97.4464 801.737 94.7232C801.737 91.5584 802.584 88.7616 804.277 86.3328C805.969 83.904 808.361 82.0272 811.453 80.7024C814.617 79.304 818.334 78.6048 822.603 78.6048C828.859 78.6048 833.79 80.04 837.397 82.9104C841.077 85.7808 843.248 89.8656 843.91 95.1648H834.747C834.379 92.4416 833.128 90.3072 830.993 88.7616C828.859 87.216 826.025 86.4432 822.493 86.4432C818.739 86.4432 815.905 87.1424 813.992 88.5408C812.078 89.9392 811.121 91.7792 811.121 94.0608C811.121 95.7536 811.526 97.2992 812.336 98.6976C813.219 100.022 814.691 101.163 816.752 102.12C818.813 103.003 821.573 103.666 825.032 104.107C829.374 104.622 833.054 105.469 836.072 106.646C839.089 107.75 841.371 109.48 842.917 111.835C844.536 114.19 845.309 117.392 845.235 121.44C845.235 125.267 844.315 128.506 842.475 131.155C840.709 133.805 838.206 135.829 834.968 137.227C831.803 138.626 828.086 139.325 823.817 139.325ZM334.76 237L363.022 159.72H377.816L406.078 237H392.058L370.309 175.176L348.56 237H334.76ZM347.346 218.784L350.878 208.296H388.966L392.499 218.784H347.346ZM412.955 261.288V181.358H424.768L426.203 189.418C427.381 187.798 428.779 186.29 430.398 184.891C432.091 183.419 434.115 182.242 436.47 181.358C438.899 180.475 441.659 180.034 444.75 180.034C449.976 180.034 454.576 181.322 458.55 183.898C462.598 186.474 465.763 189.97 468.045 194.386C470.326 198.728 471.467 203.696 471.467 209.29C471.467 214.883 470.29 219.888 467.934 224.304C465.653 228.646 462.488 232.069 458.44 234.571C454.466 237.074 449.902 238.325 444.75 238.325C440.555 238.325 436.875 237.552 433.71 236.006C430.619 234.387 428.117 232.106 426.203 229.162V261.288H412.955ZM441.99 226.843C445.082 226.843 447.842 226.107 450.27 224.635C452.699 223.163 454.576 221.102 455.901 218.453C457.299 215.803 457.998 212.749 457.998 209.29C457.998 205.757 457.299 202.666 455.901 200.016C454.576 197.366 452.699 195.306 450.27 193.834C447.842 192.362 445.082 191.626 441.99 191.626C438.826 191.626 436.029 192.362 433.6 193.834C431.245 195.306 429.368 197.366 427.97 200.016C426.645 202.666 425.982 205.72 425.982 209.179C425.982 212.712 426.645 215.803 427.97 218.453C429.368 221.029 431.245 223.09 433.6 224.635C436.029 226.107 438.826 226.843 441.99 226.843ZM481.015 261.288V181.358H492.828L494.263 189.418C495.441 187.798 496.839 186.29 498.458 184.891C500.151 183.419 502.175 182.242 504.53 181.358C506.959 180.475 509.719 180.034 512.81 180.034C518.036 180.034 522.636 181.322 526.61 183.898C530.658 186.474 533.823 189.97 536.105 194.386C538.386 198.728 539.527 203.696 539.527 209.29C539.527 214.883 538.349 219.888 535.994 224.304C533.713 228.646 530.548 232.069 526.5 234.571C522.525 237.074 517.962 238.325 512.81 238.325C508.615 238.325 504.935 237.552 501.77 236.006C498.679 234.387 496.177 232.106 494.263 229.162V261.288H481.015ZM510.05 226.843C513.141 226.843 515.901 226.107 518.33 224.635C520.759 223.163 522.636 221.102 523.961 218.453C525.359 215.803 526.058 212.749 526.058 209.29C526.058 205.757 525.359 202.666 523.961 200.016C522.636 197.366 520.759 195.306 518.33 193.834C515.901 192.362 513.141 191.626 510.05 191.626C506.885 191.626 504.089 192.362 501.66 193.834C499.305 195.306 497.428 197.366 496.029 200.016C494.705 202.666 494.042 205.72 494.042 209.179C494.042 212.712 494.705 215.803 496.029 218.453C497.428 221.029 499.305 223.09 501.66 224.635C504.089 226.107 506.885 226.843 510.05 226.843ZM571.265 238.325C566.334 238.325 562.028 237.552 558.348 236.006C554.742 234.387 551.872 232.179 549.737 229.382C547.676 226.512 546.462 223.237 546.094 219.557H559.342C559.71 221.102 560.372 222.538 561.329 223.862C562.286 225.114 563.574 226.107 565.193 226.843C566.886 227.579 568.873 227.947 571.155 227.947C573.363 227.947 575.166 227.653 576.564 227.064C577.963 226.402 578.993 225.555 579.656 224.525C580.318 223.494 580.649 222.39 580.649 221.213C580.649 219.446 580.171 218.085 579.214 217.128C578.257 216.171 576.859 215.435 575.019 214.92C573.252 214.331 571.118 213.779 568.616 213.264C565.966 212.749 563.39 212.123 560.888 211.387C558.459 210.578 556.251 209.584 554.264 208.406C552.35 207.229 550.804 205.72 549.627 203.88C548.523 202.04 547.971 199.795 547.971 197.146C547.971 193.907 548.817 191 550.51 188.424C552.276 185.848 554.779 183.824 558.017 182.352C561.329 180.806 565.267 180.034 569.83 180.034C576.307 180.034 581.459 181.542 585.286 184.56C589.187 187.504 591.468 191.662 592.131 197.035H579.545C579.177 194.974 578.147 193.392 576.454 192.288C574.761 191.11 572.516 190.522 569.72 190.522C566.849 190.522 564.641 191.074 563.096 192.178C561.624 193.208 560.888 194.606 560.888 196.373C560.888 197.477 561.329 198.507 562.212 199.464C563.169 200.347 564.531 201.12 566.297 201.782C568.064 202.371 570.235 202.96 572.811 203.549C576.932 204.358 580.576 205.315 583.74 206.419C586.905 207.523 589.408 209.142 591.248 211.277C593.088 213.411 594.008 216.429 594.008 220.33C594.081 223.862 593.161 226.99 591.248 229.714C589.408 232.437 586.795 234.571 583.409 236.117C580.024 237.589 575.976 238.325 571.265 238.325Z" fill="#1B3139"/> </svg></div></div>
# MAGIC       <div style="font-size: 12.5pt; color: #5A6F77; margin-top: 10px; line-height: 1.5;">Go straight to something shared with you and <strong>use it as-is</strong>.</div>
# MAGIC     </div>
# MAGIC     <div style="flex: 1.4 1 0; min-width: 0; background: #FFFFFF; border-radius: 10px; padding: 16px 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06); box-sizing: border-box;">
# MAGIC       <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #FF5F46; border-radius: 10px 10px 0 0;"></div>
# MAGIC       <div style="font-size: 15pt; font-weight: 700; margin: 8px 0 4px 0;">2. Ask a question in Genie One Chat</div>
# MAGIC       <div style="font-size: 12.5pt; color: #5A6F77; margin-bottom: 12px;">Unified chat. Routes each question to the best source.</div>
# MAGIC       <div style="background: #F9F7F4; border: 2px solid #4299E0; border-radius: 10px; padding: 10px 14px; font-size: 13.5pt; font-style: italic; color: #5A6F77;">&ldquo;Top 5 franchises by sales?&rdquo;</div>
# MAGIC       <div style="text-align: center; font-size: 12pt; color: #618794; font-style: italic; margin: 8px 0 6px;">Chat routes it (you don't pick an agent) &darr;</div>
# MAGIC       <div style="background: rgba(255,95,70,0.08); border-left: 4px solid #FF5F46; border-radius: 0 8px 8px 0; padding: 10px 12px;">
# MAGIC         <div style="font-size: 11.5pt; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; color: #B83A24; margin-bottom: 8px;">Checked first: Genie Agents</div>
# MAGIC         <div style="display: flex; gap: 8px; flex-wrap: wrap;"><span style="background:#fff; border:2px solid #FF5F46; border-radius:7px; padding:5px 10px; display:inline-flex; align-items:center;"><svg style="height:26px;width:auto;display:inline-block;vertical-align:middle;flex-shrink:0;" viewBox="0 0 881 200" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M81.7909 159.789C75.0244 159.789 69.5392 166.599 69.5392 175H126.368C126.368 166.599 120.883 159.789 114.116 159.789H81.7909Z" fill="#FF5F46"/> <path d="M179.614 80.7871C167.525 100.208 149.376 126.933 141.272 133.79C133.167 140.647 121.149 153.009 93.2907 153.009C73.7741 153.009 56.9864 140.474 49.5352 122.498C49.5353 122.519 49.5356 122.54 49.5358 122.561C48.4799 119.938 45.9132 118.085 42.9121 118.085C38.969 118.085 35.7721 121.282 35.7721 125.225C35.7722 126.15 35.9484 126.997 36.2689 127.752C37.984 131.793 42.5469 131.965 42.5469 144.569C42.5469 143.103 42.5469 146.404 42.5469 144.569C30.6947 144.569 21.0865 134.96 21.0863 123.108C21.0863 111.256 30.6945 101.647 42.5469 101.647H45.4249V101.644H79.5153C82.062 101.644 84.5067 102.722 86.0978 104.71C88.8856 108.194 91.0222 111.438 92.5969 114.114C94.056 116.594 98.4255 116.618 99.8699 114.13C101.393 111.506 103.416 108.337 105.98 104.929C107.573 102.813 110.103 101.644 112.752 101.644H125.427C143.951 101.644 154.105 92.7623 159.289 86.3612C161.972 83.049 165.782 80.7871 170.045 80.7871H179.614Z" fill="#FABFBA"/> <path d="M96.3843 111.768C96.3842 87.8629 77.3194 68.4739 53.768 68.3843C77.3196 68.2949 96.3845 48.9049 96.3845 25C96.3845 25 96.3845 25 96.3845 25C96.3845 48.9602 115.538 68.3838 139.165 68.3838C115.538 68.3838 96.3844 87.8075 96.3843 111.768Z" fill="#FF5F46"/> <path d="M274.824 139.867C267.307 139.867 260.701 138.158 255.006 134.742C249.388 131.325 245.022 126.579 241.909 120.505C238.796 114.355 237.239 107.18 237.239 98.9793C237.239 90.855 238.834 83.6798 242.023 77.4537C245.212 71.1516 249.767 66.2543 255.69 62.7615C261.688 59.1929 268.787 57.4086 276.988 57.4086C286.251 57.4086 293.92 59.6485 299.994 64.1283C306.144 68.5321 310.13 74.6823 311.952 82.5788H296.577C295.438 78.6306 293.198 75.5555 289.857 73.3535C286.516 71.1516 282.189 70.0507 276.874 70.0507C271.483 70.0507 266.851 71.2276 262.979 73.5813C259.182 75.8592 256.259 79.2 254.209 83.6039C252.235 87.9318 251.248 93.0949 251.248 99.0932C251.248 105.092 252.235 110.255 254.209 114.583C256.259 118.911 259.144 122.213 262.865 124.491C266.585 126.693 270.951 127.794 275.962 127.794C283.403 127.794 289.022 125.706 292.819 121.53C296.615 117.354 298.855 111.925 299.538 105.243H278.924V94.8792H313.319V138.5H300.791L299.652 127.566C297.906 130.148 295.894 132.388 293.616 134.286C291.338 136.108 288.642 137.513 285.529 138.5C282.492 139.411 278.924 139.867 274.824 139.867ZM351.07 139.867C345.375 139.867 340.364 138.652 336.036 136.222C331.708 133.717 328.33 130.224 325.9 125.744C323.47 121.264 322.255 116.101 322.255 110.255C322.255 104.18 323.432 98.8654 325.786 94.3097C328.216 89.7541 331.594 86.1854 335.922 83.6039C340.326 81.0223 345.413 79.7315 351.184 79.7315C356.803 79.7315 361.7 80.9843 365.876 83.49C370.052 85.9956 373.279 89.3744 375.557 93.6264C377.835 97.8024 378.974 102.51 378.974 107.749C378.974 108.508 378.974 109.344 378.974 110.255C378.974 111.166 378.898 112.115 378.746 113.102H332.05V104.332H365.193C365.041 100.156 363.636 96.8913 360.979 94.5375C358.321 92.1078 355.018 90.893 351.07 90.893C348.261 90.893 345.679 91.5384 343.325 92.8291C340.972 94.1199 339.111 96.0561 337.745 98.6377C336.378 101.143 335.695 104.332 335.695 108.205V111.507C335.695 115.076 336.34 118.151 337.631 120.733C338.997 123.314 340.82 125.288 343.098 126.655C345.451 127.946 348.071 128.591 350.956 128.591C354.145 128.591 356.765 127.908 358.815 126.541C360.941 125.175 362.497 123.352 363.484 121.074H377.379C376.316 124.643 374.57 127.87 372.14 130.755C369.71 133.565 366.711 135.805 363.143 137.475C359.574 139.069 355.55 139.867 351.07 139.867ZM388.176 138.5V81.0982H400.248L401.273 90.6652C403.02 87.3243 405.525 84.6669 408.79 82.6927C412.055 80.7186 415.928 79.7315 420.407 79.7315C425.039 79.7315 428.987 80.7186 432.252 82.6927C435.517 84.5909 438.023 87.4003 439.769 91.1208C441.591 94.8412 442.503 99.4729 442.503 105.016V138.5H428.835V106.268C428.835 101.485 427.772 97.8024 425.646 95.2209C423.52 92.6393 420.369 91.3485 416.193 91.3485C413.46 91.3485 410.992 91.9939 408.79 93.2847C406.664 94.5755 404.956 96.4737 403.665 98.9793C402.45 101.409 401.843 104.37 401.843 107.863V138.5H388.176ZM454.064 138.5V81.0982H467.731V138.5H454.064ZM460.898 71.9868C458.392 71.9868 456.304 71.2275 454.634 69.709C453.039 68.1145 452.242 66.1783 452.242 63.9005C452.242 61.5467 453.039 59.6485 454.634 58.2059C456.304 56.6873 458.392 55.928 460.898 55.928C463.404 55.928 465.454 56.6873 467.048 58.2059C468.719 59.6485 469.554 61.5467 469.554 63.9005C469.554 66.1783 468.719 68.1145 467.048 69.709C465.454 71.2275 463.404 71.9868 460.898 71.9868ZM506.987 139.867C501.292 139.867 496.281 138.652 491.953 136.222C487.625 133.717 484.246 130.224 481.817 125.744C479.387 121.264 478.172 116.101 478.172 110.255C478.172 104.18 479.349 98.8654 481.703 94.3097C484.133 89.7541 487.511 86.1854 491.839 83.6039C496.243 81.0223 501.33 79.7315 507.101 79.7315C512.72 79.7315 517.617 80.9843 521.793 83.49C525.969 85.9956 529.196 89.3744 531.474 93.6264C533.752 97.8024 534.891 102.51 534.891 107.749C534.891 108.508 534.891 109.344 534.891 110.255C534.891 111.166 534.815 112.115 534.663 113.102H487.967V104.332H521.11C520.958 100.156 519.553 96.8913 516.896 94.5375C514.238 92.1078 510.935 90.893 506.987 90.893C504.178 90.893 501.596 91.5384 499.242 92.8291C496.889 94.1199 495.028 96.0561 493.662 98.6377C492.295 101.143 491.612 104.332 491.612 108.205V111.507C491.612 115.076 492.257 118.151 493.548 120.733C494.914 123.314 496.737 125.288 499.015 126.655C501.368 127.946 503.988 128.591 506.873 128.591C510.062 128.591 512.682 127.908 514.732 126.541C516.858 125.175 518.414 123.352 519.401 121.074H533.296C532.233 124.643 530.487 127.87 528.057 130.755C525.627 133.565 522.628 135.805 519.06 137.475C515.491 139.069 511.467 139.867 506.987 139.867Z" fill="#0B2026"/> <rect x="572" y="58" width="308.12" height="84" rx="42" fill="#0B2026"/> <path d="M672.51 113.74L682.313 86.9347H687.444L697.247 113.74H692.384L684.84 92.2958L677.296 113.74H672.51ZM676.875 107.422L678.1 103.784H691.312L692.537 107.422H676.875ZM715.676 114.2C713.149 114.2 710.928 113.625 709.013 112.477C707.124 111.328 705.656 109.732 704.609 107.69C703.563 105.622 703.039 103.209 703.039 100.452C703.039 97.7207 703.575 95.3082 704.648 93.2148C705.72 91.0959 707.252 89.4493 709.243 88.275C711.26 87.0751 713.647 86.4752 716.404 86.4752C719.518 86.4752 722.097 87.2283 724.139 88.7345C726.207 90.2152 727.547 92.283 728.16 94.9381H722.99C722.607 93.6105 721.854 92.5766 720.731 91.8363C719.608 91.0959 718.152 90.7258 716.365 90.7258C714.553 90.7258 712.996 91.1215 711.694 91.9129C710.417 92.6787 709.434 93.802 708.745 95.2827C708.081 96.7379 707.749 98.4738 707.749 100.491C707.749 102.507 708.081 104.243 708.745 105.699C709.434 107.154 710.404 108.264 711.655 109.03C712.906 109.77 714.374 110.141 716.059 110.141C718.561 110.141 720.45 109.439 721.727 108.034C723.003 106.63 723.756 104.805 723.986 102.558H717.055V99.0738H728.619V113.74H724.407L724.024 110.064C723.437 110.932 722.76 111.685 721.995 112.323C721.229 112.936 720.322 113.408 719.276 113.74C718.255 114.047 717.055 114.2 715.676 114.2ZM738.172 113.74V86.9347H755.481V90.6492H742.767V98.3462H754.332V101.984H742.767V110.026H755.481V113.74H738.172ZM764.906 113.74V86.9347H769.501L782.406 106.311V86.9347H787.001V113.74H782.406L769.501 94.4019V113.74H764.906ZM803.229 113.74V90.6492H795.341V86.9347H815.675V90.6492H807.786V113.74H803.229ZM832.683 114.2C830.742 114.2 829.019 113.855 827.513 113.166C826.007 112.477 824.832 111.494 823.99 110.217C823.148 108.941 822.714 107.422 822.688 105.66H827.551C827.551 106.554 827.756 107.358 828.164 108.073C828.598 108.762 829.185 109.311 829.925 109.719C830.691 110.128 831.61 110.332 832.683 110.332C833.602 110.332 834.393 110.192 835.057 109.911C835.746 109.605 836.269 109.183 836.627 108.647C837.01 108.086 837.201 107.435 837.201 106.694C837.201 105.852 836.997 105.162 836.589 104.626C836.206 104.065 835.67 103.592 834.98 103.209C834.291 102.827 833.5 102.495 832.606 102.214C831.713 101.907 830.768 101.588 829.772 101.257C827.653 100.542 826.058 99.6354 824.986 98.5377C823.913 97.4144 823.377 95.9209 823.377 94.0573C823.377 92.5 823.747 91.1597 824.488 90.0365C825.228 88.9132 826.262 88.0452 827.59 87.4325C828.943 86.7943 830.5 86.4752 832.261 86.4752C834.048 86.4752 835.606 86.7943 836.933 87.4325C838.286 88.0707 839.346 88.9642 840.112 90.1131C840.903 91.2363 841.311 92.5894 841.337 94.1722H836.435C836.41 93.5084 836.231 92.8957 835.899 92.3341C835.567 91.7469 835.082 91.2746 834.444 90.9172C833.831 90.5343 833.078 90.3428 832.185 90.3428C831.419 90.3173 830.73 90.4449 830.117 90.7258C829.53 90.981 829.058 91.364 828.7 91.8746C828.368 92.3596 828.202 92.9723 828.202 93.7127C828.202 94.4275 828.355 95.0274 828.662 95.5125C828.994 95.972 829.466 96.3677 830.079 96.6996C830.691 97.0059 831.406 97.2995 832.223 97.5803C833.04 97.8611 833.934 98.1675 834.904 98.4994C836.231 98.9334 837.431 99.4695 838.503 100.108C839.601 100.72 840.469 101.525 841.107 102.52C841.745 103.516 842.065 104.805 842.065 106.388C842.065 107.766 841.707 109.056 840.992 110.256C840.278 111.43 839.231 112.387 837.852 113.128C836.474 113.842 834.75 114.2 832.683 114.2Z" fill="white"/> <path d="M632.893 74.0239C632.893 74.0239 632.893 74.02 632.893 74.0221L634.136 80.6146C635.485 87.7644 641.078 93.3568 648.228 94.7065L654.82 95.9495C654.82 97.6494 654.82 102.901 654.82 102.901L648.228 104.144C641.078 105.494 635.485 111.086 634.136 118.236L632.893 124.829C631.193 124.829 625.941 124.829 625.941 124.829L624.698 118.236C623.348 111.086 617.756 105.494 610.606 104.144L604.014 102.901C604.014 102.901 604.015 97.6494 604.015 95.9495H604.014L610.606 94.7065C617.756 93.3568 623.348 87.7644 624.698 80.6146L625.941 74.0221C625.941 74.0221 631.193 74.0239 632.893 74.0239Z" fill="#FF3621"/> </svg></span><span style="background:#fff; border:2px solid #FF5F46; border-radius:7px; padding:5px 10px; display:inline-flex; align-items:center;"><svg style="height:26px;width:auto;display:inline-block;vertical-align:middle;flex-shrink:0;" viewBox="0 0 881 200" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M81.7909 159.789C75.0244 159.789 69.5392 166.599 69.5392 175H126.368C126.368 166.599 120.883 159.789 114.116 159.789H81.7909Z" fill="#FF5F46"/> <path d="M179.614 80.7871C167.525 100.208 149.376 126.933 141.272 133.79C133.167 140.647 121.149 153.009 93.2907 153.009C73.7741 153.009 56.9864 140.474 49.5352 122.498C49.5353 122.519 49.5356 122.54 49.5358 122.561C48.4799 119.938 45.9132 118.085 42.9121 118.085C38.969 118.085 35.7721 121.282 35.7721 125.225C35.7722 126.15 35.9484 126.997 36.2689 127.752C37.984 131.793 42.5469 131.965 42.5469 144.569C42.5469 143.103 42.5469 146.404 42.5469 144.569C30.6947 144.569 21.0865 134.96 21.0863 123.108C21.0863 111.256 30.6945 101.647 42.5469 101.647H45.4249V101.644H79.5153C82.062 101.644 84.5067 102.722 86.0978 104.71C88.8856 108.194 91.0222 111.438 92.5969 114.114C94.056 116.594 98.4255 116.618 99.8699 114.13C101.393 111.506 103.416 108.337 105.98 104.929C107.573 102.813 110.103 101.644 112.752 101.644H125.427C143.951 101.644 154.105 92.7623 159.289 86.3612C161.972 83.049 165.782 80.7871 170.045 80.7871H179.614Z" fill="#FABFBA"/> <path d="M96.3843 111.768C96.3842 87.8629 77.3194 68.4739 53.768 68.3843C77.3196 68.2949 96.3845 48.9049 96.3845 25C96.3845 25 96.3845 25 96.3845 25C96.3845 48.9602 115.538 68.3838 139.165 68.3838C115.538 68.3838 96.3844 87.8075 96.3843 111.768Z" fill="#FF5F46"/> <path d="M274.824 139.867C267.307 139.867 260.701 138.158 255.006 134.742C249.388 131.325 245.022 126.579 241.909 120.505C238.796 114.355 237.239 107.18 237.239 98.9793C237.239 90.855 238.834 83.6798 242.023 77.4537C245.212 71.1516 249.767 66.2543 255.69 62.7615C261.688 59.1929 268.787 57.4086 276.988 57.4086C286.251 57.4086 293.92 59.6485 299.994 64.1283C306.144 68.5321 310.13 74.6823 311.952 82.5788H296.577C295.438 78.6306 293.198 75.5555 289.857 73.3535C286.516 71.1516 282.189 70.0507 276.874 70.0507C271.483 70.0507 266.851 71.2276 262.979 73.5813C259.182 75.8592 256.259 79.2 254.209 83.6039C252.235 87.9318 251.248 93.0949 251.248 99.0932C251.248 105.092 252.235 110.255 254.209 114.583C256.259 118.911 259.144 122.213 262.865 124.491C266.585 126.693 270.951 127.794 275.962 127.794C283.403 127.794 289.022 125.706 292.819 121.53C296.615 117.354 298.855 111.925 299.538 105.243H278.924V94.8792H313.319V138.5H300.791L299.652 127.566C297.906 130.148 295.894 132.388 293.616 134.286C291.338 136.108 288.642 137.513 285.529 138.5C282.492 139.411 278.924 139.867 274.824 139.867ZM351.07 139.867C345.375 139.867 340.364 138.652 336.036 136.222C331.708 133.717 328.33 130.224 325.9 125.744C323.47 121.264 322.255 116.101 322.255 110.255C322.255 104.18 323.432 98.8654 325.786 94.3097C328.216 89.7541 331.594 86.1854 335.922 83.6039C340.326 81.0223 345.413 79.7315 351.184 79.7315C356.803 79.7315 361.7 80.9843 365.876 83.49C370.052 85.9956 373.279 89.3744 375.557 93.6264C377.835 97.8024 378.974 102.51 378.974 107.749C378.974 108.508 378.974 109.344 378.974 110.255C378.974 111.166 378.898 112.115 378.746 113.102H332.05V104.332H365.193C365.041 100.156 363.636 96.8913 360.979 94.5375C358.321 92.1078 355.018 90.893 351.07 90.893C348.261 90.893 345.679 91.5384 343.325 92.8291C340.972 94.1199 339.111 96.0561 337.745 98.6377C336.378 101.143 335.695 104.332 335.695 108.205V111.507C335.695 115.076 336.34 118.151 337.631 120.733C338.997 123.314 340.82 125.288 343.098 126.655C345.451 127.946 348.071 128.591 350.956 128.591C354.145 128.591 356.765 127.908 358.815 126.541C360.941 125.175 362.497 123.352 363.484 121.074H377.379C376.316 124.643 374.57 127.87 372.14 130.755C369.71 133.565 366.711 135.805 363.143 137.475C359.574 139.069 355.55 139.867 351.07 139.867ZM388.176 138.5V81.0982H400.248L401.273 90.6652C403.02 87.3243 405.525 84.6669 408.79 82.6927C412.055 80.7186 415.928 79.7315 420.407 79.7315C425.039 79.7315 428.987 80.7186 432.252 82.6927C435.517 84.5909 438.023 87.4003 439.769 91.1208C441.591 94.8412 442.503 99.4729 442.503 105.016V138.5H428.835V106.268C428.835 101.485 427.772 97.8024 425.646 95.2209C423.52 92.6393 420.369 91.3485 416.193 91.3485C413.46 91.3485 410.992 91.9939 408.79 93.2847C406.664 94.5755 404.956 96.4737 403.665 98.9793C402.45 101.409 401.843 104.37 401.843 107.863V138.5H388.176ZM454.064 138.5V81.0982H467.731V138.5H454.064ZM460.898 71.9868C458.392 71.9868 456.304 71.2275 454.634 69.709C453.039 68.1145 452.242 66.1783 452.242 63.9005C452.242 61.5467 453.039 59.6485 454.634 58.2059C456.304 56.6873 458.392 55.928 460.898 55.928C463.404 55.928 465.454 56.6873 467.048 58.2059C468.719 59.6485 469.554 61.5467 469.554 63.9005C469.554 66.1783 468.719 68.1145 467.048 69.709C465.454 71.2275 463.404 71.9868 460.898 71.9868ZM506.987 139.867C501.292 139.867 496.281 138.652 491.953 136.222C487.625 133.717 484.246 130.224 481.817 125.744C479.387 121.264 478.172 116.101 478.172 110.255C478.172 104.18 479.349 98.8654 481.703 94.3097C484.133 89.7541 487.511 86.1854 491.839 83.6039C496.243 81.0223 501.33 79.7315 507.101 79.7315C512.72 79.7315 517.617 80.9843 521.793 83.49C525.969 85.9956 529.196 89.3744 531.474 93.6264C533.752 97.8024 534.891 102.51 534.891 107.749C534.891 108.508 534.891 109.344 534.891 110.255C534.891 111.166 534.815 112.115 534.663 113.102H487.967V104.332H521.11C520.958 100.156 519.553 96.8913 516.896 94.5375C514.238 92.1078 510.935 90.893 506.987 90.893C504.178 90.893 501.596 91.5384 499.242 92.8291C496.889 94.1199 495.028 96.0561 493.662 98.6377C492.295 101.143 491.612 104.332 491.612 108.205V111.507C491.612 115.076 492.257 118.151 493.548 120.733C494.914 123.314 496.737 125.288 499.015 126.655C501.368 127.946 503.988 128.591 506.873 128.591C510.062 128.591 512.682 127.908 514.732 126.541C516.858 125.175 518.414 123.352 519.401 121.074H533.296C532.233 124.643 530.487 127.87 528.057 130.755C525.627 133.565 522.628 135.805 519.06 137.475C515.491 139.069 511.467 139.867 506.987 139.867Z" fill="#0B2026"/> <rect x="572" y="58" width="308.12" height="84" rx="42" fill="#0B2026"/> <path d="M672.51 113.74L682.313 86.9347H687.444L697.247 113.74H692.384L684.84 92.2958L677.296 113.74H672.51ZM676.875 107.422L678.1 103.784H691.312L692.537 107.422H676.875ZM715.676 114.2C713.149 114.2 710.928 113.625 709.013 112.477C707.124 111.328 705.656 109.732 704.609 107.69C703.563 105.622 703.039 103.209 703.039 100.452C703.039 97.7207 703.575 95.3082 704.648 93.2148C705.72 91.0959 707.252 89.4493 709.243 88.275C711.26 87.0751 713.647 86.4752 716.404 86.4752C719.518 86.4752 722.097 87.2283 724.139 88.7345C726.207 90.2152 727.547 92.283 728.16 94.9381H722.99C722.607 93.6105 721.854 92.5766 720.731 91.8363C719.608 91.0959 718.152 90.7258 716.365 90.7258C714.553 90.7258 712.996 91.1215 711.694 91.9129C710.417 92.6787 709.434 93.802 708.745 95.2827C708.081 96.7379 707.749 98.4738 707.749 100.491C707.749 102.507 708.081 104.243 708.745 105.699C709.434 107.154 710.404 108.264 711.655 109.03C712.906 109.77 714.374 110.141 716.059 110.141C718.561 110.141 720.45 109.439 721.727 108.034C723.003 106.63 723.756 104.805 723.986 102.558H717.055V99.0738H728.619V113.74H724.407L724.024 110.064C723.437 110.932 722.76 111.685 721.995 112.323C721.229 112.936 720.322 113.408 719.276 113.74C718.255 114.047 717.055 114.2 715.676 114.2ZM738.172 113.74V86.9347H755.481V90.6492H742.767V98.3462H754.332V101.984H742.767V110.026H755.481V113.74H738.172ZM764.906 113.74V86.9347H769.501L782.406 106.311V86.9347H787.001V113.74H782.406L769.501 94.4019V113.74H764.906ZM803.229 113.74V90.6492H795.341V86.9347H815.675V90.6492H807.786V113.74H803.229ZM832.683 114.2C830.742 114.2 829.019 113.855 827.513 113.166C826.007 112.477 824.832 111.494 823.99 110.217C823.148 108.941 822.714 107.422 822.688 105.66H827.551C827.551 106.554 827.756 107.358 828.164 108.073C828.598 108.762 829.185 109.311 829.925 109.719C830.691 110.128 831.61 110.332 832.683 110.332C833.602 110.332 834.393 110.192 835.057 109.911C835.746 109.605 836.269 109.183 836.627 108.647C837.01 108.086 837.201 107.435 837.201 106.694C837.201 105.852 836.997 105.162 836.589 104.626C836.206 104.065 835.67 103.592 834.98 103.209C834.291 102.827 833.5 102.495 832.606 102.214C831.713 101.907 830.768 101.588 829.772 101.257C827.653 100.542 826.058 99.6354 824.986 98.5377C823.913 97.4144 823.377 95.9209 823.377 94.0573C823.377 92.5 823.747 91.1597 824.488 90.0365C825.228 88.9132 826.262 88.0452 827.59 87.4325C828.943 86.7943 830.5 86.4752 832.261 86.4752C834.048 86.4752 835.606 86.7943 836.933 87.4325C838.286 88.0707 839.346 88.9642 840.112 90.1131C840.903 91.2363 841.311 92.5894 841.337 94.1722H836.435C836.41 93.5084 836.231 92.8957 835.899 92.3341C835.567 91.7469 835.082 91.2746 834.444 90.9172C833.831 90.5343 833.078 90.3428 832.185 90.3428C831.419 90.3173 830.73 90.4449 830.117 90.7258C829.53 90.981 829.058 91.364 828.7 91.8746C828.368 92.3596 828.202 92.9723 828.202 93.7127C828.202 94.4275 828.355 95.0274 828.662 95.5125C828.994 95.972 829.466 96.3677 830.079 96.6996C830.691 97.0059 831.406 97.2995 832.223 97.5803C833.04 97.8611 833.934 98.1675 834.904 98.4994C836.231 98.9334 837.431 99.4695 838.503 100.108C839.601 100.72 840.469 101.525 841.107 102.52C841.745 103.516 842.065 104.805 842.065 106.388C842.065 107.766 841.707 109.056 840.992 110.256C840.278 111.43 839.231 112.387 837.852 113.128C836.474 113.842 834.75 114.2 832.683 114.2Z" fill="white"/> <path d="M632.893 74.0239C632.893 74.0239 632.893 74.02 632.893 74.0221L634.136 80.6146C635.485 87.7644 641.078 93.3568 648.228 94.7065L654.82 95.9495C654.82 97.6494 654.82 102.901 654.82 102.901L648.228 104.144C641.078 105.494 635.485 111.086 634.136 118.236L632.893 124.829C631.193 124.829 625.941 124.829 625.941 124.829L624.698 118.236C623.348 111.086 617.756 105.494 610.606 104.144L604.014 102.901C604.014 102.901 604.015 97.6494 604.015 95.9495H604.014L610.606 94.7065C617.756 93.3568 623.348 87.7644 624.698 80.6146L625.941 74.0221C625.941 74.0221 631.193 74.0239 632.893 74.0239Z" fill="#FF3621"/> </svg></span><span style="background:#fff; border:2px solid #FF5F46; border-radius:7px; padding:5px 10px; display:inline-flex; align-items:center;"><svg style="height:26px;width:auto;display:inline-block;vertical-align:middle;flex-shrink:0;" viewBox="0 0 881 200" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M81.7909 159.789C75.0244 159.789 69.5392 166.599 69.5392 175H126.368C126.368 166.599 120.883 159.789 114.116 159.789H81.7909Z" fill="#FF5F46"/> <path d="M179.614 80.7871C167.525 100.208 149.376 126.933 141.272 133.79C133.167 140.647 121.149 153.009 93.2907 153.009C73.7741 153.009 56.9864 140.474 49.5352 122.498C49.5353 122.519 49.5356 122.54 49.5358 122.561C48.4799 119.938 45.9132 118.085 42.9121 118.085C38.969 118.085 35.7721 121.282 35.7721 125.225C35.7722 126.15 35.9484 126.997 36.2689 127.752C37.984 131.793 42.5469 131.965 42.5469 144.569C42.5469 143.103 42.5469 146.404 42.5469 144.569C30.6947 144.569 21.0865 134.96 21.0863 123.108C21.0863 111.256 30.6945 101.647 42.5469 101.647H45.4249V101.644H79.5153C82.062 101.644 84.5067 102.722 86.0978 104.71C88.8856 108.194 91.0222 111.438 92.5969 114.114C94.056 116.594 98.4255 116.618 99.8699 114.13C101.393 111.506 103.416 108.337 105.98 104.929C107.573 102.813 110.103 101.644 112.752 101.644H125.427C143.951 101.644 154.105 92.7623 159.289 86.3612C161.972 83.049 165.782 80.7871 170.045 80.7871H179.614Z" fill="#FABFBA"/> <path d="M96.3843 111.768C96.3842 87.8629 77.3194 68.4739 53.768 68.3843C77.3196 68.2949 96.3845 48.9049 96.3845 25C96.3845 25 96.3845 25 96.3845 25C96.3845 48.9602 115.538 68.3838 139.165 68.3838C115.538 68.3838 96.3844 87.8075 96.3843 111.768Z" fill="#FF5F46"/> <path d="M274.824 139.867C267.307 139.867 260.701 138.158 255.006 134.742C249.388 131.325 245.022 126.579 241.909 120.505C238.796 114.355 237.239 107.18 237.239 98.9793C237.239 90.855 238.834 83.6798 242.023 77.4537C245.212 71.1516 249.767 66.2543 255.69 62.7615C261.688 59.1929 268.787 57.4086 276.988 57.4086C286.251 57.4086 293.92 59.6485 299.994 64.1283C306.144 68.5321 310.13 74.6823 311.952 82.5788H296.577C295.438 78.6306 293.198 75.5555 289.857 73.3535C286.516 71.1516 282.189 70.0507 276.874 70.0507C271.483 70.0507 266.851 71.2276 262.979 73.5813C259.182 75.8592 256.259 79.2 254.209 83.6039C252.235 87.9318 251.248 93.0949 251.248 99.0932C251.248 105.092 252.235 110.255 254.209 114.583C256.259 118.911 259.144 122.213 262.865 124.491C266.585 126.693 270.951 127.794 275.962 127.794C283.403 127.794 289.022 125.706 292.819 121.53C296.615 117.354 298.855 111.925 299.538 105.243H278.924V94.8792H313.319V138.5H300.791L299.652 127.566C297.906 130.148 295.894 132.388 293.616 134.286C291.338 136.108 288.642 137.513 285.529 138.5C282.492 139.411 278.924 139.867 274.824 139.867ZM351.07 139.867C345.375 139.867 340.364 138.652 336.036 136.222C331.708 133.717 328.33 130.224 325.9 125.744C323.47 121.264 322.255 116.101 322.255 110.255C322.255 104.18 323.432 98.8654 325.786 94.3097C328.216 89.7541 331.594 86.1854 335.922 83.6039C340.326 81.0223 345.413 79.7315 351.184 79.7315C356.803 79.7315 361.7 80.9843 365.876 83.49C370.052 85.9956 373.279 89.3744 375.557 93.6264C377.835 97.8024 378.974 102.51 378.974 107.749C378.974 108.508 378.974 109.344 378.974 110.255C378.974 111.166 378.898 112.115 378.746 113.102H332.05V104.332H365.193C365.041 100.156 363.636 96.8913 360.979 94.5375C358.321 92.1078 355.018 90.893 351.07 90.893C348.261 90.893 345.679 91.5384 343.325 92.8291C340.972 94.1199 339.111 96.0561 337.745 98.6377C336.378 101.143 335.695 104.332 335.695 108.205V111.507C335.695 115.076 336.34 118.151 337.631 120.733C338.997 123.314 340.82 125.288 343.098 126.655C345.451 127.946 348.071 128.591 350.956 128.591C354.145 128.591 356.765 127.908 358.815 126.541C360.941 125.175 362.497 123.352 363.484 121.074H377.379C376.316 124.643 374.57 127.87 372.14 130.755C369.71 133.565 366.711 135.805 363.143 137.475C359.574 139.069 355.55 139.867 351.07 139.867ZM388.176 138.5V81.0982H400.248L401.273 90.6652C403.02 87.3243 405.525 84.6669 408.79 82.6927C412.055 80.7186 415.928 79.7315 420.407 79.7315C425.039 79.7315 428.987 80.7186 432.252 82.6927C435.517 84.5909 438.023 87.4003 439.769 91.1208C441.591 94.8412 442.503 99.4729 442.503 105.016V138.5H428.835V106.268C428.835 101.485 427.772 97.8024 425.646 95.2209C423.52 92.6393 420.369 91.3485 416.193 91.3485C413.46 91.3485 410.992 91.9939 408.79 93.2847C406.664 94.5755 404.956 96.4737 403.665 98.9793C402.45 101.409 401.843 104.37 401.843 107.863V138.5H388.176ZM454.064 138.5V81.0982H467.731V138.5H454.064ZM460.898 71.9868C458.392 71.9868 456.304 71.2275 454.634 69.709C453.039 68.1145 452.242 66.1783 452.242 63.9005C452.242 61.5467 453.039 59.6485 454.634 58.2059C456.304 56.6873 458.392 55.928 460.898 55.928C463.404 55.928 465.454 56.6873 467.048 58.2059C468.719 59.6485 469.554 61.5467 469.554 63.9005C469.554 66.1783 468.719 68.1145 467.048 69.709C465.454 71.2275 463.404 71.9868 460.898 71.9868ZM506.987 139.867C501.292 139.867 496.281 138.652 491.953 136.222C487.625 133.717 484.246 130.224 481.817 125.744C479.387 121.264 478.172 116.101 478.172 110.255C478.172 104.18 479.349 98.8654 481.703 94.3097C484.133 89.7541 487.511 86.1854 491.839 83.6039C496.243 81.0223 501.33 79.7315 507.101 79.7315C512.72 79.7315 517.617 80.9843 521.793 83.49C525.969 85.9956 529.196 89.3744 531.474 93.6264C533.752 97.8024 534.891 102.51 534.891 107.749C534.891 108.508 534.891 109.344 534.891 110.255C534.891 111.166 534.815 112.115 534.663 113.102H487.967V104.332H521.11C520.958 100.156 519.553 96.8913 516.896 94.5375C514.238 92.1078 510.935 90.893 506.987 90.893C504.178 90.893 501.596 91.5384 499.242 92.8291C496.889 94.1199 495.028 96.0561 493.662 98.6377C492.295 101.143 491.612 104.332 491.612 108.205V111.507C491.612 115.076 492.257 118.151 493.548 120.733C494.914 123.314 496.737 125.288 499.015 126.655C501.368 127.946 503.988 128.591 506.873 128.591C510.062 128.591 512.682 127.908 514.732 126.541C516.858 125.175 518.414 123.352 519.401 121.074H533.296C532.233 124.643 530.487 127.87 528.057 130.755C525.627 133.565 522.628 135.805 519.06 137.475C515.491 139.069 511.467 139.867 506.987 139.867Z" fill="#0B2026"/> <rect x="572" y="58" width="308.12" height="84" rx="42" fill="#0B2026"/> <path d="M672.51 113.74L682.313 86.9347H687.444L697.247 113.74H692.384L684.84 92.2958L677.296 113.74H672.51ZM676.875 107.422L678.1 103.784H691.312L692.537 107.422H676.875ZM715.676 114.2C713.149 114.2 710.928 113.625 709.013 112.477C707.124 111.328 705.656 109.732 704.609 107.69C703.563 105.622 703.039 103.209 703.039 100.452C703.039 97.7207 703.575 95.3082 704.648 93.2148C705.72 91.0959 707.252 89.4493 709.243 88.275C711.26 87.0751 713.647 86.4752 716.404 86.4752C719.518 86.4752 722.097 87.2283 724.139 88.7345C726.207 90.2152 727.547 92.283 728.16 94.9381H722.99C722.607 93.6105 721.854 92.5766 720.731 91.8363C719.608 91.0959 718.152 90.7258 716.365 90.7258C714.553 90.7258 712.996 91.1215 711.694 91.9129C710.417 92.6787 709.434 93.802 708.745 95.2827C708.081 96.7379 707.749 98.4738 707.749 100.491C707.749 102.507 708.081 104.243 708.745 105.699C709.434 107.154 710.404 108.264 711.655 109.03C712.906 109.77 714.374 110.141 716.059 110.141C718.561 110.141 720.45 109.439 721.727 108.034C723.003 106.63 723.756 104.805 723.986 102.558H717.055V99.0738H728.619V113.74H724.407L724.024 110.064C723.437 110.932 722.76 111.685 721.995 112.323C721.229 112.936 720.322 113.408 719.276 113.74C718.255 114.047 717.055 114.2 715.676 114.2ZM738.172 113.74V86.9347H755.481V90.6492H742.767V98.3462H754.332V101.984H742.767V110.026H755.481V113.74H738.172ZM764.906 113.74V86.9347H769.501L782.406 106.311V86.9347H787.001V113.74H782.406L769.501 94.4019V113.74H764.906ZM803.229 113.74V90.6492H795.341V86.9347H815.675V90.6492H807.786V113.74H803.229ZM832.683 114.2C830.742 114.2 829.019 113.855 827.513 113.166C826.007 112.477 824.832 111.494 823.99 110.217C823.148 108.941 822.714 107.422 822.688 105.66H827.551C827.551 106.554 827.756 107.358 828.164 108.073C828.598 108.762 829.185 109.311 829.925 109.719C830.691 110.128 831.61 110.332 832.683 110.332C833.602 110.332 834.393 110.192 835.057 109.911C835.746 109.605 836.269 109.183 836.627 108.647C837.01 108.086 837.201 107.435 837.201 106.694C837.201 105.852 836.997 105.162 836.589 104.626C836.206 104.065 835.67 103.592 834.98 103.209C834.291 102.827 833.5 102.495 832.606 102.214C831.713 101.907 830.768 101.588 829.772 101.257C827.653 100.542 826.058 99.6354 824.986 98.5377C823.913 97.4144 823.377 95.9209 823.377 94.0573C823.377 92.5 823.747 91.1597 824.488 90.0365C825.228 88.9132 826.262 88.0452 827.59 87.4325C828.943 86.7943 830.5 86.4752 832.261 86.4752C834.048 86.4752 835.606 86.7943 836.933 87.4325C838.286 88.0707 839.346 88.9642 840.112 90.1131C840.903 91.2363 841.311 92.5894 841.337 94.1722H836.435C836.41 93.5084 836.231 92.8957 835.899 92.3341C835.567 91.7469 835.082 91.2746 834.444 90.9172C833.831 90.5343 833.078 90.3428 832.185 90.3428C831.419 90.3173 830.73 90.4449 830.117 90.7258C829.53 90.981 829.058 91.364 828.7 91.8746C828.368 92.3596 828.202 92.9723 828.202 93.7127C828.202 94.4275 828.355 95.0274 828.662 95.5125C828.994 95.972 829.466 96.3677 830.079 96.6996C830.691 97.0059 831.406 97.2995 832.223 97.5803C833.04 97.8611 833.934 98.1675 834.904 98.4994C836.231 98.9334 837.431 99.4695 838.503 100.108C839.601 100.72 840.469 101.525 841.107 102.52C841.745 103.516 842.065 104.805 842.065 106.388C842.065 107.766 841.707 109.056 840.992 110.256C840.278 111.43 839.231 112.387 837.852 113.128C836.474 113.842 834.75 114.2 832.683 114.2Z" fill="white"/> <path d="M632.893 74.0239C632.893 74.0239 632.893 74.02 632.893 74.0221L634.136 80.6146C635.485 87.7644 641.078 93.3568 648.228 94.7065L654.82 95.9495C654.82 97.6494 654.82 102.901 654.82 102.901L648.228 104.144C641.078 105.494 635.485 111.086 634.136 118.236L632.893 124.829C631.193 124.829 625.941 124.829 625.941 124.829L624.698 118.236C623.348 111.086 617.756 105.494 610.606 104.144L604.014 102.901C604.014 102.901 604.015 97.6494 604.015 95.9495H604.014L610.606 94.7065C617.756 93.3568 623.348 87.7644 624.698 80.6146L625.941 74.0221C625.941 74.0221 631.193 74.0239 632.893 74.0239Z" fill="#FF3621"/> </svg></span></div>
# MAGIC         <div style="font-size: 12pt; color: #5A6F77; margin-top: 8px; line-height: 1.5;">If one matches, Genie uses that agent's datasets, instructions, and Knowledge Store.</div>
# MAGIC       </div>
# MAGIC       <div style="text-align: center; font-size: 12pt; color: #618794; font-style: italic; margin: 6px 0;">if none match &darr;</div>
# MAGIC       <div style="background: rgba(97,135,148,0.10); border-left: 4px solid #618794; border-radius: 0 8px 8px 0; padding: 10px 12px;">
# MAGIC         <div style="font-size: 11.5pt; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; color: #1B5162; margin-bottom: 6px;">Falls back to</div>
# MAGIC         <div style="font-size: 13pt; font-weight: 700;">Dashboards &middot; Queries &middot; Metric Views</div>
# MAGIC       </div>
# MAGIC       <div style="font-size: 12pt; color: #5A6F77; margin-top: 10px; line-height: 1.5; display: flex; align-items: center; gap: 8px;"><svg style="height:24px;width:auto;display:inline-block;vertical-align:middle;flex-shrink:0;" viewBox="0 0 1014 200" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M81.7911 159.789C75.0247 159.789 69.5394 166.599 69.5394 175H126.368C126.368 166.599 120.883 159.789 114.116 159.789H81.7911Z" fill="#FF5F46"/> <path d="M179.614 80.7871C167.525 100.208 149.375 126.933 141.271 133.79C133.167 140.647 121.149 153.009 93.2904 153.009C73.7738 153.009 56.986 140.474 49.5348 122.498C49.535 122.519 49.5353 122.54 49.5355 122.561C48.4796 119.938 45.9128 118.085 42.9117 118.085C38.9686 118.085 35.7718 121.282 35.7718 125.225C35.7719 126.15 35.948 126.997 36.2686 127.752C37.9837 131.793 42.5465 131.965 42.5465 144.569C42.5466 143.103 42.5465 146.404 42.5465 144.569C30.6943 144.569 21.0862 134.96 21.0859 123.108C21.0859 111.256 30.6942 101.647 42.5465 101.647H45.4246V101.644H79.515C82.0617 101.644 84.5063 102.722 86.0974 104.71C88.8852 108.194 91.0218 111.438 92.5966 114.114C94.0556 116.594 98.4251 116.618 99.8695 114.13C101.393 111.506 103.415 108.337 105.98 104.929C107.572 102.813 110.103 101.644 112.751 101.644H125.427C143.951 101.644 154.104 92.7623 159.289 86.3612C161.972 83.049 165.782 80.7871 170.045 80.7871H179.614Z" fill="#FABFBA"/> <path d="M94.9395 25C102.306 25 108.277 30.9717 108.277 38.3379C108.277 39.8523 108.024 41.3073 107.559 42.6641L122.083 50.9297C123.011 49.8819 124.121 48.9631 125.4 48.2246C131.78 44.5416 139.937 46.7274 143.62 53.1064C147.303 59.4858 145.118 67.6431 138.738 71.3262C132.359 75.0093 124.202 72.8237 120.519 66.4443C118.585 63.0954 118.269 59.2564 119.328 55.832L104.65 47.4785C102.812 49.4307 100.393 50.829 97.668 51.3955V65.0605C99.8593 65.341 102.033 66.0509 104.065 67.2246C112.278 71.966 115.092 82.4674 110.351 90.6797C105.609 98.8919 95.1078 101.705 86.8955 96.9639C79.5979 92.7505 76.5631 83.9891 79.3047 76.3271L61.9561 66.2676C59.2266 68.5054 55.2912 68.9472 52.0537 67.0781C47.8779 64.6672 46.4467 59.3273 48.8574 55.1514C51.2683 50.9756 56.6083 49.5445 60.7842 51.9551C64.1935 53.9234 65.7716 57.8437 64.9248 61.4893L82.0361 71.4111C84.6022 68.1737 88.1807 66.0631 92.0449 65.2725V51.3594C86.0706 50.0373 81.6017 44.71 81.6016 38.3379C81.6016 30.9717 87.5732 25 94.9395 25Z" fill="#FF5F46"/> <path d="M273.51 138.825C266.224 138.825 259.821 137.169 254.301 133.857C248.854 130.545 244.622 125.945 241.605 120.057C238.587 114.095 237.078 107.14 237.078 99.1912C237.078 91.316 238.624 84.3608 241.715 78.3256C244.806 72.2168 249.222 67.4696 254.963 64.084C260.778 60.6248 267.659 58.8952 275.608 58.8952C284.587 58.8952 292.021 61.0664 297.909 65.4088C303.87 69.6776 307.734 75.6392 309.501 83.2936H294.597C293.493 79.4664 291.322 76.4856 288.083 74.3512C284.845 72.2168 280.65 71.1496 275.498 71.1496C270.272 71.1496 265.782 72.2904 262.029 74.572C258.349 76.78 255.515 80.0184 253.528 84.2872C251.614 88.4824 250.658 93.4872 250.658 99.3016C250.658 105.116 251.614 110.121 253.528 114.316C255.515 118.511 258.312 121.713 261.918 123.921C265.525 126.055 269.757 127.122 274.614 127.122C281.827 127.122 287.274 125.098 290.954 121.05C294.634 117.002 296.805 111.74 297.467 105.263H277.485V95.2168H310.826V137.5H298.682L297.578 126.902C295.885 129.404 293.934 131.575 291.726 133.415C289.518 135.182 286.906 136.543 283.888 137.5C280.944 138.383 277.485 138.825 273.51 138.825ZM347.419 138.825C341.899 138.825 337.041 137.647 332.846 135.292C328.651 132.863 325.376 129.478 323.02 125.135C320.665 120.793 319.488 115.788 319.488 110.121C319.488 104.233 320.628 99.0808 322.91 94.6648C325.265 90.2488 328.54 86.7896 332.736 84.2872C337.004 81.7848 341.936 80.5336 347.529 80.5336C352.976 80.5336 357.723 81.748 361.771 84.1768C365.819 86.6056 368.947 89.8808 371.155 94.0024C373.363 98.0504 374.467 102.614 374.467 107.692C374.467 108.428 374.467 109.238 374.467 110.121C374.467 111.004 374.393 111.924 374.246 112.881H328.982V104.38H361.108C360.961 100.332 359.6 97.1672 357.024 94.8856C354.448 92.5304 351.246 91.3528 347.419 91.3528C344.696 91.3528 342.193 91.9784 339.912 93.2296C337.63 94.4808 335.827 96.3576 334.502 98.86C333.177 101.289 332.515 104.38 332.515 108.134V111.335C332.515 114.794 333.14 117.775 334.392 120.278C335.716 122.78 337.483 124.694 339.691 126.018C341.972 127.27 344.512 127.895 347.308 127.895C350.4 127.895 352.939 127.233 354.926 125.908C356.987 124.583 358.496 122.817 359.452 120.609H372.921C371.891 124.068 370.198 127.196 367.843 129.993C365.488 132.716 362.58 134.887 359.121 136.506C355.662 138.052 351.761 138.825 347.419 138.825ZM383.387 137.5V81.8584H395.089L396.083 91.132C397.776 87.8936 400.204 85.3176 403.369 83.404C406.534 81.4904 410.288 80.5336 414.63 80.5336C419.12 80.5336 422.947 81.4904 426.112 83.404C429.276 85.244 431.705 87.9672 433.398 91.5736C435.164 95.18 436.048 99.6696 436.048 105.042V137.5H422.8V106.257C422.8 101.62 421.769 98.0504 419.708 95.548C417.648 93.0456 414.593 91.7944 410.545 91.7944C407.896 91.7944 405.504 92.42 403.369 93.6712C401.308 94.9224 399.652 96.7624 398.401 99.1912C397.224 101.546 396.635 104.417 396.635 107.802V137.5H383.387ZM447.255 137.5V81.8584H460.503V137.5H447.255ZM453.879 73.0264C451.45 73.0264 449.426 72.2904 447.807 70.8184C446.261 69.2728 445.489 67.396 445.489 65.188C445.489 62.9064 446.261 61.0664 447.807 59.668C449.426 58.196 451.45 57.46 453.879 57.46C456.308 57.46 458.295 58.196 459.841 59.668C461.46 61.0664 462.269 62.9064 462.269 65.188C462.269 67.396 461.46 69.2728 459.841 70.8184C458.295 72.2904 456.308 73.0264 453.879 73.0264ZM498.555 138.825C493.035 138.825 488.177 137.647 483.982 135.292C479.787 132.863 476.512 129.478 474.156 125.135C471.801 120.793 470.624 115.788 470.624 110.121C470.624 104.233 471.764 99.0808 474.046 94.6648C476.401 90.2488 479.676 86.7896 483.872 84.2872C488.14 81.7848 493.072 80.5336 498.665 80.5336C504.112 80.5336 508.859 81.748 512.907 84.1768C516.955 86.6056 520.083 89.8808 522.291 94.0024C524.499 98.0504 525.603 102.614 525.603 107.692C525.603 108.428 525.603 109.238 525.603 110.121C525.603 111.004 525.529 111.924 525.382 112.881H480.118V104.38H512.244C512.097 100.332 510.736 97.1672 508.16 94.8856C505.584 92.5304 502.382 91.3528 498.555 91.3528C495.832 91.3528 493.329 91.9784 491.048 93.2296C488.766 94.4808 486.963 96.3576 485.638 98.86C484.313 101.289 483.651 104.38 483.651 108.134V111.335C483.651 114.794 484.276 117.775 485.528 120.278C486.852 122.78 488.619 124.694 490.827 126.018C493.108 127.27 495.648 127.895 498.444 127.895C501.536 127.895 504.075 127.233 506.062 125.908C508.123 124.583 509.632 122.817 510.588 120.609H524.057C523.027 124.068 521.334 127.196 518.979 129.993C516.624 132.716 513.716 134.887 510.257 136.506C506.798 138.052 502.897 138.825 498.555 138.825ZM593.823 138.825C586.389 138.825 579.802 137.169 574.061 133.857C568.394 130.471 563.941 125.798 560.703 119.836C557.465 113.801 555.845 106.809 555.845 98.86C555.845 90.9848 557.465 84.0664 560.703 78.1048C563.941 72.0696 568.394 67.3592 574.061 63.9736C579.802 60.588 586.389 58.8952 593.823 58.8952C601.404 58.8952 608.065 60.588 613.805 63.9736C619.546 67.3592 623.999 72.0696 627.164 78.1048C630.329 84.0664 631.911 90.9848 631.911 98.86C631.911 106.809 630.329 113.801 627.164 119.836C623.999 125.798 619.546 130.471 613.805 133.857C608.065 137.169 601.404 138.825 593.823 138.825ZM593.933 126.902C598.865 126.902 603.17 125.798 606.85 123.59C610.53 121.308 613.364 118.07 615.351 113.874C617.338 109.679 618.332 104.674 618.332 98.86C618.332 93.0456 617.338 88.0408 615.351 83.8456C613.364 79.6504 610.53 76.4488 606.85 74.2408C603.17 71.9592 598.865 70.8184 593.933 70.8184C589.002 70.8184 584.697 71.9592 581.017 74.2408C577.337 76.4488 574.466 79.6504 572.405 83.8456C570.418 88.0408 569.425 93.0456 569.425 98.86C569.425 104.674 570.418 109.679 572.405 113.874C574.466 118.07 577.337 121.308 581.017 123.59C584.697 125.798 589.002 126.902 593.933 126.902ZM641.102 137.5V81.8584H652.804L653.798 91.132C655.491 87.8936 657.919 85.3176 661.084 83.404C664.249 81.4904 668.003 80.5336 672.345 80.5336C676.835 80.5336 680.662 81.4904 683.827 83.404C686.991 85.244 689.42 87.9672 691.113 91.5736C692.879 95.18 693.763 99.6696 693.763 105.042V137.5H680.515V106.257C680.515 101.62 679.484 98.0504 677.423 95.548C675.363 93.0456 672.308 91.7944 668.26 91.7944C665.611 91.7944 663.219 92.42 661.084 93.6712C659.023 94.9224 657.367 96.7624 656.116 99.1912C654.939 101.546 654.35 104.417 654.35 107.802V137.5H641.102ZM728.596 137.5C724.842 137.5 721.567 136.911 718.77 135.734C716.047 134.556 713.912 132.606 712.367 129.882C710.821 127.159 710.048 123.479 710.048 118.842V93.0088H700.554V81.8584H710.048L711.594 67.1752H723.296V81.8584H738.421V93.0088H723.296V118.842C723.296 121.639 723.885 123.59 725.063 124.694C726.314 125.724 728.375 126.239 731.245 126.239H738.09V137.5H728.596ZM772.116 138.825C766.816 138.825 762.032 137.61 757.764 135.182C753.568 132.679 750.256 129.257 747.828 124.914C745.472 120.498 744.295 115.457 744.295 109.79C744.295 103.975 745.509 98.8968 747.938 94.5544C750.367 90.1384 753.679 86.716 757.874 84.2872C762.143 81.7848 766.927 80.5336 772.226 80.5336C777.525 80.5336 782.272 81.7848 786.468 84.2872C790.736 86.716 794.048 90.1016 796.404 94.444C798.832 98.7864 800.047 103.865 800.047 109.679C800.047 115.494 798.832 120.572 796.404 124.914C793.975 129.257 790.626 132.679 786.357 135.182C782.162 137.61 777.415 138.825 772.116 138.825ZM772.116 127.454C774.765 127.454 777.157 126.791 779.292 125.466C781.5 124.142 783.266 122.154 784.591 119.505C785.916 116.855 786.578 113.58 786.578 109.679C786.578 105.778 785.916 102.54 784.591 99.964C783.34 97.3144 781.61 95.3272 779.402 94.0024C777.268 92.6776 774.876 92.0152 772.226 92.0152C769.65 92.0152 767.258 92.6776 765.05 94.0024C762.842 95.3272 761.076 97.3144 759.751 99.964C758.426 102.54 757.764 105.778 757.764 109.679C757.764 113.58 758.426 116.855 759.751 119.505C761.076 122.154 762.805 124.142 764.94 125.466C767.148 126.791 769.54 127.454 772.116 127.454ZM809.703 137.5V58.012H822.951V137.5H809.703ZM860.367 138.825C855.067 138.825 850.283 137.61 846.015 135.182C841.819 132.679 838.507 129.257 836.079 124.914C833.723 120.498 832.546 115.457 832.546 109.79C832.546 103.975 833.76 98.8968 836.189 94.5544C838.618 90.1384 841.93 86.716 846.125 84.2872C850.394 81.7848 855.178 80.5336 860.477 80.5336C865.776 80.5336 870.523 81.7848 874.719 84.2872C878.987 86.716 882.299 90.1016 884.655 94.444C887.083 98.7864 888.298 103.865 888.298 109.679C888.298 115.494 887.083 120.572 884.655 124.914C882.226 129.257 878.877 132.679 874.608 135.182C870.413 137.61 865.666 138.825 860.367 138.825ZM860.367 127.454C863.016 127.454 865.408 126.791 867.543 125.466C869.751 124.142 871.517 122.154 872.842 119.505C874.167 116.855 874.829 113.58 874.829 109.679C874.829 105.778 874.167 102.54 872.842 99.964C871.591 97.3144 869.861 95.3272 867.653 94.0024C865.519 92.6776 863.127 92.0152 860.477 92.0152C857.901 92.0152 855.509 92.6776 853.301 94.0024C851.093 95.3272 849.327 97.3144 848.002 99.964C846.677 102.54 846.015 105.778 846.015 109.679C846.015 113.58 846.677 116.855 848.002 119.505C849.327 122.154 851.056 124.142 853.191 125.466C855.399 126.791 857.791 127.454 860.367 127.454ZM918.125 163.113C912.899 163.113 908.299 162.45 904.325 161.126C900.424 159.874 897.37 157.924 895.162 155.274C893.027 152.698 891.96 149.46 891.96 145.559C891.96 143.278 892.512 141.033 893.616 138.825C894.794 136.69 896.523 134.703 898.805 132.863C901.16 130.95 904.141 129.294 907.747 127.895L913.598 134.298C910.066 135.55 907.6 137.058 906.202 138.825C904.803 140.591 904.104 142.394 904.104 144.234C904.104 146.148 904.693 147.73 905.87 148.982C907.122 150.306 908.778 151.3 910.838 151.962C912.973 152.625 915.365 152.956 918.014 152.956C920.59 152.956 922.835 152.588 924.749 151.852C926.662 151.19 928.134 150.233 929.165 148.982C930.269 147.73 930.821 146.222 930.821 144.455C930.821 142.247 930.048 140.444 928.502 139.046C926.957 137.721 923.902 136.911 919.339 136.617C915.438 136.322 912.016 135.918 909.072 135.402C906.128 134.814 903.589 134.151 901.454 133.415C899.394 132.679 897.627 131.87 896.155 130.986C894.683 130.03 893.469 129.073 892.512 128.116V125.577L904.104 113.433L913.93 116.634L900.902 129.33L904.325 122.927C905.061 123.442 905.797 123.921 906.533 124.362C907.342 124.804 908.336 125.209 909.514 125.577C910.765 125.871 912.384 126.166 914.371 126.46C916.358 126.754 918.934 127.049 922.099 127.343C927.03 127.711 931.042 128.594 934.133 129.993C937.224 131.391 939.506 133.268 940.978 135.623C942.45 137.978 943.186 140.812 943.186 144.124C943.186 147.362 942.266 150.417 940.426 153.287C938.659 156.158 935.936 158.513 932.256 160.353C928.576 162.193 923.866 163.113 918.125 163.113ZM918.125 120.83C913.488 120.83 909.477 119.946 906.091 118.18C902.779 116.34 900.24 113.911 898.474 110.894C896.707 107.802 895.824 104.417 895.824 100.737C895.824 96.9832 896.707 93.5976 898.474 90.58C900.24 87.5624 902.779 85.1336 906.091 83.2936C909.477 81.4536 913.488 80.5336 918.125 80.5336C922.762 80.5336 926.736 81.4536 930.048 83.2936C933.36 85.1336 935.899 87.5624 937.666 90.58C939.432 93.5976 940.315 96.9832 940.315 100.737C940.315 104.417 939.432 107.802 937.666 110.894C935.899 113.911 933.36 116.34 930.048 118.18C926.736 119.946 922.762 120.83 918.125 120.83ZM918.125 110.562C921.29 110.562 923.829 109.716 925.742 108.023C927.656 106.33 928.613 103.902 928.613 100.737C928.613 97.572 927.656 95.18 925.742 93.5608C923.829 91.868 921.29 91.0216 918.125 91.0216C914.96 91.0216 912.384 91.868 910.397 93.5608C908.41 95.18 907.416 97.572 907.416 100.737C907.416 103.902 908.41 106.33 910.397 108.023C912.384 109.716 914.96 110.562 918.125 110.562ZM927.288 91.5736L924.749 81.8584H947.602V90.1384L927.288 91.5736ZM962.722 161.788L976.301 131.318H972.989L950.799 81.8584H965.261L981.821 119.615L997.498 81.8584H1011.52L976.743 161.788H962.722Z" fill="#1B3139"/> </svg><span>Ranks and reconciles context. Genie enforces <strong>Unity Catalog permissions</strong>. Can also use connected company documents.</span></div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="text-align: center; margin: 8px 0;"><div style="font-size: 12pt; color: #618794; font-style: italic;">grounded in governed data</div><div style="font-size: 30pt; color: #618794; line-height: 1;">&darr;</div></div>
# MAGIC
# MAGIC <!-- UNITY CATALOG -->
# MAGIC <div style="background: #F9F7F4; border: 2px solid #FF3621; border-radius: 14px; padding: 16px 20px;">
# MAGIC   <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
# MAGIC     <svg width="30" height="30" viewBox="-5.315 -5.0 210.0 210.0"><path d="M51.5066 84.0254H19.5312V115.974H51.5066V84.0254Z" fill="#FABFBA"/>
# MAGIC <path d="M21.6914 129.215L35.5186 153.105L49.3457 129.215H21.6914Z" fill="#FF5F46"/>
# MAGIC <path d="M21.6914 70.9293H49.2017L35.3745 47.0396L21.6914 70.9293Z" fill="#FF5F46"/>
# MAGIC <path d="M61.7338 133.82L45.7461 161.451L73.4004 177.426L89.3881 149.794L61.7338 133.82Z" fill="#FABFBA"/>
# MAGIC <path d="M73.4004 22.7178L45.7461 38.6923L61.7338 66.3238L89.3881 50.3493L73.4004 22.7178Z" fill="#FABFBA"/>
# MAGIC <path d="M99.7571 72.3687L75.8477 86.1844V113.816L99.7571 127.632L123.667 113.816V86.1844L99.7571 72.3687Z" fill="#FF5F46"/>
# MAGIC <path d="M85.9297 182.031H113.44L99.6128 158.142L85.9297 182.031Z" fill="#FF5F46"/>
# MAGIC <path d="M85.9297 17.9688L99.7568 41.8585L113.584 17.9688H85.9297Z" fill="#FF5F46"/>
# MAGIC <path d="M125.972 22.7178L109.984 50.3493L137.639 66.3238L153.626 38.6923L125.972 22.7178Z" fill="#FABFBA"/>
# MAGIC <path d="M137.639 133.82L109.984 149.794L125.972 177.426L153.626 161.451L137.639 133.82Z" fill="#FABFBA"/>
# MAGIC <path d="M179.839 84.0254H147.863V115.974H179.839V84.0254Z" fill="#FABFBA"/>
# MAGIC <path d="M150.168 70.9293H177.678L163.851 47.0396L150.168 70.9293Z" fill="#FF5F46"/>
# MAGIC <path d="M150.168 129.215L163.995 153.105L177.822 129.215H150.168Z" fill="#FF5F46"/></svg>
# MAGIC     <div style="font-size: 16pt; font-weight: 800;">Unity Catalog</div>
# MAGIC     <span style="font-size: 12.5pt; color: #5A6F77;">governed data foundation</span>
# MAGIC   </div>
# MAGIC   <div style="display: flex; gap: 14px; flex-wrap: nowrap;">
# MAGIC     <div style="flex: 1 1 0; min-width: 0; background: #FFFFFF; border-radius: 8px; border-left: 6px solid #FF3621; padding: 12px 16px; box-sizing: border-box;">
# MAGIC       <div style="font-size: 15pt; font-weight: 700;">Tables</div>
# MAGIC       <div style="font-size: 13pt; color: #5A6F77;">structured data</div>
# MAGIC     </div>
# MAGIC     <div style="flex: 1 1 0; min-width: 0; background: #FFFFFF; border-radius: 8px; border-left: 6px solid #FF3621; padding: 12px 16px; box-sizing: border-box;">
# MAGIC       <div style="font-size: 15pt; font-weight: 700;">Unstructured data</div>
# MAGIC       <div style="font-size: 13pt; color: #5A6F77;">files, docs, text</div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- DOCS FOOTER: GENIE ONE -->
# MAGIC <div style="margin-top: 18px; padding: 14px 22px; background: #1B5162; border-radius: 8px; display: flex; align-items: center; justify-content: space-between; gap: 20px;">
# MAGIC   <div style="font-size: 14pt; color: white; line-height: 1.5;">Genie One has many more features than we covered here. Explore the <strong>Genie One</strong> docs for the full picture.</div>
# MAGIC   <div style="display: flex; gap: 10px; flex-shrink: 0;">
# MAGIC     <a href="https://docs.databricks.com/aws/en/genie-one/" target="_blank" style="background: white; color: #1B5162; font-size: 14pt; font-weight: 700; padding: 8px 18px; border-radius: 6px; text-decoration: none; white-space: nowrap;">AWS →</a>
# MAGIC     <a href="https://learn.microsoft.com/en-us/azure/databricks/genie-one/" target="_blank" style="background: white; color: #1B5162; font-size: 14pt; font-weight: 700; padding: 8px 18px; border-radius: 6px; text-decoration: none; white-space: nowrap;">Azure →</a>
# MAGIC     <a href="https://docs.databricks.com/gcp/en/genie-one/" target="_blank" style="background: white; color: #1B5162; font-size: 14pt; font-weight: 700; padding: 8px 18px; border-radius: 6px; text-decoration: none; white-space: nowrap;">GCP →</a>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- DOCS FOOTER: GENIE ONTOLOGY -->
# MAGIC <div style="margin-top: 10px; padding: 14px 22px; background: #1B5162; border-radius: 8px; display: flex; align-items: center; justify-content: space-between; gap: 20px;">
# MAGIC   <div style="font-size: 14pt; color: white; line-height: 1.5;">For how the <strong>Genie Ontology</strong> ranks and reconciles context, see the docs.</div>
# MAGIC   <div style="display: flex; gap: 10px; flex-shrink: 0;">
# MAGIC     <a href="https://docs.databricks.com/aws/en/genie-one/chat#genie-ontology" target="_blank" style="background: white; color: #1B5162; font-size: 14pt; font-weight: 700; padding: 8px 18px; border-radius: 6px; text-decoration: none; white-space: nowrap;">AWS →</a>
# MAGIC     <a href="https://learn.microsoft.com/en-us/azure/databricks/genie-one/chat#genie-ontology" target="_blank" style="background: white; color: #1B5162; font-size: 14pt; font-weight: 700; padding: 8px 18px; border-radius: 6px; text-decoration: none; white-space: nowrap;">Azure →</a>
# MAGIC     <a href="https://docs.databricks.com/gcp/en/genie-one/chat#genie-ontology" target="_blank" style="background: white; color: #1B5162; font-size: 14pt; font-weight: 700; padding: 8px 18px; border-radius: 6px; text-decoration: none; white-space: nowrap;">GCP →</a>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### D2. Open Your Genie Agent in Genie One
# MAGIC
# MAGIC 1. In the **top-right corner** of your Databricks workspace, click the **Apps** button ![Apps Button](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/icons/apps-button.png).
# MAGIC
# MAGIC 2. Open **Genie One** in a new tab from the apps menu. 
# MAGIC     - Right-click and choose **Open Link in New Tab**, to keep your workspace tab open alongside.
# MAGIC
# MAGIC 3. In Genie One, search for your **Genie Agent** by name (you should also see the tile).
# MAGIC
# MAGIC
# MAGIC 4. Open it. You should see a clean chat interface
# MAGIC     - Recall you own this Genie, so you will still all available options since you have **CAN MANAGE**.
# MAGIC     - **CAN VIEW/CAN RUN** will not see the configuration panels or SQL editor. Just a place to ask questions.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### D3. Ask Questions and Rate Responses as a "Consumer"
# MAGIC
# MAGIC You will now ask **3 questions** as if you were a business user exploring bakehouse data. After each response, you will **rate it** to simulate real feedback.
# MAGIC
# MAGIC 1. Select **Chat** in your **Genie Agent** and ask the following.
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Important - Rate Every Response
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Our goal here is not perfect answers.
# MAGIC
# MAGIC It is to **generate feedback data** that you will review as a curator in the **Monitoring** section.
# MAGIC
# MAGIC Make sure to use a mix of:
# MAGIC - Thumbs up
# MAGIC - Thumbs down
# MAGIC - Request review
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC #### Question 1: `What is our best-selling product?`
# MAGIC
# MAGIC Ask this question in Genie, review the response, then rate it **👍 Thumbs Up**.
# MAGIC
# MAGIC > **Expected:** *"The best-selling product is Golden Gate Ginger with total sales of $11,595.00."*
# MAGIC >
# MAGIC > Genie should query `sales_transactions_gold`, aggregate by `product`, and return the top result by revenue.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Question 2: `What were our Q3 sales last year?`
# MAGIC
# MAGIC Ask this question in Genie, review the response, then
# MAGIC
# MAGIC - Rate it **👎 Thumbs Down** 
# MAGIC - Select any reason
# MAGIC - Add a comment
# MAGIC
# MAGIC > **Expected:** *"The total sales for Q3 last year (August to October 2023) were $0.00."*
# MAGIC >
# MAGIC > We have no data for this period, so the result will be zero
# MAGIC
# MAGIC > But as a business user you wouldn't know that. Rate it thumbs down regardless, so we have negative feedback to review in Monitoring. Fiscal calendar questions are also a common source of errors worth flagging.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Question 3: `Which franchise locations have the worst customer reviews?`
# MAGIC
# MAGIC Ask this question in Genie, review the response, then
# MAGIC  
# MAGIC - Rate it **Request Review (?)** 
# MAGIC - Add a comment
# MAGIC
# MAGIC > Many locations has 3 negative reviews. Even if the result looks correct, flag it for practice. We'll revisit this feedback in the **Monitoring** demonstration.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### D4. Summary of Ratings
# MAGIC
# MAGIC
# MAGIC Here is a recap of the feedback you just provided:
# MAGIC
# MAGIC <table style="width: 100%; border-collapse: collapse; font-size: 11pt;">
# MAGIC   <thead>
# MAGIC     <tr style="background: #1B5162; color: white;">
# MAGIC       <th style="padding: 10px; text-align: center; width: 40px;">#</th>
# MAGIC       <th style="padding: 10px; text-align: left;">Question</th>
# MAGIC       <th style="padding: 10px; text-align: center;">Rating</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background: #d4edda;">
# MAGIC       <td style="padding: 10px; text-align: center;">1</td>
# MAGIC       <td style="padding: 10px;">What is our best-selling product?</td>
# MAGIC       <td style="padding: 10px; text-align: center;">Thumbs Up</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #f8d7da;">
# MAGIC       <td style="padding: 10px; text-align: center;">2</td>
# MAGIC       <td style="padding: 10px;">What were our Q3 sales last year?</td>
# MAGIC       <td style="padding: 10px; text-align: center;">Thumbs Down</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #FFF6D6;">
# MAGIC       <td style="padding: 10px; text-align: center;">3</td>
# MAGIC       <td style="padding: 10px;">Which franchise locations have the worst customer reviews?</td>
# MAGIC       <td style="padding: 10px; text-align: center;">Request Review</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC This mix of positive, negative, and review-requested feedback is exactly what a real Genie Agent accumulates over time.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## E. Unity Catalog Governance with Genie
# MAGIC
# MAGIC You have shared your Genie Agent and seen how end users interact with it. 
# MAGIC
# MAGIC But how do you ensure that **sensitive data stays protected** when users ask questions?
# MAGIC
# MAGIC #### Genie Agents does not bypass Unity Catalog permissions.
# MAGIC
# MAGIC - Any **ABAC policies**, **row filters**, **column masks**, or **table ACLs** applied to the underlying tables are automatically enforced when Genie generates and executes SQL.
# MAGIC
# MAGIC - This means you can safely share a Genie Agent with business users, knowing that they will only see data they are authorized to access.
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Training Disclaimer
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC This is a brief introduction to how Unity Catalog governance integrates with Genie. It is not a comprehensive ABAC guide.
# MAGIC
# MAGIC View the documentation for more information:
# MAGIC
# MAGIC - Attribute-based access control (ABAC):
# MAGIC [AWS](https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/abac/)
# MAGIC
# MAGIC - Row filters and column masks:
# MAGIC [AWS](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/filters-and-masks/) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/filters-and-masks/)
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Important: Impact on Prompt Matching
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Tables with **row filters** or **column masks** are **excluded from entity matching** in the Knowledge Store. This means that after applying a column mask in this section, entity matching will no longer apply to `sales_customers_gold`.
# MAGIC
# MAGIC This is by design.  Databricks prevents prompt matching on governed tables to ensure data governance is not inadvertently bypassed.
# MAGIC
# MAGIC For more information, see:
# MAGIC - Configure entity matching:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/knowledge-store#configure-entity-matching) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/tune-quality#configure-entity-matching) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/knowledge-store#configure-entity-matching)
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### E1. Applying an ABAC Policy to a Genie Agent Source Table
# MAGIC
# MAGIC Your organization wants to centrally manage PII protection across all tables without applying individual masks one by one.
# MAGIC
# MAGIC We'll set this up in three SQL steps, then ask Genie about <code>email_address</code> to prove the policy is enforced automatically.
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="display: flex; align-items: center; gap: 12px;">
# MAGIC
# MAGIC   <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); position: relative;">
# MAGIC     <div style="position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: #4299E0; border-radius: 8px 8px 0 0;"></div>
# MAGIC     <div style="font-size: 13pt; font-weight: 700; color: #618794; margin-bottom: 4px; margin-top: 4px;">STEP 1</div>
# MAGIC     <div style="font-size: 15pt; font-weight: 700; color: #0b2026;">Tag the column</div>
# MAGIC     <div style="font-size: 14pt; color: #5A6F77; margin-top: 4px;">Apply a governed PII tag to <code>email_address</code></div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="font-size: 22pt; color: #618794; flex-shrink: 0;">→</div>
# MAGIC
# MAGIC   <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); position: relative;">
# MAGIC     <div style="position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: #00A972; border-radius: 8px 8px 0 0;"></div>
# MAGIC     <div style="font-size: 13pt; font-weight: 700; color: #618794; margin-bottom: 4px; margin-top: 4px;">STEP 2</div>
# MAGIC     <div style="font-size: 15pt; font-weight: 700; color: #0b2026;">Create a masking UDF</div>
# MAGIC     <div style="font-size: 14pt; color: #5A6F77; margin-top: 4px;">A SQL function that masks the value at query time</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="font-size: 22pt; color: #618794; flex-shrink: 0;">→</div>
# MAGIC
# MAGIC   <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); position: relative;">
# MAGIC     <div style="position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: #FFAB00; border-radius: 8px 8px 0 0;"></div>
# MAGIC     <div style="font-size: 13pt; font-weight: 700; color: #618794; margin-bottom: 4px; margin-top: 4px;">STEP 3</div>
# MAGIC     <div style="font-size: 15pt; font-weight: 700; color: #0b2026;">Attach an ABAC policy</div>
# MAGIC     <div style="font-size: 14pt; color: #5A6F77; margin-top: 4px;">Policy auto-masks any tagged column across the schema</div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC 1. Run the cell below to create a masking function and apply it to the `email_address` column.
# MAGIC     - This function masks email addresses for everyone except members of the `email_admins` group. 
# MAGIC     - Since you are not in that group, **you will see masked emails**.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 1. Apply the system governed tag to identify this column for ABAC policies
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC ALTER COLUMN email_address SET TAGS ('class.email_address');
# MAGIC
# MAGIC -- 2. Create a masking UDF for ABAC policy
# MAGIC CREATE OR REPLACE FUNCTION genie_course_bakehouse.abac_mask_email(email_value STRING)
# MAGIC RETURNS STRING
# MAGIC RETURN CONCAT('***@', SPLIT(email_value, '@')[1]);
# MAGIC
# MAGIC -- 3. The POLICY's TO clause determines which groups are affected and binds everything together
# MAGIC CREATE OR REPLACE POLICY mask_email_policy
# MAGIC   ON SCHEMA genie_course_bakehouse
# MAGIC   COMMENT 'Mask email addresses for general users across all tagged tables'
# MAGIC   COLUMN MASK abac_mask_email TO `account users`
# MAGIC   FOR TABLES MATCH COLUMNS hasTag('class.email_address') AS email_col ON COLUMN email_col;

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     System vs. User-Defined Governed Tags
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC - **System tags**: Pre-defined by Databricks (e.g., `class.email_address`, `class.phone_number`).
# MAGIC - **User-defined tags**: Created via UI/API for your specific use cases.
# MAGIC
# MAGIC - View the Apply tags to Unity Catalog securable objects documentation:
# MAGIC [AWS](https://docs.databricks.com/aws/en/database-objects/tags) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/database-objects/tags) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/database-objects/tags)
# MAGIC
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC 2. Run the cell below to query **sales_customers_gold** table and confirm the mask is active on the **email_address** column.
# MAGIC
# MAGIC     You should see masked email addresses (e.g., `***@example.com`).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customerID, first_name, last_name, email_address
# MAGIC FROM sales_customers_gold
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### E2. Ask Genie a Question That Uses the Masked Column
# MAGIC
# MAGIC 1. In your **Genie Agent**, ask: `Show me the email addresses of our top 5 customers by total spend`
# MAGIC
# MAGIC 2. Review the results. The email addresses should appear **masked**, just like they did in the SQL query above.
# MAGIC
# MAGIC **Example Results**
# MAGIC | customerID | first_name | last_name   | email_address   | total_spend |
# MAGIC |------------|------------|-------------|-----------------|-------------|
# MAGIC | 2000112    | Lorraine   | James       | ***@example.net | 672         |
# MAGIC | 2000134    | Charles    | Wong        | ***@example.org | 519         |
# MAGIC | 2000248    | Chad       | Mills       | ***@example.net | 498         |
# MAGIC | 2000006    | Christopher| Miller      | ***@example.net | 480         |
# MAGIC | 2000275    | Katherine  | Anderson    | ***@example.com | 465         |
# MAGIC
# MAGIC
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #4caf50;
# MAGIC   background: #e8f5e9;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#2e7d32; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Key Takeaway
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Genie Agent executed SQL against `sales_customers_gold`, and Unity Catalog applied the column mask **automatically**. 
# MAGIC
# MAGIC You did not need to configure anything in the Genie Agent itself.
# MAGIC
# MAGIC Governance travels with the data, not the tool.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## F (BONUS) - Try Agent Mode!
# MAGIC > Agent mode extends Genie's capabilities to answer both straightforward data questions and complex business questions. It uses multi-step reasoning and hypothesis testing to uncover deeper insights.
# MAGIC
# MAGIC > See Requirements and availability:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/agent-mode#requirements-and-availability) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/concepts#requirements-and-availability) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/agent-mode#requirements-and-availability)
# MAGIC
# MAGIC > Agent mode in Genie Agents:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/agent-mode) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/genie-agents/concepts#agent-mode) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/agent-mode)
# MAGIC
# MAGIC
# MAGIC 1. In your Genie Agent chat window select **Agent** (If available).
# MAGIC
# MAGIC 2. Ask the following question: `Which franchise locations are underperforming, and what do you think is causing it?`

# COMMAND ----------

# MAGIC %md
# MAGIC ## G. Conclusion
# MAGIC
# MAGIC In this demo, you:
# MAGIC
# MAGIC 1. Reviewed the **four required permissions** to create or edit a Genie Agent.
# MAGIC 2. Explored the **four Genie ACL levels** and what each role can and cannot do.
# MAGIC 3. Walked through the **sharing workflow** to give users access to a Genie Agent.
# MAGIC 4. Opened your Genie Agent through **Genie** and experienced the end-user interface.
# MAGIC 5. Asked **3 natural language questions** and rated each response with thumbs up or thumbs down.
# MAGIC 6. Applied an **ABAC column mask** and confirmed that **Genie respects Unity Catalog governance** automatically.
# MAGIC
# MAGIC ### Key Takeaway
# MAGIC
# MAGIC Sharing a Genie Agent gives users access to ask questions, but governance travels with the data in Unity Catalog, not the tool. 
# MAGIC
# MAGIC You can confidently share your space knowing that Unity Catalog enforcement is always active.
# MAGIC
# MAGIC In the next demo, you will switch back to the **curator perspective** and use the **Monitoring** tab to review the feedback you just generated.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
