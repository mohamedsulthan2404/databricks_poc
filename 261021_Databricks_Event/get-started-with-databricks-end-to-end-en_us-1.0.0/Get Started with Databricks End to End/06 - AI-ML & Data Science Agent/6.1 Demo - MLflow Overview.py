# Databricks notebook source
# MAGIC %md
# MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Tracking and managing models with MLflow
# MAGIC
# MAGIC In this demo, we will explore the model development lifecycle using MLflow with bakehouse sales data. You'll train a model to predict product purchases, log artifacts, metrics, and parameters using MLflow, and then register the model in Unity Catalog for production readiness. 
# MAGIC
# MAGIC You don't need to be a data scientist to follow along. This lesson shows you what model training looks like in Databricks so you can recognize the pattern when working with data science teams.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC - Prepare features using SQL from bakehouse sales transactions
# MAGIC - Train and log models using MLflow
# MAGIC - Track experiments and view runs using MLflow UI
# MAGIC - Register a model in Unity Catalog
# MAGIC - Use model version aliases like `staging` and `dev`

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
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Key Terms
# MAGIC
# MAGIC Before you begin, review the definitions for the machine learning concepts used in this lesson.
# MAGIC
# MAGIC | Term | Definition |
# MAGIC | --- | --- |
# MAGIC | **Features** | Input variables used to make predictions. In this case, these are customer behaviors like transaction count, average purchase amount, and payment preferences. |
# MAGIC | **Train a model** | The process of teaching a machine learning algorithm to recognize patterns in data. The model learns by analyzing examples (training data) to make predictions on new data. |
# MAGIC | **MLflow** | An open-source platform for managing the complete machine learning lifecycle, including experiment tracking, model versioning, and deployment. |
# MAGIC | **Experiments** | A collection of related model training runs, which organizes all attempts to solve a specific prediction problem. |
# MAGIC | **Runs** | A single execution of model training code. Each run captures parameters (settings), metrics (performance scores), and artifacts (the trained model files). |
# MAGIC | **Register a model** | The process of saving a trained model to a centralized registry (Unity Catalog) where it can be versioned, shared, and deployed. |
# MAGIC | **Model version aliases** | Human-readable labels (like `dev`, `staging`, `production`) that point to specific model versions, making it easier to manage which model is deployed where. |

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Classroom Setup
# MAGIC
# MAGIC Run the cell below to prepare your environment. This setup script will:
# MAGIC
# MAGIC 1. Create or use your personal catalog named **labuser_UNIQUE_ID**.
# MAGIC 2. Create a schema called **ai_ml_ds**.
# MAGIC 3. Set your default catalog and schema.

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-ai-ml-ds

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Data Preparation with SQL
# MAGIC
# MAGIC In this first part, you will use SQL to read and prepare **features** from the bakehouse sales transactions that will be used for building your machine learning model later. You will create features that help predict which product a customer will purchase based on:
# MAGIC
# MAGIC - Customer purchase history (total transactions, average quantity)
# MAGIC - Franchise characteristics
# MAGIC - Transaction timing patterns
# MAGIC - Payment behavior

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create features from sales transactions
# MAGIC -- We'll aggregate customer behavior to predict their next product purchase
# MAGIC CREATE OR REPLACE TABLE customer_features AS
# MAGIC SELECT 
# MAGIC   customerID,
# MAGIC   franchiseID,
# MAGIC   product,
# MAGIC   -- Purchase behavior features
# MAGIC   COUNT(*) as transaction_count,
# MAGIC   AVG(quantity) as avg_quantity,
# MAGIC   AVG(totalPrice) as avg_total_price,
# MAGIC   SUM(totalPrice) as total_spent,
# MAGIC   -- Payment preference (encode as numbers)
# MAGIC   SUM(CASE WHEN paymentMethod = 'visa' THEN 1 ELSE 0 END) as visa_count,
# MAGIC   SUM(CASE WHEN paymentMethod = 'mastercard' THEN 1 ELSE 0 END) as mastercard_count,
# MAGIC   SUM(CASE WHEN paymentMethod = 'amex' THEN 1 ELSE 0 END) as amex_count,
# MAGIC   -- Time-based features
# MAGIC   HOUR(MAX(dateTime)) as last_purchase_hour,
# MAGIC   DAYOFWEEK(MAX(dateTime)) as last_purchase_day
# MAGIC FROM samples.bakehouse.sales_transactions
# MAGIC GROUP BY customerID, franchiseID, product;
# MAGIC
# MAGIC SELECT * FROM customer_features LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ### C1. Prepare Training Data
# MAGIC
# MAGIC Now that you've created a feature table using SQL, you need to prepare the data for machine learning:
# MAGIC
# MAGIC 1. **Convert to Pandas** - Transform the SQL results into a Pandas DataFrame for scikit-learn compatibility.
# MAGIC 2. **Encode the target** - Convert product names (text) into numeric labels that the model can predict.
# MAGIC 3. **Select features** - Choose which columns will be used as input features for prediction.
# MAGIC 4. **Split the data** - Divide into training (80%) and testing (20%) sets to evaluate model performance.
# MAGIC
# MAGIC This step transforms your business data into the format required for machine learning model training.
# MAGIC
# MAGIC **NOTE:** You convert the Spark DataFrame to a Pandas DataFrame (using `.toPandas()`) because the ML library used in this example, scikit-learn, works with Pandas DataFrames.

# COMMAND ----------

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Convert the SQL results to Pandas DataFrame
training_df = spark.sql("SELECT * FROM customer_features").toPandas()

# Encode the target variable (product) as numeric
le = LabelEncoder()
training_df['product_encoded'] = le.fit_transform(training_df['product'])

# Select features and target
feature_cols = ['franchiseID', 'transaction_count', 'avg_quantity', 'avg_total_price', 
                'total_spent', 'visa_count', 'mastercard_count', 'amex_count',
                'last_purchase_hour', 'last_purchase_day']

X = training_df[feature_cols]
y = training_df['product_encoded']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")
print(f"Products to predict: {list(le.classes_)}")

# COMMAND ----------

# Display the training data with features and target
display(training_df[feature_cols + ['product', 'product_encoded']].head(20))

# COMMAND ----------

# DBTITLE 1,Cell 12
# MAGIC %md-sandbox
# MAGIC ## D. Walkthrough of the Run Block
# MAGIC
# MAGIC The panel below breaks down the key lines of the training run. **Click a highlighted line or an annotation chip** to reveal an explanation of what that line contributes to the tracked run.
# MAGIC
# MAGIC <div id="sx-mount"></div>
# MAGIC
# MAGIC <style>
# MAGIC   .sx-wrap { position: relative; font-family: sans-serif; border: 1px solid #DCE0E2; border-radius: 12px; overflow: hidden; background: #F9F7F4; margin: 16px 0; }
# MAGIC   .sx-title { background: #EEEDE9; border-bottom: 1px solid #DCE0E2; padding: 8px 14px; font-size: 14pt; font-weight: 700; color: #5A6F77; }
# MAGIC   .sx-rail { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 14px; background: #F8F9FC; border-bottom: 1px solid #EEEDE9; }
# MAGIC   .sx-chip { border: 1px solid #DCE0E2; background: #FFFFFF; border-radius: 999px; padding: 5px 12px; font-size: 14pt; font-weight: 700; color: #1B3139; cursor: pointer; }
# MAGIC   .sx-chip:hover, .sx-chip.active { background: rgba(66,153,224,0.12); border-color: #4299E0; color: #2272B4; }
# MAGIC   .sx-chip-hovered-from-line { background: rgba(66,153,224,0.12); border-color: #4299E0; color: #2272B4; }
# MAGIC   .sx-code { padding: 10px 0; overflow-x: auto; font-size: 14pt; line-height: 1.55; }
# MAGIC   .sx-code, .sx-line-code { font-family: Menlo, Consolas, monospace !important; }
# MAGIC   .sx-line { display: grid; grid-template-columns: 52px 1fr; }
# MAGIC   .sx-line.no-lines { grid-template-columns: 1fr; }
# MAGIC   .sx-line.no-lines .sx-line-code { padding-left: 16px; }
# MAGIC   .sx-line-no { color: #5A6F77; text-align: right; padding: 0 12px; user-select: none; border-right: 1px solid #EEEDE9; }
# MAGIC   .sx-line-code { padding: 0 16px; white-space: pre; }
# MAGIC   .sx-active-line { background: rgba(66,153,224,0.18); }
# MAGIC   .sx-active-line .sx-line-code { border-left: 3px solid #4299E0; padding-left: 13px; }
# MAGIC   .sx-line.sx-active-line { background: rgba(66,153,224,0.18); }
# MAGIC   .sx-line.sx-active-line .sx-line-code { border-left: 3px solid #4299E0; padding-left: 13px; }
# MAGIC   .sx-hotspot { background: rgba(66,153,224,0.08); cursor: pointer; }
# MAGIC   .sx-hotspot .sx-line-code { border-left: 3px solid rgba(66,153,224,0.5); padding-left: 13px; }
# MAGIC   .sx-hotspot:hover, .sx-hovered-from-chip { background: rgba(66,153,224,0.16); }
# MAGIC   .sx-line.sx-hotspot.sx-active-line { background: rgba(66,153,224,0.22) !important; }
# MAGIC   .sx-line.sx-hotspot.sx-active-line .sx-line-code { border-left: 3px solid #4299E0 !important; padding-left: 13px !important; }
# MAGIC   .sx-hotspot .sx-line-no { color: #2272B4; font-weight: 700; }
# MAGIC   .sx-overlay { display: none; position: absolute; right: 18px; top: 96px; width: 360px; max-width: calc(100% - 36px); background: #FFFFFF; border: 1px solid #DCE0E2; border-left: 5px solid #4299E0; border-radius: 12px; box-shadow: 0 6px 18px rgba(27,49,57,0.12), 0 16px 36px rgba(27,49,57,0.10); padding: 14px 16px; z-index: 5; }
# MAGIC   .sx-overlay-title { font-weight: 800; font-size: 15pt; margin-bottom: 6px; color: #1B3139; }
# MAGIC   .sx-overlay-body { color: #0b2026; line-height: 1.45; font-size: 14pt; }
# MAGIC </style>
# MAGIC
# MAGIC <script>
# MAGIC (function () {
# MAGIC   const config = {
# MAGIC     mountId: "sx-mount",
# MAGIC     title: "MLflow Breakdown",
# MAGIC     showAnnotationRail: true,
# MAGIC     hotspots: [
# MAGIC       {
# MAGIC         title: "Start the run",
# MAGIC         startLine: 1,
# MAGIC         endLine: 1,
# MAGIC         description: "<code>mlflow.start_run()</code> opens a named run inside the active experiment. Everything logged within this <code>with</code> block is attached to this single run, and the <em>run object</em> exposes metadata such as <code>run.info.run_id</code>."
# MAGIC       },
# MAGIC       {
# MAGIC         title: "Enable autolog",
# MAGIC         startLine: 7,
# MAGIC         endLine: 10,
# MAGIC         description: "<code>mlflow.sklearn.autolog()</code> automatically captures parameters, metrics, and the model. It <em>must</em> be called before <code>fit()</code> so training-phase values are recorded. <code>log_input_examples=True</code> stores sample inputs and <code>silent=True</code> suppresses autolog warnings."
# MAGIC       },
# MAGIC       {
# MAGIC         title: "Fit the model",
# MAGIC         startLine: 13,
# MAGIC         endLine: 13,
# MAGIC         description: "Training the estimator with <code>fit()</code> triggers autologging. Parameters like <code>n_estimators</code> and training metrics are logged to the run without any explicit logging calls."
# MAGIC       },
# MAGIC       {
# MAGIC         title: "Log custom metric",
# MAGIC         startLine: 19,
# MAGIC         endLine: 19,
# MAGIC         description: "<code>mlflow.log_metric()</code> records a metric autolog does not compute — here the macro-averaged test F1 score. Custom metrics complement autologged values for a fuller picture of model quality."
# MAGIC       },
# MAGIC       {
# MAGIC         title: "Log the model",
# MAGIC         startLine: 21,
# MAGIC         endLine: 26,
# MAGIC         description: "<code>mlflow.sklearn.log_model()</code> saves the trained model as a versioned artifact. The <code>signature</code> from <code>infer_signature()</code> records the input/output schema and <code>input_example</code> stores a sample payload for validation and serving."
# MAGIC       },
# MAGIC       {
# MAGIC         title: "Build the model URI",
# MAGIC         startLine: 28,
# MAGIC         endLine: 28,
# MAGIC         description: "The <code>runs:/&lt;run_id&gt;/model-artifacts</code> URI uniquely references the logged model within this run. Use it to load the model later or to register it in the Model Registry."
# MAGIC       }
# MAGIC     ],
# MAGIC     source: `with mlflow.start_run(run_name='bakehouse-product-prediction-run') as run:
# MAGIC     # Initialize the Random Forest classifier
# MAGIC     rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
# MAGIC
# MAGIC     # Enable automatic logging of inputs, metrics, parameters, and models
# MAGIC     # Must be called BEFORE fit() to capture training-phase values
# MAGIC     mlflow.sklearn.autolog(
# MAGIC         log_input_examples=True,
# MAGIC         silent=True
# MAGIC     )
# MAGIC
# MAGIC     # Fit the model on the training data
# MAGIC     rf_classifier.fit(X_train, y_train)
# MAGIC
# MAGIC     # Make predictions on the test data
# MAGIC     y_pred = rf_classifier.predict(X_test)
# MAGIC
# MAGIC     # Calculate F1 score with 'macro' averaging for multiclass
# MAGIC     mlflow.log_metric("test_f1", f1_score(y_test, y_pred, average='macro'))
# MAGIC
# MAGIC     mlflow.sklearn.log_model(
# MAGIC         rf_classifier,
# MAGIC         artifact_path="model-artifacts",
# MAGIC         input_example=X_train[:3],
# MAGIC         signature=infer_signature(X_train, y_train)
# MAGIC     )
# MAGIC
# MAGIC     model_uri = f"runs:/{run.info.run_id}/model-artifacts"`,
# MAGIC     showLineNumbers: true,
# MAGIC     displayStartLine: 1,
# MAGIC   };
# MAGIC
# MAGIC   function escapeHtml(value) {
# MAGIC     return String(value)
# MAGIC       .replace(/&/g, "&amp;")
# MAGIC       .replace(/</g, "&lt;")
# MAGIC       .replace(/>/g, "&gt;");
# MAGIC   }
# MAGIC
# MAGIC   function renderSourceExplorer(config) {
# MAGIC     const mount = document.getElementById(config.mountId);
# MAGIC     const lines = config.source.replace(/\n$/, "").split("\n");
# MAGIC     const start = config.startLine || 1;
# MAGIC     const end = config.endLine || lines.length;
# MAGIC     const visible = lines.slice(start - 1, end);
# MAGIC     const hotspots = config.hotspots || [];
# MAGIC     const displayStartLine = config.displayStartLine || start;
# MAGIC
# MAGIC     function hotspotFor(lineNo) {
# MAGIC       const index = hotspots.findIndex(h => lineNo >= h.startLine && lineNo <= h.endLine);
# MAGIC       return index >= 0 ? { hotspot: hotspots[index], index } : null;
# MAGIC     }
# MAGIC
# MAGIC     const codeHtml = visible.map((line, idx) => {
# MAGIC       const actualLineNo = start + idx;
# MAGIC       const displayLineNo = displayStartLine + idx;
# MAGIC       const hotspot = hotspotFor(actualLineNo);
# MAGIC
# MAGIC       const classes = hotspot
# MAGIC         ? `sx-line sx-hotspot sx-hotspot-${hotspot.index}`
# MAGIC         : "sx-line";
# MAGIC
# MAGIC       const attrs = hotspot
# MAGIC         ? `data-hotspot-index="${hotspot.index}"`
# MAGIC         : "";
# MAGIC
# MAGIC       return `
# MAGIC         <div class="${classes} ${config.showLineNumbers ? "" : "no-lines"}" ${attrs}>
# MAGIC           ${config.showLineNumbers
# MAGIC             ? `<div class="sx-line-no">${displayLineNo}</div>`
# MAGIC             : ""}
# MAGIC           <div class="sx-line-code">${escapeHtml(line)}</div>
# MAGIC         </div>`;
# MAGIC     }).join("");
# MAGIC
# MAGIC     const railHtml = config.showAnnotationRail && hotspots.length > 0
# MAGIC       ? `<div class="sx-rail">
# MAGIC           ${hotspots.map((h, i) => `
# MAGIC             <button class="sx-chip" data-hotspot-index="${i}">
# MAGIC               ${escapeHtml(h.title)}
# MAGIC             </button>
# MAGIC           `).join("")}
# MAGIC         </div>`
# MAGIC       : "";
# MAGIC
# MAGIC     const overlayHtml = hotspots.length > 0
# MAGIC       ? `<div class="sx-overlay">
# MAGIC           <div class="sx-overlay-title"></div>
# MAGIC           <div class="sx-overlay-body"></div>
# MAGIC         </div>`
# MAGIC       : "";
# MAGIC
# MAGIC     mount.innerHTML = `
# MAGIC       <div class="sx-wrap">
# MAGIC         <div class="sx-title">${escapeHtml(config.title)}</div>
# MAGIC         ${railHtml}
# MAGIC         <div class="sx-code">${codeHtml}</div>
# MAGIC         ${overlayHtml}
# MAGIC       </div>`;
# MAGIC
# MAGIC     if (hotspots.length === 0) return;
# MAGIC
# MAGIC     const overlay = mount.querySelector(".sx-overlay");
# MAGIC     const overlayTitle = mount.querySelector(".sx-overlay-title");
# MAGIC     const overlayBody = mount.querySelector(".sx-overlay-body");
# MAGIC     let activeHotspotIndex = null;
# MAGIC
# MAGIC     function setActiveLines(idx) {
# MAGIC       mount.querySelectorAll(".sx-active-line").forEach(el => {
# MAGIC         el.classList.remove("sx-active-line");
# MAGIC       });
# MAGIC       if (idx === null) return;
# MAGIC       mount.querySelectorAll(`.sx-hotspot-${idx}`).forEach(el => {
# MAGIC         el.classList.add("sx-active-line");
# MAGIC       });
# MAGIC     }
# MAGIC
# MAGIC     function setActiveChip(idx) {
# MAGIC       mount.querySelectorAll(".sx-chip").forEach(chip => {
# MAGIC         chip.classList.toggle(
# MAGIC           "active",
# MAGIC           idx !== null && Number(chip.dataset.hotspotIndex) === idx
# MAGIC         );
# MAGIC       });
# MAGIC     }
# MAGIC
# MAGIC     function setChipHover(idx, on) {
# MAGIC       mount.querySelectorAll(".sx-chip").forEach(chip => {
# MAGIC         const isMatch = Number(chip.dataset.hotspotIndex) === idx;
# MAGIC         chip.classList.toggle("sx-chip-hovered-from-line", on && isMatch);
# MAGIC       });
# MAGIC     }
# MAGIC
# MAGIC     function setLineHover(idx, on) {
# MAGIC       mount.querySelectorAll(`.sx-hotspot-${idx}`).forEach(line => {
# MAGIC         line.classList.toggle("sx-hovered-from-chip", on);
# MAGIC       });
# MAGIC     }
# MAGIC
# MAGIC     function showHotspot(idx, triggerEl = null) {
# MAGIC       const hotspot = hotspots[idx];
# MAGIC       if (!hotspot) return;
# MAGIC
# MAGIC       if (overlay.style.display === "block" && activeHotspotIndex === idx) {
# MAGIC         overlay.style.display = "none";
# MAGIC         activeHotspotIndex = null;
# MAGIC         setActiveChip(null);
# MAGIC         setActiveLines(null);
# MAGIC         return;
# MAGIC       }
# MAGIC
# MAGIC       overlayTitle.textContent = hotspot.title;
# MAGIC       overlayBody.innerHTML = hotspot.description;
# MAGIC       overlay.style.display = "block";
# MAGIC
# MAGIC       const wrap = mount.querySelector(".sx-wrap");
# MAGIC       const trigger = triggerEl || mount.querySelector(`.sx-hotspot-${idx}`) || mount.querySelector(`.sx-chip[data-hotspot-index="${idx}"]`);
# MAGIC
# MAGIC       if (trigger) {
# MAGIC         const wrapRect = wrap.getBoundingClientRect();
# MAGIC         const triggerRect = trigger.getBoundingClientRect();
# MAGIC         const desiredTop = triggerRect.top - wrapRect.top;
# MAGIC         const maxTop = wrap.clientHeight - overlay.offsetHeight - 18;
# MAGIC         overlay.style.top = `${Math.max(18, Math.min(desiredTop, maxTop))}px`;
# MAGIC       }
# MAGIC
# MAGIC       activeHotspotIndex = idx;
# MAGIC       setActiveChip(idx);
# MAGIC       setActiveLines(idx);
# MAGIC     }
# MAGIC
# MAGIC     mount.querySelectorAll(".sx-hotspot").forEach(el => {
# MAGIC       const idx = Number(el.dataset.hotspotIndex);
# MAGIC       el.addEventListener("click", () => { showHotspot(idx, el); });
# MAGIC       el.addEventListener("mouseenter", () => { setLineHover(idx, true); setChipHover(idx, true); });
# MAGIC       el.addEventListener("mouseleave", () => {
# MAGIC         setLineHover(idx, false);
# MAGIC         setChipHover(idx, false);
# MAGIC         if (activeHotspotIndex !== null) { setActiveLines(activeHotspotIndex); }
# MAGIC       });
# MAGIC     });
# MAGIC
# MAGIC     mount.querySelectorAll(".sx-chip").forEach(chip => {
# MAGIC       const idx = Number(chip.dataset.hotspotIndex);
# MAGIC       chip.addEventListener("click", () => {
# MAGIC         const associatedLine = mount.querySelector(`.sx-hotspot-${idx}`);
# MAGIC         showHotspot(idx, associatedLine || chip);
# MAGIC       });
# MAGIC       chip.addEventListener("mouseenter", () => { setLineHover(idx, true); });
# MAGIC       chip.addEventListener("mouseleave", () => {
# MAGIC         setLineHover(idx, false);
# MAGIC         if (activeHotspotIndex !== null) { setActiveLines(activeHotspotIndex); }
# MAGIC       });
# MAGIC     });
# MAGIC
# MAGIC     mount.querySelector(".sx-wrap").addEventListener("click", (e) => {
# MAGIC       if (e.target.closest(".sx-hotspot")) return;
# MAGIC       if (e.target.closest(".sx-chip")) return;
# MAGIC       if (e.target.closest(".sx-overlay")) return;
# MAGIC       overlay.style.display = "none";
# MAGIC       activeHotspotIndex = null;
# MAGIC       setActiveChip(null);
# MAGIC       setActiveLines(null);
# MAGIC     });
# MAGIC   }
# MAGIC
# MAGIC   renderSourceExplorer(config);
# MAGIC })();
# MAGIC </script>

# COMMAND ----------

import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# set the path for mlflow experiment
mlflow.set_experiment(f"/Users/{username}/bakehouse-product-prediction-experiment")

with mlflow.start_run(run_name = 'bakehouse-product-prediction-run') as run:  
    # Initialize the Random Forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

    # Enable automatic logging of input samples, metrics, parameters, and models
    # Must be called BEFORE fit() to capture training-phase metrics and parameters
    mlflow.sklearn.autolog(
        log_input_examples = True,
        silent = True
    )

    # Fit the model on the training data
    rf_classifier.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = rf_classifier.predict(X_test)

    # Calculate F1 score with 'macro' averaging for multiclass
    mlflow.log_metric("test_f1", f1_score(y_test, y_pred, average='macro'))
        
    mlflow.sklearn.log_model(
        rf_classifier,
        name = "model-artifacts", 
        input_example=X_train[:3],
        signature=infer_signature(X_train, y_train)
    )

    model_uri = f"runs:/{run.info.run_id}/model-artifacts"
    
print(f"Model trained successfully! Run ID: {run.info.run_id}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### D1. Viewing MLflow Run Details
# MAGIC
# MAGIC Now that you've logged your model training run, here's how to view and explore the details.

# COMMAND ----------

# MAGIC %md
# MAGIC #### D1.1 Accessing the MLflow UI
# MAGIC
# MAGIC You can open the MLflow UI in one of two ways.
# MAGIC
# MAGIC **Option 1: Click the Experiment Link**
# MAGIC
# MAGIC 1. In the cell output above, locate the link that says **View Logged Model at:...**.
# MAGIC 2. Click this link to open the MLflow UI directly.
# MAGIC
# MAGIC **Option 2: Navigate via Experiments**
# MAGIC
# MAGIC 1. Click **Experiments** in the left sidebar.
# MAGIC 2. Find your experiment: `bakehouse-product-prediction-experiment`.
# MAGIC 3. Click on the run name: `bakehouse-product-prediction-run`.

# COMMAND ----------

# DBTITLE 1,Cell 16
# MAGIC %md
# MAGIC #### D1.2 What You'll See in the Run Details
# MAGIC
# MAGIC The MLflow UI displays comprehensive information about your training run across several sections.
# MAGIC
# MAGIC **Metrics**
# MAGIC
# MAGIC - `test_f1` — the F1 score you logged manually on the test set.
# MAGIC - Additional metrics captured by `autolog` (e.g. training accuracy, precision, recall).
# MAGIC
# MAGIC **Parameters**
# MAGIC
# MAGIC - All hyperparameters captured by `autolog` (e.g. `n_estimators`, `random_state`, `max_depth`).
# MAGIC
# MAGIC **About this logged model**
# MAGIC
# MAGIC - Meta information displayed on the right panel: creation time, author, experiment name, and run ID.
# MAGIC
# MAGIC **Artifacts tab**
# MAGIC
# MAGIC - The pickled model file and Python environment configuration — these are required when loading the model later.
# MAGIC - Under **Source run artifacts** you will find additional files generated by `autolog`, including a training confusion matrix and a feature importance chart.

# COMMAND ----------

# MAGIC %md
# MAGIC #### D1.3 Why This Matters
# MAGIC
# MAGIC Tracking run details supports several key parts of the machine learning workflow.
# MAGIC
# MAGIC - **Reproducibility** - Every detail needed to recreate this model is saved.
# MAGIC - **Comparison** - Run multiple experiments and compare metrics side-by-side.
# MAGIC - **Collaboration** - Share run links with teammates for review.
# MAGIC - **Debugging** - Review parameters and metrics when investigating issues.
# MAGIC - **Production** - Track which model version is deployed and performing best.
# MAGIC
# MAGIC After reviewing the run, you can compare it with other experiments, load the model for predictions with `mlflow.sklearn.load_model(model_uri)`, deploy the model to a serving endpoint, or set up model monitoring and alerts.

# COMMAND ----------

# DBTITLE 1,Cell 18
# MAGIC %md
# MAGIC ## E. Register the Model to the Model Registry
# MAGIC
# MAGIC Now that you've trained and logged your model, the next step is to **register it to Unity Catalog** under your catalog and schema. This makes the model available for:
# MAGIC
# MAGIC - **Deployment** - Move models from development to staging to production.
# MAGIC - **Version Control** - Track multiple versions of the same model.
# MAGIC - **Collaboration** - Share models across teams and projects.
# MAGIC - **Discovery** - Find and reuse models across the organization.
# MAGIC - **Lineage** - Automatically tracks the upstream tables used for training and downstream consumers such as serving endpoints.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### E1. What Registration Does
# MAGIC
# MAGIC 1. **Creates a named model** - Assigns a user-friendly name to your model.
# MAGIC 2. **Versions automatically** - Each registration creates a new version (1, 2, 3...).
# MAGIC 3. **Links to the run** - Maintains connection to training metrics and parameters.
# MAGIC 4. **Enables lifecycle management** - Supports aliases like `dev`, `staging`, and `production`.
# MAGIC 5. **Captures lineage** - Unity Catalog records the relationship between training data, the MLflow run, and the registered model automatically.
# MAGIC
# MAGIC After registration, the model can be loaded by name and version from any notebook, job, or serving endpoint.

# COMMAND ----------

# Register the model to Unity Catalog
# Define the model name in Unity Catalog format: catalog.schema.model_name
model_name = f"{my_catalog}.ai_ml_ds.bakehouse_product_predictor_{username.split('@')[0].replace('.', '_')}"

# Register the model in Unity Catalog
registered_model = mlflow.register_model(model_uri=model_uri, name=model_name)

print(f"Model registered as: {model_name}")
print(f"Version: {registered_model.version}")

# COMMAND ----------

# DBTITLE 1,Cell F2 - UC Lineage
# MAGIC %md
# MAGIC    
# MAGIC ### E2. Model Lineage
# MAGIC
# MAGIC One of the most valuable features of registering models to Unity Catalog is **automatic lineage** — no extra configuration required. Unity Catalog builds a lineage graph connecting your model to the data it was trained on and every downstream consumer that uses it.
# MAGIC
# MAGIC **What lineage tracks**
# MAGIC
# MAGIC - **Upstream** — the tables read during training (e.g. `bakehouse_sales`), the MLflow run that produced the model, and the notebook or job that triggered it.
# MAGIC - **Downstream** — serving endpoints, notebooks, and jobs that load the registered model by name or alias.
# MAGIC
# MAGIC **Where to find it**
# MAGIC
# MAGIC 1. Click **Catalog** in the left sidebar.
# MAGIC 2. Navigate to your model under `catalog_name` > `schema_name` > **Models**.
# MAGIC 3. Open the model and select the **Lineage** tab.
# MAGIC
# MAGIC The lineage graph lets you trace exactly which data produced a given model version and which systems depend on it, which is critical for governance, debugging model quality issues, and assessing the impact of changes to upstream tables.

# COMMAND ----------

# MAGIC %md
# MAGIC ## F. Model Aliases: Managing Deployment Stages
# MAGIC
# MAGIC Now that your model is registered, you'll add an **alias** to this version. Aliases are human-readable labels that point to specific model versions, making deployment management much easier.

# COMMAND ----------

# MAGIC %md
# MAGIC ### F1. What Are Model Aliases?
# MAGIC
# MAGIC Model aliases are named pointers to specific model versions. Instead of referencing `bakehouse_product_predictor version 3`, you can reference `bakehouse_product_predictor@production`.
# MAGIC
# MAGIC The following table summarizes common alias patterns.
# MAGIC
# MAGIC | Alias | Purpose |
# MAGIC | --- | --- |
# MAGIC | `dev` | Latest model being developed and tested by data scientists. |
# MAGIC | `staging` | Model undergoing QA testing before production release. |
# MAGIC | `production` | Currently serving live predictions to end users. |
# MAGIC | `champion` | Best performing model (for A/B testing scenarios). |
# MAGIC | `challenger` | New model being compared against the champion. |

# COMMAND ----------

# DBTITLE 1,G2 Example Workflow
# MAGIC %md
# MAGIC    
# MAGIC ### F2. Example Workflow
# MAGIC
# MAGIC A typical alias-driven deployment workflow follows these steps:
# MAGIC
# MAGIC 1. Train a new model and register it as version 3.
# MAGIC 2. Assign the `dev` alias and test in the development environment.
# MAGIC 3. When tests pass, move the `staging` alias to version 3.
# MAGIC 4. When QA approves, move the `production` alias to version 3.
# MAGIC 5. Complete all of this without changing any application code.

# COMMAND ----------

from mlflow.tracking.client import MlflowClient

# Initialize an MLflow Client
client = MlflowClient()

# Assign a "dev" alias to model version 1
client.set_registered_model_alias(
    name= registered_model.name,  # The registered model name
    alias="dev",  # The alias representing the dev environment
    version=registered_model.version  # The version of the model you want to move to "dev"
)

# COMMAND ----------

# DBTITLE 1,G3 Loading Models with Aliases
# MAGIC %md-sandbox
# MAGIC ### F3. Loading Models with Aliases
# MAGIC
# MAGIC The two approaches below show how you can reference a model at load time. **Click a highlighted line or an annotation chip** to compare the version-pinned and alias-based approaches.
# MAGIC
# MAGIC <div id="g3-mount"></div>
# MAGIC
# MAGIC <style>
# MAGIC   .sx-wrap { position: relative; font-family: sans-serif; border: 1px solid #DCE0E2; border-radius: 12px; overflow: hidden; background: #F9F7F4; margin: 16px 0; }
# MAGIC   .sx-title { background: #EEEDE9; border-bottom: 1px solid #DCE0E2; padding: 8px 14px; font-size: 14pt; font-weight: 700; color: #5A6F77; }
# MAGIC   .sx-rail { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 14px; background: #F8F9FC; border-bottom: 1px solid #EEEDE9; }
# MAGIC   .sx-chip { border: 1px solid #DCE0E2; background: #FFFFFF; border-radius: 999px; padding: 5px 12px; font-size: 14pt; font-weight: 700; color: #1B3139; cursor: pointer; }
# MAGIC   .sx-chip:hover, .sx-chip.active { background: rgba(66,153,224,0.12); border-color: #4299E0; color: #2272B4; }
# MAGIC   .sx-chip-hovered-from-line { background: rgba(66,153,224,0.12); border-color: #4299E0; color: #2272B4; }
# MAGIC   .sx-code { padding: 10px 0; overflow-x: auto; font-size: 14pt; line-height: 1.55; }
# MAGIC   .sx-code, .sx-line-code { font-family: Menlo, Consolas, monospace !important; }
# MAGIC   .sx-line { display: grid; grid-template-columns: 52px 1fr; }
# MAGIC   .sx-line.no-lines { grid-template-columns: 1fr; }
# MAGIC   .sx-line.no-lines .sx-line-code { padding-left: 16px; }
# MAGIC   .sx-line-no { color: #5A6F77; text-align: right; padding: 0 12px; user-select: none; border-right: 1px solid #EEEDE9; }
# MAGIC   .sx-line-code { padding: 0 16px; white-space: pre; }
# MAGIC   .sx-active-line { background: rgba(66,153,224,0.18); }
# MAGIC   .sx-active-line .sx-line-code { border-left: 3px solid #4299E0; padding-left: 13px; }
# MAGIC   .sx-line.sx-active-line { background: rgba(66,153,224,0.18); }
# MAGIC   .sx-line.sx-active-line .sx-line-code { border-left: 3px solid #4299E0; padding-left: 13px; }
# MAGIC   .sx-hotspot { background: rgba(66,153,224,0.08); cursor: pointer; }
# MAGIC   .sx-hotspot .sx-line-code { border-left: 3px solid rgba(66,153,224,0.5); padding-left: 13px; }
# MAGIC   .sx-hotspot:hover, .sx-hovered-from-chip { background: rgba(66,153,224,0.16); }
# MAGIC   .sx-line.sx-hotspot.sx-active-line { background: rgba(66,153,224,0.22) !important; }
# MAGIC   .sx-line.sx-hotspot.sx-active-line .sx-line-code { border-left: 3px solid #4299E0 !important; padding-left: 13px !important; }
# MAGIC   .sx-hotspot .sx-line-no { color: #2272B4; font-weight: 700; }
# MAGIC   .sx-overlay { display: none; position: absolute; right: 18px; top: 96px; width: 360px; max-width: calc(100% - 36px); background: #FFFFFF; border: 1px solid #DCE0E2; border-left: 5px solid #4299E0; border-radius: 12px; box-shadow: 0 6px 18px rgba(27,49,57,0.12), 0 16px 36px rgba(27,49,57,0.10); padding: 14px 16px; z-index: 5; }
# MAGIC   .sx-overlay-title { font-weight: 800; font-size: 15pt; margin-bottom: 6px; color: #1B3139; }
# MAGIC   .sx-overlay-body { color: #0b2026; line-height: 1.45; font-size: 14pt; }
# MAGIC   #g3-mount .sx-overlay { position: static; width: auto; max-width: none; right: auto; top: auto; border-radius: 0; box-shadow: none; border: none; border-top: 1px solid #DCE0E2; border-left: 5px solid #4299E0; }
# MAGIC </style>
# MAGIC
# MAGIC <script>
# MAGIC (function () {
# MAGIC   const config = {
# MAGIC     mountId: "g3-mount",
# MAGIC     title: "Version-Pinned vs Alias-Based Loading",
# MAGIC     showAnnotationRail: true,
# MAGIC     hotspots: [
# MAGIC       {
# MAGIC         title: "Version-pinned",
# MAGIC         startLine: 1,
# MAGIC         endLine: 2,
# MAGIC         description: "Pinning to an explicit version number ties your application code to the current state of the registry. Every time a new version is promoted — dev to staging, or staging to production — every downstream consumer must be updated with the new number. A missed update means the wrong model is serving predictions."
# MAGIC       },
# MAGIC       {
# MAGIC         title: "Alias-based",
# MAGIC         startLine: 4,
# MAGIC         endLine: 5,
# MAGIC         description: "<code>@production</code> is a named pointer that MLflow resolves at load time. When a new model version is ready, operations teams move the alias — your application code does not change. This decoupling between version management and application code is the recommended pattern for production ML systems."
# MAGIC       }
# MAGIC     ],
# MAGIC     source: `# Version-pinned: requires a code change on every promotion.
# MAGIC model = mlflow.pyfunc.load_model(f"models:/{model_name}/3")
# MAGIC
# MAGIC # Alias-based: the pointer moves — your code never changes.
# MAGIC model = mlflow.pyfunc.load_model(f"models:/{model_name}@production")`,
# MAGIC     showLineNumbers: true,
# MAGIC     displayStartLine: 1,
# MAGIC   };
# MAGIC
# MAGIC   function escapeHtml(value) {
# MAGIC     return String(value)
# MAGIC       .replace(/&/g, "&amp;")
# MAGIC       .replace(/</g, "&lt;")
# MAGIC       .replace(/>/g, "&gt;");
# MAGIC   }
# MAGIC
# MAGIC   function renderSourceExplorer(config) {
# MAGIC     const mount = document.getElementById(config.mountId);
# MAGIC     const lines = config.source.replace(/\n$/, "").split("\n");
# MAGIC     const start = config.startLine || 1;
# MAGIC     const end = config.endLine || lines.length;
# MAGIC     const visible = lines.slice(start - 1, end);
# MAGIC     const hotspots = config.hotspots || [];
# MAGIC     const displayStartLine = config.displayStartLine || start;
# MAGIC
# MAGIC     function hotspotFor(lineNo) {
# MAGIC       const index = hotspots.findIndex(h => lineNo >= h.startLine && lineNo <= h.endLine);
# MAGIC       return index >= 0 ? { hotspot: hotspots[index], index } : null;
# MAGIC     }
# MAGIC
# MAGIC     const codeHtml = visible.map((line, idx) => {
# MAGIC       const actualLineNo = start + idx;
# MAGIC       const displayLineNo = displayStartLine + idx;
# MAGIC       const hotspot = hotspotFor(actualLineNo);
# MAGIC       const classes = hotspot ? `sx-line sx-hotspot sx-hotspot-${hotspot.index}` : "sx-line";
# MAGIC       const attrs = hotspot ? `data-hotspot-index="${hotspot.index}"` : "";
# MAGIC       return `
# MAGIC         <div class="${classes} ${config.showLineNumbers ? "" : "no-lines"}" ${attrs}>
# MAGIC           ${config.showLineNumbers ? `<div class="sx-line-no">${displayLineNo}</div>` : ""}
# MAGIC           <div class="sx-line-code">${escapeHtml(line)}</div>
# MAGIC         </div>`;
# MAGIC     }).join("");
# MAGIC
# MAGIC     const railHtml = config.showAnnotationRail && hotspots.length > 0
# MAGIC       ? `<div class="sx-rail">${hotspots.map((h, i) => `<button class="sx-chip" data-hotspot-index="${i}">${escapeHtml(h.title)}</button>`).join("")}</div>`
# MAGIC       : "";
# MAGIC
# MAGIC     const overlayHtml = hotspots.length > 0
# MAGIC       ? `<div class="sx-overlay"><div class="sx-overlay-title"></div><div class="sx-overlay-body"></div></div>`
# MAGIC       : "";
# MAGIC
# MAGIC     mount.innerHTML = `<div class="sx-wrap"><div class="sx-title">${escapeHtml(config.title)}</div>${railHtml}<div class="sx-code">${codeHtml}</div>${overlayHtml}</div>`;
# MAGIC
# MAGIC     if (hotspots.length === 0) return;
# MAGIC
# MAGIC     const overlay = mount.querySelector(".sx-overlay");
# MAGIC     const overlayTitle = mount.querySelector(".sx-overlay-title");
# MAGIC     const overlayBody = mount.querySelector(".sx-overlay-body");
# MAGIC     let activeHotspotIndex = null;
# MAGIC
# MAGIC     function setActiveLines(idx) {
# MAGIC       mount.querySelectorAll(".sx-active-line").forEach(el => el.classList.remove("sx-active-line"));
# MAGIC       if (idx === null) return;
# MAGIC       mount.querySelectorAll(`.sx-hotspot-${idx}`).forEach(el => el.classList.add("sx-active-line"));
# MAGIC     }
# MAGIC
# MAGIC     function setActiveChip(idx) {
# MAGIC       mount.querySelectorAll(".sx-chip").forEach(chip => {
# MAGIC         chip.classList.toggle("active", idx !== null && Number(chip.dataset.hotspotIndex) === idx);
# MAGIC       });
# MAGIC     }
# MAGIC
# MAGIC     function setChipHover(idx, on) {
# MAGIC       mount.querySelectorAll(".sx-chip").forEach(chip => {
# MAGIC         chip.classList.toggle("sx-chip-hovered-from-line", on && Number(chip.dataset.hotspotIndex) === idx);
# MAGIC       });
# MAGIC     }
# MAGIC
# MAGIC     function setLineHover(idx, on) {
# MAGIC       mount.querySelectorAll(`.sx-hotspot-${idx}`).forEach(line => line.classList.toggle("sx-hovered-from-chip", on));
# MAGIC     }
# MAGIC
# MAGIC     function showHotspot(idx, triggerEl = null) {
# MAGIC       const hotspot = hotspots[idx];
# MAGIC       if (!hotspot) return;
# MAGIC       if (overlay.style.display === "block" && activeHotspotIndex === idx) {
# MAGIC         overlay.style.display = "none";
# MAGIC         activeHotspotIndex = null;
# MAGIC         setActiveChip(null);
# MAGIC         setActiveLines(null);
# MAGIC         return;
# MAGIC       }
# MAGIC       overlayTitle.textContent = hotspot.title;
# MAGIC       overlayBody.innerHTML = hotspot.description;
# MAGIC       overlay.style.display = "block";
# MAGIC       activeHotspotIndex = idx;
# MAGIC       setActiveChip(idx);
# MAGIC       setActiveLines(idx);
# MAGIC     }
# MAGIC
# MAGIC     mount.querySelectorAll(".sx-hotspot").forEach(el => {
# MAGIC       const idx = Number(el.dataset.hotspotIndex);
# MAGIC       el.addEventListener("click", () => { showHotspot(idx, el); });
# MAGIC       el.addEventListener("mouseenter", () => { setLineHover(idx, true); setChipHover(idx, true); });
# MAGIC       el.addEventListener("mouseleave", () => {
# MAGIC         setLineHover(idx, false);
# MAGIC         setChipHover(idx, false);
# MAGIC         if (activeHotspotIndex !== null) { setActiveLines(activeHotspotIndex); }
# MAGIC       });
# MAGIC     });
# MAGIC
# MAGIC     mount.querySelectorAll(".sx-chip").forEach(chip => {
# MAGIC       const idx = Number(chip.dataset.hotspotIndex);
# MAGIC       chip.addEventListener("click", () => {
# MAGIC         const associatedLine = mount.querySelector(`.sx-hotspot-${idx}`);
# MAGIC         showHotspot(idx, associatedLine || chip);
# MAGIC       });
# MAGIC       chip.addEventListener("mouseenter", () => { setLineHover(idx, true); });
# MAGIC       chip.addEventListener("mouseleave", () => {
# MAGIC         setLineHover(idx, false);
# MAGIC         if (activeHotspotIndex !== null) { setActiveLines(activeHotspotIndex); }
# MAGIC       });
# MAGIC     });
# MAGIC
# MAGIC     mount.querySelector(".sx-wrap").addEventListener("click", (e) => {
# MAGIC       if (e.target.closest(".sx-hotspot")) return;
# MAGIC       if (e.target.closest(".sx-chip")) return;
# MAGIC       if (e.target.closest(".sx-overlay")) return;
# MAGIC       overlay.style.display = "none";
# MAGIC       activeHotspotIndex = null;
# MAGIC       setActiveChip(null);
# MAGIC       setActiveLines(null);
# MAGIC     });
# MAGIC   }
# MAGIC
# MAGIC   renderSourceExplorer(config);
# MAGIC })();
# MAGIC </script>

# COMMAND ----------

# Version-pinned: requires a code change on every promotion.
model = mlflow.pyfunc.load_model(f"models:/{model_name}/1")
# Alias-based: the pointer moves — your code never changes.
model = mlflow.pyfunc.load_model(f"models:/{model_name}@dev")

# COMMAND ----------

# DBTITLE 1,G4 Champion Challenger
# MAGIC %md-sandbox
# MAGIC ### F4. Champion–Challenger Evaluation Loop
# MAGIC
# MAGIC For A/B testing scenarios, the `champion` and `challenger` aliases drive a continuous evaluation cycle. A challenger is trained, compared against the current champion, and either promoted or retired — then the loop repeats.
# MAGIC
# MAGIC <div style="max-width: 520px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 480 480" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Champion-Challenger Evaluation Loop</title>
# MAGIC   <desc>Four stages arranged in a clockwise loop: Train Challenger, Compare vs Champion, Promote or Retire, and Monitor Champion, repeating continuously.</desc>
# MAGIC   <defs>
# MAGIC     <marker id="cyc-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5E7077" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
# MAGIC   </defs>
# MAGIC   <path d="M 315 110 A 150 150 0 0 1 370 165" fill="none" stroke="#5E7077" stroke-width="2" marker-end="url(#cyc-arrow)"/>
# MAGIC   <path d="M 370 315 A 150 150 0 0 1 315 370" fill="none" stroke="#5E7077" stroke-width="2" marker-end="url(#cyc-arrow)"/>
# MAGIC   <path d="M 165 370 A 150 150 0 0 1 110 315" fill="none" stroke="#5E7077" stroke-width="2" marker-end="url(#cyc-arrow)"/>
# MAGIC   <path d="M 110 165 A 150 150 0 0 1 165 110" fill="none" stroke="#5E7077" stroke-width="2" marker-end="url(#cyc-arrow)"/>
# MAGIC   <rect x="168" y="58" width="144" height="64" rx="8" fill="#4299E0" fill-opacity="0.12" stroke="#4299E0" stroke-width="1.5"/>
# MAGIC   <text text-anchor="middle" font-size="14" font-weight="700" fill="#0b2026"><tspan x="240" y="83">Train</tspan><tspan x="240" dy="18">Challenger</tspan></text>
# MAGIC   <rect x="318" y="208" width="144" height="64" rx="8" fill="#00A972" fill-opacity="0.12" stroke="#00A972" stroke-width="1.5"/>
# MAGIC   <text x="390" y="245" text-anchor="middle" font-size="14" font-weight="700" fill="#0b2026">Compare</text>
# MAGIC   <rect x="168" y="358" width="144" height="64" rx="8" fill="#FFAB00" fill-opacity="0.15" stroke="#FFAB00" stroke-width="1.5"/>
# MAGIC   <text text-anchor="middle" font-size="14" font-weight="700" fill="#0b2026"><tspan x="240" y="383">Promote/</tspan><tspan x="240" dy="18">Retire</tspan></text>
# MAGIC   <rect x="18" y="208" width="144" height="64" rx="8" fill="#FF5F46" fill-opacity="0.10" stroke="#FF5F46" stroke-width="1.5"/>
# MAGIC   <text text-anchor="middle" font-size="14" font-weight="700" fill="#0b2026"><tspan x="90" y="233">Monitor</tspan><tspan x="90" dy="18">Champion</tspan></text>
# MAGIC   <text x="240" y="246" text-anchor="middle" font-size="14" font-weight="700" fill="#5E7077">Repeat</text>
# MAGIC </svg>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this demonstration, you walked through the model development lifecycle using MLflow and bakehouse sales data:
# MAGIC
# MAGIC 1. Prepared features using SQL from bakehouse sales transactions.
# MAGIC 2. Trained and logged a random forest model using MLflow.
# MAGIC 3. Tracked the experiment and reviewed run details in the MLflow UI.
# MAGIC 4. Registered the model in Unity Catalog.
# MAGIC 5. Applied a model version alias (`dev`) to manage deployment stages.
# MAGIC
# MAGIC ### Next Steps
# MAGIC
# MAGIC With the model registered and aliased, you can compare additional experiment runs, promote versions through `staging` and `production` aliases, and deploy the model to a serving endpoint for real-time predictions.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
