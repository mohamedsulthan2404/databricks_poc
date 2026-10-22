# Databricks notebook source
# Change the course name as per your course name
COURSE_NAME = "Building Reliable Conversational Agents with Genie"
RUN_QA_CHECKER = True
QA_TASK_RELATIVE_PATH = "./qa_content_checker"
QA_TASK_NAME = "QA Content Checker — Grammar, Deprecated, UI Steps"

# Tester emails — notified on job failure and success. Add as many as you like with comma seperated emails
TESTER_EMAILS = [
    "gourav.prajapati@databricks.com"
]

# Course folder — this runner lives INSIDE the course folder at
# .../Includes/automation/, so "../.." goes up two levels to the course root.
# Each relative_path is then "../../<notebook>".
_PKG = "../.."

# No lab notebooks need auto-filling: this course has NO <FILL_IN> placeholders anywhere
# (verified across all 13 lesson notebooks). The two Labs (05, 12) are SQL exploration +
# UI "build a Genie agent" exercises whose executable cells are complete SQL. Leave empty.
LAB_NOTEBOOKS = []

# ── Compute Type Registry ─────────────────────────────────────────────────────
# Define all compute configurations available to tasks in this course.
# Each key becomes the compute_type value you assign to a task in COURSE_TASKS.
# Cell 14 reads these entries to create the correct compute resource per task.
#
# Supported "type" values:
#   "serverless"      – Databricks Serverless. Requires: environment_version (str)
#   "classic_cluster" – Existing all-purpose cluster. Requires: cluster_id (str)
#   "new_cluster"     – New cluster per run. Requires: cluster_config (dict)
#                       Keys map directly to ClusterSpec fields:
#                       spark_version, node_type_id, num_workers, etc.
#
# Tasks that omit compute_type fall back to DEFAULT_COMPUTE_TYPE.
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_COMPUTE_TYPE = "serverless_v5"

COMPUTE_TYPES = {
    "serverless_v5": {
        "type": "serverless",
        "environment_version": "5",
    },
    # ── SQL Warehouse ─────────────────────────────────────────────────────────
    # Use for notebooks that require a SQL warehouse (e.g. SQL Scripting,
    # Stored Procedures). The job will find an existing warehouse by name or
    # create one automatically using the config below.
    # Only PRO / Serverless warehouses are supported — not Classic.
    "shared_warehouse": {
        "type": "warehouse",
        "warehouse_name": "shared_warehouse",
        "cluster_size": "2X-Small",
        "warehouse_type": "PRO",
        "auto_stop_mins": 30,
    },
    # "serverless_v4": {
    #     "type": "serverless",
    #     "environment_version": "4",
    # },
    # "my_classic_cluster": {
    #     "type": "classic_cluster",
    #     "cluster_id": "<your-cluster-id>",
    # },
    # "new_standard_cluster": {
    #     "type": "new_cluster",
    #     "cluster_config": {
    #         "spark_version": "15.4.x-scala2.12",
    #         "node_type_id":  "i3.xlarge",
    #         "num_workers":   2,
    #     },
    # },
}

# ── Task Retry Policy ─────────────────────────────────────────────────────────
# Controls automatic retries for failed tasks. Helps handle transient issues
# like Unity Catalog metadata propagation delays after the setup task creates
# schemas/tables that aren't immediately visible to downstream tasks.
#
# Set TASK_MAX_RETRIES = 0 to disable retries entirely.
# Per-task override: add "max_retries" and/or "retry_interval_seconds" keys
# to any entry in COURSE_TASKS to override the global defaults for that task.
# ─────────────────────────────────────────────────────────────────────────────
TASK_MAX_RETRIES = 2                    # Number of retries on failure (0 = no retries)
TASK_RETRY_INTERVAL_SECONDS = 30        # Seconds to wait between retry attempts (global default)
WAREHOUSE_RETRY_INTERVAL_SECONDS = 45   # Seconds for warehouse tasks (cross-compute metadata sync is slower)

# ── Course notebook DAG ───────────────────────────────────────────────────────
# Classification (by executable-cell content + language). This is a Genie-agent course:
# lessons alternate SQL data-exploration notebooks with UI walk-throughs (build/curate a
# Genie space by hand). Only notebooks with real runnable SQL become tasks. NO lesson
# notebook makes a live Genie API/SDK call — every code cell is SQL against setup-created
# tables (verified), so they all run headless.
#
#   RUN AS NOTEBOOK TASKS:
#     bakehouse_setup 02 Demo - Bakehouse Setup      shared_warehouse  (%run creating-genie-agent → 0-REQUIRED: CREATEs the shared Bakehouse sales_*_gold + media_customer_reviews_gold tables; then SHOW/SELECT previews)
#     demo_04         04 Demo - Adding Benchmarks    shared_warehouse  (SQL: benchmark queries + DECLARE my_query on Bakehouse _gold tables)
#     demo_07         07 Demo - Adding Metadata      serverless        (python-lang .ipynb, %sql cells: COMMENT ON / ALTER / DESCRIBE on Bakehouse tables)
#     demo_08         08 Demo - SQL Logic & Instr.   serverless        (python-lang .ipynb, %sql cells: DECLARE my_query benchmark SQL)
#     demo_09         09 Demo - Sharing / End User   serverless        (python-lang .ipynb, %sql cells: ALTER TABLE SET TAG + SELECT)
#     hr_lab_setup    05 Lab - Create an HR Agent    shared_warehouse  (%run lab-setup: self-contained, CREATEs the genie_course_hr tables; then SHOW/SELECT previews)
#     lab_12          12 Lab - Improve HR Knowledge  shared_warehouse  (SQL: COMMENT ON / DESCRIBE / DECLARE my_query on HR tables)
#
#   COMPUTE RULE ([[feedback_compute_type_nonsql]]): notebooks whose default language is
#   Python (07, 08, 09 — .ipynb with %sql cells) run on serverless. The pure sql-language
#   notebooks (02, 04, 05, 12) run on shared_warehouse; their setups %run only the
#   SQL-language Classroom-Setup-Common-SQL-WAREHOUSE chain (no Python), so warehouse is fine.
#
#   EXCLUDED — lecture / pure-UI (0 executable cells; verified none create shared data):
#     00 - Course Overview                     overview, 0 code cells.
#     01 Lecture - Introduction to Genie       lecture, 0 code cells.
#     03 Demo - Creating & Exploring a Genie    UI: build a Genie agent by hand; its ONLY
#                                               exec cell is the same %run creating-genie-agent
#                                               setup that bakehouse_setup (02) already runs.
#     06 Lecture - Curating an Effective Agent  lecture, 0 code cells.
#     10 Demo - Monitoring Genie Conversations  UI: review monitoring in the Genie UI, 0 code cells.
#     11 Lecture - Summary and Next Steps       lecture, 0 code cells.
#     Solution Demo Genie Agent/                instructor asset (SDK-creates the solution Genie
#                                               agents); not a student lesson.
#
# DATA PREREQUISITE (two independent datasets):
#   • BAKEHOUSE (sales_*_gold, media_customer_reviews_gold): created ONLY by
#     Classroom-Setup-0-REQUIRED-tables, which is chained solely through
#     Classroom-Setup-creating-genie-agent — i.e. by notebook 02. Demos 04/07/08/09 %run
#     setups (adding-benchmarks / creating-table-column-descriptions /
#     adding-sql-logic-instructions / consuming-monitoring) that only run Common-SQL-WAREHOUSE
#     (procedures + catalog/schema) and DO NOT create the tables — so they hard-depend on 02.
#   • HR (employees, compensation, managers, resignations): created by the self-contained
#     Classroom-Setup-lab-setup — i.e. by notebook 05. Lab 12 %runs the same lab-setup, so
#     it depends on 05 (both use schema genie_course_hr).
#   Common-SQL-WAREHOUSE sets my_schema and USE SCHEMA so bare table names resolve.
#
# DEPENDENCIES: 04/07/08/09 chain after bakehouse_setup (02); 12 chains after hr_lab_setup
# (05). The Bakehouse demos only read the _gold tables (07 also runs COMMENT ON / ALTER
# COLUMN metadata — additive, idempotent), so serialize the Bakehouse branch to avoid two
# tasks mutating the same tables at once. HR branch (05 → 12) is independent and parallel.
COURSE_TASKS = [
    # ── Bakehouse branch ─────────────────────────────────────────────────────────
    {
        "task_key": "bakehouse_setup",
        "name": "02 Demo - Bakehouse Setup and Data Exploration (creates shared Bakehouse _gold tables)",
        "relative_path": f"{_PKG}/02 Demo - Bakehouse Setup and Data Exploration",
        "depends_on": [],
        "compute_type": "shared_warehouse",   # sql-lang; setup chain is pure SQL
    },
    {
        "task_key": "demo_04",
        "name": "04 Demo - Adding Genie Benchmarks",
        "relative_path": f"{_PKG}/04 Demo - Adding Genie Benchmarks",
        "depends_on": ["bakehouse_setup"],
        "compute_type": "shared_warehouse",   # SQL on Bakehouse _gold tables
    },
    {
        "task_key": "demo_07",
        "name": "07 Demo - Adding Metadata to the Knowledge Store",
        "relative_path": f"{_PKG}/07 Demo - Adding Metadata to the Knowledge Store",
        "depends_on": ["demo_04"],
        "compute_type": "serverless_v5",   # python-lang .ipynb w/ %sql cells (COMMENT ON / ALTER)
    },
    {
        "task_key": "demo_08",
        "name": "08 Demo - Adding SQL Logic and Instructions to the Knowledge Store",
        "relative_path": f"{_PKG}/08 Demo - Adding SQL Logic and Instructions to the Knowledge Store",
        "depends_on": ["demo_07"],
        "compute_type": "serverless_v5",   # python-lang .ipynb w/ %sql cells
    },
    {
        "task_key": "demo_09",
        "name": "09 Demo - Sharing and the End User Experience with Genie One",
        "relative_path": f"{_PKG}/09 Demo - Sharing and the End User Experience with Genie One",
        "depends_on": ["demo_08"],
        "compute_type": "serverless_v5",   # python-lang .ipynb w/ %sql cells (ALTER TABLE SET TAG)
    },
    # ── HR branch (independent of Bakehouse) ─────────────────────────────────────
    {
        "task_key": "hr_lab_setup",
        "name": "05 Lab - Create an HR Genie Agent (creates genie_course_hr tables)",
        "relative_path": f"{_PKG}/05 Lab - Create an HR Genie Agent",
        "depends_on": [],
        "compute_type": "shared_warehouse",   # sql-lang; lab-setup self-contained
    },
    {
        "task_key": "lab_12",
        "name": "12 Lab - Improve the Knowledge Store for the HR Genie Agent",
        "relative_path": f"{_PKG}/12 Lab - Improve the Knowledge Store for the HR Genie Agent",
        "depends_on": ["hr_lab_setup"],
        "compute_type": "shared_warehouse",   # SQL on HR tables
    },
]

# COMMAND ----------

# ─────────────────────────────────────────────────────────────────────────────
# Utility: wrap_failing_sql_cell / restore_sql_cell
#
# Purpose
# -------
# Some demo notebooks contain SQL cells that are *intentionally designed to fail*
# (e.g. to demonstrate BEGIN...END halting behaviour). When those notebooks run
# as job tasks the cell failure stops the entire notebook, skipping all
# subsequent cells (cleanup, further demos, etc.).
#
# These helpers let the course tester temporarily wrap any such cell with an
# outer BEGIN...DECLARE EXIT HANDLER...END block — pure SQL, no language change
# — so the notebook continues past the intentional failure. After the job
# completes the original source is restored so students always see the clean
# demo notebook.
#
# Identifying the target cell
# ----------------------------
# Cells are identified by cell_index: the 1-based position of the cell within
# the notebook (counting ALL cells, markdown included). Unlike cell_nuid —
# which regenerates every time a lab notebook is re-provisioned/reset — a
# cell's position in an unchanged template stays the same across resets, so
# cell_index remains valid as long as no cells are added/removed above the
# target cell.
#
# How to use
# ----------
# 1. Before job creation / run:
#       restores = patch_notebooks_for_job(CELLS_TO_PATCH)
#
# 2. After job completes (pass/fail):
#       restore_notebooks_after_job(restores)
#
# CELLS_TO_PATCH is a list of dicts defined in the cell that follows this one.
# Each entry:
#   {
#       "notebook_path"  : absolute workspace path to the notebook,
#       "cell_index"     : 1-based position of the SQL cell to wrap,
#       "handler_message": (optional) text returned by the handler SELECT,
#   }
# ─────────────────────────────────────────────────────────────────────────────

import base64, json, os
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ExportFormat, ImportFormat

_sdk_client = None

def _get_client(w=None):
    """Returns a WorkspaceClient, reusing a module-level instance if available."""
    if w:
        return w
    global _sdk_client
    if _sdk_client is None:
        _sdk_client = WorkspaceClient()
    return _sdk_client


def _get_cell_source(cell):
    """Returns a cell's source as a single string, regardless of list/str form."""
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def wrap_failing_sql_cell(
    notebook_path: str,
    cell_index: int,
    handler_message: str = None,
    w=None,
) -> str:
    """
    Wraps a SQL cell's BEGIN...END block with an outer DECLARE EXIT HANDLER
    so the notebook continues executing even if the inner block fails.
    The cell stays SQL — no language change.

    Args:
        notebook_path   : Absolute workspace path to the target notebook.
        cell_index      : 1-based position of the cell to wrap (counting ALL
                          cells, markdown included).
        handler_message : Optional message shown as a result row when the
                          exception is caught.
        w               : WorkspaceClient to reuse (optional).
    Returns:
        original_source (str) — pass this to restore_sql_cell() to undo.
    """
    _w  = _get_client(w)
    msg = handler_message or (
        "[Expected failure] The inner BEGIN...END block failed as designed. "
        "Notebook continues."
    )

    # --- export
    export  = _w.workspace.export(path=notebook_path, format=ExportFormat.JUPYTER)
    nb      = json.loads(base64.b64decode(export.content))
    cells   = nb.get("cells", [])

    if not (1 <= cell_index <= len(cells)):
        raise ValueError(
            f"cell_index={cell_index} out of range for {notebook_path} "
            f"(notebook has {len(cells)} cells)"
        )
    cell = cells[cell_index - 1]

    original_source = _get_cell_source(cell)
    indented = "\n".join("  " + line for line in original_source.splitlines())
    cell["source"] = (
        "-- Outer block catches the expected error; inner block is unchanged.\n"
        "BEGIN\n"
        "  DECLARE EXIT HANDLER FOR SQLEXCEPTION\n"
        f"    SELECT '{msg}' AS message;\n\n"
        "  BEGIN\n"
        f"{indented}\n"
        "  END;\n"
        "END;"
    )

    # --- re-import
    encoded = base64.b64encode(json.dumps(nb).encode()).decode()
    _w.workspace.import_(
        path=notebook_path,
        format=ImportFormat.JUPYTER,
        overwrite=True,
        content=encoded,
    )
    print(f"  ✅ Wrapped  : {notebook_path.split('/')[-1]}  (cell index {cell_index})")
    return original_source


def restore_sql_cell(
    notebook_path: str,
    cell_index: int,
    original_source: str,
    w=None,
):
    """
    Restores a cell to its original source. Reverses wrap_failing_sql_cell().
    Use the SAME cell_index that was passed to wrap_failing_sql_cell().

    Args:
        notebook_path  : Absolute workspace path to the target notebook.
        cell_index     : 1-based position of the cell to restore.
        original_source: The string returned by wrap_failing_sql_cell().
        w              : WorkspaceClient to reuse (optional).
    """
    _w     = _get_client(w)
    export = _w.workspace.export(path=notebook_path, format=ExportFormat.JUPYTER)
    nb     = json.loads(base64.b64decode(export.content))
    cells  = nb.get("cells", [])

    if not (1 <= cell_index <= len(cells)):
        raise ValueError(
            f"cell_index={cell_index} out of range for {notebook_path} "
            f"(notebook has {len(cells)} cells)"
        )
    cells[cell_index - 1]["source"] = original_source

    encoded = base64.b64encode(json.dumps(nb).encode()).decode()
    _w.workspace.import_(
        path=notebook_path,
        format=ImportFormat.JUPYTER,
        overwrite=True,
        content=encoded,
    )
    print(f"  ✅ Restored : {notebook_path.split('/')[-1]}  (cell index {cell_index})")


def patch_notebooks_for_job(patches: list, w=None) -> list:
    """
    Wraps all cells listed in `patches` before a job run.
    Returns a restore-list to pass to restore_notebooks_after_job().

    Args:
        patches : list of dicts, each with keys:
                    notebook_path   (str) — absolute workspace path
                    cell_index      (int) — 1-based position of the failing cell
                    handler_message (str, opt) — custom handler message
        w       : WorkspaceClient to reuse (optional).
    Returns:
        restores (list) — same dicts with 'original_source' added.
    """
    print("\n═" * 36 + "\nPATCHING NOTEBOOKS FOR JOB RUN\n" + "═" * 36)
    restores = []
    for p in patches:
        original = wrap_failing_sql_cell(
            notebook_path   = p["notebook_path"],
            cell_index      = p["cell_index"],
            handler_message = p.get("handler_message"),
            w               = w,
        )
        restores.append({**p, "original_source": original})
    print(f"  {len(restores)} cell(s) patched.\n")
    return restores


def restore_notebooks_after_job(restores: list, w=None):
    """
    Restores all cells patched by patch_notebooks_for_job().

    Args:
        restores : the list returned by patch_notebooks_for_job().
        w        : WorkspaceClient to reuse (optional).
    """
    print("\n═" * 36 + "\nRESTORING NOTEBOOKS AFTER JOB RUN\n" + "═" * 36)
    for r in restores:
        restore_sql_cell(r["notebook_path"], r["cell_index"], r["original_source"], w=w)
    print(f"  {len(restores)} cell(s) restored.\n")



# ─────────────────────────────────────────────────────────────────────────────
# replace_cell_text / restore_cell_text
#
# Purpose
# -------
# Generic text-replacement helpers: swap a specific substring in a notebook
# cell's source before a job run, then put it back afterward.
#
# Useful when a single line in an already-filled notebook needs a small tweak
# for automated testing (e.g. converting an intentional single-statement
# failure into a no-op) without wrapping the whole cell in a
# BEGIN...DECLARE EXIT HANDLER block.
#
# Four parameters
# ---------------
#   notebook_path    — absolute workspace path to the notebook
#   cell_index       — 1-based position of the cell (counting ALL cells)
#   original_text    — the exact text to find (can span multiple lines)
#   replacement_text — the text to substitute in
# ─────────────────────────────────────────────────────────────────────────────

def replace_cell_text(
    notebook_path: str,
    cell_index: int,
    original_text: str,
    replacement_text: str,
    w=None,
) -> str:
    """
    Replaces a specific text substring in a notebook cell's source.

    Args:
        notebook_path    : Absolute workspace path to the target notebook.
        cell_index       : 1-based position of the cell to modify (counting ALL cells).
        original_text    : The exact text to find and replace.
        replacement_text : The text to substitute in.
        w                : WorkspaceClient to reuse (optional).
    Returns:
        original_source (str) — the full original cell source before replacement.
                                Pass to restore_cell_text() to undo.
    """
    _w = _get_client(w)
    export = _w.workspace.export(path=notebook_path, format=ExportFormat.JUPYTER)
    nb = json.loads(base64.b64decode(export.content))
    cells = nb.get("cells", [])

    if not (1 <= cell_index <= len(cells)):
        raise ValueError(
            f"cell_index={cell_index} out of range for {notebook_path} "
            f"(notebook has {len(cells)} cells)"
        )

    cell = cells[cell_index - 1]
    original_source = _get_cell_source(cell)

    if original_text not in original_source:
        raise ValueError(
            f"original_text not found in cell {cell_index} of "
            f"{notebook_path.split('/')[-1]!r}.\n"
            f"original_text: {original_text!r}"
        )

    cell["source"] = original_source.replace(original_text, replacement_text, 1)

    encoded = base64.b64encode(json.dumps(nb).encode()).decode()
    _w.workspace.import_(
        path=notebook_path,
        format=ImportFormat.JUPYTER,
        overwrite=True,
        content=encoded,
    )
    print(f"  ✅ Replaced : {notebook_path.split('/')[-1]}  (cell index {cell_index})")
    return original_source


def restore_cell_text(
    notebook_path: str,
    cell_index: int,
    original_source: str,
    w=None,
):
    """
    Restores a cell to its original source. Reverses replace_cell_text().

    Args:
        notebook_path  : Absolute workspace path to the target notebook.
        cell_index     : 1-based position of the cell to restore.
        original_source: The string returned by replace_cell_text().
        w              : WorkspaceClient to reuse (optional).
    """
    _w = _get_client(w)
    export = _w.workspace.export(path=notebook_path, format=ExportFormat.JUPYTER)
    nb = json.loads(base64.b64decode(export.content))
    cells = nb.get("cells", [])

    if not (1 <= cell_index <= len(cells)):
        raise ValueError(
            f"cell_index={cell_index} out of range for {notebook_path} "
            f"(notebook has {len(cells)} cells)"
        )
    cells[cell_index - 1]["source"] = original_source

    encoded = base64.b64encode(json.dumps(nb).encode()).decode()
    _w.workspace.import_(
        path=notebook_path,
        format=ImportFormat.JUPYTER,
        overwrite=True,
        content=encoded,
    )
    print(f"  ✅ Restored : {notebook_path.split('/')[-1]}  (cell index {cell_index})")


def patch_text_replacements_for_job(patches: list, w=None) -> list:
    """
    Applies targeted text replacements to notebook cells before a job run.
    Returns a restore-list to pass to restore_text_replacements_after_job().

    Args:
        patches : list of dicts, each with keys:
                    notebook_path    (str) — absolute workspace path
                    cell_index       (int) — 1-based position of the cell
                    original_text    (str) — exact text to replace
                    replacement_text (str) — text to substitute in
        w       : WorkspaceClient to reuse (optional).
    Returns:
        restores (list) — same dicts with 'original_source' added.
    """
    if not patches:
        print("  (no text replacements configured)\n")
        return []
    print("\n" + "═" * 36 + "\nAPPLYING TEXT REPLACEMENTS FOR JOB RUN\n" + "═" * 36)
    restores = []
    for p in patches:
        original = replace_cell_text(
            notebook_path    = p["notebook_path"],
            cell_index       = p["cell_index"],
            original_text    = p["original_text"],
            replacement_text = p["replacement_text"],
            w                = w,
        )
        restores.append({**p, "original_source": original})
    print(f"  {len(restores)} cell(s) patched.\n")
    return restores


def restore_text_replacements_after_job(restores: list, w=None):
    """
    Restores all cells patched by patch_text_replacements_for_job().

    Args:
        restores : the list returned by patch_text_replacements_for_job().
        w        : WorkspaceClient to reuse (optional).
    """
    if not restores:
        print("  (nothing to restore)\n")
        return
    print("\n" + "═" * 36 + "\nRESTORING TEXT REPLACEMENTS AFTER JOB RUN\n" + "═" * 36)
    for r in restores:
        restore_cell_text(r["notebook_path"], r["cell_index"], r["original_source"], w=w)
    print(f"  {len(restores)} cell(s) restored.\n")


print("✅ Utility functions loaded: wrap_failing_sql_cell, restore_sql_cell,"
      " patch_notebooks_for_job, restore_notebooks_after_job,"
      " replace_cell_text, restore_cell_text,"
      " patch_text_replacements_for_job, restore_text_replacements_after_job")
