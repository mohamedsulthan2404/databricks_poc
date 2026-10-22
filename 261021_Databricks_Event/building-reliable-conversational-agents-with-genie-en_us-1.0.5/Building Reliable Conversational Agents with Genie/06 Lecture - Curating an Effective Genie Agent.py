# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC # Lecture - Curating an Effective Genie Agent
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC In the previous demo, you created a Genie Agent with no metadata, instructions, or example SQL and observed how Genie can struggle with ambiguous business terms, shared column names, and opaque column values. Those gaps are not limitations of Genie itself, they are gaps in how the agent was configured.
# MAGIC
# MAGIC In this lecture, you will learn how to think like a **Genie Agent curator**, someone who iteratively improves a Genie Agent by adding the right metadata and guidance. 
# MAGIC
# MAGIC You will explore the Knowledge Store as the centralized curation surface, understand the recommended order for applying curation tools, and connect each tool back to the specific problems you observed in the previous demo.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. **Describe the iterative curation process** for building an effective Genie Agent: build, test, observe, improve, repeat.
# MAGIC 2. **Recall the six curation components** from the previous lecture and connect them to Knowledge Store configuration.
# MAGIC 3. **Explain the Knowledge Store** as the centralized configuration surface for curation, including its components: space-level metadata, prompt matching, join relationships, SQL expressions, and knowledge mining.
# MAGIC 4. **Explain the recommended order of operations** for adding metadata to a Genie Agent and why descriptions come first.
# MAGIC 5. **Map each problem observed in the previous demo** to the specific curation tool that addresses it.
# MAGIC 6. **Apply table selection best practices** to ensure the foundation of a Genie Agent supports accurate and consistent query generation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. The Curation Mindset

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### A1. Think Like a Curator, Not a Developer
# MAGIC
# MAGIC A Genie Agent is not something you build once and walk away from.
# MAGIC
# MAGIC #### It is a product that you design, test, and refine over time, just like a dashboard or a report.
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div class="two-pane">
# MAGIC
# MAGIC <style>
# MAGIC
# MAGIC .two-sides {
# MAGIC     display: flex;
# MAGIC     justify-content: center;
# MAGIC     align-items: stretch;
# MAGIC     gap: 40px;
# MAGIC     flex-wrap: wrap;
# MAGIC }
# MAGIC
# MAGIC .box {
# MAGIC     width: 520px;
# MAGIC     min-height: 320px;
# MAGIC     background: #F9F7F4;
# MAGIC     border-radius: 8px;
# MAGIC     box-shadow: 0 2px 8px rgba(27,49,57,0.06);
# MAGIC     display: flex;
# MAGIC     flex-direction: column;
# MAGIC     justify-content: flex-start;
# MAGIC     gap: 14px;
# MAGIC     padding: 22px;
# MAGIC     text-align: left;
# MAGIC     position: relative;
# MAGIC     box-sizing: border-box;
# MAGIC }
# MAGIC
# MAGIC .box::before {
# MAGIC     content: "";
# MAGIC     position: absolute;
# MAGIC     top: 0;
# MAGIC     left: 0;
# MAGIC     width: 100%;
# MAGIC     height: 8px;
# MAGIC }
# MAGIC
# MAGIC .box.curator::before { background: #02A36F; }
# MAGIC .box.consumer::before { background: #2574B5; }
# MAGIC
# MAGIC .box-title {
# MAGIC     font-size: 20pt;
# MAGIC     font-weight: 700;
# MAGIC     color: #0b2026;
# MAGIC     text-align: center;
# MAGIC     margin-top: 6px;
# MAGIC }
# MAGIC
# MAGIC .box-image {
# MAGIC     text-align: center;
# MAGIC     margin: 4px 0 8px 0;
# MAGIC }
# MAGIC
# MAGIC .box-image img {
# MAGIC     width: 120px;
# MAGIC     height: auto;
# MAGIC     object-fit: contain;
# MAGIC }
# MAGIC
# MAGIC .box-text {
# MAGIC     font-size: 14pt;
# MAGIC     color: #0b2026;
# MAGIC     line-height: 1.55;
# MAGIC }
# MAGIC
# MAGIC .box-text ul {
# MAGIC     margin: 0;
# MAGIC     padding-left: 18px;
# MAGIC }
# MAGIC
# MAGIC .box-text li {
# MAGIC     margin-bottom: 12px;
# MAGIC }
# MAGIC
# MAGIC .box-text li:last-child {
# MAGIC     margin-bottom: 0;
# MAGIC }
# MAGIC
# MAGIC </style>
# MAGIC
# MAGIC <div class="two-sides">
# MAGIC
# MAGIC <div class="box curator">
# MAGIC <div class="box-title">Genie Agent Curator</div>
# MAGIC <div class="box-image">
# MAGIC <img src="https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/icons/curator.png">
# MAGIC </div>
# MAGIC <div class="box-text">
# MAGIC <ul>
# MAGIC <li>A <strong>domain expert</strong> who understands the data and the business questions it should answer</li>
# MAGIC <li>Typically a <strong>data analyst or analytics engineer</strong> who is proficient in SQL</li>
# MAGIC <li>Responsible for <strong>selecting tables</strong>, writing <strong>instructions</strong>, adding <strong>descriptions</strong>, and providing <strong>example SQL</strong></li>
# MAGIC <li>Continuously <strong>monitors and refines</strong> the agent based on user feedback</li>
# MAGIC <li><strong>Can Edit, update, modify Genie</strong></li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <div class="box consumer">
# MAGIC <div class="box-title">Genie Agent Consumers</div>
# MAGIC <div class="box-image">
# MAGIC <img src="https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/icons/people-blue.png">
# MAGIC </div>
# MAGIC <div class="box-text">
# MAGIC <ul>
# MAGIC <li>A <strong>business user</strong> who asks questions in natural language</li>
# MAGIC <li><strong>No SQL knowledge required</strong>. Genie handles the query generation</li>
# MAGIC <li>Provides <strong>feedback</strong> through thumbs up/down and review requests</li>
# MAGIC <li>Expects <strong>accurate, consistent answers</strong> without needing to understand the underlying data model</li>
# MAGIC <li>Requires CAN VIEW permission on Genie, and access to the Unity Catalog tables and views</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC Building an effective Genie Agent requires two distinct roles:
# MAGIC
# MAGIC #### The Genie Agent Curator
# MAGIC The curator is the person who builds and maintains the Genie Agent. This person needs two things:
# MAGIC 1. **Domain knowledge** - They understand what the data means, how metrics are calculated, and what terminology the business uses.
# MAGIC 2. **SQL proficiency** - They can write the example queries and instructions that teach Genie how to interpret questions correctly.
# MAGIC
# MAGIC Data analysts are often the ideal curators because they sit at the intersection of business knowledge and technical skill.
# MAGIC
# MAGIC #### The Genie Agent Consumer
# MAGIC - The consumer is the end user, the person asking questions.
# MAGIC
# MAGIC - They should not need to know SQL, understand table schemas, or worry about which column to filter on.
# MAGIC
# MAGIC - Their experience is only as good as the curation behind the space.
# MAGIC
# MAGIC #### Summary
# MAGIC The quality of a Genie Agent is determined by the **curator**, not the consumer.
# MAGIC
# MAGIC If consumers are getting wrong answers, the fix is better curation, not better questions.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### A2. The Iterative Curation Loop Overview
# MAGIC Effective Genie Agents are built through <b>iteration</b>, not perfection on the first try. Start small, test with real questions, and improve based on what you observe.
# MAGIC
# MAGIC <br></br>
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

# MAGIC %md-sandbox
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC The curation loop is the most important concept in this lecture. Here is how it works:
# MAGIC
# MAGIC #### 1. Create
# MAGIC Start with the minimum viable space. Add only the tables needed to answer your target set of questions. 
# MAGIC
# MAGIC Do not try to add every instruction or description upfront. You will not know what is needed until you test.
# MAGIC
# MAGIC #### 2. Test
# MAGIC Ask questions that you expect your business users to ask. 
# MAGIC
# MAGIC Start with simple questions and work toward more complex ones. This is exactly what we did in the previous demo.
# MAGIC
# MAGIC #### 3. Observe
# MAGIC After each question, **review the generated SQL carefully**. Do not just look at the result. Look at *how* Genie arrived at the result. Ask yourself:
# MAGIC - Did Genie use the right table?
# MAGIC - Did it join correctly?
# MAGIC - Did it filter on the right column values?
# MAGIC - Did it interpret the business term the way I intended?
# MAGIC
# MAGIC #### 4. Improve
# MAGIC Based on what you observed, add the appropriate metadata. Then go back to Step 2 and re-ask the same questions **in a new chat thread** to confirm the improvement.
# MAGIC
# MAGIC #### Why a New Chat Thread?
# MAGIC Genie loads instructions when a new chat starts. After updating instructions, always test in a **new chat** to ensure the latest configuration is being used.
# MAGIC
# MAGIC #### Start Small
# MAGIC It is impossible to define a fully complete agent on the first try. Start with a small set of target questions and a minimal set of tables. A focused agent with 5 well-described tables will outperform a broad agent with 20 poorly documented ones.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Improving Genie with the Knowledge Store

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B1. The Knowledge Store
# MAGIC The **Knowledge Store** is where you configure how Genie understands your data and responds to questions.
# MAGIC
# MAGIC This collection of curated semantic definitions **improves Genie's understanding of your data and increases response accuracy**. 
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="display: flex; flex-direction: column; gap: 16px;">
# MAGIC
# MAGIC <!-- Header -->
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px 8px 4px 4px; padding: 20px 24px; text-align: center;">
# MAGIC   <div style="font-size: 22pt; font-weight: 700;">Genie Knowledge Store Components</div>
# MAGIC   <div style="font-size: 15pt; margin-top: 6px; opacity: 0.9;">Access via <strong>Configure</strong> in your Genie Agent</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Row 1 -->
# MAGIC <div style="display: flex; gap: 12px;">
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #98182A; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">1. Space-Level Metadata</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5;">
# MAGIC     <ul>
# MAGIC       <li><strong>Descriptions</strong> for tables and columns</li>
# MAGIC       <li><strong>Synonyms</strong> aligned to business language</li>
# MAGIC       <li>Overrides or extensions of Unity Catalog metadata</li>
# MAGIC       <li>No changes to underlying data assets</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #4299E0; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">2. Prompt Matching</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5;">
# MAGIC     <ul>
# MAGIC       <li><strong>Format assistance</strong> provides representative column values</li>
# MAGIC       <li><strong>Entity matching</strong> maps user language to real data values</li>
# MAGIC       <li>Improves accuracy for categorical filters</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Row 2 -->
# MAGIC <div style="display: flex; gap: 12px;">
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #02A36F; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">3. SQL Joins</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5;">
# MAGIC     <ul>
# MAGIC       <li>Define how tables relate to each other</li>
# MAGIC       <li>Specify join conditions explicitly</li>
# MAGIC       <li>Set relationship types:
# MAGIC         <ul>
# MAGIC           <li>One-to-many</li>
# MAGIC           <li>Many-to-one</li>
# MAGIC           <li>One-to-one</li>
# MAGIC         </ul>
# MAGIC       </li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #FFAB00; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">4. SQL Expressions</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5;">
# MAGIC     <ul>
# MAGIC       <li><strong>Measures</strong>, KPIs</li>
# MAGIC       <li><strong>Filters</strong>, reusable conditions</li>
# MAGIC       <li><strong>Dimensions</strong>, grouping attributes</li>
# MAGIC       <li>Each includes synonyms for natural language queries</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Row 3 -->
# MAGIC <div style="display: flex; gap: 12px;">
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #618794; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">5. SQL Queries</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5;">
# MAGIC     <ul>
# MAGIC       <li><strong>Example SQL queries</strong> teach Genie how to answer common questions</li>
# MAGIC       <li>Pair a <strong>user question</strong> with the SQL that answers it</li>
# MAGIC       <li>Can be <strong>parameterized</strong> and reused as patterns</li>
# MAGIC       <li><strong>SQL functions</strong> enable reusable, trusted logic across teams</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 18px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #FF5F46; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">6. General Instructions</div>
# MAGIC   <div style="font-size: 14pt; color: #333; line-height: 1.5;">
# MAGIC     <ul>
# MAGIC       <li><strong>Global text guidance</strong> that applies to all Genie responses</li>
# MAGIC       <li>Capture <strong>business context</strong> and domain-specific rules</li>
# MAGIC       <li>Control <strong>formatting and behavior</strong> such as language, rounding, and output style</li>
# MAGIC       <li>Use only for logic that <strong>cannot be expressed in SQL or metadata</strong></li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Secondary note -->
# MAGIC <div style="margin-top: 16px; padding: 14px 18px; background: #F8F9FC; border-left: 4px solid #1B5162; border-radius: 6px;">
# MAGIC   <div style="font-size: 15pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>Also available:</strong> Space-level data customization lets you hide columns and simplify datasets for users. This improves usability, but does not change how Genie understands questions or generates SQL.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Key point -->
# MAGIC <div style="margin-top: 20px; padding: 18px 24px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 16pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <div style="font-weight: 700; margin-bottom: 8px;">Key points:</div>
# MAGIC     <ul style="padding-left: 20px; margin: 0;">
# MAGIC       <li>Configurations are scoped to a single Genie Agent</li>
# MAGIC       <li>No changes to Unity Catalog metadata</li>
# MAGIC       <li>Safe experimentation across multiple spaces</li>
# MAGIC       <li>Shared data remains unchanged</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <br><br/>
# MAGIC
# MAGIC Build a knowledge store:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/knowledge-store) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/genie-agents/tune-quality) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/knowledge-store)
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC The Knowledge Store is where you configure how Genie understands your data and responds to questions.
# MAGIC
# MAGIC It brings together multiple layers of context that guide how Genie interprets natural language and generates SQL.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 1. Space-Level Metadata
# MAGIC This is where you define **descriptions and synonyms** for tables and columns.
# MAGIC
# MAGIC - Helps map business language to the correct data fields
# MAGIC - Clarifies ambiguous columns (for example, customer country vs franchise country)
# MAGIC - Can extend or override Unity Catalog metadata without modifying the underlying data
# MAGIC
# MAGIC This is one of the **highest-impact areas for improving accuracy**.
# MAGIC
# MAGIC
# MAGIC #### 2. Prompt Matching
# MAGIC Prompt matching improves how Genie connects user input to actual data values.
# MAGIC
# MAGIC - **Format assistance** provides representative values for columns
# MAGIC - **Entity matching** maps user terms to real values in the data
# MAGIC
# MAGIC This is especially important for **categorical filters** like region, product names, or status fields.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 3. SQL Joins
# MAGIC Defines how tables relate to each other.
# MAGIC
# MAGIC - Specify join conditions explicitly
# MAGIC - Set relationship types (one-to-many, many-to-one, etc.)
# MAGIC
# MAGIC Without clear joins, Genie may generate incorrect or incomplete queries.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 4. SQL Expressions
# MAGIC This is where you define reusable business logic.
# MAGIC
# MAGIC - Measures and KPIs (for example, revenue = SUM(totalPrice))
# MAGIC - Filters and reusable conditions
# MAGIC - Dimensions used for grouping
# MAGIC
# MAGIC This is the **preferred way to encode business definitions**, rather than using text instructions.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 5. SQL Queries (Example Queries and Functions)
# MAGIC These teach Genie how to answer real business questions.
# MAGIC
# MAGIC - Pair a **natural language question** with the SQL that answers it
# MAGIC - Can be static or **parameterized** for reuse
# MAGIC - Genie can reuse these directly or learn patterns from them
# MAGIC - SQL functions can be registered in Unity Catalog for reusable, trusted logic
# MAGIC
# MAGIC This is one of the most effective ways to improve **accuracy and consistency**.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 6. General Instructions
# MAGIC Text-based guidance that applies globally across all queries.
# MAGIC
# MAGIC - Capture **business context** and domain-specific rules
# MAGIC - Control formatting and response behavior (language, rounding, output style)
# MAGIC - Apply rules that cannot be expressed in SQL or metadata
# MAGIC
# MAGIC **Important:** Instructions should be used as a **last resort**, not for defining metrics or joins.
# MAGIC
# MAGIC
# MAGIC
# MAGIC ### Key takeaway
# MAGIC
# MAGIC Genie performs best when you prioritize:
# MAGIC
# MAGIC 1. **Metadata** for meaning  
# MAGIC 2. **SQL logic and queries** for business definitions  
# MAGIC 3. **Instructions only when necessary**
# MAGIC
# MAGIC Think of the Knowledge Store as a system where:
# MAGIC
# MAGIC - Structured inputs (SQL, metadata) drive accuracy  
# MAGIC - Text instructions provide fallback guidance  
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ### B2. Recommended Order of Operations
# MAGIC
# MAGIC Curate iteratively, but start with the highest-impact foundations first.
# MAGIC
# MAGIC Steps 2-6 are all configured through the **Knowledge Store**.
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="display: flex; align-items: stretch; gap: 16px;">
# MAGIC
# MAGIC <!-- Left arrow label -->
# MAGIC <div style="
# MAGIC     writing-mode: vertical-lr;
# MAGIC     transform: rotate(180deg);
# MAGIC     text-align: center;
# MAGIC     font-weight: 700;
# MAGIC     font-size: 15pt;
# MAGIC     color: #618794;
# MAGIC     padding: 0 6px;
# MAGIC     display: flex;
# MAGIC     justify-content: flex-end;
# MAGIC ">
# MAGIC &larr; ORDER OF OPERATIONS (RECOMMENDED)
# MAGIC </div>
# MAGIC
# MAGIC <!-- Stacked layers -->
# MAGIC <div style="flex: 1; display: flex; flex-direction: column; gap: 6px;">
# MAGIC
# MAGIC <div style="background: #1C3037; color: white; border-radius: 8px 8px 4px 4px; padding: 22px 24px; text-align: center;">
# MAGIC   <div style="font-size: 20pt; font-weight: 700;">1. Define Purpose and Scope</div>
# MAGIC   <div style="font-size: 15pt; margin-top: 6px; opacity: 0.9;">Start with a focused audience, topic, and small set of business questions</div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="background: #2574B5; color: white; border-radius: 4px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 18pt; font-weight: 700;">2. Add Focused Unity Catalog Tables</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;">Pick a small, well-documented set of tables or views and ensure relationships are defined</div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="background: #98182A; color: white; border-radius: 4px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 18pt; font-weight: 700;">3. Add Metadata and Prompt Matching</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;"><strong>Strongest early accuracy lever</strong> — add descriptions, synonyms, and prompt matching</div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="background: #02A36F; color: white; border-radius: 4px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 18pt; font-weight: 700;">4. Add SQL Expressions</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;">Define reusable metrics, filters, dimensions, and business logic in SQL</div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="background: #F8A805; color: #0b2026; border-radius: 4px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 18pt; font-weight: 700;">5. Add Example SQL Queries</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;">Teach Genie common or complex question patterns with verified SQL examples</div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="background: #FE3722; color: white; border-radius: 4px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 18pt; font-weight: 700;">6. Add General Instructions</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;">Use text only for global rules or edge cases that SQL and metadata cannot express</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC The order matters. Each layer builds on the previous one.
# MAGIC
# MAGIC
# MAGIC #### 1. Define Purpose and Scope
# MAGIC Start by deciding what the Genie Agent is for.
# MAGIC
# MAGIC - Define the audience and business topic
# MAGIC - Identify the key questions the agent should answer
# MAGIC - Keep the scope narrow and focused
# MAGIC
# MAGIC A Genie Agent should support a specific use case, not every possible question across the business.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 2. Add Focused Unity Catalog Tables and Relationships
# MAGIC Once the purpose is clear, select the data that supports it.
# MAGIC
# MAGIC - Use a small, focused set of Unity Catalog tables or views
# MAGIC - Ensure **relationships (joins)** are defined (PK/FK, views, or Knowledge Store)
# MAGIC - Prefer well-documented, analytics-ready tables
# MAGIC - Aim for about **5 tables or fewer** when possible
# MAGIC - Pre-join or simplify data with views or metric views if needed
# MAGIC
# MAGIC Without clean data and clear relationships, the rest of the curation work is much harder.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 3. Add Metadata and Prompt Matching
# MAGIC Metadata is the **strongest early accuracy lever** and often the easiest win.
# MAGIC
# MAGIC - Add **descriptions and synonyms** to clarify what columns mean
# MAGIC - Resolve ambiguity across similar fields
# MAGIC - Help Genie select the right columns when questions are vague
# MAGIC
# MAGIC Also enable **prompt matching**:
# MAGIC
# MAGIC - **Format assistance** helps Genie understand data formats and value patterns
# MAGIC - **Entity matching** maps user language, including misspellings, to real data values
# MAGIC
# MAGIC Many spaces improve significantly at this stage before any SQL is added.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 4. Add SQL Expressions
# MAGIC SQL expressions define your reusable business logic.
# MAGIC
# MAGIC - Define metrics and KPIs
# MAGIC - Create reusable filters and dimensions
# MAGIC - Standardize how business terms are calculated
# MAGIC
# MAGIC Recommended to use SQL expressions for **common, reusable definitions** instead of text.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 5. Add Example SQL Queries
# MAGIC Example SQL queries teach Genie how to answer common or complex questions.
# MAGIC
# MAGIC - Pair natural language questions with verified SQL
# MAGIC - Use them for multi-step logic or ambiguous prompts
# MAGIC - Parameterized examples can be reused as patterns
# MAGIC
# MAGIC Genie can use these examples directly or learn from them to answer similar questions.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### 6. Add General Instructions
# MAGIC Use text instructions only when something **cannot be expressed in SQL or metadata**.
# MAGIC
# MAGIC Good use cases include:
# MAGIC
# MAGIC - Clarification rules
# MAGIC - Formatting and output behavior
# MAGIC - Language or response preferences
# MAGIC
# MAGIC **Avoid using instructions to define metrics, joins, or logic.**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### A Practical Guideline
# MAGIC
# MAGIC - **Start small** and expand over time
# MAGIC - Use **clear column names and descriptions**
# MAGIC - Focus on a few high-value questions first
# MAGIC - Prioritize **structured context** like metadata and SQL over plain text guidance
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B3. View Genie Agent Knowledge Store
# MAGIC
# MAGIC Follow the steps below to explore the configuration options available in your Genie Agent.
# MAGIC
# MAGIC 1. Right-click **Genie Agents** in the left navigation and select **Open Link in New Tab**.
# MAGIC
# MAGIC 2. Open your sales Genie Agent from the previous demonstration.
# MAGIC
# MAGIC 3. Select **Configure**.
# MAGIC
# MAGIC 4. Select **Data**
# MAGIC    - View available **Table and Column Metadata** (descriptions and synonyms)
# MAGIC
# MAGIC 5. Select **Instructions**
# MAGIC    - **Text**: Define **text instructions** for behavior and edge cases
# MAGIC    - **Joins**: Specify **relationships between tables** (SQL logic)
# MAGIC    - **SQL Expressions**: Define **business metrics as SQL expressions** (SQL logic)
# MAGIC    - **SQL Queries**: Add **example queries** that Genie uses as trusted patterns (SQL logic)

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Connecting Problems to Solutions

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C1. Mapping Demo Problems to Curation Tools
# MAGIC
# MAGIC In the previous demo, you observed that Genie can struggle with specific types of questions without the right context.
# MAGIC
# MAGIC Each problem maps directly to a curation tool.
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="font-family: sans-serif; color: #0b2026; max-width: 1400px; margin: 0 auto;">
# MAGIC
# MAGIC <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: nowrap;">
# MAGIC
# MAGIC   <!-- Problem 1 -->
# MAGIC   <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden;">
# MAGIC     <div style="background: #2574B5; color: white; padding: 14px 20px; text-align: center;">
# MAGIC       <div style="font-size: 18pt; font-weight: bold;">Opaque Column Names and Values</div>
# MAGIC     </div>
# MAGIC     <div style="padding: 18px 20px;">
# MAGIC       <div style="font-size: 15pt; font-style: italic; color: #333; margin-bottom: 10px; text-align: center;">"Count of Bad Reviews by Location?"</div>
# MAGIC       <div style="font-size: 14pt; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC         Genie might not know the valid values for the <code>flag</code> column. It may have guessed the wrong case, value, or skipped the column entirely.
# MAGIC       </div>
# MAGIC       <div style="background: rgba(37,116,181,0.10); border-left: 4px solid #2574B5; padding: 10px 12px; border-radius: 6px; font-size: 14pt;">
# MAGIC         <strong>Fix:</strong> Add a <strong>column description</strong> listing valid values: <code>positive</code>, <code>negative</code>, <code>mixed</code>
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC
# MAGIC   <!-- Problem 2 -->
# MAGIC   <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden;">
# MAGIC     <div style="background: #02A36F; color: white; padding: 14px 20px; text-align: center;">
# MAGIC       <div style="font-size: 18pt; font-weight: bold;">Ambiguous Business Terms</div>
# MAGIC     </div>
# MAGIC     <div style="padding: 18px 20px;">
# MAGIC       <div style="font-size: 15pt; font-style: italic; color: #333; margin-bottom: 10px; text-align: center;">"Who are our best customers?"</div>
# MAGIC       <div style="font-size: 14pt; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC         Genie had to guess whether "best" meant highest spend, most orders, or most recent purchase. Different runs may give different answers.
# MAGIC       </div>
# MAGIC       <div style="background: rgba(2,163,111,0.10); border-left: 4px solid #02A36F; padding: 10px 12px; border-radius: 6px; font-size: 14pt;">
# MAGIC         <strong>Fix:</strong> Add a <strong>SQL query</strong>: "Define a question with an example query for the Genie Agent".
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC
# MAGIC   <!-- Problem 3 -->
# MAGIC   <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden;">
# MAGIC     <div style="background: #FE3722; color: white; padding: 14px 20px; text-align: center;">
# MAGIC       <div style="font-size: 18pt; font-weight: bold;">Complex Query Patterns</div>
# MAGIC     </div>
# MAGIC     <div style="padding: 18px 20px;">
# MAGIC       <div style="font-size: 15pt; font-style: italic; color: #333; margin-bottom: 10px; text-align: center;">"How Many Franchises Does Each Supplier Serve?"</div>
# MAGIC       <div style="font-size: 14pt; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC         Genie struggled to generate the LEFT JOIN + IS NULL pattern needed to find orphaned foreign keys and aggregate all of the data.
# MAGIC       </div>
# MAGIC       <div style="background: rgba(254,55,34,0.10); border-left: 4px solid #FE3722; padding: 10px 12px; border-radius: 6px; font-size: 14pt;">
# MAGIC         <strong>Fix:</strong> Add an <strong>example SQL query</strong> and/or <strong>define a SQL JOIN</strong> demonstrating the LEFT JOIN pattern
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Docs callout -->
# MAGIC <div id="acc-container"></div>
# MAGIC
# MAGIC <!-- Docs callout -->
# MAGIC <div style="margin-top: 24px; padding: 16px 24px; background: #1B5162; border-radius: 8px; display: flex; align-items: center; justify-content: space-between; gap: 20px;">
# MAGIC   <div style="font-size: 15pt; color: white; line-height: 1.5;">
# MAGIC     For more common issues and troubleshooting guidance, visit the official Databricks documentation.
# MAGIC   </div>
# MAGIC   <div style="display: flex; gap: 10px; flex-shrink: 0;">
# MAGIC     <a href="https://docs.databricks.com/aws/en/genie/troubleshooting" target="_blank" style="background: white; color: #1B5162; font-size: 14pt; font-weight: 700; padding: 10px 20px; border-radius: 6px; text-decoration: none; white-space: nowrap;">
# MAGIC       AWS →
# MAGIC     </a>
# MAGIC     <a href="https://learn.microsoft.com/en-us/azure/databricks/genie-agents/troubleshooting" target="_blank" style="background: white; color: #1B5162; font-size: 14pt; font-weight: 700; padding: 10px 20px; border-radius: 6px; text-decoration: none; white-space: nowrap;">
# MAGIC       Azure →
# MAGIC     </a>
# MAGIC     <a href="https://docs.databricks.com/gcp/en/genie/troubleshooting" target="_blank" style="background: white; color: #1B5162; font-size: 14pt; font-weight: 700; padding: 10px 20px; border-radius: 6px; text-decoration: none; white-space: nowrap;">
# MAGIC       GCP →
# MAGIC     </a>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C2. Good Spaces Start with Good Tables
# MAGIC
# MAGIC Before adding instructions and examples, make sure your **foundation** is solid.
# MAGIC
# MAGIC The quality of your input tables directly affects how well Genie can answer questions.
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC
# MAGIC <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
# MAGIC
# MAGIC <div style="flex: 1; min-width: 420px; background: #F9F7F4; border-radius: 8px; padding: 20px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 8px; background: #00A972; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 22pt; font-weight: 700; text-align: center; margin: 12px 0 10px 0; color: #00A972;">Do</div>
# MAGIC   <ul style="font-size: 15pt; line-height: 1.7; padding-left: 18px; margin: 0; color: #0b2026;">
# MAGIC     <li style="margin-bottom: 10px;">Aim for <strong>5 or fewer tables</strong>, the more focused the space, the better Genie performs</li>
# MAGIC     <li style="margin-bottom: 10px;">Use <strong>clear, descriptive column names</strong></li>
# MAGIC     <li style="margin-bottom: 10px;">Add <strong>column descriptions</strong> for non-obvious fields</li>
# MAGIC     <li style="margin-bottom: 10px;">Define <strong>foreign key relationships</strong> in Unity Catalog when possible</li>
# MAGIC     <li>Use <strong>curated gold tables</strong> that are analytics-ready</li>
# MAGIC   </ul>
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; min-width: 420px; background: #F9F7F4; border-radius: 8px; padding: 20px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 8px; background: #98182A; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="font-size: 22pt; font-weight: 700; text-align: center; margin: 12px 0 10px 0; color: #98182A;">Avoid</div>
# MAGIC   <ul style="font-size: 15pt; line-height: 1.7; padding-left: 18px; margin: 0; color: #0b2026;">
# MAGIC     <li style="margin-bottom: 10px;">Adding <strong>every table you can think of</strong>. Stay focused!</li>
# MAGIC     <li style="margin-bottom: 10px;">Using tables with <strong>cryptic column names</strong> like <code>col_a</code> or <code>resource_aid</code></li>
# MAGIC     <li style="margin-bottom: 10px;">Blindly using <strong>AI-generated column descriptions</strong> without review</li>
# MAGIC     <li style="margin-bottom: 10px;">Including <strong>raw or staging tables</strong> that need cleanup</li>
# MAGIC     <li>Splitting a wide table into multiple tables. <strong>Keep it as-is</strong></li>
# MAGIC   </ul>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC #### Why Table Quality Matters
# MAGIC No amount of instructions can compensate for poorly structured input data. If your column names are cryptic, your data is inconsistent, or your tables require complex transformations to be useful, Genie will struggle regardless of how much guidance you provide.
# MAGIC
# MAGIC #### Best Practices
# MAGIC - **Use gold tables** - curated, analytics-ready tables that represent the final layer of your data pipeline. This is what we did in the previous demo with the `_gold` suffix tables.
# MAGIC - **Keep tables focused** - An agent with 5 well-chosen tables will outperform an agent with 20 loosely related ones. The more tables you add, the more likely Genie is to pick the wrong one.
# MAGIC - **Define relationships** - If foreign key relationships are defined in Unity Catalog, Genie can use them to determine how tables join together. If they are not defined, document the relationships in instructions.
# MAGIC - **Clear column names** - If a column is named `size`, that is ambiguous. A column named `franchise_size_category` is self-documenting. When you cannot rename columns, add descriptions instead.
# MAGIC - **Don't auto-generate descriptions** - AI-generated column comments can be generic or misleading. Only add descriptions that provide context Genie would not otherwise have.
# MAGIC
# MAGIC #### When to Use Views
# MAGIC If your data model is complex with many self-joins, complicated aggregations, or columns that need transformation consider creating a **view** that simplifies the data for Genie. 
# MAGIC
# MAGIC **A pre-joined, pre-aggregated view can dramatically reduce the complexity of the SQL Genie needs to generate.**
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C3. What Actually Improves Genie Quality
# MAGIC
# MAGIC <br></br>
# MAGIC <!-- TITLE BLOCK -->
# MAGIC <div style="max-width: 1000px; margin: 0 auto 20px auto; font-family: sans-serif; text-align: center;">
# MAGIC   <div style="font-size: 22pt; font-weight: 700; color: #0b2026;">
# MAGIC     Where to Invest Time for the Biggest Impact
# MAGIC   </div>
# MAGIC   <div style="width: 500px; height: 4px; background: #1B5162; margin: 10px auto 0 auto; border-radius: 2px;"></div>
# MAGIC </div>
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="display: flex; gap: 16px;">
# MAGIC
# MAGIC <!-- High Impact -->
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 20px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #02A36F; border-radius: 8px 8px 0 0;"></div>
# MAGIC
# MAGIC   <div style="position: absolute; top: 12px; right: 12px;">
# MAGIC     <img src="https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/icons/green-check.png" style="height: 50px;">
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 12px;">
# MAGIC     High-Impact Levers
# MAGIC   </div>
# MAGIC
# MAGIC   <ul style="font-size: 14pt; line-height: 1.6; padding-left: 20px; margin: 0;">
# MAGIC     <li style="margin-bottom: 10px;"><strong>Start with clear business questions</strong> and a focused scope</li>
# MAGIC     <li style="margin-bottom: 10px;"><strong>Well-described tables and columns</strong> using business language</li>
# MAGIC     <li style="margin-bottom: 10px;"><strong>Example SQL aligned to real usage patterns</strong></li>
# MAGIC     <li><strong>Simple, consistent joins </strong> with a clear row-level meaning</li>
# MAGIC   </ul>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Low Impact -->
# MAGIC <div style="flex: 1; background: #F9F7F4; border-radius: 8px; padding: 20px; position: relative; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #98182A; border-radius: 8px 8px 0 0;"></div>
# MAGIC
# MAGIC   <div style="position: absolute; top: 12px; right: 12px;">
# MAGIC     <img src="https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/icons/warning.png" style="height: 50px;">
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 12px;">
# MAGIC     Low-Impact (Common Traps)
# MAGIC   </div>
# MAGIC
# MAGIC   <ul style="font-size: 14pt; line-height: 1.6; padding-left: 20px; margin: 0;">
# MAGIC     <li style="margin-bottom: 10px;"><strong>Overly long or complex instructions</strong></li>
# MAGIC     <li style="margin-bottom: 10px;"><strong>Adding too many tables upfront</strong></li>
# MAGIC     <li style="margin-bottom: 10px;"><strong>Over-optimizing edge cases early</strong></li>
# MAGIC     <li><strong>Treating Genie as 'set and forget'</strong></li>
# MAGIC   </ul>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC ## Where to Invest Time for the Biggest Impact
# MAGIC
# MAGIC When building a Genie Agent, not all effort produces equal results.  
# MAGIC
# MAGIC Some improvements significantly increase accuracy and usability, while others add complexity without much benefit.
# MAGIC
# MAGIC Focus your time on the areas that have the **largest impact on how Genie understands and answers questions**.
# MAGIC
# MAGIC
# MAGIC ### High-Impact Levers
# MAGIC
# MAGIC These are the areas where your effort will most improve Genie performance:
# MAGIC
# MAGIC - **Start with clear business questions and a focused scope** - Define the key questions you want Genie to answer. Avoid trying to support everything at once.
# MAGIC
# MAGIC - **Well-described tables and columns using business language** - Add clear, human-readable descriptions. Genie relies heavily on this context to interpret user questions correctly.
# MAGIC
# MAGIC - **Example SQL aligned to real usage patterns** - Provide sample queries that reflect how users actually ask questions. These act as patterns Genie can learn from.
# MAGIC
# MAGIC - **Simple, consistent joins with a clear row-level meaning** - Make relationships between tables easy to follow, and ensure each table clearly represents one type of record. Avoid joins that unintentionally duplicate or distort results.
# MAGIC
# MAGIC
# MAGIC ### Low-Impact (Common Traps)
# MAGIC
# MAGIC These are common areas where effort often does not translate into better outcomes:
# MAGIC
# MAGIC - **Overly long or complex instructions** - More text does not mean better results. Keep instructions concise and focused.
# MAGIC
# MAGIC - **Adding too many tables upfront** - A large, unfocused dataset makes it harder for Genie to choose the right data.
# MAGIC
# MAGIC - **Over-optimizing edge cases early** - Focus on the most common and important questions first. Handle edge cases later.
# MAGIC
# MAGIC - **Treating Genie as 'set and forget'**  - Genie improves through iteration. Regularly review results and refine your setup.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Key Takeaway
# MAGIC
# MAGIC Genie works best when you treat it like a product:
# MAGIC
# MAGIC - Start small  
# MAGIC - Focus on clarity  
# MAGIC - Improve based on real usage  
# MAGIC
# MAGIC Investing in the right areas early will lead to **more accurate, consistent, and trustworthy results**.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## D. Genie Agent Authoring Checklist Review
# MAGIC
# MAGIC Everything you learned in this lecture from the curation mindset, the Knowledge Store, the order of operations, and the problem-to-solution mapping  comes together in this general 6-step checklist (steps 3 - 5).
# MAGIC
# MAGIC Use this as a general reference whenever you create or improve a Genie Agent.
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <!--
# MAGIC   HOW TO DIM A STEP DURING TEACHING:
# MAGIC   Add the class "dim" to any step you want grayed out.
# MAGIC   Example: <div class="gsac-step dim" data-step="3" ...>
# MAGIC   Remove the "dim" word to bring it back to full color.
# MAGIC   You can dim multiple steps at once.
# MAGIC -->
# MAGIC <style>
# MAGIC   .gsac-step.dim {
# MAGIC     background: #EEEDE9 !important;
# MAGIC     border-color: #C2C2C2 !important;
# MAGIC     box-shadow: none !important;
# MAGIC     opacity: 0.55;
# MAGIC   }
# MAGIC   .gsac-step.dim .gsac-step-num {
# MAGIC     color: #90A5B1 !important;
# MAGIC   }
# MAGIC   .gsac-step.dim .gsac-step-title {
# MAGIC     color: #5A6F77 !important;
# MAGIC   }
# MAGIC </style>
# MAGIC
# MAGIC <div style="max-width: 1280px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <!-- TITLE BAR -->
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 20px 28px; margin-bottom: 22px;">
# MAGIC   <div style="font-size: 22pt; font-weight: 700; margin-bottom: 6px;">Genie Agent Authoring Checklist</div>
# MAGIC   <div style="font-size: 15pt; font-weight: 400; line-height: 1.45; opacity: 0.95;">A general <b>6-step approach</b> whenever you create a Genie Agent.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- 6-STEP FLOW -->
# MAGIC <div style="display: grid; grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr; gap: 0; align-items: stretch;">
# MAGIC   <div class="gsac-step" data-step="1" style="background: #F9F7F4; border: 3px solid #2574B5; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div class="gsac-step-num" style="font-size: 26pt; font-weight: 800; color: #2574B5; line-height: 1; margin-bottom: 8px;">1</div>
# MAGIC     <div class="gsac-step-title" style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Start with purpose<br>and questions</div>
# MAGIC   </div>
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC   <div class="gsac-step" data-step="2" style="background: #F9F7F4; border: 3px solid #02A36F; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div class="gsac-step-num" style="font-size: 26pt; font-weight: 800; color: #02A36F; line-height: 1; margin-bottom: 8px;">2</div>
# MAGIC     <div class="gsac-step-title" style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Select a minimal<br>data slice</div>
# MAGIC   </div>
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC   <div class="gsac-step" data-step="3" style="background: #F9F7F4; border: 3px solid #F8A805; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div class="gsac-step-num" style="font-size: 26pt; font-weight: 800; color: #F8A805; line-height: 1; margin-bottom: 8px;">3</div>
# MAGIC     <div class="gsac-step-title" style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Add metadata<br>and synonyms</div>
# MAGIC   </div>
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC   <div class="gsac-step" data-step="4" style="background: #F9F7F4; border: 3px solid #FF5F46; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div class="gsac-step-num" style="font-size: 26pt; font-weight: 800; color: #FF5F46; line-height: 1; margin-bottom: 8px;">4</div>
# MAGIC     <div class="gsac-step-title" style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Encode business<br>logic in SQL</div>
# MAGIC   </div>
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC   <div class="gsac-step" data-step="5" style="background: #F9F7F4; border: 3px solid #98182A; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div class="gsac-step-num" style="font-size: 26pt; font-weight: 800; color: #98182A; line-height: 1; margin-bottom: 8px;">5</div>
# MAGIC     <div class="gsac-step-title" style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Add light global<br>text instructions</div>
# MAGIC   </div>
# MAGIC   <div style="display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1;">&rarr;</div>
# MAGIC   <div class="gsac-step" data-step="6" style="background: #F9F7F4; border: 3px solid #1C3037; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div class="gsac-step-num" style="font-size: 26pt; font-weight: 800; color: #1C3037; line-height: 1; margin-bottom: 8px;">6</div>
# MAGIC     <div class="gsac-step-title" style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Test, benchmark,<br>and iterate with users</div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Conclusion
# MAGIC
# MAGIC In this lecture, you learned how to approach Genie Agent curation as an iterative, structured process:
# MAGIC
# MAGIC - A Genie Agent is a **product** that requires ongoing testing and refinement by a domain-expert curator.
# MAGIC - The **iterative curation loop**: create, test, observe, improve
# MAGIC   - This is the core workflow for building an effective space.
# MAGIC - The **Knowledge Store** is the centralized configuration surface within your Genie Agent where you apply these curation tools. It includes space-level metadata, prompt matching (format assistance and entity matching), join relationships, SQL expressions, and knowledge mining recommendations — all scoped to your agent without affecting Unity Catalog.
# MAGIC - **Table quality is the foundation**: Use 5 or fewer focused, well-named gold tables.
# MAGIC   - No amount of instructions can compensate for poorly structured input data.
# MAGIC - The **6-step authoring checklist** brings it all together: start with purpose, select minimal data, add metadata and prompt matching, encode SQL logic, add text instructions, then test and iterate.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
