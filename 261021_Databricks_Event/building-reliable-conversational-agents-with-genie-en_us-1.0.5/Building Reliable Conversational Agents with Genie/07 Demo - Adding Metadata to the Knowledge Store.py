# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](https://files.training.databricks.com/binder/prod_main/building-reliable-conversational-agents-with-genie-en_us-1.0.5/images/20260929T112315Z/Building Reliable Conversational Agents with Genie/Includes/images/db-academy.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Demo - Adding Metadata to the Knowledge Store
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC In this demo, you will improve a Genie Agent by adding table and column descriptions directly in Unity Catalog. Descriptions give Genie the context it needs to understand your data, like what each table contains, what each column means, and what values are valid. 
# MAGIC
# MAGIC You will use `ALTER TABLE` SQL statements to add descriptions to all five bakehouse tables at once, then return to Genie to observe how those descriptions affect the quality of its responses. You will also add column synonyms in the Knowledge Store to map business language to column names. 
# MAGIC
# MAGIC Finally, you will enable prompt matching features to help Genie map user language to actual data values.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this demo, you will be able to:
# MAGIC
# MAGIC 1. **Add table and column descriptions** to Unity Catalog tables using `ALTER TABLE` SQL statements.
# MAGIC 2. **Verify descriptions** in Unity Catalog using `DESCRIBE TABLE EXTENDED` and Catalog Explorer.
# MAGIC 3. **Add column synonyms** in the Knowledge Store to map business terms to column names.
# MAGIC 4. **Evaluate the impact of descriptions** on Genie's SQL generation by re-asking questions from a prior demo.
# MAGIC 5. **Distinguish what descriptions solve** from what requires general instructions or example SQL.
# MAGIC 6. **Enable prompt matching** (format assistance and entity matching) on key categorical columns in the Knowledge Store.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #f44336; background: #ffebee; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC <div>
# MAGIC <strong style="color: #c62828; font-size: 1.1em;">Prerequisites</strong>
# MAGIC <p style="margin: 8px 0 0 0; color: #333;">Complete <strong>the previous demonstrations</strong> before proceeding. 
# MAGIC
# MAGIC This demo builds on the tables and benchmarks we added to Genie.</p>
# MAGIC </div>
# MAGIC </div>
# MAGIC </div>

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

# MAGIC %run ./Includes/Classroom-Setup-creating-table-column-descriptions

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## B. Genie Agent Authoring Checklist
# MAGIC
# MAGIC General 6-step approach whenever you create a new Genie Agent. Here we will focus on **Step 3**. 
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
# MAGIC   <!-- STEP 3 (active) -->
# MAGIC   <div style="background: #F9F7F4; border: 3px solid #F8A805; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #F8A805; line-height: 1; margin-bottom: 8px;">3</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35;">Add metadata<br>and synonyms</div>
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
# MAGIC   <!-- STEP 6 (DIMMED) -->
# MAGIC   <!-- ACTIVE: <div style="background: #F9F7F4; border: 3px solid #1C3037; border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0;"> -->
# MAGIC   <div style="background: #EEEDE9; border: 3px solid #C2C2C2; border-radius: 10px; padding: 16px 12px; box-shadow: none; text-align: center; min-width: 0; opacity: 0.7;">
# MAGIC     <div style="font-size: 26pt; font-weight: 800; color: #90A5B1; line-height: 1; margin-bottom: 8px;">6</div>
# MAGIC     <div style="font-size: 14pt; font-weight: 600; color: #5A6F77; line-height: 1.35;">Test, benchmark,<br>and iterate with users</div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Add Table and Column Descriptions
# MAGIC
# MAGIC Rather than manually adding descriptions one by one in the Catalog Explorer UI, you will use `ALTER TABLE` SQL statements to add all table and column descriptions and primary/foreign key constraints at once.
# MAGIC
# MAGIC These are stored directly in **Unity Catalog** and Genie reads them automatically. 
# MAGIC
# MAGIC **No additional configuration is required.**

# COMMAND ----------

# MAGIC %md
# MAGIC ### C1. Add Descriptions and Constraints with `ALTER TABLE`
# MAGIC
# MAGIC The SQL below does three things for each of the five bakehouse tables:
# MAGIC
# MAGIC | What | Why |
# MAGIC |------|-----|
# MAGIC | **Table descriptions** (`COMMENT ON TABLE`) | Tells Genie what each table represents and when to use it |
# MAGIC | **Column descriptions** (`ALTER COLUMN ... COMMENT`) | Clarifies what each column means, lists valid values, and disambiguates shared column names across tables |
# MAGIC | **Primary / foreign key constraints** (`ADD CONSTRAINT ... NOT ENFORCED`) | Informational metadata that tells Genie how tables join together. They are not enforced at the data level, but Genie reads them to auto-detect join relationships |

# COMMAND ----------

# MAGIC %md
# MAGIC 1. Run the cell below to add all descriptions and constraints at once instead of adding them manually (to save time). 
# MAGIC
# MAGIC     Feel free to explore the metadata being added as the code is executing.
# MAGIC
# MAGIC **NOTES:** 
# MAGIC
# MAGIC - The code has been prepared for you to avoid manual entry. 
# MAGIC - In production scenarios it's important to add the correct metadata on your tables and columns to give Genie the correct information in the Knowledge store.
# MAGIC - **NOTE:** You can also use **Genie Code** to help create metadata for your tables and columns. You should always review the AI generated metadata for accuracy.
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie-code/) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/genie-code/use-genie-code) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie-code/)
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- -----------------------------------------------------------
# MAGIC -- sales_customers_gold
# MAGIC -- -----------------------------------------------------------
# MAGIC COMMENT ON TABLE sales_customers_gold
# MAGIC   IS 'Customer profiles for the bakehouse franchise business. Each row represents one unique customer. There are no duplicate or null customerIDs. To count total customers, use COUNT(*) on this table. Use customerID to join with sales_transactions_gold.';
# MAGIC
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN customerID      COMMENT 'Unique identifier for each customer. Primary key — every row has a non-null, unique value. Use COUNT(*) to count total customers. Join key to sales_transactions_gold.customerID.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN first_name      COMMENT 'Customer first name.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN last_name       COMMENT 'Customer last name.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN email_address   COMMENT 'Customer email address.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN phone_number    COMMENT 'Customer phone number.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN address         COMMENT 'Customer street address.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN city            COMMENT 'City where the customer lives. This is the customer city, not the franchise city.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN state           COMMENT 'State or province where the customer lives.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN country         COMMENT 'Country where the customer lives. This is the customer country, not the franchise country.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN continent       COMMENT 'Continent where the customer lives.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN postal_zip_code COMMENT 'Postal or zip code for the customer address.';
# MAGIC ALTER TABLE sales_customers_gold
# MAGIC   ALTER COLUMN gender          COMMENT 'Customer gender. Valid values: female, male.';
# MAGIC
# MAGIC ALTER TABLE sales_customers_gold ALTER COLUMN customerID SET NOT NULL;
# MAGIC ALTER TABLE sales_customers_gold ADD CONSTRAINT pk_customers PRIMARY KEY (customerID) NOT ENFORCED;
# MAGIC
# MAGIC -- -----------------------------------------------------------
# MAGIC -- sales_suppliers_gold  (must come before franchises so PK exists for FK reference)
# MAGIC -- -----------------------------------------------------------
# MAGIC COMMENT ON TABLE sales_suppliers_gold
# MAGIC   IS 'Ingredient suppliers for bakehouse franchises. Each row represents a supplier that provides a specific ingredient. Use supplierID to join with sales_franchises_gold.';
# MAGIC
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN supplierID   COMMENT 'Unique identifier for each supplier. Join key to sales_franchises_gold.supplierID.';
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN name         COMMENT 'Name of the supplier company.';
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN ingredient   COMMENT 'The specific ingredient this supplier provides (e.g., almonds, vanilla, cinnamon, honey).';
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN continent    COMMENT 'Continent where the supplier is located.';
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN city         COMMENT 'City where the supplier is located.';
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN district     COMMENT 'District or neighborhood where the supplier is located.';
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN size         COMMENT 'Size category of the supplier. Valid values: S (Small), M (Medium), L (Large), XL (Extra Large), XXL (Extra Extra Large).';
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN longitude    COMMENT 'Geographic longitude coordinate of the supplier.';
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN latitude     COMMENT 'Geographic latitude coordinate of the supplier.';
# MAGIC ALTER TABLE sales_suppliers_gold
# MAGIC   ALTER COLUMN approved     COMMENT 'Approval status of the supplier. Valid values: Y (Yes). All suppliers in this dataset are approved.';
# MAGIC
# MAGIC ALTER TABLE sales_suppliers_gold ALTER COLUMN supplierID SET NOT NULL;
# MAGIC ALTER TABLE sales_suppliers_gold ADD CONSTRAINT pk_suppliers PRIMARY KEY (supplierID) NOT ENFORCED;
# MAGIC
# MAGIC -- -----------------------------------------------------------
# MAGIC -- sales_franchises_gold  (FK references sales_suppliers_gold PK defined above)
# MAGIC -- -----------------------------------------------------------
# MAGIC COMMENT ON TABLE sales_franchises_gold
# MAGIC   IS 'Bakery franchise locations worldwide. Each row represents a unique franchise with its location, size category, and assigned supplier. Use franchiseID to join with sales_transactions_gold and media_customer_reviews_gold (use the store column to join). Some franchises have the same name but different locations — always include city or franchiseID to uniquely identify a location. IMPORTANT: Many of the franchises do not have a supplierID that matches any record in sales_suppliers_gold when combining the tables. When querying franchise-supplier relationships, always use a LEFT JOIN to include all franchises, not an INNER JOIN.';
# MAGIC
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN franchiseID COMMENT 'Unique identifier for each franchise location. Join key to sales_transactions_gold.franchiseID and media_customer_reviews_gold.ref. Multiple franchises can share the same name in different locations. Always include franchiseID and city in GROUP BY when aggregating by franchise to avoid merging distinct locations.';
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN name        COMMENT 'Name of the franchise location. Note: some franchise names are shared across different cities, so always include city and franchiseID to uniquely identify a location.';
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN city        COMMENT 'City where the franchise is located. This is the franchise city, not the customer city.';
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN district    COMMENT 'District or neighborhood within the city where the franchise is located.';
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN zipcode     COMMENT 'Postal or zip code for the franchise location.';
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN country     COMMENT 'Country where the franchise is located. This is the franchise country, not the customer country. Use this when asked about franchise location or revenue by country. Valid values: US, Canada, Japan, Australia, Netherlands, France, Germany, Italy, Sweden.';
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN size        COMMENT 'Size category of the franchise. Valid values: S (Small), M (Medium), L (Large), XL (Extra Large), XXL (Extra Extra Large).';
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN longitude   COMMENT 'Geographic longitude coordinate of the franchise.';
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN latitude    COMMENT 'Geographic latitude coordinate of the franchise.';
# MAGIC ALTER TABLE sales_franchises_gold
# MAGIC   ALTER COLUMN supplierID  COMMENT 'Foreign key to sales_suppliers_gold.supplierID. IMPORTANT: Only 27 of 48 franchises have a matching supplier. The remaining 21 have supplierIDs that do not exist in sales_suppliers_gold. Always use LEFT JOIN when joining to sales_suppliers_gold to avoid silently dropping unmatched franchises.';
# MAGIC
# MAGIC ALTER TABLE sales_franchises_gold ALTER COLUMN franchiseID SET NOT NULL;
# MAGIC ALTER TABLE sales_franchises_gold ADD CONSTRAINT pk_franchises PRIMARY KEY (franchiseID) NOT ENFORCED;
# MAGIC ALTER TABLE sales_franchises_gold ADD CONSTRAINT fk_franchises_supplier FOREIGN KEY (supplierID) REFERENCES sales_suppliers_gold(supplierID) NOT ENFORCED;
# MAGIC
# MAGIC -- -----------------------------------------------------------
# MAGIC -- sales_transactions_gold
# MAGIC -- -----------------------------------------------------------
# MAGIC COMMENT ON TABLE sales_transactions_gold
# MAGIC   IS 'Sales transactions for bakehouse franchise products. Each row represents a single purchase. Use customerID and franchiseID to join with customer and franchise tables.';
# MAGIC
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN transactionID COMMENT 'Unique identifier for each transaction.';
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN customerID    COMMENT 'Foreign key to sales_customers_gold.customerID. Identifies the customer who made the purchase.';
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN franchiseID   COMMENT 'Foreign key to sales_franchises_gold.franchiseID. Identifies the franchise where the purchase was made.';
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN dateTime      COMMENT 'Timestamp of when the transaction occurred.';
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN product       COMMENT 'Name of the bakehouse product purchased. Valid values: Austin Almond Biscotti, Golden Gate Ginger, Orchard Oasis, Outback Oatmeal, Pearly Pies, Tokyo Tidbits.';
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN quantity      COMMENT 'Number of units purchased in this transaction.';
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN unitPrice     COMMENT 'Price per unit of the product.';
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN totalPrice    COMMENT 'Total price for this transaction (unitPrice * quantity). Use SUM(totalPrice) to calculate revenue or total spend. When ranking customers or franchises by performance, use SUM(totalPrice) as the metric.';
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN paymentMethod COMMENT 'Payment method used. Valid values: amex, mastercard, visa.';
# MAGIC ALTER TABLE sales_transactions_gold
# MAGIC   ALTER COLUMN cardNumber    COMMENT 'Card number used for the transaction.';
# MAGIC
# MAGIC ALTER TABLE sales_transactions_gold ALTER COLUMN transactionID SET NOT NULL;
# MAGIC ALTER TABLE sales_transactions_gold ADD CONSTRAINT pk_transactions PRIMARY KEY (transactionID) NOT ENFORCED;
# MAGIC ALTER TABLE sales_transactions_gold ADD CONSTRAINT fk_transactions_customer FOREIGN KEY (customerID) REFERENCES sales_customers_gold(customerID) NOT ENFORCED;
# MAGIC ALTER TABLE sales_transactions_gold ADD CONSTRAINT fk_transactions_franchise FOREIGN KEY (franchiseID) REFERENCES sales_franchises_gold(franchiseID) NOT ENFORCED;
# MAGIC
# MAGIC -- -----------------------------------------------------------
# MAGIC -- media_customer_reviews_gold
# MAGIC -- -----------------------------------------------------------
# MAGIC COMMENT ON TABLE media_customer_reviews_gold
# MAGIC   IS 'Customer reviews for bakehouse franchise locations. Each row contains free-text feedback and a sentiment classification. Use the ref column to join with sales_franchises_gold.franchiseID to obtain franchise information. The flag column contains the sentiment classification.';
# MAGIC
# MAGIC ALTER TABLE media_customer_reviews_gold
# MAGIC   ALTER COLUMN new_id       COMMENT 'Unique identifier for each review.';
# MAGIC ALTER TABLE media_customer_reviews_gold
# MAGIC   ALTER COLUMN ref          COMMENT 'Foreign key to sales_franchises_gold.franchiseID. Identifies the franchise (store/location) being reviewed. Join this column to sales_franchises_gold.franchiseID to get franchise names and locations. Always include ref, franchise name and city in SELECT and GROUP BY when counting or aggregating reviews per franchise, since franchise names are not unique and we want exact information about the reviews by franchise.';
# MAGIC ALTER TABLE media_customer_reviews_gold
# MAGIC   ALTER COLUMN review       COMMENT 'Free-text customer review. Contains unstructured feedback about the franchise experience.';
# MAGIC ALTER TABLE media_customer_reviews_gold
# MAGIC   ALTER COLUMN review_date  COMMENT 'Date when the review was submitted.';
# MAGIC ALTER TABLE media_customer_reviews_gold
# MAGIC   ALTER COLUMN flag         COMMENT 'Sentiment classification of the review. Valid values: positive, negative, mixed. "Bad" reviews mean negative. "Neutral" reviews mean mixed. "Good or great" means positive. Use this column to filter reviews by sentiment rather than analyzing the raw review text.';
# MAGIC
# MAGIC ALTER TABLE media_customer_reviews_gold ALTER COLUMN new_id SET NOT NULL;
# MAGIC ALTER TABLE media_customer_reviews_gold ADD CONSTRAINT pk_reviews PRIMARY KEY (new_id) NOT ENFORCED;
# MAGIC ALTER TABLE media_customer_reviews_gold ADD CONSTRAINT fk_reviews_franchise FOREIGN KEY (ref) REFERENCES sales_franchises_gold(franchiseID) NOT ENFORCED;

# COMMAND ----------

# MAGIC %md
# MAGIC 2. Run the cell below to verify that the:
# MAGIC    -  Descriptions were added to the table.
# MAGIC    -  The following columns have been set as primary and foreign keys.
# MAGIC       - **pk_transactions**
# MAGIC       - **fk_transactions_franchise**
# MAGIC       - **fk_transactions_customer**
# MAGIC
# MAGIC    - **NOTE:** You can use **Catalog Explorer** or run `DESCRIBE TABLE EXTENDED <table_name>` to view each of the table details if you'd like. We will simply look at one.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE EXTENDED sales_transactions_gold;

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
# MAGIC     Metadata is extremely important
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Genie sometimes gets it right without metadata, but the answers can be inconsistent across runs. 
# MAGIC
# MAGIC **Metadata makes it more reliable and consistent.**
# MAGIC
# MAGIC Our training data introduces these concepts, but putting into production relies on the curator to improve the knowledge store for better results.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### C2. View Table and Column Descriptions in the Knowledge Store
# MAGIC
# MAGIC The **Knowledge Store** is the centralized configuration surface within your Genie where all curation settings live. 
# MAGIC
# MAGIC Table and column descriptions that are added in Unity Catalog are automatically pulled into the Knowledge Store for Genie.
# MAGIC
# MAGIC 1. Open your **Genie Agent** in a new tab. (YOUR_NAME - Bakehouse Sales) that you created previously.
# MAGIC
# MAGIC 2. Select **Configure** > **Sources** tab.
# MAGIC
# MAGIC 3. Select any table and confirm that (**You might have to refresh your Genie page if you already had Genie open**):
# MAGIC    - The **table description** appears at the top
# MAGIC    - Each **column** has a description, with valid values listed where applicable
# MAGIC
# MAGIC **NOTES:** 
# MAGIC    - The Genie Agent automatically reads these descriptions from **Unity Catalog** with no additional configuration required. 
# MAGIC    - You can also **override or extend these descriptions** directly in the Knowledge Store for this specific Genie Agent without modifying the underlying Unity Catalog metadata.

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Add Column Display Names and Synonyms in the Knowledge Store
# MAGIC
# MAGIC In addition to descriptions, the Knowledge Store supports **synonyms** and **display names**.
# MAGIC
# MAGIC - **Synonyms** - Alternate names that map business language to column names. This will help Genie map the data to the different ways users would ask the prompt. 
# MAGIC
# MAGIC - **Display names** - Uses a friendly display name for this column. **This won't rename the column in Unity Catalog.**
# MAGIC
# MAGIC **NOTE:** These will be configured in the knowledge store UI.  If using a **Metric View** as the source, they can be configured there. 

# COMMAND ----------

# MAGIC %md
# MAGIC 1. In your **Genie Agent**, select **Configure** > **Sources** > **sales_transactions_gold**.
# MAGIC
# MAGIC    a. Select the **pencil icon** next to the **totalPrice** column.
# MAGIC
# MAGIC    b. **Display Name** field - `Total Price`
# MAGIC
# MAGIC    c. **Synonyms** field, add: `revenue, sales, total sales, total revenue, income`
# MAGIC
# MAGIC    d. Click **Save**.
# MAGIC
# MAGIC **NOTE:** This allows Genie to map terms like "revenue" or "sales" to the **totalPrice** column.

# COMMAND ----------

# MAGIC %md
# MAGIC 2. Add synonyms to the **flag** column.
# MAGIC
# MAGIC    a. Select **Sources** > **media_customer_reviews_gold**.
# MAGIC
# MAGIC    b. Select the **pencil icon** next to the **flag** column.
# MAGIC
# MAGIC    c. **Display Name** field - `Review Sentiment`
# MAGIC
# MAGIC    d. **Synonyms** field, add:
# MAGIC       `sentiment, summary sentiment, feedback sentiment, review sentiment, opinion, review`
# MAGIC
# MAGIC    e. Click **Save**.
# MAGIC
# MAGIC **NOTE:** This helps Genie map terms like "negative rating" or "feedback type" to the **flag** column.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Note
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC For training purposes, we will stop here with just two synonym and display name examples.
# MAGIC
# MAGIC Feel free to continue adding synonyms and display names to other columns as needed.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

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
# MAGIC     Metric Views as a source for Genie are recommended
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Instead of referencing tables directly in Genie, you can also use Metric Views.
# MAGIC
# MAGIC #### Recall, Metric Views centrally define business metrics and semantics across Databricks, ensuring consistent, governed definitions across all tools.
# MAGIC
# MAGIC - Metric views let you define display names, formats, and synonyms for dimensions and measures in a YAML file stored in Unity Catalog.
# MAGIC
# MAGIC - This gives you a code-managed, reusable semantic layer that Genie and AI/BI dashboards can share.
# MAGIC
# MAGIC - In Genie, synonyms are usually configured per space in the knowledge store UI, not through SQL on the underlying tables. Metric views are a good choice when you want synonyms managed in code.
# MAGIC
# MAGIC **NOTE:** Metric views are outside the scope of this Genie course. View the documentation below or check out the [Building Semantic Models in Databricks with UC Metric Views](https://www.databricks.com/training/catalog/building-semantic-models-in-databricks-with-uc-metric-views-4962) Databricks training.
# MAGIC
# MAGIC - Unity Catalog Metric Views:
# MAGIC [AWS](https://docs.databricks.com/aws/en/metric-views/) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/metric-views/) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/metric-views/)
# MAGIC
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## E. Enable Prompt Matching
# MAGIC
# MAGIC Beyond descriptions, display names and synonyms, the Knowledge Store offers **prompt matching**.
# MAGIC
# MAGIC **Prompt matching** is a set of features that help Genie bridge the gap between how users phrase questions and how data is actually stored.
# MAGIC
# MAGIC Prompt matching has two parts:
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 950px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <div style="display: flex; gap: 20px; justify-content: center;">
# MAGIC
# MAGIC <!-- Format Assistance -->
# MAGIC <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden;">
# MAGIC   <div style="background: #4299E0; color: white; padding: 14px 20px; text-align: center;">
# MAGIC     <div style="font-size: 1.6em; font-weight: bold;">Format Assistance</div>
# MAGIC   </div>
# MAGIC   <div style="padding: 18px 20px;">
# MAGIC     <div style="font-size: 1.3em; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC       Samples a few <strong>representative values</strong> from a column so Genie understands data types and formatting patterns (dates, codes, numeric shapes, etc.).<br/><br/>
# MAGIC       Helps Genie generate literals in the right format and avoid obviously wrong patterns in filters and comparisons.
# MAGIC     </div>
# MAGIC     <div style="background: rgba(66,153,224,0.10); border-left: 4px solid #4299E0; padding: 10px 12px; border-radius: 6px; font-size: 1em;">
# MAGIC       <strong>Use broadly</strong> — enabled by default on most columns. Low cost, high value.
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Entity Matching -->
# MAGIC <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden;">
# MAGIC   <div style="background: #00A972; color: white; padding: 14px 20px; text-align: center;">
# MAGIC     <div style="font-size: 1.3em; font-weight: bold;">Entity Matching</div>
# MAGIC   </div>
# MAGIC   <div style="padding: 18px 20px;">
# MAGIC     <div style="font-size: 1.3em; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC       Builds a <strong>curated list of distinct values</strong> for key categorical columns (e.g., product names, status codes, regions).<br/><br/>
# MAGIC       Lets Genie map user language and typos to real values — so <em>"Florida"</em> correctly becomes <code>state = 'FL'</code> instead of <code>state ILIKE '%Florida%'</code>.
# MAGIC     </div>
# MAGIC     <div style="background: rgba(0,169,114,0.10); border-left: 4px solid #00A972; padding: 10px 12px; border-radius: 6px; font-size: 1em;">
# MAGIC       <strong>Use selectively</strong> — reserve for high-signal categorical columns that appear in user questions.
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC Prompt Matching Review - [AWS](https://docs.databricks.com/aws/en/genie/knowledge-store#-prompt-matching-overview) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/genie-agents/tune-quality) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/knowledge-store#-prompt-matching-overview) 

# COMMAND ----------

# MAGIC %md
# MAGIC ### E1. View Format Assistance 
# MAGIC
# MAGIC Format assistance is **enabled by default** on most columns. Let's confirm it is active.
# MAGIC
# MAGIC 1. In your Genie Agent, select **Configure** > **Data** > **sales_transactions_gold**.
# MAGIC
# MAGIC 2. Click the **pencil icon** next to the **product** column.
# MAGIC
# MAGIC 3. Click **Advanced**.
# MAGIC
# MAGIC 4. Confirm that **Format assistance** is toggled **on**.
# MAGIC    - This means Genie has already sampled representative values from this column (e.g., `Austin Almond Biscotti`, `Golden Gate Ginger`, etc.).
# MAGIC    - These values help Genie understand the formatting pattern and generate correct filter literals.
# MAGIC
# MAGIC 5. Leave this open.

# COMMAND ----------

# MAGIC %md
# MAGIC ### E2. Enable Entity Matching on Key Columns
# MAGIC
# MAGIC Entity matching goes further than format assistance.
# MAGIC
# MAGIC It builds a **complete list of distinct values** for a column so Genie can map user language (including misspellings and synonyms) to exact data values.
# MAGIC
# MAGIC **Best practice:** Enable entity matching on a small set of **high-signal categorical columns** that users frequently reference in questions.
# MAGIC
# MAGIC For the bakehouse dataset, good candidates would be:
# MAGIC
# MAGIC | Table | Column | Why |
# MAGIC |-------|--------|-----|
# MAGIC | `sales_transactions_gold` | `product` | Users ask about specific products by name |
# MAGIC | `media_customer_reviews_gold` | `flag` | Users filter reviews by sentiment |
# MAGIC | `sales_transactions_gold` | `paymentMethod` | Users may ask about payment types |
# MAGIC | `sales_franchises_gold` | `size` | Users ask about franchise size categories |

# COMMAND ----------

# MAGIC %md
# MAGIC 1. In your Genie Agent, select **Configure** > **Sources** > **sales_transactions_gold**.
# MAGIC
# MAGIC 2. Click the **pencil icon** next to the **product** column.
# MAGIC
# MAGIC 3. Click **Advanced**.
# MAGIC
# MAGIC 4. Confirm **Format assistance** is on (required for entity matching).
# MAGIC
# MAGIC 5. Confirm **Entity matching** to **on**.
# MAGIC
# MAGIC 6. Click **Save**.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Note
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC For training purposes, we confirmed **entity matching and format assistant** was enabled on a single column. Feel free to enable/disable it on additional categorical columns like `paymentMethod` or `size`. By default it most likely is turned on where necessary.
# MAGIC
# MAGIC **Limitations:**
# MAGIC - Entity matching supports only **string columns**
# MAGIC - Up to **120 columns** with up to **1,024 distinct values** per column (max 127 characters per value)
# MAGIC - Cannot be applied to tables with **row filters or column masks**
# MAGIC - **Format assistance must be enabled** before entity matching can be turned on
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### E3. Refresh Prompt Matching Data
# MAGIC
# MAGIC When new values are added to a column or existing values change format, you should refresh the stored prompt matching data.
# MAGIC
# MAGIC In our demonstration it's not necessary.
# MAGIC
# MAGIC - View Refresh or remove prompt matching data for more information:
# MAGIC [AWS](https://docs.databricks.com/aws/en/genie/knowledge-store#refresh-or-remove-prompt-matching-data) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/genie-agents/tune-quality#refresh-or-remove-prompt-matching-data) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/genie/knowledge-store#refresh-or-remove-prompt-matching-data)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## F. Run Benchmarks (Select Chat Mode)
# MAGIC
# MAGIC In **an earlier demonstration**, you saved benchmark questions to establish a **baseline** for your Genie Agent before any metadata was added. 
# MAGIC
# MAGIC Now that you have added table descriptions, column descriptions, synonyms, and prompt matching, let's run those same benchmarks to measure the impact.
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Why Run Benchmarks Now?
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Asking questions manually is useful for exploring behavior, but it is **subjective** and **not repeatable**. 
# MAGIC
# MAGIC Benchmarks give you a **structured, repeatable way** to measure whether your changes actually improved Genie's accuracy and consistency.
# MAGIC
# MAGIC Each time you make a change to your Genie Agent: descriptions, instructions, example SQL, you should re-run benchmarks to confirm:
# MAGIC - Did the change **fix** the questions it was intended to fix?
# MAGIC - Did the change **break** anything that was already working?
# MAGIC
# MAGIC This is the **test, benchmark, and iterate** step from the authoring checklist.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC 1. In your Genie Agent, select the **Benchmark > Questions** tab in the top navigation.
# MAGIC
# MAGIC 2. Review the benchmark questions you added during in an earlier demo. 
# MAGIC
# MAGIC       You should see up to six questions:
# MAGIC
# MAGIC    | # | Benchmark Question | Has Ground Truth SQL? |
# MAGIC    |---|--------------------|-----------------------|
# MAGIC    | 1 | How many customers do we have? | Yes |
# MAGIC    | 2 | What are the top 5 franchise locations by total revenue? | Yes |
# MAGIC    | 3 | Who are our best customers? | Yes |
# MAGIC    | 4 | How many franchises does each supplier serve? | Yes |
# MAGIC    | 5 | What are total sales by region? | Yes |
# MAGIC    | 6 | Count of bad reviews by locations? | Yes |
# MAGIC
# MAGIC 3. Select **Run all benchmarks (Chat Mode)** to execute all the benchmark questions.
# MAGIC
# MAGIC    - Recall, benchmarks run each question as a **new, independent conversation**
# MAGIC       - **Genie does not carry any context from previous questions or threads**.
# MAGIC       - This simulates how a real user would interact with the space for the first time.
# MAGIC
# MAGIC 4. As each benchmark completes, review the output. For each question, check:
# MAGIC
# MAGIC    - **Assessment** - Did Genie produce a correct response?
# MAGIC
# MAGIC    - **Failure analysis** - Is the SQL correct and business-aligned?
# MAGIC
# MAGIC    - **Result match** (for questions with ground truth) - Does Genie's output match the expected result? Why or why not? 
# MAGIC       - What else can we add to the knowledge store or metadata to improve our results?
# MAGIC
# MAGIC 5. **After adding metadata, a 1-2 additional benchmarks should pass.**

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
# MAGIC     Key Takeaways
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC
# MAGIC Metadata and synonyms are the **foundation** of a well-curated Genie Agent. 
# MAGIC
# MAGIC They are the easiest change to make and often have the biggest immediate impact. 
# MAGIC
# MAGIC But as the benchmark results show, some questions require more than metadata:
# MAGIC
# MAGIC - **Business terms** like "best customer" or "region" need **general instructions or a SQL query** to define what they mean.
# MAGIC
# MAGIC - **Complex query patterns** like `LEFT JOIN` + `IS NULL` need **example SQL** to teach Genie the correct approach.
# MAGIC
# MAGIC - **Derived columns** like mapping countries to regions need **SQL expressions** to encode the logic.
# MAGIC
# MAGIC You will address these gaps in the next demo. Each time you add a new layer of context, you will re-run these benchmarks to measure progress.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## G. What Metadata Solves and It Doesn't
# MAGIC
# MAGIC <br></br>
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
# MAGIC     width: 480px;
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
# MAGIC .box.left::before { background: #00A972; }
# MAGIC .box.right::before { background: #FF5F46; }
# MAGIC
# MAGIC .box-title {
# MAGIC     font-size: 20pt;
# MAGIC     font-weight: 700;
# MAGIC     color: #0b2026;
# MAGIC     text-align: center;
# MAGIC     margin-top: 6px;
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
# MAGIC <div class="box left">
# MAGIC <div class="box-title">✓ What They Solve</div>
# MAGIC <div class="box-text">
# MAGIC <ul>
# MAGIC <li>Clarify what each column contains</li>
# MAGIC <li>List valid values for categorical columns</li>
# MAGIC <li>Clarify shared column names (e.g., customer city vs. franchise city)</li>
# MAGIC <li>Explain join relationships between tables</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <div class="box right">
# MAGIC <div class="box-title">✗ What They Don't Solve</div>
# MAGIC <div class="box-text">
# MAGIC <ul>
# MAGIC <li>Define business terms like "best customer"</li>
# MAGIC <li>Teach complex query patterns like <code>LEFT JOIN</code> + <code>IS NULL</code></li>
# MAGIC <li>Specify default behaviors (e.g., always round to 2 decimals)</li>
# MAGIC <li>Provide reusable SQL templates for common questions</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <br></br>
# MAGIC
# MAGIC <div style="max-width: 1020px; margin: 0 auto; padding: 18px 24px; background: #F8F9FC; border: 3px solid #1B5162; border-radius: 8px; font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC   <ul style="margin: 0; padding-left: 20px;">
# MAGIC     <li style="margin-bottom: 12px;">Descriptions and synonyms are the <strong>first and highest-impact lever</strong> for improving a Genie Agent</li>
# MAGIC     <li style="margin-bottom: 12px;">Together with <strong>prompt matching</strong> features in the Knowledge Store, they form the metadata foundation of your space</li>
# MAGIC     <li style="margin-bottom: 12px;">For business logic, query patterns, and behavioral rules, you'll need <strong>general instructions</strong> and <strong>example SQL</strong></li>
# MAGIC   </ul>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC #### What Descriptions Solve
# MAGIC
# MAGIC - **Column clarity** — Genie reads descriptions to understand what a column actually contains, not just its name. A column called `flag` means nothing without a description explaining it holds sentiment values.
# MAGIC - **Valid values** — Listing valid categorical values (e.g., `positive`, `negative`, `mixed`) prevents Genie from guessing or hallucinating filter conditions.
# MAGIC - **Disambiguation** — When two tables both have a `city` column, descriptions clarify which is the customer's city and which is the franchise's city. Without this, Genie may join or filter on the wrong one.
# MAGIC - **Join relationships** — Describing which column is a foreign key and what it joins to helps Genie construct correct multi-table queries without being told explicitly each time.
# MAGIC
# MAGIC #### What Descriptions Don't Solve
# MAGIC
# MAGIC - **Business definitions** — "Best customer" could mean highest spend, most visits, or longest tenure. Descriptions can't encode that decision. It requires a general instruction or example SQL.
# MAGIC - **Complex query patterns** — `LEFT JOIN` + `IS NULL` to find non-matching rows is a pattern, not a metadata fact. Genie needs an example SQL query to learn it.
# MAGIC - **Default behaviors** — If every revenue query should round to 2 decimals or filter to the current fiscal year, that rule belongs in general instructions, not a column description.
# MAGIC - **Reusable templates** — Recurring questions like "top 10 franchises by revenue last month" are best handled with saved example SQL, not descriptions.
# MAGIC
# MAGIC #### The Bigger Picture
# MAGIC
# MAGIC **Descriptions are the foundation.**
# MAGIC
# MAGIC They're the easiest win and should always come first. But they have a ceiling. 
# MAGIC
# MAGIC Once the metadata is clean, the next layer is behavioral: 
# MAGIC - general instructions tell Genie *how* to behave, 
# MAGIC - and example SQL shows it *how* to write specific query patterns. 
# MAGIC
# MAGIC </details>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## H. Conclusion
# MAGIC
# MAGIC In this demo, you:
# MAGIC
# MAGIC 1. Used `ALTER TABLE` SQL statements to add table and column descriptions to all five bakehouse tables in Unity Catalog.
# MAGIC 2. Verified descriptions using `DESCRIBE TABLE EXTENDED` and Catalog Explorer.
# MAGIC 3. Added column synonyms in the Knowledge Store to map business terms like "revenue" and "rating" to the correct columns.
# MAGIC 4. Re-asked Genie the same questions from the first demo and observed how descriptions improved SQL accuracy for column values, join logic, and disambiguation.
# MAGIC 5. Identified the limits of descriptions. They can clarify data but cannot define business terms or teach complex query patterns.
# MAGIC 6. Enabled **prompt matching** (format assistance and entity matching) on key categorical columns to help Genie map user language to actual data values.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved.
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
# MAGIC <script>
# MAGIC   document.getElementById("dbx-year").textContent = new Date().getFullYear();
# MAGIC </script>
