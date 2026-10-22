# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">Informational context. Use for helpful background, tips, or extra detail.</div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #FFAB00; background: rgba(255,171,0,0.12); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#0b2026; margin-bottom:6px; font-size:15pt;">Warning</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC   A warning. Use to flag a caveat, limitation, or something the reader should watch for.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #FF5F46; background: rgba(255,95,70,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#98102A; margin-bottom:6px; font-size:15pt;">Error</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC   An error or danger message. Use to highlight critical issues or anti-patterns to avoid.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #00A972; background: rgba(0,169,114,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#00A972; margin-bottom:6px; font-size:15pt;">Success</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC   A success or confirmation message. Use to flag a good outcome or a recommended practice.
# MAGIC   
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC   A neutral note. Use for remarks or observations the reader should keep in mind.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ## Theme Light
# MAGIC
# MAGIC | Color | Hex |
# MAGIC |------|------|
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#0b2026;border:1px solid #ccc;"></span> | #0b2026 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#F9F7F4;border:1px solid #ccc;"></span> | #F9F7F4 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FF5F46;border:1px solid #ccc;"></span> | #FF5F46 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#EEEDE9;border:1px solid #ccc;"></span> | #EEEDE9 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#1B5162;border:1px solid #ccc;"></span> | #1B5162 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#00A972;border:1px solid #ccc;"></span> | #00A972 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#98102A;border:1px solid #ccc;"></span> | #98102A |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FFAB00;border:1px solid #ccc;"></span> | #FFAB00 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#618794;border:1px solid #ccc;"></span> | #618794 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#4299E0;border:1px solid #ccc;"></span> | #4299E0 |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Custom
# MAGIC
# MAGIC | Color | Hex |
# MAGIC |------|------|
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#C2C2C2;border:1px solid #ccc;"></span> | #C2C2C2 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#801C17;border:1px solid #ccc;"></span> | #801C17 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FABFBA;border:1px solid #ccc;"></span> | #FABFBA |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FF9E94;border:1px solid #ccc;"></span> | #FF9E94 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FF3621;border:1px solid #ccc;"></span> | #FF3621 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FF6952;border:1px solid #ccc;"></span> | #FF6952 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FF5F46;border:1px solid #ccc;"></span> | #FF5F46 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FF8774;border:1px solid #ccc;"></span> | #FF8774 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#CD7F32;border:1px solid #ccc;"></span> | #CD7F32 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#F9F7F4;border:1px solid #ccc;"></span> | #F9F7F4 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FFCC66;border:1px solid #ccc;"></span> | #FFCC66 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#FFAB00;border:1px solid #ccc;"></span> | #FFAB00 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#EEEDE9;border:1px solid #ccc;"></span> | #EEEDE9 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#00A972;border:1px solid #ccc;"></span> | #00A972 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#0B2026;border:1px solid #ccc;"></span> | #0B2026 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#618794;border:1px solid #ccc;"></span> | #618794 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#1B3139;border:1px solid #ccc;"></span> | #1B3139 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#5A6F77;border:1px solid #ccc;"></span> | #5A6F77 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#DCE0E2;border:1px solid #ccc;"></span> | #DCE0E2 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#303F47;border:1px solid #ccc;"></span> | #303F47 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#90A5B1;border:1px solid #ccc;"></span> | #90A5B1 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#2272B4;border:1px solid #ccc;"></span> | #2272B4 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#C4CCD6;border:1px solid #ccc;"></span> | #C4CCD6 |
# MAGIC | <span style="display:inline-block;width:18px;height:18px;background:#98102A;border:1px solid #ccc;"></span> | #98102A |
# MAGIC
