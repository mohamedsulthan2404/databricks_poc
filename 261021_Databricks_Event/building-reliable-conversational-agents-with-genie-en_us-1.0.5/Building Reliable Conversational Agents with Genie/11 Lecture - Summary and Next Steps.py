# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Lecture - Summary and Next Steps

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Genie Code!
# MAGIC
# MAGIC <br></br>
# MAGIC <div style="max-width: 1200px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #F9F7F4; border-radius: 10px; padding: 24px 28px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); border-top: 6px solid #FF5F46;">
# MAGIC
# MAGIC   <img src="https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/icons/genie-code.png" style="height: 48px; margin-bottom: 10px;">
# MAGIC   <div style="font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 14px;">Try Genie Code to Build Your Next Genie Agent</div>
# MAGIC
# MAGIC   <div style="font-size: 15pt; color: #0b2026; line-height: 1.7; margin-bottom: 16px;">
# MAGIC     Now that you understand the fundamentals of building a Genie Agent, from table selection and Knowledge Store curation to benchmarks and monitoring, try using <strong>Genie Code</strong> to accelerate the process.
# MAGIC   </div>
# MAGIC
# MAGIC   <div style="font-size: 15pt; color: #0b2026; line-height: 1.7; margin-bottom: 18px;">
# MAGIC     Genie Code is your autonomous AI partner for data work. It lives inside notebooks, the SQL editor, and dashboards. It can help you write <code style="background: #EEEDE9; padding: 2px 6px; border-radius: 3px;">ALTER TABLE</code> descriptions, draft example SQL queries, generate benchmark ground truth SQL, and iterate faster on Knowledge Store configuration.
# MAGIC   </div>
# MAGIC
# MAGIC   <a href="https://www.databricks.com/blog/introducing-genie-code" target="_blank" style="display: inline-block; background: #FF5F46; color: white; font-size: 15pt; font-weight: 700; padding: 10px 24px; border-radius: 8px; text-decoration: none;">
# MAGIC     Introducing Genie Code →
# MAGIC   </a>
# MAGIC   <div style="display: flex; gap: 10px; margin-top: 12px;">
# MAGIC     <a href="https://docs.databricks.com/aws/en/genie-code/" target="_blank" style="display: inline-block; background: #1B5162; color: white; font-size: 15pt; font-weight: 700; padding: 10px 24px; border-radius: 8px; text-decoration: none;">
# MAGIC       AWS →
# MAGIC     </a>
# MAGIC     <a href="https://learn.microsoft.com/en-us/azure/databricks/genie-code/" target="_blank" style="display: inline-block; background: #1B5162; color: white; font-size: 15pt; font-weight: 700; padding: 10px 24px; border-radius: 8px; text-decoration: none;">
# MAGIC       Azure →
# MAGIC     </a>
# MAGIC     <a href="https://docs.databricks.com/gcp/en/genie-code/" target="_blank" style="display: inline-block; background: #1B5162; color: white; font-size: 15pt; font-weight: 700; padding: 10px 24px; border-radius: 8px; text-decoration: none;">
# MAGIC       GCP →
# MAGIC     </a>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Additional Resources
# MAGIC
# MAGIC Explore the following resources to learn more about Genie and stay up to date with the latest platform updates.
# MAGIC
# MAGIC ### A1. Documentation
# MAGIC
# MAGIC - AI/BI release notes - Stay informed about new features, improvements, and platform updates:
# MAGIC [AWS](https://docs.databricks.com/aws/en/ai-bi/release-notes/) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/ai-bi/release-notes/) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/ai-bi/release-notes/)
# MAGIC
# MAGIC - What is a Genie Agent - Learn more about Genie, a Databricks feature that allows business teams to interact with their data using natural language:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie/) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/)
# MAGIC
# MAGIC ### A2. Blog and Announcements
# MAGIC
# MAGIC - [AI/BI Genie is now Generally Available](https://www.databricks.com/blog/aibi-genie-now-generally-available) - With the new Knowledge Store, upcoming Deep Research and democratized access through Genie One, Genie is ready to answer your organization's most complex data questions.
# MAGIC
# MAGIC - [How to Build Production-Ready Genie Spaces, and Build Trust Along the Way](https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way) - A journey of building a Genie space from scratch to production-ready, improving accuracy through benchmark evaluation and systematic optimization
# MAGIC
# MAGIC - [Introducing Databricks Genie](https://www.databricks.com/blog/introducing-databricks-one) - A Simple Way to Bring Data + AI to Every Business User
# MAGIC
# MAGIC - [Use Genie Everywhere with Enterprise OAuth](https://www.databricks.com/blog/access-genie-everywhere) - Databricks Genie, users can now talk to their data directly from the tools they already use: Teams, Slack, Confluence, or custom web apps.
# MAGIC
# MAGIC - [5 key lessons from implementing AI/BI Genie for self-service marketing insights](https://www.databricks.com/blog/5-key-lessons-implementing-aibi-genie-self-service-marketing-insights) - How to build high-quality Genie Agents that marketers can trust
# MAGIC
# MAGIC ### A3. Additional Features Outside the Scope of this Course
# MAGIC
# MAGIC - Analyzing files (unstructured data) in volumes with a Genie Agent is in **Beta**:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie-agents/volumes) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/volumes) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie-agents/volumes) 
# MAGIC
# MAGIC
# MAGIC - Use parameters in SQL queries in Genie:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/add-instructions#add-query-parameters) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/tune-quality#add-query-parameters) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/add-instructions#add-query-parameters)
# MAGIC
# MAGIC - Use trusted assets in Genie Agents:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/add-instructions#trusted-assets) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/tune-quality#trusted-assets) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/add-instructions#trusted-assets)
# MAGIC
# MAGIC - Unity Catalog metric views as a source to Genie:
# MAGIC [AWS](https://docs.databricks.com/aws/en/metric-views/) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/uc-semantics/metric-views/) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/metric-views/)
# MAGIC
# MAGIC - Agent mode in Genie Agents:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/agent-mode) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/concepts#agent-mode) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/agent-mode)
# MAGIC
# MAGIC - Chat in Genie:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie-ui/genie-chat) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-one/chat) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie-ui/genie-chat)
# MAGIC
# MAGIC - Use Agent Bricks: Supervisor Agent to create a coordinated multi-agent system:
# MAGIC [AWS](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/multi-agent-supervisor) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/agents/agent-bricks/multi-agent-supervisor) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/generative-ai/agent-bricks/multi-agent-supervisor)
# MAGIC
# MAGIC - Use the Genie API to integrate Genie into your applications:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/conversation-api) |
# MAGIC [Azure](https://learn.microsoft.com/en-in/azure/databricks/genie-agents/conversation-api) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/conversation-api)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Next Steps
# MAGIC
# MAGIC Continue building your Databricks skills with additional training and certification resources.
# MAGIC
# MAGIC ### B1. Continue Your Learning
# MAGIC
# MAGIC Expand your data and AI knowledge through Databricks self-paced and instructor-led training. These courses help you deepen your technical skills and gain hands-on experience with the Databricks platform.
# MAGIC
# MAGIC Visit the [Databricks Training and Certification](https://www.databricks.com/learn/training/home)
# MAGIC
# MAGIC - [Building Semantic Models in Databricks with UC Metric Views](https://www.databricks.com/training/catalog/building-semantic-models-in-databricks-with-uc-metric-views-4962)
# MAGIC
# MAGIC - [AI/BI for Data Analysts](https://www.databricks.com/training/catalog/aibi-for-data-analysts-3707)
# MAGIC
# MAGIC ### B2. Earn a Certification
# MAGIC
# MAGIC Validate your Databricks expertise by earning an official credential. Certifications demonstrate your ability to apply Databricks technologies in real-world data and AI workloads.
# MAGIC
# MAGIC Visit the [Databricks Certification and Badging](https://www.databricks.com/learn/training/certification)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
