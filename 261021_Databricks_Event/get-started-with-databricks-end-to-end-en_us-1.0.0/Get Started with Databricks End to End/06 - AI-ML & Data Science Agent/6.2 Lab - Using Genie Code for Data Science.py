# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC # BONUS Lab - Using Genie Code for Data Science
# MAGIC ##### This bonus lab is designed to be completed after the live class. There will not be enough time to finish it during the live training session.
# MAGIC
# MAGIC ### Estimated Duration: ~25 minutes
# MAGIC
# MAGIC
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC Genie Code can read your data, suggest models, write the code, and run it, all from natural-language prompts. In this demonstration you will use Genie Code against the bakehouse dataset to explore data, perform exploratory data analysis, and build and evaluate machine learning models. Throughout the notebook you will paste ready-made prompts into the Genie Code Agent interface, review the generated code, and interpret the results like a data scientist.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this demonstration, you will be able to:
# MAGIC
# MAGIC 1. **Enable and configure Genie Code** in Genie and toggle Agent mode.
# MAGIC 2. **Use natural language prompts** to perform exploratory data analysis on datasets.
# MAGIC 3. **Generate data visualizations and statistical summaries** through Genie.
# MAGIC 4. **Build and evaluate machine learning models** using Genie.
# MAGIC 5. **Apply best practices** for Genie-assisted data science workflows.
# MAGIC
# MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC   <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC     <div>
# MAGIC       <strong style="color: #e65100; font-size: 1.1em;">Warning - Review AI Output</strong>
# MAGIC       <p style="margin: 8px 0 0 0; color: #333;">Genie Code generates and executes code. Always review what it is about to run before approving, like you would for a teammate's pull request.</p>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - Select a Compute Environment
# MAGIC
# MAGIC <div style="border-left: 4px solid #FF5F46; background: rgba(255,95,70,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#98102A; margin-bottom:6px; font-size:15pt;">Select Serverless Compute</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC
# MAGIC Before starting this notebook, select the required compute environment listed below.
# MAGIC
# MAGIC - **Serverless Compute, Version 5**
# MAGIC
# MAGIC ![Serverless Select](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/select-compute.png)
# MAGIC
# MAGIC <br></br>
# MAGIC How to select an environment version:
# MAGIC [AWS](https://docs.databricks.com/aws/en/compute/serverless/dependencies#-select-an-environment-version) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies#-select-an-environment-version) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/compute/serverless/dependencies#-select-an-environment-version)
# MAGIC
# MAGIC **NOTE:** This notebook requires **SQL and Python**, and was tested using **Serverless V5**. All-purpose compute may work but is not guaranteed to behave the same or support all features demonstrated.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Classroom Setup
# MAGIC
# MAGIC Run the cell below. It will:
# MAGIC
# MAGIC 1. Create or use your personal catalog named **labuser_UNIQUE_ID**.
# MAGIC 2. Create a schema called **ai_ml_ds**.
# MAGIC 3. Set your default catalog and schema.

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-ai-ml-ds

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Getting Started with Genie Code

# COMMAND ----------

# MAGIC %md
# MAGIC ### B1. Best Practices for AI-Assisted Data Science
# MAGIC
# MAGIC As you work through this demonstration, keep the following best practices in mind:
# MAGIC
# MAGIC 1. **Clear prompts:** Provide specific, context-rich prompts referencing datasets with `@table_name`.
# MAGIC 2. **Iterative refinement:** Use follow-up prompts to refine and improve results.
# MAGIC 3. **Human oversight:** Always review and validate generated code and insights.
# MAGIC 4. **Domain knowledge:** Combine AI capabilities with your domain expertise.
# MAGIC 5. **Documentation:** Use Genie Code to help document and explain complex analyses.

# COMMAND ----------

# MAGIC %md
# MAGIC ### B2. Access Genie Code
# MAGIC
# MAGIC To begin using Genie Code, open the Genie Code side panel in your notebook by clicking ![Genie.png](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/Genie.png "Genie Icon").

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Data Discovery and Initial Exploration
# MAGIC
# MAGIC Genie Code can help you discover and understand datasets through natural language queries. We will start by exploring available data sources.

# COMMAND ----------

# MAGIC %md
# MAGIC ### C1. Discover Available Datasets
# MAGIC
# MAGIC Use Genie Code to find suitable datasets for our analysis. Paste the prompt below into the Agent interface.
# MAGIC
# MAGIC **NOTE:** Genie Code should find the `sales_transactions` table in the `samples.bakehouse` catalog/schema. If it does not, check that the `samples.bakehouse` dataset is available in the Catalog Explorer.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Find a dataset that contains bakehouse sales transaction data.</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### C2. Initial Data Examination
# MAGIC
# MAGIC Now that you have identified a dataset, use Genie Code to perform an initial examination. Paste the prompt below into Genie Code.
# MAGIC
# MAGIC After pasting, place the cursor at the end of the words `@sales_transactions`, then select the name of the table from the list that pops up above the prompt window and execute the prompt. Sending the following prompt will push Genie Code to execute code on your behalf. 
# MAGIC
# MAGIC **NOTE:** If Genie Code needs to execute code, it will ask for your approval unless you have already changed permissions with Genie Code prior to this training.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Describe the @sales_transactions dataset. Show me the schema, first few rows, and basic statistics about the data.</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Comprehensive Exploratory Data Analysis
# MAGIC
# MAGIC Genie Code can perform sophisticated EDA tasks through natural language instructions. This section guides you through comprehensive data exploration.

# COMMAND ----------

# MAGIC %md
# MAGIC ### D1. Statistical Analysis and Data Profiling
# MAGIC
# MAGIC Use Genie Code to generate comprehensive statistical summaries and identify data quality issues. Use the same process as above to execute the prompt below. Genie Code will write cells in this notebook and execute code. Once EDA has been performed, select **accept all** in Genie Code to confirm the generated cells. 
# MAGIC
# MAGIC **NOTE:** You may again have to place the cursor at the end of the words `@sales_transactions` and select the name of the table from the list that pops up above the prompt window.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Perform comprehensive EDA on @sales_transactions. I want to understand column statistics, data distributions, missing values, and potential data quality issues. Generate correlation analysis and heatmaps to identify relationships between numeric columns. Analyze the data to identify business insights and any anomalies or outliers that need attention. Think like a data scientist and provide insights.</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Machine Learning Model Development
# MAGIC
# MAGIC Now we will use Genie Code to build and evaluate machine learning models based on our exploratory analysis.

# COMMAND ----------

# MAGIC %md
# MAGIC ### E1. Define the Machine Learning Problem
# MAGIC
# MAGIC Work with Genie Code to identify appropriate machine learning use cases based on your data exploration. Use the same process as above to execute the prompt below.
# MAGIC
# MAGIC **NOTE:** When Genie Code suggests a use case, ask yourself: does it match a real business question? Would I be able to act on this if it worked?

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Which machine learning use cases would you recommend with this data?</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### E2. Data Preparation and Feature Engineering
# MAGIC
# MAGIC Use Genie Code to prepare your data for machine learning, including feature engineering and data preprocessing. Use the same process as above to execute the prompt below.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Identify which features most influence customer purchase behavior and product preferences, guiding inventory management and marketing strategies.</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## F. Optional: Further ML Tasks
# MAGIC #### Please complete outside of a live teach.
# MAGIC
# MAGIC In the sections that follow, you can continue building with Genie Code. Though this is recommended, it is not required for this training. At the very least, view the prompts that follow to understand how you can use Genie Code
# MAGIC 1. Perform model training and evaluation
# MAGIC 2. Perform model optimization and tune hyperparameters
# MAGIC 3. Extract feature importance
# MAGIC 4. Determine business recommendations based off your ML results

# COMMAND ----------

# MAGIC %md
# MAGIC ### F1. Model Training and Evaluation
# MAGIC
# MAGIC Leverage Genie Code to build, train, and evaluate multiple machine learning models. Use the same process as above to execute the prompt below.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Train multiple machine learning models on our prepared dataset to predict which product customers will purchase using the most important features. Compare different algorithms (e.g., Random Forest, Gradient Boosting, Logistic Regression) and evaluate them using appropriate metrics. Show me model performance comparisons and feature importance.</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### F2. Model Optimization and Hyperparameter Tuning
# MAGIC
# MAGIC Use Genie Code to optimize your best-performing model through hyperparameter tuning. Use the same process as above to execute the prompt below.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Perform hyperparameter tuning on the best-performing model from our comparison. Use techniques like grid search or random search to optimize model performance. Show me the improvement in metrics after tuning.</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### F3. Feature Importance and Model Explainability
# MAGIC
# MAGIC Use the same process as above to execute the prompt below.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Analyze the feature importance of our final model. Create visualizations showing which features are most predictive of product purchases and explain what this means for the bakehouse business. Use SHAP values or other explainability techniques if appropriate.</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### F4. Business Recommendations
# MAGIC
# MAGIC Use the same process as above to execute the prompt below.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
# MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
# MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
# MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
# MAGIC   </div>
# MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Based on our EDA and machine learning results, provide business recommendations and actionable insights for the bakehouse franchise. What should stakeholders know about customer purchasing patterns we discovered? What are the next steps for deploying or improving this model?</pre>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## G. Conclusion
# MAGIC
# MAGIC In this demonstration, you used Genie Code in Agent mode to run an end-to-end data science workflow with natural language:
# MAGIC
# MAGIC 1. Enabled and configured Genie Code and toggled Agent mode.
# MAGIC 2. Discovered and examined the `sales_transactions` dataset from `samples.bakehouse`.
# MAGIC 3. Performed comprehensive exploratory data analysis, including statistics, distributions, and correlation analysis.
# MAGIC 4. Built, compared, and tuned multiple machine learning models to predict customer product purchases.
# MAGIC 5. Interpreted feature importance and translated results into actionable business recommendations.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
