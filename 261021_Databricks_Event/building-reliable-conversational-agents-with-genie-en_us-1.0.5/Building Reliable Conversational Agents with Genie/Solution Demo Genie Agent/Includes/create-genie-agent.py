# Databricks notebook source
# DBTITLE 1,Install SDK
# MAGIC %pip install databricks-sdk==0.103.0

# COMMAND ----------

# DBTITLE 1,Restart Python
# MAGIC %restart_python

# COMMAND ----------

# DBTITLE 1,Catalog Setup Function
# MAGIC %run ../../Includes/Classroom-Setup-Common-Python

# COMMAND ----------

spark.sql(f'USE CATALOG {my_catalog}')
spark.sql(f'USE SCHEMA genie_course_bakehouse')

# COMMAND ----------

# DBTITLE 1,Get Serialized Space from the Genie Space
# import json
# from databricks.sdk import WorkspaceClient

# def get_serialized_json_from_agent(genie_agent_id: str) -> str:
#     w = WorkspaceClient()
#     resp = w.api_client.do(
#         "GET",
#         f"/api/2.0/genie/spaces/{genie_agent_id}?include_serialized_space=true",
#     )
#     return json.dumps(json.loads(resp["serialized_space"]), indent=2)

# resp = get_serialized_json_from_agent()
# print(resp)

# COMMAND ----------

# Curate the bakehouse Knowledge Store metadata for the Genie Agent:
# table/column COMMENTs, NOT NULL, and PRIMARY/FOREIGN KEY constraints.
#
# Each statement runs inside try/except so one failure does not stop the rest from
# applying. Re-running is safe: statements that are already applied (for example, a
# constraint that already exists) are reported as "skipped", not as errors, and the
# noisy JVM stacktrace is suppressed so it does not alarm learners. Only genuine
# failures are surfaced, as a single clean line.
#
# In a SQL notebook, put this in a %python cell.

ddl_statements = [
    # -----------------------------------------------------------
    # sales_customers_gold
    # -----------------------------------------------------------
    """COMMENT ON TABLE sales_customers_gold
         IS 'Customer profiles for the bakehouse franchise business. Each row represents one unique customer. There are no duplicate or null customerIDs. To count total customers, use COUNT(*) on this table. Use customerID to join with sales_transactions_gold.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN customerID      COMMENT 'Unique identifier for each customer. Primary key. Every row has a non-null, unique value. Use COUNT(*) to count total customers. Join key to sales_transactions_gold.customerID.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN first_name      COMMENT 'Customer first name.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN last_name       COMMENT 'Customer last name.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN email_address   COMMENT 'Customer email address.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN phone_number    COMMENT 'Customer phone number.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN address         COMMENT 'Customer street address.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN city            COMMENT 'City where the customer lives. This is the customer city, not the franchise city.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN state           COMMENT 'State or province where the customer lives.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN country         COMMENT 'Country where the customer lives. This is the customer country, not the franchise country.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN continent       COMMENT 'Continent where the customer lives.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN postal_zip_code COMMENT 'Postal or zip code for the customer address.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN gender          COMMENT 'Customer gender. Valid values: female, male.'""",
    """ALTER TABLE sales_customers_gold ALTER COLUMN customerID SET NOT NULL""",
    """ALTER TABLE sales_customers_gold ADD CONSTRAINT pk_customers PRIMARY KEY (customerID) NOT ENFORCED""",

    # -----------------------------------------------------------
    # sales_suppliers_gold  (must come before franchises so PK exists for FK reference)
    # -----------------------------------------------------------
    """COMMENT ON TABLE sales_suppliers_gold
         IS 'Ingredient suppliers for bakehouse franchises. Each row represents a supplier that provides a specific ingredient. Use supplierID to join with sales_franchises_gold.'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN supplierID   COMMENT 'Unique identifier for each supplier. Join key to sales_franchises_gold.supplierID.'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN name         COMMENT 'Name of the supplier company.'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN ingredient   COMMENT 'The specific ingredient this supplier provides (e.g., almonds, vanilla, cinnamon, honey).'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN continent    COMMENT 'Continent where the supplier is located.'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN city         COMMENT 'City where the supplier is located.'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN district     COMMENT 'District or neighborhood where the supplier is located.'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN size         COMMENT 'Size category of the supplier. Valid values: S (Small), M (Medium), L (Large), XL (Extra Large), XXL (Extra Extra Large).'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN longitude    COMMENT 'Geographic longitude coordinate of the supplier.'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN latitude     COMMENT 'Geographic latitude coordinate of the supplier.'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN approved     COMMENT 'Approval status of the supplier. Valid values: Y (Yes). All suppliers in this dataset are approved.'""",
    """ALTER TABLE sales_suppliers_gold ALTER COLUMN supplierID SET NOT NULL""",
    """ALTER TABLE sales_suppliers_gold ADD CONSTRAINT pk_suppliers PRIMARY KEY (supplierID) NOT ENFORCED""",

    # -----------------------------------------------------------
    # sales_franchises_gold  (FK references sales_suppliers_gold PK defined above)
    # -----------------------------------------------------------
    """COMMENT ON TABLE sales_franchises_gold
         IS 'Bakery franchise locations worldwide. Each row represents a unique franchise with its location, size category, and assigned supplier. Use franchiseID to join with sales_transactions_gold and media_customer_reviews_gold (use the store column to join). Some franchises have the same name but different locations, so always include city or franchiseID to uniquely identify a location. IMPORTANT: Many of the franchises do not have a supplierID that matches any record in sales_suppliers_gold when combining the tables. When querying franchise-supplier relationships, always use a LEFT JOIN to include all franchises, not an INNER JOIN.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN franchiseID COMMENT 'Unique identifier for each franchise location. Join key to sales_transactions_gold.franchiseID and media_customer_reviews_gold.ref. Multiple franchises can share the same name in different locations. Always include franchiseID and city in GROUP BY when aggregating by franchise to avoid merging distinct locations.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN name        COMMENT 'Name of the franchise location. Note: some franchise names are shared across different cities, so always include city and franchiseID to uniquely identify a location.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN city        COMMENT 'City where the franchise is located. This is the franchise city, not the customer city.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN district    COMMENT 'District or neighborhood within the city where the franchise is located.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN zipcode     COMMENT 'Postal or zip code for the franchise location.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN country     COMMENT 'Country where the franchise is located. This is the franchise country, not the customer country. Use this when asked about franchise location or revenue by country. Valid values: US, Canada, Japan, Australia, Netherlands, France, Germany, Italy, Sweden.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN size        COMMENT 'Size category of the franchise. Valid values: S (Small), M (Medium), L (Large), XL (Extra Large), XXL (Extra Extra Large).'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN longitude   COMMENT 'Geographic longitude coordinate of the franchise.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN latitude    COMMENT 'Geographic latitude coordinate of the franchise.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN supplierID  COMMENT 'Foreign key to sales_suppliers_gold.supplierID. IMPORTANT: Only 27 of 48 franchises have a matching supplier. The remaining 21 have supplierIDs that do not exist in sales_suppliers_gold. Always use LEFT JOIN when joining to sales_suppliers_gold to avoid silently dropping unmatched franchises.'""",
    """ALTER TABLE sales_franchises_gold ALTER COLUMN franchiseID SET NOT NULL""",
    """ALTER TABLE sales_franchises_gold ADD CONSTRAINT pk_franchises PRIMARY KEY (franchiseID) NOT ENFORCED""",
    """ALTER TABLE sales_franchises_gold ADD CONSTRAINT fk_franchises_supplier FOREIGN KEY (supplierID) REFERENCES sales_suppliers_gold(supplierID) NOT ENFORCED""",

    # -----------------------------------------------------------
    # sales_transactions_gold
    # -----------------------------------------------------------
    """COMMENT ON TABLE sales_transactions_gold
         IS 'Sales transactions for bakehouse franchise products. Each row represents a single purchase. Use customerID and franchiseID to join with customer and franchise tables.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN transactionID COMMENT 'Unique identifier for each transaction.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN customerID    COMMENT 'Foreign key to sales_customers_gold.customerID. Identifies the customer who made the purchase.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN franchiseID   COMMENT 'Foreign key to sales_franchises_gold.franchiseID. Identifies the franchise where the purchase was made.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN dateTime      COMMENT 'Timestamp of when the transaction occurred.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN product       COMMENT 'Name of the bakehouse product purchased. Valid values: Austin Almond Biscotti, Golden Gate Ginger, Orchard Oasis, Outback Oatmeal, Pearly Pies, Tokyo Tidbits.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN quantity      COMMENT 'Number of units purchased in this transaction.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN unitPrice     COMMENT 'Price per unit of the product.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN totalPrice    COMMENT 'Total price for this transaction (unitPrice * quantity). Use SUM(totalPrice) to calculate revenue or total spend. When ranking customers or franchises by performance, use SUM(totalPrice) as the metric.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN paymentMethod COMMENT 'Payment method used. Valid values: amex, mastercard, visa.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN cardNumber    COMMENT 'Card number used for the transaction.'""",
    """ALTER TABLE sales_transactions_gold ALTER COLUMN transactionID SET NOT NULL""",
    """ALTER TABLE sales_transactions_gold ADD CONSTRAINT pk_transactions PRIMARY KEY (transactionID) NOT ENFORCED""",
    """ALTER TABLE sales_transactions_gold ADD CONSTRAINT fk_transactions_customer FOREIGN KEY (customerID) REFERENCES sales_customers_gold(customerID) NOT ENFORCED""",
    """ALTER TABLE sales_transactions_gold ADD CONSTRAINT fk_transactions_franchise FOREIGN KEY (franchiseID) REFERENCES sales_franchises_gold(franchiseID) NOT ENFORCED""",

    # -----------------------------------------------------------
    # media_customer_reviews_gold
    # -----------------------------------------------------------
    """COMMENT ON TABLE media_customer_reviews_gold
         IS 'Customer reviews for bakehouse franchise locations. Each row contains free-text feedback and a sentiment classification. Use the ref column to join with sales_franchises_gold.franchiseID to obtain franchise information. The flag column contains the sentiment classification.'""",
    """ALTER TABLE media_customer_reviews_gold ALTER COLUMN new_id       COMMENT 'Unique identifier for each review.'""",
    """ALTER TABLE media_customer_reviews_gold ALTER COLUMN ref          COMMENT 'Foreign key to sales_franchises_gold.franchiseID. Identifies the franchise (store/location) being reviewed. Join this column to sales_franchises_gold.franchiseID to get franchise names and locations. Always include ref, franchise name and city in SELECT and GROUP BY when counting or aggregating reviews per franchise, since franchise names are not unique and we want exact information about the reviews by franchise.'""",
    """ALTER TABLE media_customer_reviews_gold ALTER COLUMN review       COMMENT 'Free-text customer review. Contains unstructured feedback about the franchise experience.'""",
    """ALTER TABLE media_customer_reviews_gold ALTER COLUMN review_date  COMMENT 'Date when the review was submitted.'""",
    """ALTER TABLE media_customer_reviews_gold ALTER COLUMN flag         COMMENT 'Sentiment classification of the review. Valid values: positive, negative, mixed. "Bad" reviews mean negative. "Neutral" reviews mean mixed. "Good or great" means positive. Use this column to filter reviews by sentiment rather than analyzing the raw review text.'""",
    """ALTER TABLE media_customer_reviews_gold ALTER COLUMN new_id SET NOT NULL""",
    """ALTER TABLE media_customer_reviews_gold ADD CONSTRAINT pk_reviews PRIMARY KEY (new_id) NOT ENFORCED""",
    """ALTER TABLE media_customer_reviews_gold ADD CONSTRAINT fk_reviews_franchise FOREIGN KEY (ref) REFERENCES sales_franchises_gold(franchiseID) NOT ENFORCED""",
]

# Errors that just mean "this was already applied on a previous run" and are safe to skip.
ALREADY_APPLIED_MARKERS = ("ALREADY_EXISTS", "already exists")


def clean_message(exc):
    """Return the human-readable first line of a Spark error, dropping the JVM stacktrace."""
    text = str(exc).split("JVM stacktrace:")[0].strip()
    return text.splitlines()[0] if text else str(exc)


applied = 0
skipped = 0
failures = []

for stmt in ddl_statements:
    # Short one-line label for reporting (collapses whitespace, trims to 90 chars).
    label = " ".join(stmt.split())[:90]
    try:
        spark.sql(stmt)
        applied += 1
    except Exception as e:
        message = clean_message(e)
        if any(marker in message for marker in ALREADY_APPLIED_MARKERS):
            skipped += 1          # already applied on a previous run, nothing to do
        else:
            failures.append((label, message))

print("Knowledge Store metadata curation complete.")
print(f"  Applied: {applied}")
print(f"  Skipped (already applied): {skipped}")
print(f"  Failed:  {len(failures)}")

if failures:
    print("\nStatements that need attention:")
    for label, message in failures:
        print(f"  - {label}")
        print(f"      {message}")


# COMMAND ----------

# DBTITLE 1,Create Genie Space Function
"""
Bakehouse Genie Space — single-file backup script.

LAYOUT
------
1. create_genie_space()      -- reusable function (works for any course)
2. Bakehouse content         -- module-level variables   (ADD YOUR CONTENT)
3. build_bakehouse_space()   -- calls #1 with #2          (ADD YOUR CONTENT)

NOTEBOOK USAGE
--------------
    my_catalog = "labuser_jane_doe"   # set this FIRST
    %run ./bakehouse_genie_space
    space_id = build_bakehouse_space()

`my_catalog` MUST be defined in the notebook before %run -- the variables
below interpolate it at module-load time.

Backed by the documented endpoint POST /api/2.0/genie/spaces.

FIX (2026-09-03): the export proto requires several id-keyed lists to be sorted
ascending by `id` (for example, instructions.example_question_sqls). The previous
version used random uuid4 hex ids, so list order was random and creation failed
intermittently with:

    InvalidParameterValue: Invalid export proto:
    instructions.example_question_sqls must be sorted by id

The ids are now MONOTONIC (a zero-padded counter prefix + random suffix), so every
id-keyed list is naturally ascending by id AND preserves the order you authored the
items in. No post-hoc sorting needed.
"""

import uuid
import json
from typing import Optional

from databricks.sdk import WorkspaceClient


# =====================================================================
# 1. Reusable function: create a Genie Space from any inputs
# =====================================================================

def create_genie_space(
    *,
    title: str,
    description: str,
    table_identifiers: list[str],
    warehouse_name: str = "shared_warehouse",
    sample_questions: Optional[list[str]] = None,
    general_instructions: Optional[str] = None,
    sql_examples: Optional[list[dict]] = None,
    sql_expressions: Optional[list[dict]] = None,
    benchmarks: Optional[list[dict]] = None,
) -> str:
    """Create a Genie Space and return its space_id.

    `sql_expressions` are custom dimensions / metrics (CASE statements,
    calculated columns) shown under Knowledge Store -> SQL Expressions.
    Each item: {"name": str, "sql": str, "instruction": str (optional),
    "synonyms": list[str] (optional)}.
    """
    def make_id(seq: int) -> str:
        # Monotonic, unique id. The zero-padded counter prefix keeps every id-keyed
        # list ascending by id (required by the export proto) while preserving the
        # order the items were authored in. The random suffix guarantees uniqueness.
        return f"{seq:08x}{uuid.uuid4().hex[:24]}"

    def lines(text: str) -> list[str]:
        return text.splitlines(keepends=True)

    print(f"[setup]    Building Genie Space '{title}'")
    print(
        f"[setup]    {len(table_identifiers)} tables, "
        f"{len(sample_questions or [])} sample questions, "
        f"{len(sql_examples or [])} SQL examples, "
        f"{len(sql_expressions or [])} SQL expressions, "
        f"{len(benchmarks or [])} benchmarks"
    )

    # ---- Build serialized_space JSON ----
    payload: dict = {
        "version": 2,
        "data_sources": {
            "tables": sorted(
                [{"identifier": t} for t in table_identifiers],
                key=lambda x: x["identifier"],
            ),
        },
    }

    if sample_questions:
        payload["config"] = {
            "sample_questions": [
                {"id": make_id(i), "question": [q]}
                for i, q in enumerate(sample_questions)
            ],
        }

    instructions: dict = {}
    if general_instructions:
        instructions["text_instructions"] = [
            {"id": make_id(0), "content": lines(general_instructions)},
        ]
    if sql_examples:
        instructions["example_question_sqls"] = [
            {"id": make_id(i), "question": [e["question"]], "sql": lines(e["sql"])}
            for i, e in enumerate(sql_examples)
        ]
    if sql_expressions:
        instructions["sql_snippets"] = {
            "expressions": [
                {
                    "id": make_id(i),
                    "display_name": e["name"],
                    "sql": lines(e["sql"]),
                    **({"instruction": lines(e["instruction"])} if e.get("instruction") else {}),
                    **({"synonyms": list(e["synonyms"])} if e.get("synonyms") else {}),
                }
                for i, e in enumerate(sql_expressions)
            ],
        }
    if instructions:
        payload["instructions"] = instructions

    if benchmarks:
        payload["benchmarks"] = {
            "questions": [
                {
                    "id": make_id(i),
                    "question": [b["question"]],
                    "answer": [{"format": "SQL", "content": lines(b["sql"])}],
                }
                for i, b in enumerate(benchmarks)
            ],
        }

    serialized_space = json.dumps(payload)

    # ---- Resolve warehouse ----
    w = WorkspaceClient()

    FREE_EDITION = "Serverless Starter Warehouse"
    warehouses = list(w.warehouses.list())
    warehouse_id = None
    for candidate in (warehouse_name, FREE_EDITION):
        matches = [wh for wh in warehouses if wh.name == candidate]
        if len(matches) == 1:
            warehouse_id = matches[0].id
            break
        if len(matches) > 1:
            raise ValueError(f"Multiple warehouses named {candidate!r}.")
    if not warehouse_id:
        available = ", ".join(sorted(wh.name or "" for wh in warehouses)) or "(none)"
        raise ValueError(
            f"No warehouse named {warehouse_name!r} or {FREE_EDITION!r}. "
            f"Available: {available}"
        )
    resolved_name = next(wh.name for wh in warehouses if wh.id == warehouse_id)
    print(f"[setup]    Warehouse: '{resolved_name}' ({warehouse_id})")

    # ---- Create the Space ----
    parent_path = f"/Workspace/Users/{w.current_user.me().user_name}"
    print(f"[setup]    Parent path: {parent_path}")

    space = w.genie.create_space(
        warehouse_id=warehouse_id,
        serialized_space=serialized_space,
        title=title,
        description=description,
        parent_path=parent_path,
    )
    space_id = getattr(space, "space_id", None) or getattr(space, "id", None)
    if not space_id:
        raise RuntimeError(f"Create response missing space_id: {space}")
    print(f"[create] Genie Space '{title}' -> {space_id}. This might take 1-2 minutes to appear in your workspace Genie Agents.")
    return space_id

# COMMAND ----------

# DBTITLE 1,Instructions
SPACE_INSTRUCTIONS = """
- Formatting
    - Format all results using US dollars
    - Round all currency values to 2 decimal places.

- Business Rules
    - `totalPrice` represents both revenue and sales volume
    - Always include franchise name with franchise ID
    - Use `totalPrice` for total sales and performance comparisons

- Fiscal Calendar
    - Fiscal year starts in February
    - Q1: February, March, April
    - Q2: May, June, July
    - Q3: August, September, October
    - Q4: November, December, January
"""

# COMMAND ----------

# DBTITLE 1,Sample Questions
SAMPLE_QUESTIONS = [
    "How many customers do we have?"
]

# COMMAND ----------

# DBTITLE 1,SQL Expressions
SQL_EXPRESSIONS = [
    {
        "name": "region",
        "sql": f"""CASE
    WHEN {my_catalog}.genie_course_bakehouse.sales_franchises_gold.country IN ('Japan', 'Australia')
      THEN 'APJ'
    WHEN {my_catalog}.genie_course_bakehouse.sales_franchises_gold.country IN ('US', 'Canada')
      THEN 'AMER'
    WHEN {my_catalog}.genie_course_bakehouse.sales_franchises_gold.country IN ('Netherlands', 'France', 'Germany', 'Italy', 'Sweden')
      THEN 'EMEA'
    ELSE 'Other'
END""",
        "instruction": (
            "When user asks for metrics by 'region' where region is defined by "
            "business mapping of country to APJ, AMER, EMEA, or Other; "
            "SCOPE_TABLES: Use with sales_franchises_gold and sales_transactions_gold, "
            "grouping or reporting at the franchise-location level; "
            "RISK_IF_MISUSED: Do not use unless the user explicitly refers to regions "
            "per this mapping (e.g., could mislead if a different regional breakdown is "
            "implied). This is a company-specific mapping."
        ),
        "synonyms": ["franchise region", "region sales"],
    },
]

# COMMAND ----------

# DBTITLE 1,SQL Queries
SQL_EXAMPLES = [
    {"question": "Who are our best customers?", "sql": f"""
        SELECT
            c.customerID,
            c.first_name,
            c.last_name,
            SUM(t.totalPrice) AS total_spend
        FROM {my_catalog}.genie_course_bakehouse.sales_transactions_gold AS t
            JOIN {my_catalog}.genie_course_bakehouse.sales_customers_gold AS c
                ON t.customerID = c.customerID
        GROUP BY c.customerID, c.first_name, c.last_name
        ORDER BY total_spend DESC
        LIMIT 10
    """},
    {"question": "How many franchises does each supplier serve?", "sql": f"""
        SELECT
            COALESCE(s.name, 'No Matching Supplier') AS supplier_name,
            COUNT(f.franchiseID) AS franchise_count
        FROM {my_catalog}.genie_course_bakehouse.sales_franchises_gold AS f
            LEFT JOIN {my_catalog}.genie_course_bakehouse.sales_suppliers_gold AS s
                ON f.supplierID = s.supplierID
        GROUP BY s.name
        ORDER BY franchise_count DESC
    """},
]

# COMMAND ----------

# DBTITLE 1,Benchmarks
BENCHMARKS = [
    {"question": "How many customers do we have?", "sql": f"""
        SELECT COUNT(*) AS total_customers
        FROM {my_catalog}.genie_course_bakehouse.sales_customers_gold
    """},
    {"question": "What are the top 5 franchise locations by total revenue?", "sql": f"""
        WITH franchise_revenue AS (
            SELECT
                f.franchiseID,
                f.city,
                f.name,
                SUM(t.totalPrice) AS total_revenue
            FROM {my_catalog}.genie_course_bakehouse.sales_transactions_gold t
                JOIN {my_catalog}.genie_course_bakehouse.sales_franchises_gold f
                    ON t.franchiseID = f.franchiseID
            WHERE t.franchiseID IS NOT NULL
                AND t.totalPrice IS NOT NULL
                AND f.city IS NOT NULL
            GROUP BY f.franchiseID, f.city, f.name
        )
        SELECT city, name, total_revenue
        FROM (
            SELECT
                city,
                name,
                total_revenue,
                RANK() OVER (ORDER BY total_revenue DESC) AS rank
            FROM franchise_revenue
        )
        WHERE rank <= 5
    """},
    {"question": "How many franchises does each supplier serve?", "sql": f"""
        SELECT
            COALESCE(s.name, 'No Matching Supplier') AS supplier_name,
            COUNT(f.franchiseID) AS franchise_count
        FROM {my_catalog}.genie_course_bakehouse.sales_franchises_gold AS f
            LEFT JOIN {my_catalog}.genie_course_bakehouse.sales_suppliers_gold AS s
                ON f.supplierID = s.supplierID
        GROUP BY s.name
        ORDER BY franchise_count DESC
    """},
    {"question": "Who are our best customers?", "sql": f"""
        SELECT
            c.customerID,
            c.first_name,
            c.last_name,
            SUM(t.totalPrice) AS total_spend
        FROM {my_catalog}.genie_course_bakehouse.sales_transactions_gold AS t
            JOIN {my_catalog}.genie_course_bakehouse.sales_customers_gold AS c
                ON t.customerID = c.customerID
        GROUP BY c.customerID, c.first_name, c.last_name
        ORDER BY total_spend DESC
        LIMIT 10
    """},
    {"question": "What are total sales by region?", "sql": f"""
        SELECT
            CASE
                WHEN f.country IN ('Japan', 'Australia') THEN 'APJ'
                WHEN f.country IN ('US', 'Canada') THEN 'AMER'
                WHEN f.country IN ('Netherlands', 'France', 'Germany', 'Italy', 'Sweden') THEN 'EMEA'
                ELSE 'Other'
            END AS region,
            SUM(t.totalPrice) AS total_sales
        FROM {my_catalog}.genie_course_bakehouse.sales_franchises_gold AS f
            JOIN {my_catalog}.genie_course_bakehouse.sales_transactions_gold AS t
                ON f.franchiseID = t.franchiseID
        GROUP BY region
        ORDER BY total_sales DESC
    """},
    {"question": "Count of bad reviews by locations?", "sql": f"""
        SELECT
            r.ref,
            f.name AS franchise_name,
            f.city,
            COUNT(*) AS negative_review_count
        FROM {my_catalog}.genie_course_bakehouse.media_customer_reviews_gold r
            JOIN {my_catalog}.genie_course_bakehouse.sales_franchises_gold f
                ON r.ref = f.franchiseID
        WHERE r.flag = 'negative'
        GROUP BY r.ref, f.name, f.city
        ORDER BY negative_review_count DESC
    """},
]

# COMMAND ----------

# DBTITLE 1,Tables
# =====================================================================
# TABLES
# =====================================================================


TABLE_IDENTIFIERS = [
    f"{my_catalog}.genie_course_bakehouse.sales_customers_gold",
    f"{my_catalog}.genie_course_bakehouse.sales_franchises_gold",
    f"{my_catalog}.genie_course_bakehouse.sales_suppliers_gold",
    f"{my_catalog}.genie_course_bakehouse.sales_transactions_gold",
    f"{my_catalog}.genie_course_bakehouse.media_customer_reviews_gold",
]

