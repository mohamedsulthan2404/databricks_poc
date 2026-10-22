# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Monitoring Genie Conversations
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC In the previous demo, you stepped into the role of a business user by asking questions and rating responses. Now it is time to switch back to the **curator perspective** and review that feedback.
# MAGIC
# MAGIC The **Monitoring** tab gives you visibility into every question asked, the SQL Genie generated, and the feedback users provided. This is where you identify gaps and prioritize your next round of curation.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this demo, you will be able to:
# MAGIC
# MAGIC 1. **Navigate the Monitoring tab** to review user questions, ratings, and generated SQL.
# MAGIC 2. **Filter monitoring data** by rating type (thumbs up, thumbs down, request review).
# MAGIC 3. **Apply the 4-step curator workflow** (Triage, Diagnose, Fix, Verify) to process monitoring feedback.
# MAGIC 4. **Follow monitoring best practices** for ongoing Genie Agent improvement.
# MAGIC 5. **Understand the continuous improvement loop** that connects user feedback to curation actions.

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
# MAGIC Complete **all previous demonstrations** before proceeding, especially the end-user experience demo where you asked questions and rated responses in Genie (formerly Databricks One).
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## A. Genie Monitoring
# MAGIC
# MAGIC
# MAGIC Now switch back to the **curator** perspective. 
# MAGIC
# MAGIC The Monitoring tab gives you visibility into every question asked, the SQL Genie generated, and the feedback users provided.
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Why Monitoring Matters
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Benchmarks test what you **planned** for. Monitoring shows you what users **actually ask**. The gap between the two is where your next round of curation should focus.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <!-- FRAME HEADER LABEL -->
# MAGIC <div style="background: #1B5162; color: white; padding: 10px 24px; font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; text-align: center; border-radius: 10px 10px 0 0;">Iterative Curation Loop</div>
# MAGIC
# MAGIC <!-- LOOP FRAME -->
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 10px 10px; background: #F8F9FC; padding: 28px 32px 16px 32px;">
# MAGIC <!-- 4-STEP FLOW (NO BLANK LINES INSIDE THE GRID) -->
# MAGIC <div style="display: grid; grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr; gap: 0; align-items: stretch;">
# MAGIC   <div style="background: #FFFFFF; border: 3px solid #4299E0; border-radius: 10px; padding: 16px 14px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center;">
# MAGIC     <div style="font-size: 13pt; font-weight: 700; color: #4299E0; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;">Step 1</div>
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 10px;">Create</div>
# MAGIC     <div style="font-size: 14pt; line-height: 1.4; color: #0b2026;">Add tables and metadata</div>
# MAGIC   </div>
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #618794; font-size: 26pt; line-height: 1; padding: 0 10px;">&rarr;</div>
# MAGIC   <div style="background: #FFFFFF; border: 3px solid #00A972; border-radius: 10px; padding: 16px 14px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center;">
# MAGIC     <div style="font-size: 13pt; font-weight: 700; color: #00A972; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;">Step 2</div>
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 10px;">Test</div>
# MAGIC     <div style="font-size: 14pt; line-height: 1.4; color: #0b2026;">Ask questions you expect users to ask</div>
# MAGIC   </div>
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #618794; font-size: 26pt; line-height: 1; padding: 0 10px;">&rarr;</div>
# MAGIC   <div style="background: #FFFFFF; border: 3px solid #FFAB00; border-radius: 10px; padding: 16px 14px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center;">
# MAGIC     <div style="font-size: 13pt; font-weight: 700; color: #FFAB00; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;">Step 3</div>
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 10px;">Observe</div>
# MAGIC     <div style="font-size: 14pt; line-height: 1.4; color: #0b2026;">Review generated SQL and identify gaps</div>
# MAGIC   </div>
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #618794; font-size: 26pt; line-height: 1; padding: 0 10px;">&rarr;</div>
# MAGIC   <div style="background: #FFFFFF; border: 3px solid #FF5F46; border-radius: 10px; padding: 16px 14px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center;">
# MAGIC     <div style="font-size: 13pt; font-weight: 700; color: #FF5F46; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;">Step 4</div>
# MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 10px;">Improve</div>
# MAGIC     <div style="font-size: 14pt; line-height: 1.4; color: #0b2026;">Add descriptions, instructions, or example SQL</div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC <!-- LOOP-BACK U-SHAPE (NO BLANK LINES INSIDE) -->
# MAGIC <div style="position: relative; height: 80px; margin-top: 12px;">
# MAGIC   <div style="position: absolute; left: 37%; right: 13%; top: 0; height: 52px; border-left: 3px dashed #98102A; border-right: 3px dashed #98102A; border-bottom: 3px dashed #98102A; border-bottom-left-radius: 14px; border-bottom-right-radius: 14px;"></div>
# MAGIC   <div style="position: absolute; left: calc(37% - 7px); top: -6px; width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-bottom: 11px solid #98102A;"></div>
# MAGIC   <div style="position: absolute; left: 50%; top: 42px; transform: translateX(-50%); background: #F8F9FC; padding: 2px 14px; color: #98102A; font-weight: 700; font-size: 14pt;">iterate</div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- BOTTOM TAKEAWAY -->
# MAGIC <div style="margin-top: 20px; padding: 14px 20px; background: #FFF6F4; border-left: 4px solid #FF5F46; border-radius: 6px; font-size: 14pt; line-height: 1.5;">
# MAGIC   <b style="color: #B83A24;">Key idea:</b> The loop never really ends. Every real user question is a chance to improve the Space, and small, frequent passes beat large rewrites.
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### A1. Open the Monitoring Tab
# MAGIC
# MAGIC 1. Return to your **Genie Agent** in the workspace.
# MAGIC
# MAGIC 2. Select the **Monitor** in the top navigation.
# MAGIC
# MAGIC 3. You should see a list of all questions asked against this space.
# MAGIC     - Plus any feedback for the responses.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### A2. Explore the Monitoring Interface
# MAGIC
# MAGIC The Monitoring tab shows a table of all user interactions. For each question, you can see:
# MAGIC
# MAGIC | Column | What It Shows |
# MAGIC |--------|--------------|
# MAGIC | **Question** | The natural language question the user asked |
# MAGIC | **Rating** | Thumbs up, thumbs down, or request review (if rated) |
# MAGIC |**Comment** | Comment if a **thumbs down**|
# MAGIC | **User** | Who asked the question |
# MAGIC | **Created** | When the question was asked |
# MAGIC
# MAGIC 1. **You can filter by Rating** - Use the filters to show only **Positive or Negative** responses.
# MAGIC
# MAGIC 2. **TO DO: Filter by Request - `Requested`**
# MAGIC
# MAGIC    a. Select the **Requested for review question**. 
# MAGIC       - Should be the question **Which franchise locations have the worst customer reviews?**. This is the question that was rated as a **Request Review** in an earlier demonstration.
# MAGIC
# MAGIC    b. Scroll through the question and user request.
# MAGIC
# MAGIC    c. Notice as the curator you can:
# MAGIC       - **Add a comment for the user**
# MAGIC       - **Cancel Request**
# MAGIC       - **Mark as reviewed**
# MAGIC
# MAGIC    d. Add a comment and select **Mark as reviewed**.
# MAGIC
# MAGIC    e. Navigate back to **Monitoring** and remove the filter on the questions. 
# MAGIC    
# MAGIC    f. Notice now that the question is marked as **Reviewed** under the **Request** column.
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### A3. What to Do with Monitoring Data
# MAGIC
# MAGIC Monitoring is not just for observation. 
# MAGIC
# MAGIC #### It should **drive action**.
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 1200px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: nowrap;">
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #FF5F46; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin: 10px 0 8px 0; text-align: center;">1. Triage</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5; text-align: left;">
# MAGIC     <ul style="padding-left: 18px; margin: 0;">
# MAGIC       <li>Filter for <strong>thumbs down</strong></li>
# MAGIC       <li>Focus on highest-priority items first</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #FFAB00; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin: 10px 0 8px 0; text-align: center;">2. Diagnose</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5; text-align: left;">
# MAGIC     <ul style="padding-left: 18px; margin: 0;">
# MAGIC       <li>Open each flagged question</li>
# MAGIC       <li>Review the generated SQL</li>
# MAGIC       <li>Identify root cause:
# MAGIC         <ul style="padding-left: 16px; margin-top: 4px;">
# MAGIC           <li>Missing description</li>
# MAGIC           <li>Missing instruction</li>
# MAGIC           <li>Missing example query</li>
# MAGIC         </ul>
# MAGIC       </li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #02A36F; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin: 10px 0 8px 0; text-align: center;">3. Fix</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5; text-align: left;">
# MAGIC     <ul style="padding-left: 18px; margin: 0;">
# MAGIC       <li>Update the <strong>Knowledge Store</strong></li>
# MAGIC       <li>Add or refine:
# MAGIC         <ul style="padding-left: 16px; margin-top: 4px;">
# MAGIC           <li>Descriptions</li>
# MAGIC           <li>SQL expressions</li>
# MAGIC           <li>Example queries</li>
# MAGIC           <li>Text instructions</li>
# MAGIC         </ul>
# MAGIC       </li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #1B5162; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin: 10px 0 8px 0; text-align: center;">4. Verify</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5; text-align: left;">
# MAGIC     <ul style="padding-left: 18px; margin: 0;">
# MAGIC       <li>Add the issue as a <strong>benchmark</strong></li>
# MAGIC       <li>Re-run benchmarks</li>
# MAGIC       <li>Confirm:
# MAGIC         <ul style="padding-left: 16px; margin-top: 4px;">
# MAGIC           <li>The fix works</li>
# MAGIC           <li>No regressions introduced</li>
# MAGIC         </ul>
# MAGIC       </li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### A4. Monitoring Best Practices
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Best Practices for Monitoring
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC - **Check Monitoring regularly** - Set a cadence (daily at first, then weekly) to review new questions and feedback. Do not wait for complaints.
# MAGIC - **Prioritize thumbs-down and request-review** - These are your users telling you where Genie needs help. Start here every time.
# MAGIC - **Look for patterns, not one-offs** - If multiple users ask similar questions that Genie gets wrong, that is a systemic gap worth fixing. A single unusual question may not need a Knowledge Store change.
# MAGIC - **Turn monitoring insights into benchmarks** - When you find a question that Genie answered incorrectly, add it as a benchmark with ground truth SQL. This prevents the same failure from recurring after future changes.
# MAGIC - **Review thumbs-up responses too** - Occasionally check positive-rated responses to confirm they are actually correct. Users sometimes rate quickly without verifying the SQL.
# MAGIC - **Track improvement over time** - As you add more curation, the ratio of thumbs-up to thumbs-down should improve. Monitoring is how you measure that trend.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## B. The Continuous Improvement Loop
# MAGIC
# MAGIC This demo completes the full authoring cycle. Looking back at everything you have done across all demos:
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <style>
# MAGIC table td, table th {
# MAGIC   font-size: 14pt !important;
# MAGIC }
# MAGIC </style>
# MAGIC
# MAGIC <table style="width: 100%; border-collapse: separate; border-spacing: 0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <thead>
# MAGIC     <tr style="background: #1B5162; color: white;">
# MAGIC       <th style="padding: 14px 18px; text-align: center; width: 50px;">Step</th>
# MAGIC       <th style="padding: 14px 18px; text-align: left;">What You Did</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 12px 18px; text-align: center; font-weight: 700; color: #1B5162; border-bottom: 1px solid #EEEDE9;">1</td>
# MAGIC       <td style="padding: 12px 18px; border-bottom: 1px solid #EEEDE9;"><strong>Created a Genie Agent</strong> — Selected tables and set up the space with no metadata</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #FFFFFF;">
# MAGIC       <td style="padding: 12px 18px; text-align: center; font-weight: 700; color: #1B5162; border-bottom: 1px solid #EEEDE9;">2</td>
# MAGIC       <td style="padding: 12px 18px; border-bottom: 1px solid #EEEDE9;"><strong>Established a baseline</strong> — Asked questions, observed failures, and added benchmarks</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 12px 18px; text-align: center; font-weight: 700; color: #1B5162; border-bottom: 1px solid #EEEDE9;">3</td>
# MAGIC       <td style="padding: 12px 18px; border-bottom: 1px solid #EEEDE9;"><strong>Added metadata</strong> — Table and column descriptions, synonyms, and prompt matching</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #FFFFFF;">
# MAGIC       <td style="padding: 12px 18px; text-align: center; font-weight: 700; color: #1B5162; border-bottom: 1px solid #EEEDE9;">4</td>
# MAGIC       <td style="padding: 12px 18px; border-bottom: 1px solid #EEEDE9;"><strong>Added SQL logic and instructions</strong> — SQL expressions, example queries, and text instructions</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 12px 18px; text-align: center; font-weight: 700; color: #1B5162; border-bottom: 1px solid #EEEDE9;">5</td>
# MAGIC       <td style="padding: 12px 18px; border-bottom: 1px solid #EEEDE9;"><strong>Tested as an end user</strong> — Used Genie to ask questions and rate responses</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #FFFFFF;">
# MAGIC       <td style="padding: 12px 18px; text-align: center; font-weight: 700; color: #1B5162; border-bottom: 1px solid #EEEDE9;">6</td>
# MAGIC       <td style="padding: 12px 18px; border-bottom: 1px solid #EEEDE9;"><strong>Reviewed as a curator</strong> — Used Monitoring to find gaps and prioritize fixes</td>
# MAGIC     </tr>
# MAGIC     <tr style="background: #F9F7F4;">
# MAGIC       <td style="padding: 12px 18px; text-align: center; font-weight: 700; color: #1B5162;">7</td>
# MAGIC       <td style="padding: 12px 18px;"><strong>Verified UC governance with Genie</strong> — Applied an ABAC policy and observed that Genie respects Unity Catalog enforcement automatically</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC In production, steps 3–7 repeat continuously. Users ask new questions, curators monitor and improve, and benchmarks catch regressions.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Conclusion
# MAGIC
# MAGIC In this demo, you:
# MAGIC
# MAGIC 1. Navigated the **Monitoring tab** to review user questions, ratings, and generated SQL.
# MAGIC 2. Filtered monitoring data by **thumbs down** and **request review** to find priority items.
# MAGIC 3. Learned the **4-step curator workflow**: Triage, Diagnose, Fix, Verify.
# MAGIC 4. Reviewed **monitoring best practices** for ongoing Genie Agent improvement.
# MAGIC 5. Connected monitoring back to the **continuous improvement loop** that drives Genie quality over time.
# MAGIC
# MAGIC ### Key Takeaway
# MAGIC
# MAGIC Building a Genie Agent is not a one-time task.
# MAGIC
# MAGIC It is an ongoing process. **Monitoring** closes the loop between what you built and what your users actually need.
# MAGIC
# MAGIC The best Genie Agents are the ones that improve continuously based on real user feedback.
# MAGIC
# MAGIC You have now completed all demonstrations. Continue to the **Summary and Next Steps** notebook to review additional resources and next steps for your Genie journey.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
