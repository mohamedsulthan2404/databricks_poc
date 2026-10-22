-- Databricks notebook source
-- MAGIC %md
-- MAGIC ![Databricks Academy](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/databricks_academy_logo.png)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Demo - Using Genie Code
-- MAGIC
-- MAGIC This notebook demonstrates how to use Genie Code, Databricks' AI-powered coding assistant, to generate SQL code, explain existing code, debug queries, and understand notebook contents.
-- MAGIC
-- MAGIC ## Learning objectives
-- MAGIC
-- MAGIC By the end of this lesson, you should be able to:
-- MAGIC
-- MAGIC - **Generate** SQL code using Genie Code to copy tables between schemas.
-- MAGIC - **Explain** what existing code does using Genie Code.
-- MAGIC - **Debug** SQL queries with Genie Code's error diagnosis feature.
-- MAGIC - **Retrieve** information about notebook contents using Genie Code.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## REQUIRED - Select a Compute Environment
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #FF5F46; background: rgba(255,95,70,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
-- MAGIC   <strong style="display:block; color:#98102A; margin-bottom:6px; font-size:15pt;">Select Serverless Compute</strong>
-- MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
-- MAGIC
-- MAGIC Before starting this notebook, select the required compute environment listed below.
-- MAGIC
-- MAGIC - **Serverless Compute, Version 5**
-- MAGIC
-- MAGIC ![Serverless Select](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/select-compute.png)
-- MAGIC
-- MAGIC <br></br>
-- MAGIC How to select an environment version:
-- MAGIC [AWS](https://docs.databricks.com/aws/en/compute/serverless/dependencies#-select-an-environment-version) |
-- MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies#-select-an-environment-version) |
-- MAGIC [GCP](https://docs.databricks.com/gcp/en/compute/serverless/dependencies#-select-an-environment-version)
-- MAGIC
-- MAGIC **NOTE:** This notebook requires **SQL and Python**, and was tested using **Serverless V5**. All-purpose compute may work but is not guaranteed to behave the same or support all features demonstrated.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## A. Classroom Setup
-- MAGIC
-- MAGIC 1. Run the cell below. 
-- MAGIC     - It will create or use your personal catalog named **labuser_UNIQUE_ID**.
-- MAGIC     - Create the **example** schema if necessary.
-- MAGIC     - Sets your default catalog to **labuser_UNIQUE_ID** and the default schema to **example**.
-- MAGIC

-- COMMAND ----------

-- DBTITLE 1,Setup
-- MAGIC %run ../Includes/Classroom-Setup-catalog-schema-setup

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Sample Data for This Lesson
-- MAGIC
-- MAGIC You are going to use a sample dataset called **bakehouse**. This dataset consists of six tables:
-- MAGIC
-- MAGIC - **media_customer_reviews**
-- MAGIC - **media_gold_reviews_chunked**
-- MAGIC - **sales_customers**
-- MAGIC - **sales_franchises**
-- MAGIC - **sales_suppliers**
-- MAGIC - **sales_transactions**
-- MAGIC
-- MAGIC The tables are in the `samples` catalog, which is already installed in this workspace.
-- MAGIC
-- MAGIC 1. Open the Catalog pane by clicking ![Catalog Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/catalog.png "Catalog Icon").
-- MAGIC
-- MAGIC     - You are going to use Genie Code to help copy this data into a catalog and schema.
-- MAGIC
-- MAGIC     - Genie Code is Databricks' AI-powered coding assistant that helps you write, explain, and debug code directly within your notebooks.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## C. Generating Code with Genie Code

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC Open Genie Code to help write code. Complete the following:
-- MAGIC
-- MAGIC 1. Move your mouse in-between this cell and the next one.
-- MAGIC
-- MAGIC 2. Click ![Genie Code Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/genie-code-cell.png "Genie Code Icon") to create a new code cell with a Genie Code prompt.
-- MAGIC
-- MAGIC 3. Complete the following:
-- MAGIC     - Copy and paste the following into the prompt field.
-- MAGIC     - **REQUIRED:** Update your **ADD_YOUR_CATALOG_NAME**
-- MAGIC     - Click **Generate**
-- MAGIC
-- MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
-- MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
-- MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
-- MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='✓ Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
-- MAGIC   </div>
-- MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Generate SQL code that will copy all tables from samples.bakehouse into my ADD_YOUR_CATALOG_NAME.example schema.</pre>
-- MAGIC </div>
-- MAGIC
-- MAGIC 4. Genie Code shows you the generated SQL, so you can review it before saving or running it.
-- MAGIC
-- MAGIC 5. Click **Accept**.
-- MAGIC
-- MAGIC 6. Run the cell.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #FFAB00; background: rgba(255,171,0,0.12); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
-- MAGIC   <strong style="display:block; color:#0b2026; margin-bottom:6px; font-size:15pt;">Review AI Output</strong>
-- MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
-- MAGIC
-- MAGIC As with any AI, Genie Code can make mistakes. Review all generated code before accepting or running it.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## D. Getting Code Explanations
-- MAGIC
-- MAGIC You can also use Genie Code to explain code. Follow the steps for an example:
-- MAGIC
-- MAGIC 1. Open the Genie Code drawer by clicking ![Genie Icon](https://files.training.databricks.com/binder/prod_main/get-started-with-databricks-end-to-end-en_us-1.0.0/images/20261022T090506Z/Get Started with Databricks End to End/Includes/images/genie-icon.png "Genie Icon") in the right sidebar.
-- MAGIC
-- MAGIC 2. Copy the following prompt:
-- MAGIC
-- MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
-- MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
-- MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
-- MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='✓ Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
-- MAGIC   </div>
-- MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Explain what the code in this cell does.</pre>
-- MAGIC </div>
-- MAGIC
-- MAGIC 3. Select the code cell **Genie Code** created for you above.
-- MAGIC
-- MAGIC 4. Paste the prompt you copied.
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## E. Debugging with Genie Code
-- MAGIC The next cells contain queries with errors, perfect for practicing Genie Code's debugging feature. You can use Genie Code to help find out what is wrong with the queries and rewrite them appropriately so they will run.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### E1. Simple Debug Example
-- MAGIC
-- MAGIC
-- MAGIC 1. Try running the next cell.
-- MAGIC
-- MAGIC 2. Click **Diagnose error** to ask Genie to fix the query.
-- MAGIC
-- MAGIC     Genie Code will ask for your permission to run code.
-- MAGIC
-- MAGIC 3. In these examples, click **Allow** or **Accept** anytime Genie Code asks.

-- COMMAND ----------

-- DBTITLE 1,Error Query
SELECT * 
FROM samples.bakehouse.sales_transactions 
WHERE totalPrce = 120;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
-- MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">General Example</strong>
-- MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
-- MAGIC   
-- MAGIC This example is simple on purpose for training purposes. 
-- MAGIC
-- MAGIC The same **Diagnose error** flow works on long queries with complex joins, where the bug is much harder to spot. Genie Code surfaces the error and a fix in one step, so you don't have to read through the query line by line.
-- MAGIC
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## F. More with Genie Code!
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### F1. Genie Code Overview
-- MAGIC Genie Code can provide more than just code help within notebooks.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
-- MAGIC
-- MAGIC <!-- BRANDED LOGO LOCKUP + TAGLINE -->
-- MAGIC <div style="background: #F9F7F4; border-radius: 10px; padding: 22px 28px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); border-top: 6px solid #FF5F46; margin-bottom: 18px;">
-- MAGIC   <div style="margin-bottom: 12px;"><svg viewBox="0 0 806 200" fill="none" xmlns="http://www.w3.org/2000/svg" style="height:48px; width:auto; display:block;"><path d="M81.7909 159.789C75.0244 159.789 69.5392 166.599 69.5392 175H126.368C126.368 166.599 120.883 159.789 114.116 159.789H81.7909Z" fill="#FF5F46"/>
-- MAGIC <path d="M179.614 80.7871C167.525 100.208 149.376 126.933 141.272 133.79C133.167 140.647 121.149 153.009 93.2907 153.009C73.7741 153.009 56.9864 140.474 49.5352 122.498C49.5353 122.519 49.5356 122.54 49.5358 122.561C48.4799 119.938 45.9132 118.085 42.9121 118.085C38.969 118.085 35.7721 121.282 35.7721 125.225C35.7722 126.15 35.9484 126.997 36.2689 127.752C37.984 131.793 42.5469 131.965 42.5469 144.569C42.5469 143.103 42.5469 146.404 42.5469 144.569C30.6947 144.569 21.0865 134.96 21.0863 123.108C21.0863 111.256 30.6945 101.647 42.5469 101.647H45.4249V101.644H79.5153C82.062 101.644 84.5067 102.722 86.0978 104.71C88.8856 108.194 91.0222 111.438 92.5969 114.114C94.056 116.594 98.4255 116.618 99.8699 114.13C101.393 111.506 103.416 108.337 105.98 104.929C107.573 102.813 110.103 101.644 112.752 101.644H125.427C143.951 101.644 154.105 92.7623 159.289 86.3612C161.972 83.049 165.782 80.7871 170.045 80.7871H179.614Z" fill="#FABFBA"/>
-- MAGIC <path d="M96.3843 111.768C96.3842 87.8629 77.3194 68.4739 53.768 68.3843C77.3196 68.2949 96.3845 48.9049 96.3845 25C96.3845 25 96.3845 25 96.3845 25C96.3845 48.9602 115.538 68.3838 139.165 68.3838C115.538 68.3838 96.3844 87.8075 96.3843 111.768Z" fill="#FF5F46"/>
-- MAGIC <path d="M274.824 139.867C267.307 139.867 260.701 138.158 255.006 134.742C249.388 131.325 245.022 126.579 241.909 120.505C238.796 114.355 237.239 107.18 237.239 98.9793C237.239 90.855 238.834 83.6798 242.023 77.4537C245.212 71.1516 249.767 66.2543 255.69 62.7615C261.688 59.1929 268.787 57.4086 276.988 57.4086C286.251 57.4086 293.92 59.6485 299.994 64.1283C306.144 68.5321 310.13 74.6823 311.952 82.5788H296.577C295.438 78.6306 293.198 75.5555 289.857 73.3535C286.516 71.1516 282.189 70.0507 276.874 70.0507C271.483 70.0507 266.851 71.2276 262.979 73.5813C259.182 75.8592 256.259 79.2 254.209 83.6039C252.235 87.9318 251.248 93.0949 251.248 99.0932C251.248 105.092 252.235 110.255 254.209 114.583C256.259 118.911 259.144 122.213 262.865 124.491C266.585 126.693 270.951 127.794 275.962 127.794C283.403 127.794 289.022 125.706 292.819 121.53C296.615 117.354 298.855 111.925 299.538 105.243H278.924V94.8792H313.319V138.5H300.791L299.652 127.566C297.906 130.148 295.894 132.388 293.616 134.286C291.338 136.108 288.642 137.513 285.529 138.5C282.492 139.411 278.924 139.867 274.824 139.867ZM351.07 139.867C345.375 139.867 340.364 138.652 336.036 136.222C331.708 133.717 328.33 130.224 325.9 125.744C323.47 121.264 322.255 116.101 322.255 110.255C322.255 104.18 323.432 98.8654 325.786 94.3097C328.216 89.7541 331.594 86.1854 335.922 83.6039C340.326 81.0223 345.413 79.7315 351.184 79.7315C356.803 79.7315 361.7 80.9843 365.876 83.49C370.052 85.9956 373.279 89.3744 375.557 93.6264C377.835 97.8024 378.974 102.51 378.974 107.749C378.974 108.508 378.974 109.344 378.974 110.255C378.974 111.166 378.898 112.115 378.746 113.102H332.05V104.332H365.193C365.041 100.156 363.636 96.8913 360.979 94.5375C358.321 92.1078 355.018 90.893 351.07 90.893C348.261 90.893 345.679 91.5384 343.325 92.8291C340.972 94.1199 339.111 96.0561 337.745 98.6377C336.378 101.143 335.695 104.332 335.695 108.205V111.507C335.695 115.076 336.34 118.151 337.631 120.733C338.997 123.314 340.82 125.288 343.098 126.655C345.451 127.946 348.071 128.591 350.956 128.591C354.145 128.591 356.765 127.908 358.815 126.541C360.941 125.175 362.497 123.352 363.484 121.074H377.379C376.316 124.643 374.57 127.87 372.14 130.755C369.71 133.565 366.711 135.805 363.143 137.475C359.574 139.069 355.55 139.867 351.07 139.867ZM388.176 138.5V81.0982H400.248L401.273 90.6652C403.02 87.3243 405.525 84.6669 408.79 82.6927C412.055 80.7186 415.928 79.7315 420.407 79.7315C425.039 79.7315 428.987 80.7186 432.252 82.6927C435.517 84.5909 438.023 87.4003 439.769 91.1208C441.591 94.8412 442.503 99.4729 442.503 105.016V138.5H428.835V106.268C428.835 101.485 427.772 97.8024 425.646 95.2209C423.52 92.6393 420.369 91.3485 416.193 91.3485C413.46 91.3485 410.992 91.9939 408.79 93.2847C406.664 94.5755 404.956 96.4737 403.665 98.9793C402.45 101.409 401.843 104.37 401.843 107.863V138.5H388.176ZM454.064 138.5V81.0982H467.731V138.5H454.064ZM460.898 71.9868C458.392 71.9868 456.304 71.2275 454.634 69.709C453.039 68.1145 452.242 66.1783 452.242 63.9005C452.242 61.5467 453.039 59.6485 454.634 58.2059C456.304 56.6873 458.392 55.928 460.898 55.928C463.404 55.928 465.454 56.6873 467.048 58.2059C468.719 59.6485 469.554 61.5467 469.554 63.9005C469.554 66.1783 468.719 68.1145 467.048 69.709C465.454 71.2275 463.404 71.9868 460.898 71.9868ZM506.987 139.867C501.292 139.867 496.281 138.652 491.953 136.222C487.625 133.717 484.246 130.224 481.817 125.744C479.387 121.264 478.172 116.101 478.172 110.255C478.172 104.18 479.349 98.8654 481.703 94.3097C484.133 89.7541 487.511 86.1854 491.839 83.6039C496.243 81.0223 501.33 79.7315 507.101 79.7315C512.72 79.7315 517.617 80.9843 521.793 83.49C525.969 85.9956 529.196 89.3744 531.474 93.6264C533.752 97.8024 534.891 102.51 534.891 107.749C534.891 108.508 534.891 109.344 534.891 110.255C534.891 111.166 534.815 112.115 534.663 113.102H487.967V104.332H521.11C520.958 100.156 519.553 96.8913 516.896 94.5375C514.238 92.1078 510.935 90.893 506.987 90.893C504.178 90.893 501.596 91.5384 499.242 92.8291C496.889 94.1199 495.028 96.0561 493.662 98.6377C492.295 101.143 491.612 104.332 491.612 108.205V111.507C491.612 115.076 492.257 118.151 493.548 120.733C494.914 123.314 496.737 125.288 499.015 126.655C501.368 127.946 503.988 128.591 506.873 128.591C510.062 128.591 512.682 127.908 514.732 126.541C516.858 125.175 518.414 123.352 519.401 121.074H533.296C532.233 124.643 530.487 127.87 528.057 130.755C525.627 133.565 522.628 135.805 519.06 137.475C515.491 139.069 511.467 139.867 506.987 139.867Z" fill="#0B2026"/>
-- MAGIC <rect x="563.157" y="58.4648" width="242.843" height="84.9055" rx="42.4527" fill="#0B2026"/>
-- MAGIC <path d="M664.499 114.947C661.815 114.947 659.493 114.366 657.532 113.205C655.596 112.018 654.1 110.38 653.042 108.289C652.01 106.173 651.493 103.735 651.493 100.974C651.493 98.187 652.01 95.7485 653.042 93.6584C654.1 91.5424 655.596 89.8909 657.532 88.7039C659.493 87.517 661.815 86.9235 664.499 86.9235C667.724 86.9235 670.356 87.7234 672.395 89.3232C674.433 90.8973 675.724 93.1294 676.266 96.0195H671.156C670.795 94.497 670.06 93.2971 668.95 92.4198C667.84 91.5424 666.344 91.1037 664.46 91.1037C662.757 91.1037 661.286 91.5037 660.048 92.3036C658.835 93.0778 657.893 94.2132 657.222 95.7098C656.577 97.1807 656.254 98.9353 656.254 100.974C656.254 103.012 656.577 104.767 657.222 106.238C657.893 107.683 658.835 108.805 660.048 109.605C661.286 110.38 662.757 110.767 664.46 110.767C666.344 110.767 667.84 110.367 668.95 109.567C670.06 108.741 670.795 107.606 671.156 106.161H676.266C675.749 108.896 674.459 111.05 672.395 112.625C670.356 114.173 667.724 114.947 664.499 114.947ZM697.803 114.947C695.196 114.947 692.887 114.366 690.874 113.205C688.887 112.018 687.326 110.38 686.191 108.289C685.055 106.173 684.488 103.722 684.488 100.935C684.488 98.1741 685.055 95.7485 686.191 93.6584C687.326 91.5424 688.887 89.8909 690.874 88.7039C692.887 87.517 695.196 86.9235 697.803 86.9235C700.46 86.9235 702.796 87.517 704.808 88.7039C706.821 89.8909 708.382 91.5424 709.492 93.6584C710.602 95.7485 711.156 98.1741 711.156 100.935C711.156 103.722 710.602 106.173 709.492 108.289C708.382 110.38 706.821 112.018 704.808 113.205C702.796 114.366 700.46 114.947 697.803 114.947ZM697.841 110.767C699.57 110.767 701.08 110.38 702.37 109.605C703.66 108.805 704.654 107.67 705.35 106.199C706.047 104.728 706.395 102.974 706.395 100.935C706.395 98.8966 706.047 97.1419 705.35 95.6711C704.654 94.2003 703.66 93.0778 702.37 92.3036C701.08 91.5037 699.57 91.1037 697.841 91.1037C696.112 91.1037 694.603 91.5037 693.313 92.3036C692.022 93.0778 691.016 94.2003 690.294 95.6711C689.597 97.1419 689.249 98.8966 689.249 100.935C689.249 102.974 689.597 104.728 690.294 106.199C691.016 107.67 692.022 108.805 693.313 109.605C694.603 110.38 696.112 110.767 697.841 110.767ZM720.339 114.482V87.3879H729.087C732.235 87.3879 734.829 87.9427 736.867 89.0523C738.931 90.1619 740.454 91.7359 741.434 93.7745C742.441 95.7872 742.944 98.187 742.944 100.974C742.944 103.709 742.441 106.096 741.434 108.135C740.454 110.147 738.931 111.708 736.867 112.818C734.829 113.928 732.235 114.482 729.087 114.482H720.339ZM724.984 110.534H728.855C731.203 110.534 733.048 110.16 734.39 109.412C735.757 108.638 736.725 107.541 737.293 106.122C737.886 104.677 738.183 102.961 738.183 100.974C738.183 98.9611 737.886 97.2452 737.293 95.8259C736.725 94.3809 735.757 93.2713 734.39 92.4972C733.048 91.6972 731.203 91.2973 728.855 91.2973H724.984V110.534ZM752.124 114.482V87.3879H769.619V91.1425H756.769V98.9224H768.458V102.6H756.769V110.728H769.619V114.482H752.124Z" fill="white"/>
-- MAGIC <path d="M636.472 101.239L620.99 116.72L613.554 109.283L621.598 101.239L613.554 93.1943L620.99 85.7578L636.472 101.239Z" fill="#FF3621"/>
-- MAGIC <path d="M584.879 101.241L600.36 85.7598L607.797 93.1968L599.753 101.241L607.797 109.286L600.36 116.723L584.879 101.241Z" fill="#FF3621"/></svg></div>
-- MAGIC   <div style="font-size: 22pt; font-weight: 700; color: #0b2026; line-height: 1.2; margin-bottom: 6px;">The AI agent built for data teams</div>
-- MAGIC   <div style="font-size: 15pt; color: #5E7077; line-height: 1.5;">You just used Genie Code to write, explain, and debug SQL. But that is only the start: it is an <b>AI partner for your whole data workflow</b>, not just a code generator.</div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- THREE CORE BENEFITS (PILLARS) -->
-- MAGIC <div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; margin-bottom: 24px;">
-- MAGIC
-- MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #4299E0;">
-- MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">Designed for data work</div>
-- MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55;">Built for data engineering, data science, ML, and BI, not just software. It keeps context as it moves across your workspace.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #00A972;">
-- MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">Knows your data</div>
-- MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55;">Grounded in <b>Unity Catalog</b> metadata and semantics, so it automatically finds the authoritative tables and metrics for your task.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #FF5F46;">
-- MAGIC     <div style="font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 8px;">Keeps workflows healthy</div>
-- MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55;">It plans and runs multi-step work end to end, then proactively monitors and resolves issues to keep things running.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- WHAT YOU CAN ASK IT TO DO -->
-- MAGIC <div style="font-size: 12pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #1B5162; margin-bottom: 12px;">What you can ask it to do</div>
-- MAGIC
-- MAGIC <!-- CAPABILITY GRID: ROW 1 -->
-- MAGIC <div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; margin-bottom: 24px;">
-- MAGIC
-- MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #4299E0;">
-- MAGIC     <div style="font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #4299E0; margin-bottom: 4px;">Understand</div>
-- MAGIC     <div style="font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px;">Explain &amp; Summarize</div>
-- MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0;">Ask it to explain a query, a single cell, or what an entire notebook does, all in plain language.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #00A972;">
-- MAGIC     <div style="font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #00A972; margin-bottom: 4px;">Fix</div>
-- MAGIC     <div style="font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px;">Debug &amp; Diagnose</div>
-- MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0;">It finds what is wrong with a broken query and rewrites it so it runs, no line-by-line hunting.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #FF5F46;">
-- MAGIC     <div style="font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px;">Discover</div>
-- MAGIC     <div style="font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px;">Find the Right Data</div>
-- MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0;">It surfaces the relevant tables, columns, and metrics for your question, so you stop hunting for data.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- CAPABILITY GRID: ROW 2 -->
-- MAGIC <div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; margin-bottom: 22px;">
-- MAGIC
-- MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #FFAB00;">
-- MAGIC     <div style="font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #B37A00; margin-bottom: 4px;">Analyze</div>
-- MAGIC     <div style="font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px;">Explore Your Data</div>
-- MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0;">It automates exploratory analysis: finding and cleaning data, testing ideas, and writing up a report to share.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #98102A;">
-- MAGIC     <div style="font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #98102A; margin-bottom: 4px;">Build</div>
-- MAGIC     <div style="font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px;">Dashboards, Pipelines &amp; ML</div>
-- MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0;">Describe what you want in plain language and it builds dashboards, data pipelines, and even trains ML models.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC   <div style="flex: 1; min-width: 240px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid #4299E0;">
-- MAGIC     <div style="font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #4299E0; margin-bottom: 4px;">Automate</div>
-- MAGIC     <div style="font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px;">Plan &amp; Run Tasks</div>
-- MAGIC     <div style="font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0;">Give it a goal and it lays out a plan for you to review, then runs the steps across notebooks, dashboards, and pipelines.</div>
-- MAGIC   </div>
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- POWER FEATURES STRIP -->
-- MAGIC <div style="background: #1B5162; border-radius: 10px; padding: 18px 24px; margin-bottom: 22px;">
-- MAGIC   <div style="font-size: 12pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #FFFFFF; opacity: 0.85; margin-bottom: 12px;">Ways to make it work like you do</div>
-- MAGIC   <div style="font-size: 0;">
-- MAGIC     <span style="display: inline-block; background: rgba(255,255,255,0.12); color: #FFFFFF; border-radius: 20px; padding: 8px 16px; margin: 0 8px 8px 0; font-size: 14pt;">Turn a screenshot or sketch into logic</span><span style="display: inline-block; background: rgba(255,255,255,0.12); color: #FFFFFF; border-radius: 20px; padding: 8px 16px; margin: 0 8px 8px 0; font-size: 14pt;">Custom instructions</span><span style="display: inline-block; background: rgba(255,255,255,0.12); color: #FFFFFF; border-radius: 20px; padding: 8px 16px; margin: 0 8px 8px 0; font-size: 14pt;">Agent Skills for reusable know-how</span><span style="display: inline-block; background: rgba(255,255,255,0.12); color: #FFFFFF; border-radius: 20px; padding: 8px 16px; margin: 0 8px 8px 0; font-size: 14pt;">Connects to your tools (Jira, GitHub, and more)</span><span style="display: inline-block; background: rgba(255,255,255,0.12); color: #FFFFFF; border-radius: 20px; padding: 8px 16px; margin: 0; font-size: 14pt;">Point it at specific tables, notebooks, or files</span>
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- GOVERNANCE NOTE -->
-- MAGIC <div style="border-left: 4px solid #FFAB00; background: rgba(255,171,0,0.12); padding: 14px 18px; border-radius: 4px; margin: 0 0 18px 0;">
-- MAGIC   <strong style="display:block; color:#B37A00; margin-bottom:6px; font-size:15pt;">Always governed, always yours to review</strong>
-- MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">Everything Genie Code does is governed by <b>Unity Catalog</b>, so it only ever touches data you are allowed to see, with edits and actions tracked. As with any AI, review its work before you accept or run it.</div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <!-- LEARN MORE / DOC LINKS -->
-- MAGIC <div style="background: #F9F7F4; border-radius: 10px; padding: 20px 24px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); border-top: 6px solid #FF5F46;">
-- MAGIC   <div style="font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 12px;">Keep exploring Genie Code</div>
-- MAGIC   <a href="https://www.databricks.com/blog/introducing-genie-code" target="_blank" style="display: inline-block; background: #FF5F46; color: white; font-size: 14pt; font-weight: 700; padding: 10px 24px; border-radius: 8px; text-decoration: none;">Introducing Genie Code &rarr;</a>
-- MAGIC   <div style="display: flex; gap: 10px; margin-top: 12px;">
-- MAGIC     <a href="https://docs.databricks.com/aws/en/genie-code/" target="_blank" style="display: inline-block; background: #1B5162; color: white; font-size: 14pt; font-weight: 700; padding: 10px 24px; border-radius: 8px; text-decoration: none;">AWS &rarr;</a>
-- MAGIC     <a href="https://learn.microsoft.com/en-us/azure/databricks/genie-code/" target="_blank" style="display: inline-block; background: #1B5162; color: white; font-size: 14pt; font-weight: 700; padding: 10px 24px; border-radius: 8px; text-decoration: none;">Azure &rarr;</a>
-- MAGIC     <a href="https://docs.databricks.com/gcp/en/genie-code/" target="_blank" style="display: inline-block; background: #1B5162; color: white; font-size: 14pt; font-weight: 700; padding: 10px 24px; border-radius: 8px; text-decoration: none;">GCP &rarr;</a>
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### F2. Have Genie Code Explain This Notebook

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC 1. Enter the following in the **Genie Code** panel on the right:
-- MAGIC
-- MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px 0; font-family: sans-serif; max-width: 1100px; overflow: hidden;">
-- MAGIC   <div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">
-- MAGIC     <span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt to Copy</span>
-- MAGIC     <button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='✓ Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button>
-- MAGIC   </div>
-- MAGIC   <pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Tell me what this notebook does.</pre>
-- MAGIC </div>
-- MAGIC
-- MAGIC **NOTE:** Genie Code provides a nice summary of the purpose of this notebook, including this explanation.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
-- MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
-- MAGIC <script>
-- MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
-- MAGIC </script>
