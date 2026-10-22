# Databricks notebook source
# MAGIC %md
# MAGIC # Automated Test Runner — Building Reliable Conversational Agents with Genie
# MAGIC
# MAGIC Creates a **single multi-task Lakeflow Job** for one course, with optional QA checks,
# MAGIC so the full run is visible in one timeline.
# MAGIC
# MAGIC **Run structure:**
# MAGIC - Course notebooks run in the dependency order you define in `COURSE_TASKS`.
# MAGIC - **QA Content Checker** can run independently (no dependencies) alongside the course tasks.
# MAGIC - The separate **Course-specific inputs** cell makes it easy to reuse this notebook for another course.
# MAGIC
# MAGIC ```
# MAGIC  QA Check      :  qa_content_checker  (optional, parallel)
# MAGIC  Course Tasks  :  task_01  ──►  task_02  ──►  task_03
# MAGIC ```
# MAGIC
# MAGIC **What it does**
# MAGIC 1. Reads course-specific settings from a dedicated configuration cell (`COURSE_NAME`, `LAB_NOTEBOOKS`, `COURSE_TASKS`).
# MAGIC 2. Auto-fills all `<FILL_IN>` placeholders in the configured lab notebooks using the inline solution blocks.
# MAGIC 3. Resolves all notebook paths relative to this notebook's location.
# MAGIC 4. Creates (or re-creates) a single persistent Lakeflow Job for the configured course.
# MAGIC 5. Optionally adds `qa_content_checker` as an **independent task** (no dependencies).
# MAGIC 6. Triggers the job with `jobs.run_now` and polls until completion.
# MAGIC 7. Appends one result row per task to a generic results table.
# MAGIC 8. Displays a combined summary table with clickable `run_page_url` links.
# MAGIC 9. Creates and publishes a **Lakeview dashboard** from the run results and QA findings.
# MAGIC 10. Raises if any task failed — triggering Lakeflow Job failure email.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

# MAGIC %run ./Configuration

# COMMAND ----------

# MAGIC %md
# MAGIC ## Course-specific inputs

# COMMAND ----------

# Cells identified by cell_index (1-based position, counting ALL cells).
# Find the index by running: for i, c in enumerate(nb["cells"], 1): print(i, c["source"][:80])
# CELLS_TO_PATCH = [
#     {
#         "relative_path": "../data-modeling-strategies-en_us-2.0.1/Data Modeling Strategies/1. Data Warehouse Data Modeling/1.4 Demo - Entity Relationship Modeling and Constraints",
#         "cell_index": 25,
#         "handler_message": "Expected failure — demonstrating error handling. Notebook continues.",
#     }
# ]

# COMMAND ----------

# Line-level text replacements applied before the job runs and restored afterward.
#
# Each entry requires four keys:
#   relative_path    — path to the notebook, relative to this file
#   cell_index       — 1-based position of the target cell (counting ALL cells)
#   original_text    — the exact text to replace (single line or multi-line block)
#   replacement_text — the text to substitute in
#
# Leave the list empty ([]) to skip text-replacement patching entirely.
#
# This course needs NO text patches: every included notebook is complete SQL against the
# Bakehouse/HR tables created by the two setup tasks (bakehouse_setup, hr_lab_setup). There
# are no <FILL_IN> placeholders and no intentionally-broken cells. So leave this empty.
CELLS_TO_REPLACE = []

# COMMAND ----------

# # Temporarily wrap intentionally-failing cells so the job run continues past them
# # Resolve relative_path → notebook_path (absolute) before patching
# import os
# _nb_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
# _course_root = "/".join(_nb_path.split("/")[:-1])

# for p in CELLS_TO_PATCH:
#     if "notebook_path" not in p:
#         p["notebook_path"] = os.path.normpath(f"{_course_root}/{p['relative_path']}")

# restores = patch_notebooks_for_job(CELLS_TO_PATCH)

# COMMAND ----------

# ── Auto-Fill Lab Notebooks ──────────────────────────────────────────────────
# This script finds all <FILL_IN> placeholders in lab notebooks and replaces
# them with solution code extracted from the nearby solution blocks.
#
# HOW IT WORKS:
# 1. Exports each lab notebook as .ipynb JSON
# 2. Scans code cells for <FILL_IN> markers
# 3. Looks ahead in subsequent markdown cells for <code>...</code> blocks
# 4. Extracts the solution and replaces the original cell source
# 5. Re-imports the patched notebook
#
# Safe to re-run: it only patches cells that still contain <FILL_IN>.
# ──────────────────────────────────────────────────────────────────────────────

import base64
import json
import os
import re
import html as html_lib
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ExportFormat, ImportFormat, Language

w = WorkspaceClient()

# Derive course_root from this notebook's own path
_nb_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
course_root = "/".join(_nb_path.split("/")[:-1])

# LAB_NOTEBOOKS is configured in the course-specific inputs cell above.
# Resolve to absolute workspace paths
lab_abs_paths = [os.path.normpath(f"{course_root}/{p}") for p in LAB_NOTEBOOKS]

# Precompiled pattern to strip solution marker HTML comments
_MARKER_PAT = re.compile(r'\s*<!-{2,}.*?(?:ADD SOLUTION CODE|END SOLUTION CODE).*?-{2,}>\s*$')


def extract_solution_from_source(source):
    """Extract code from a Databricks solution cell.

    Handles (in priority order):
    - ADD/END SOLUTION CODE marker comments: the authoritative delimiter used by
      this course's "EXPAND FOR SOLUTION" blocks. Preferred because the surrounding
      prose often contains inline <code>…</code> snippets (e.g. <code>UPDATE</code>)
      that would otherwise be grabbed by the generic <code> fallback below and yield
      a one-word "solution". Anchoring on the markers takes only the real answer.
    - Fenced code blocks: ```python\n...\n``` (used in current labs)
    - HTML div blocks: <div class="code-block">...</div> and code-block-dark
      (this course's "Click to reveal solution" blocks use class="code-block")
    - HTML <code> tags: <code>...</code> (legacy fallback)
    - Strips %md / %md-sandbox magic prefixes before parsing.
    """
    def _clean_lines(code):
        # Strip ONLY genuine inner HTML tags (<mark>, <span ...>, </div>, <br/>, ...).
        # CRITICAL: do NOT use a greedy r'<[^>]+>' here — SQL solutions contain `<` and `>`
        # comparison operators (e.g. `AND usage_date <  '2026-03-01'`). A greedy match
        # would treat `<  '...'\n  WHERE ... >` as one "tag" and delete the SQL between
        # them, corrupting the query (observed in MOTS 2.4 Lab). A real HTML tag starts
        # with a letter or `/` right after `<` (e.g. <span>, </div>, <br/>); a SQL operator
        # is `<`/`>` followed by whitespace, a quote, digit, `=`, etc. — so anchor on that.
        code = re.sub(r'</?[a-zA-Z][a-zA-Z0-9]*(?:\s[^<>]*?)?/?>', '', code)
        lines = [l for l in code.split('\n') if not _MARKER_PAT.match(l)]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        return '\n'.join(lines) if lines else None

    # Strip Databricks magic prefix (%md, %md-sandbox, etc.)
    clean = re.sub(r'^%md[a-zA-Z-]*[ \t]*\n', '', source.lstrip(), count=1)

    # 0. ADD/END SOLUTION CODE markers (authoritative — check FIRST).
    #    The block between the "ADD SOLUTION CODE" and "END SOLUTION CODE" comment
    #    markers is the real answer. Prose before/after may contain inline <code>…</code>
    #    (e.g. the 07 Lab "UPDATE" mention) that the generic fallbacks would mis-grab.
    match = re.search(
        r'ADD SOLUTION CODE[^\n>]*-{2,}>\s*\n?(.*?)\n?\s*<!-{2,}\s*END SOLUTION CODE',
        clean, re.DOTALL,
    )
    if match:
        return _clean_lines(html_lib.unescape(match.group(1)))

    # 1. Fenced code block (most common in current labs)
    match = re.search(r'```(?:python|sql|scala|r|sh)?\s*\n(.*?)\n[ \t]*```', clean, re.DOTALL)
    if match:
        return _clean_lines(match.group(1))

    # 2. HTML div code blocks used by "Click to reveal solution" sections.
    #    Matches class="code-block" AND class="code-block-dark" (and any code-block* variant).
    #    IMPORTANT: this must run BEFORE the <code> fallback — these blocks also contain a
    #    <code> element inside the syntax-highlighter <script>, and the <code> fallback would
    #    otherwise extract that script text instead of the real SQL solution.
    match = re.search(r'<div[^>]*class="[^"]*code-block[^"]*"[^>]*>\s*\n?(.*?)\n?\s*</div>', clean, re.DOTALL)
    if match:
        return _clean_lines(html_lib.unescape(match.group(1)))

    # 3. HTML <code> tags (fallback for older lab format)
    match = re.search(r'<code[^>]*>\s*\n?(.*?)\n?\s*</code>', clean, re.DOTALL)
    if match:
        return _clean_lines(html_lib.unescape(match.group(1)))

    return None


def is_solution_candidate(cell):
    """Return True if a cell is a potential answer/solution block."""
    source = ''.join(cell.get("source", []))
    has_code_block = '```' in source or '<code>' in source or 'code-block' in source
    is_markdown_type = cell.get("cell_type") == "markdown"
    is_md_magic = cell.get("cell_type") == "code" and bool(re.match(r'\s*%md', source))
    return (is_markdown_type or is_md_magic) and has_code_block


def _source_to_lines(text):
    """Encode a cell body as a native ipynb source list (one entry per line,
    each keeping its trailing newline except the last). Databricks stores cells
    this way; writing a single joined string can round-trip inconsistently."""
    lines = text.split('\n')
    return [l + '\n' for l in lines[:-1]] + [lines[-1]]


def _needs_sql_magic(default_language, original_magic, solution):
    """Decide whether the filled cell must carry a `%sql` magic line.

    - `.sql` notebooks (default language SQL): default cells ARE SQL, no magic.
    - `.py` / `.ipynb` (default language Python): a SQL exercise cell must start
      with `%sql`, or Databricks runs it as Python and it fails. We know it's SQL
      when the original cell had a `%sql` magic OR the solution body itself is SQL.
    """
    if solution.lstrip().startswith('%'):
        return None  # solution already carries its own magic
    if default_language != 'python':
        return None  # SQL-default notebook — bare SQL is correct
    if original_magic and original_magic.lower() != '%python':
        return original_magic
    # Original magic was lost (e.g. a prior run stripped it) — infer from the body.
    if re.match(r'\s*(SELECT|INSERT|UPDATE|DELETE|MERGE|CREATE|REPLACE|DROP|ALTER|'
                r'TRUNCATE|DESCRIBE|RESTORE|WITH|USE|SHOW|GRANT|REVOKE|OPTIMIZE|'
                r'VACUUM|COPY|ANALYZE)\b', solution, re.I):
        return '%sql'
    return None


def fill_notebook(notebook_path):
    """Fill (and self-heal) all solution cells in a single lab notebook.

    Handles two cases in one pass so re-runs are safe under Pattern 2:
      1. FRESH cell — still contains <FILL_IN>: replace with the adjacent solution.
      2. STALE cell — a PRIOR run already replaced <FILL_IN> with bare SQL but
         dropped the `%sql` magic (so it now runs as Python and fails). We detect
         this when a magic-less code cell's body matches the adjacent solution
         block, and restore the `%sql` magic.

    Returns stats.
    """
    stats = {"path": notebook_path, "blanks_found": 0, "filled": 0, "healed": 0, "no_answer": 0}

    # Export notebook as ipynb
    export_resp = w.workspace.export(path=notebook_path, format=ExportFormat.JUPYTER)
    nb_json = json.loads(base64.b64decode(export_resp.content))
    cells = nb_json.get("cells", [])

    # Notebook's default language ("python" for .py/.ipynb, "sql" for .sql).
    default_language = (
        (nb_json.get("metadata", {}) or {}).get("language_info", {}) or {}
    ).get("name", "").lower()

    changed = False
    for i, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        source = ''.join(cell.get("source", []))
        if re.match(r'\s*%md', source):
            continue  # markdown-magic cell — instructional text, never fill

        has_fill = (
            bool(re.search(r'\bFILL_IN\b', source))
            or '<FILL IN>' in source
            or '--FILL IN--' in source
        )

        # Look ahead up to 5 cells for a solution block.
        solution = None
        for j in range(i + 1, min(i + 6, len(cells))):
            next_cell = cells[j]
            next_source = ''.join(next_cell.get("source", []))
            if is_solution_candidate(next_cell):
                solution = extract_solution_from_source(next_source)
                if solution:
                    break
            # Stop looking once we hit a real (non-magic) code cell
            elif next_cell.get("cell_type") == "code" and not re.match(r'\s*%', next_source):
                break

        if not solution:
            if has_fill:
                stats["blanks_found"] += 1
                stats["no_answer"] += 1
                print(f"  ⚠️  NO ANSWER FOUND for cell {i} in {notebook_path}")
            continue

        _orig_magic_m = re.match(r'\s*(%[a-zA-Z][\w-]*)', source)
        _orig_magic = _orig_magic_m.group(1) if _orig_magic_m else None
        _sol = solution.strip()

        # STALE self-heal: no <FILL_IN> left, but this magic-less code cell already
        # holds the solution body (a prior run filled it and dropped the magic).
        _body_no_magic = re.sub(r'^\s*%[a-zA-Z][\w-]*[ \t]*\n', '', source).strip()
        is_stale_filled = (not has_fill) and (_body_no_magic == _sol)

        if not has_fill and not is_stale_filled:
            continue  # unrelated code cell (e.g. %run setup) — leave alone

        if has_fill:
            stats["blanks_found"] += 1

        magic = _needs_sql_magic(default_language, _orig_magic, _sol)
        new_body = f"{magic}\n{_sol}" if magic else _sol

        if new_body.strip() == source.strip():
            continue  # already correct — nothing to change

        cell["source"] = _source_to_lines(new_body)
        changed = True
        if is_stale_filled:
            stats["healed"] += 1
            print(f"  🩹 HEALED cell {i}: restored '{magic}' magic on a previously-filled solution")
        else:
            stats["filled"] += 1

    # Re-import the patched notebook (also re-import on heal-only changes)
    if changed:
        patched_content = base64.b64encode(json.dumps(nb_json).encode()).decode()
        w.workspace.import_(
            path=notebook_path,
            content=patched_content,
            format=ImportFormat.JUPYTER,
            overwrite=True,
            language=Language.PYTHON,
        )

    return stats


# ── Run the filler ────────────────────────────────────────────────────────────
print("═" * 70)
print("AUTO-FILL LAB NOTEBOOKS")
print("═" * 70)

all_stats = []
for path in lab_abs_paths:
    print(f"\n▶ Processing: {path.split('/')[-1]}")
    try:
        s = fill_notebook(path)
        all_stats.append(s)
        print(f"   Blanks found: {s['blanks_found']}  |  Filled: {s['filled']}  |  Healed: {s.get('healed', 0)}  |  No answer: {s['no_answer']}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        all_stats.append({"path": path, "blanks_found": 0, "filled": 0, "healed": 0, "no_answer": 0, "error": str(e)})

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "═" * 70)
total_blanks = sum(s["blanks_found"] for s in all_stats)
total_filled = sum(s["filled"] for s in all_stats)
total_healed = sum(s.get("healed", 0) for s in all_stats)
total_no_ans = sum(s["no_answer"] for s in all_stats)
print(f"TOTAL:  {total_blanks} blanks found  |  {total_filled} filled  |  {total_healed} healed  |  {total_no_ans} blockers")
print("═" * 70)

# COMMAND ----------

# Apply targeted text replacements to notebook cells before the job runs.
# Resolves relative_path → notebook_path (absolute) inline, same pattern as CELLS_TO_PATCH.
import os as _os
_nb_path_tr     = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
_course_root_tr = "/".join(_nb_path_tr.split("/")[:-1])

for p in CELLS_TO_REPLACE:
    if "notebook_path" not in p:
        p["notebook_path"] = _os.path.normpath(f"{_course_root_tr}/{p['relative_path']}")

text_restores = patch_text_replacements_for_job(CELLS_TO_REPLACE)

# COMMAND ----------

# Catalog / schema / table names
# Derive catalog from the current user's login — each lab user owns a UC catalog
# named after the username portion of their email (dots/hyphens replaced with underscores).
_current_user     = spark.sql("SELECT current_user()").collect()[0][0]
_username         = _current_user.split("@")[0].replace(".", "_").replace("-", "_")

RESULTS_CATALOG   = _username   # e.g. labuser15507750_1782991657
RESULTS_SCHEMA    = "default"   # "default" schema is pre-created in every UC catalog
RESULTS_TABLE     = "notebook_run_results"
QA_FINDINGS_TABLE = "qa_content_findings"

# How long to wait for the entire job run (seconds)
TOTAL_RUN_TIMEOUT_SECONDS = 60 * 60 * 2   # 2 hour ceiling
POLL_INTERVAL_SECONDS     = 15

# Job and dashboard names
JOB_NAME       = f"[Course Validation] {COURSE_NAME}"
DASHBOARD_NAME = f"[Course Validation] {COURSE_NAME} Results Dashboard"

# Build the task list from the reusable course configuration above.
TASKS = []

if RUN_QA_CHECKER:
    TASKS.append({
        "task_key": "qa_content_checker",
        "course": "QA",
        "name": QA_TASK_NAME,
        "relative_path": QA_TASK_RELATIVE_PATH,
        "depends_on": [],
        "compute_type": DEFAULT_COMPUTE_TYPE,
    })

for task in COURSE_TASKS:
    TASKS.append({
        "task_key": task["task_key"],
        "course": COURSE_NAME,
        "name": task["name"],
        "relative_path": task["relative_path"],
        "depends_on": task.get("depends_on", []),
        "compute_type": task.get("compute_type", DEFAULT_COMPUTE_TYPE),
    })

# COMMAND ----------

# MAGIC %md
# MAGIC ## Imports and workspace client

# COMMAND ----------

import json
import os
import time
from datetime import datetime, timezone

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.compute import ClusterSpec, Environment
from databricks.sdk.service.jobs import (
    JobEmailNotifications,
    JobEnvironment,
    NotebookTask,
    RunIf,
    RunLifeCycleState,
    RunResultState,
    Task,
    TaskDependency,
)

from pyspark.sql import Row
from pyspark.sql.types import (
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

w = WorkspaceClient()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resolve workspace paths

# COMMAND ----------

this_notebook_path = (
    dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
)
course_root = "/".join(this_notebook_path.split("/")[:-1])

for t in TASKS:
    # os.path.normpath resolves '../' so Databricks gets a clean absolute path
    t["notebook_path"] = os.path.normpath(f"{course_root}/{t['relative_path']}")

# Also resolve CELLS_TO_PATCH paths
# for p in CELLS_TO_PATCH:
#     p["notebook_path"] = os.path.normpath(f"{course_root}/{p['relative_path']}")

# print(f"Course root: {course_root}\n")
for t in TASKS:
    print(f"  [{t['task_key']}]  {t['name']}\n      {t['notebook_path']}")

# if CELLS_TO_PATCH:
#     print(f"\nCells to patch ({len(CELLS_TO_PATCH)}):")
#     for p in CELLS_TO_PATCH:
#         print(f"  nuid: {p['cell_index']}  →  {p['notebook_path']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ensure results table exists

# COMMAND ----------

results_fqn = f"{RESULTS_CATALOG}.{RESULTS_SCHEMA}.{RESULTS_TABLE}"

# Ensure catalog and schema exist before writing tables
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {RESULTS_CATALOG}.{RESULTS_SCHEMA}")
print(f"Using catalog/schema: {RESULTS_CATALOG}.{RESULTS_SCHEMA}")

results_schema = StructType([
    StructField("run_timestamp",    TimestampType(), nullable=False),
    StructField("job_id",           LongType(),      nullable=True),
    StructField("job_run_id",       LongType(),      nullable=True),
    StructField("course",           StringType(),    nullable=True),
    StructField("task_key",         StringType(),    nullable=False),
    StructField("demo_name",        StringType(),    nullable=False),
    StructField("notebook_path",    StringType(),    nullable=False),
    StructField("status",           StringType(),    nullable=False),  # PASS / FAIL / TIMEOUT
    StructField("result_state",     StringType(),    nullable=True),
    StructField("life_cycle_state", StringType(),    nullable=True),
    StructField("duration_seconds", DoubleType(),    nullable=True),
    StructField("run_id",           LongType(),      nullable=True),
    StructField("run_page_url",     StringType(),    nullable=True),
    StructField("error_message",    StringType(),    nullable=True),
])

if not spark.catalog.tableExists(results_fqn):
    spark.createDataFrame([], results_schema).write.format("delta").saveAsTable(results_fqn)
    print(f"Created results table: {results_fqn}")
else:
    print(f"Results table exists: {results_fqn}")

# COMMAND ----------

# ── Optional early exit ──────────────────────────────────────────────────────
# Set RUN_SETUP_ONLY = True to run only the setup/config half (cells 1–12).
# Leave it False (or just run all cells) to continue with job creation & execution.
# ─────────────────────────────────────────────────────────────────────────────
RUN_SETUP_ONLY = False

if RUN_SETUP_ONLY:
    print("Setup complete. Stopping here — set RUN_SETUP_ONLY = False to continue with job creation.")
    dbutils.notebook.exit("Setup-only run complete.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create (or re-create) the course Lakeflow Job

# COMMAND ----------

# Delete any existing job with the same name so we always get a clean definition.

existing = [j for j in w.jobs.list(name=JOB_NAME)]
for j in existing:
    w.jobs.delete(job_id=j.job_id)
    print(f"Deleted existing job: {j.job_id} ({j.settings.name})")

# Build Task objects — compute resource determined per task via compute_type.
job_tasks = []
_warehouse_id_cache: dict = {}  # avoid repeated warehouse API calls for same warehouse
for t in TASKS:
    compute_key  = t.get("compute_type", DEFAULT_COMPUTE_TYPE)
    compute_cfg  = COMPUTE_TYPES[compute_key]
    compute_kind = compute_cfg["type"]

    # Resolve retry settings: per-task override → compute-type default → global default
    _max_retries = t.get("max_retries", TASK_MAX_RETRIES)
    _default_interval = WAREHOUSE_RETRY_INTERVAL_SECONDS if compute_kind == "warehouse" else TASK_RETRY_INTERVAL_SECONDS
    _retry_interval_ms = t.get("retry_interval_seconds", _default_interval) * 1000

    task_kwargs = dict(
        task_key=t["task_key"],
        description=t["name"],
        notebook_task=NotebookTask(notebook_path=t["notebook_path"]),
        depends_on=[TaskDependency(task_key=dep) for dep in t["depends_on"]],
        run_if=RunIf[t["run_if"]] if t.get("run_if") else None,
        max_retries=_max_retries if _max_retries > 0 else None,
        min_retry_interval_millis=_retry_interval_ms if _max_retries > 0 else None,
    )

    if compute_kind == "serverless":
        # compute_type key doubles as environment_key; tasks sharing the same
        # compute_type will reference the same JobEnvironment spec below.
        task_kwargs["environment_key"] = compute_key
    elif compute_kind == "classic_cluster":
        task_kwargs["existing_cluster_id"] = compute_cfg["cluster_id"]
    elif compute_kind == "new_cluster":
        task_kwargs["new_cluster"] = ClusterSpec(**compute_cfg["cluster_config"])
    elif compute_kind == "warehouse":
        from databricks.sdk.service.sql import CreateWarehouseRequestWarehouseType as _WarehouseType
        wh_name = compute_cfg["warehouse_name"]
        if wh_name not in _warehouse_id_cache:
            # Find existing warehouse by name, or create one
            wh_id = next((wh.id for wh in w.warehouses.list() if wh.name == wh_name), None)
            if wh_id is None:
                wh_type = _WarehouseType[compute_cfg.get("warehouse_type", "PRO").upper()]
                new_wh = w.warehouses.create(
                    name=wh_name,
                    cluster_size=compute_cfg.get("cluster_size", "2X-Small"),
                    warehouse_type=wh_type,
                    auto_stop_mins=int(compute_cfg.get("auto_stop_mins", 30)),
                )
                wh_id = new_wh.id
                print(f"  Created warehouse '{wh_name}': {wh_id}")
            else:
                print(f"  Found existing warehouse '{wh_name}': {wh_id}")
            _warehouse_id_cache[wh_name] = wh_id
        # Override notebook_task with warehouse_id — no cluster spec on Task
        task_kwargs["notebook_task"] = NotebookTask(
            notebook_path=t["notebook_path"],
            warehouse_id=_warehouse_id_cache[wh_name],
        )
    else:
        raise ValueError(f"Unknown compute type '{compute_kind}' for task '{t['task_key']}'")

    job_tasks.append(Task(**task_kwargs))

# Build one JobEnvironment per unique serverless compute_type actually used by tasks.
used_compute_keys = {t.get("compute_type", DEFAULT_COMPUTE_TYPE) for t in TASKS}
job_environments = [
    JobEnvironment(
        environment_key=ck,
        spec=Environment(environment_version=COMPUTE_TYPES[ck]["environment_version"]),
    )
    for ck in sorted(used_compute_keys)
    if COMPUTE_TYPES[ck]["type"] == "serverless"
]

created_job = w.jobs.create(
    name=JOB_NAME,
    tasks=job_tasks,
    environments=job_environments or None,
    email_notifications=JobEmailNotifications(
        on_failure=TESTER_EMAILS,
        on_success=TESTER_EMAILS,
    ),
)
job_id = created_job.job_id
print(f"Created Lakeflow Job: {job_id}  ({JOB_NAME})")
print(f"\nTask DAG:")
for t in TASKS:
    ct   = t.get("compute_type", DEFAULT_COMPUTE_TYPE)
    deps = " → depends on: " + ", ".join(t["depends_on"]) if t["depends_on"] else " (starts immediately)"
    print(f"  {t['task_key']}  [compute: {ct}]{deps}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Trigger the job run and poll until all tasks complete

# COMMAND ----------

# Brief pause after job creation to ensure config (including retry policy) is fully propagated
time.sleep(2)

run_response  = w.jobs.run_now(job_id=job_id)
job_run_id    = run_response.run_id
run_timestamp = datetime.now(timezone.utc)

print(f"Triggered job run: {job_run_id}")
print(f"Polling every {POLL_INTERVAL_SECONDS}s (timeout={TOTAL_RUN_TIMEOUT_SECONDS}s)...\n")

deadline        = time.time() + TOTAL_RUN_TIMEOUT_SECONDS
final_run       = None
terminal_states = {RunLifeCycleState.TERMINATED, RunLifeCycleState.SKIPPED, RunLifeCycleState.INTERNAL_ERROR}

while time.time() < deadline:
    run = w.jobs.get_run(run_id=job_run_id)
    lc  = run.state.life_cycle_state if run.state else None

    task_states = {
        tk.task_key: (
            tk.state.life_cycle_state.value if tk.state and tk.state.life_cycle_state else "PENDING"
        )
        for tk in (run.tasks or [])
    }
    print(f"  [{datetime.now(timezone.utc).strftime('%H:%M:%S')}] run={lc}  tasks={task_states}")

    if lc in terminal_states:
        final_run = run
        break

    time.sleep(POLL_INTERVAL_SECONDS)
else:
    print("TIMEOUT — cancelling the run.")
    try:
        w.jobs.cancel_run(run_id=job_run_id)
    except Exception:
        pass
    final_run = w.jobs.get_run(run_id=job_run_id)

print(f"\nFinal run state: {final_run.state.life_cycle_state if final_run.state else 'UNKNOWN'}")

# COMMAND ----------

# CELLS_TO_REPLACE is empty for this course, so this is a no-op (kept for parity with
# the shared runner template). CELLS_TO_PATCH restore stays disabled too.
restore_text_replacements_after_job(text_restores)
# restore_notebooks_after_job(restores)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Collect per-task results

# COMMAND ----------

task_cfg = {t["task_key"]: t for t in TASKS}

# ── Deduplicate retried tasks: keep only the latest attempt per task_key ──────
# When a task has max_retries > 0 and fails then succeeds on retry, the API
# returns ALL attempts (e.g. attempt 0 = FAILED, attempt 1 = SUCCESS).
# We only care about the final outcome.
from collections import defaultdict
_task_attempts = defaultdict(list)
for _tr in (final_run.tasks or []):
    _task_attempts[_tr.task_key].append(_tr)

deduped_tasks = []
for _tk, _attempts in _task_attempts.items():
    latest = max(_attempts, key=lambda t: t.attempt_number if t.attempt_number is not None else 0)
    deduped_tasks.append(latest)

results = []
for task_run in deduped_tasks:
    cfg   = task_cfg.get(task_run.task_key, {})
    state = task_run.state

    result_state = state.result_state.value     if state and state.result_state     else None
    life_cycle   = state.life_cycle_state.value  if state and state.life_cycle_state  else None
    error_msg    = state.state_message           if state                             else None

    duration = None
    if task_run.start_time and task_run.end_time:
        duration = float((task_run.end_time - task_run.start_time) / 1000.0)

    if life_cycle == RunLifeCycleState.TERMINATED.value and result_state == RunResultState.SUCCESS.value:
        status = "PASS"
    elif life_cycle in (RunLifeCycleState.SKIPPED.value, RunLifeCycleState.INTERNAL_ERROR.value):
        status = "FAIL"
    elif life_cycle == RunLifeCycleState.TERMINATED.value:
        status = "FAIL"
    else:
        status = "TIMEOUT"

    results.append({
        "job_id":           job_id,
        "job_run_id":       job_run_id,
        "course":           cfg.get("course", ""),
        "task_key":         task_run.task_key,
        "demo_name":        cfg.get("name", task_run.task_key),
        "notebook_path":    cfg.get("notebook_path", ""),
        "status":           status,
        "result_state":     result_state,
        "life_cycle_state": life_cycle,
        "duration_seconds": duration,
        "run_id":           task_run.run_id,
        "run_page_url":     task_run.run_page_url,
        "error_message":    error_msg,
    })

# Sort back into configured TASKS order
order = {t["task_key"]: i for i, t in enumerate(TASKS)}
results.sort(key=lambda r: order.get(r["task_key"], 999))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Append results to Delta + display summary

# COMMAND ----------

rows       = [Row(run_timestamp=run_timestamp, **r) for r in results]
results_df = spark.createDataFrame(rows, schema=results_schema)

results_df.write.format("delta").mode("append").option("mergeSchema", "true").saveAsTable(results_fqn)

print(f"Appended {results_df.count()} rows to {results_fqn}\n")

# Summary for the configured single-course run
summary_groups = [COURSE_NAME]
if RUN_QA_CHECKER:
    summary_groups.append("QA")

for group_name in summary_groups:
    group_results = [r for r in results if r["course"] == group_name]
    if not group_results:
        continue

    passed = sum(1 for r in group_results if r["status"] == "PASS")
    failed = sum(1 for r in group_results if r["status"] != "PASS")
    icon = "✅" if failed == 0 else "❌"
    label = "QA Checks" if group_name == "QA" else COURSE_NAME
    print(f"  {icon} {label}:  {passed}/{len(group_results)} passed")

print(f"\nOverall: {sum(1 for r in results if r['status'] == 'PASS')}/{len(results)} tasks passed")

display(results_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Lakeview Dashboard

# COMMAND ----------

import json
from databricks.sdk.service.dashboards import Dashboard

# ── Dashboard Configuration ────────────────────────────────────────────────────
DASHBOARD_FOLDER = "/".join(this_notebook_path.split("/")[:-2])  # Up from CourseRunner/
qa_findings_fqn = f"{RESULTS_CATALOG}.{RESULTS_SCHEMA}.{QA_FINDINGS_TABLE}"
course_label_sql = COURSE_NAME.replace("'", "''")

# ── Dataset SQL (always filters to the latest run) ────────────────────────────
run_filter = f"job_run_id = (SELECT MAX(job_run_id) FROM {results_fqn})"
qa_filter  = f"run_timestamp = (SELECT MAX(run_timestamp) FROM {qa_findings_fqn})"

status_summary_sql = (
    f"SELECT status, COUNT(*) AS task_count "
    f"FROM {results_fqn} WHERE {run_filter} "
    f"GROUP BY status ORDER BY status"
)

task_detail_sql = (
    f"SELECT CASE WHEN course = 'QA' THEN 'QA Checks' ELSE '{course_label_sql}' END AS run_group, "
    f"task_key, demo_name, status, ROUND(duration_seconds, 1) AS duration_seconds, "
    f"run_page_url, error_message "
    f"FROM {results_fqn} WHERE {run_filter} "
    f"ORDER BY CASE WHEN course = 'QA' THEN 0 ELSE 1 END, task_key"
)

qa_sev_sql = (
    f"SELECT severity, COUNT(*) AS issue_count "
    f"FROM {qa_findings_fqn} WHERE {qa_filter} "
    f"GROUP BY severity ORDER BY issue_count DESC"
) if spark.catalog.tableExists(qa_findings_fqn) else (
    "SELECT 'No Data' AS severity, 0 AS issue_count WHERE 1=0"
)

qa_detail_sql = (
    f"SELECT notebook_name, cell_index, issue_type, severity, "
    f"offending_text, suggested_fix, check_source "
    f"FROM {qa_findings_fqn} WHERE {qa_filter} "
    f"ORDER BY severity, notebook_name, cell_index"
) if spark.catalog.tableExists(qa_findings_fqn) else (
    "SELECT '' AS notebook_name, 0 AS cell_index, '' AS issue_type, "
    "'' AS severity, '' AS offending_text, '' AS suggested_fix, '' AS check_source WHERE 1=0"
)

datasets = [
    {
        "name": "ds_status_summary",
        "displayName": "Task Status Summary",
        "query": status_summary_sql,
    },
    {
        "name": "ds_task_detail",
        "displayName": "Task Results Detail",
        "query": task_detail_sql,
    },
]

pages = [
    {
        "name": "pg_runs",
        "displayName": f"{COURSE_NAME} Run Results",
        "layout": [
            {
                "widget": {
                    "name": "w_bar",
                    "title": "Task Status — Latest Run",
                    "description": "",
                    "queries": [{
                        "name": "main",
                        "query": {
                            "datasetName": "ds_status_summary",
                            "fields": [
                                {"name": "status", "expression": "`status`"},
                                {"name": "task_count", "expression": "`task_count`"}
                            ],
                            "disaggregated": True
                        }
                    }],
                    "spec": {
                        "version": 2,
                        "widgetType": "bar",
                        "encodings": {
                            "x": {"fieldName": "status", "displayName": "Status"},
                            "y": {"fieldName": "task_count", "displayName": "Tasks"},
                            "color": {"fieldName": "status", "displayName": "Status"}
                        }
                    }
                },
                "position": {"x": 0, "y": 0, "width": 6, "height": 6}
            },
            {
                "widget": {
                    "name": "w_task_table",
                    "title": "Task Results — Latest Run",
                    "description": "",
                    "queries": [{
                        "name": "main",
                        "query": {
                            "datasetName": "ds_task_detail",
                            "fields": [
                                {"name": "run_group", "expression": "`run_group`"},
                                {"name": "task_key", "expression": "`task_key`"},
                                {"name": "demo_name", "expression": "`demo_name`"},
                                {"name": "status", "expression": "`status`"},
                                {"name": "duration_seconds", "expression": "`duration_seconds`"},
                                {"name": "run_page_url", "expression": "`run_page_url`"},
                                {"name": "error_message", "expression": "`error_message`"}
                            ],
                            "disaggregated": True
                        }
                    }],
                    "spec": {
                        "version": 2,
                        "widgetType": "table",
                        "encodings": {
                            "columns": [
                                {"fieldName": "run_group", "visible": True, "title": "Run Group"},
                                {"fieldName": "task_key", "visible": True, "title": "Task Key"},
                                {"fieldName": "demo_name", "visible": True, "title": "Task Name"},
                                {"fieldName": "status", "visible": True, "title": "Status"},
                                {"fieldName": "duration_seconds", "visible": True, "title": "Duration (s)"},
                                {"fieldName": "run_page_url", "visible": True, "title": "Run URL"},
                                {"fieldName": "error_message", "visible": True, "title": "Error"}
                            ]
                        }
                    }
                },
                "position": {"x": 0, "y": 6, "width": 12, "height": 8}
            }
        ]
    }
]

if RUN_QA_CHECKER:
    datasets.extend([
        {
            "name": "ds_qa_severity",
            "displayName": "QA Issues by Severity",
            "query": qa_sev_sql,
        },
        {
            "name": "ds_qa_detail",
            "displayName": "QA Findings Detail",
            "query": qa_detail_sql,
        },
    ])

    pages.append({
        "name": "pg_qa",
        "displayName": "QA Findings",
        "layout": [
            {
                "widget": {
                    "name": "w_qa_bar",
                    "title": "QA Issues by Severity — Latest Run",
                    "description": "",
                    "queries": [{
                        "name": "main",
                        "query": {
                            "datasetName": "ds_qa_severity",
                            "fields": [
                                {"name": "severity", "expression": "`severity`"},
                                {"name": "issue_count", "expression": "`issue_count`"}
                            ],
                            "disaggregated": True
                        }
                    }],
                    "spec": {
                        "version": 2,
                        "widgetType": "bar",
                        "encodings": {
                            "x": {"fieldName": "severity", "displayName": "Severity"},
                            "y": {"fieldName": "issue_count", "displayName": "Issue Count"}
                        }
                    }
                },
                "position": {"x": 0, "y": 0, "width": 6, "height": 6}
            },
            {
                "widget": {
                    "name": "w_qa_table",
                    "title": "QA Findings Detail — Latest Run",
                    "description": "",
                    "queries": [{
                        "name": "main",
                        "query": {
                            "datasetName": "ds_qa_detail",
                            "fields": [
                                {"name": "notebook_name", "expression": "`notebook_name`"},
                                {"name": "cell_index", "expression": "`cell_index`"},
                                {"name": "issue_type", "expression": "`issue_type`"},
                                {"name": "severity", "expression": "`severity`"},
                                {"name": "offending_text", "expression": "`offending_text`"},
                                {"name": "suggested_fix", "expression": "`suggested_fix`"},
                                {"name": "check_source", "expression": "`check_source`"}
                            ],
                            "disaggregated": True
                        }
                    }],
                    "spec": {
                        "version": 2,
                        "widgetType": "table",
                        "encodings": {
                            "columns": [
                                {"fieldName": "notebook_name", "visible": True, "title": "Notebook"},
                                {"fieldName": "cell_index", "visible": True, "title": "Cell #"},
                                {"fieldName": "issue_type", "visible": True, "title": "Issue Type"},
                                {"fieldName": "severity", "visible": True, "title": "Severity"},
                                {"fieldName": "offending_text", "visible": True, "title": "Offending Text"},
                                {"fieldName": "suggested_fix", "visible": True, "title": "Suggested Fix"},
                                {"fieldName": "check_source", "visible": True, "title": "Source"}
                            ]
                        }
                    }
                },
                "position": {"x": 0, "y": 6, "width": 12, "height": 8}
            }
        ]
    })

spec = {
    "datasets": datasets,
    "pages": pages,
}

# ── Create / re-create the Lakeview Dashboard ─────────────────────────────────
try:
    for d in w.lakeview.list():
        if d.display_name == DASHBOARD_NAME:
            w.lakeview.trash(dashboard_id=d.dashboard_id)
            print(f"Replaced existing dashboard: {d.dashboard_id}")
            break
except Exception:
    pass  # No existing dashboard — proceed to create

dashboard = w.lakeview.create(Dashboard(
    display_name=DASHBOARD_NAME,
    serialized_dashboard=json.dumps(spec),
    parent_path=DASHBOARD_FOLDER,
))
w.lakeview.publish(dashboard_id=dashboard.dashboard_id)

workspace_host = spark.conf.get("spark.databricks.workspaceUrl")
dashboard_url  = f"https://{workspace_host}/dashboardsv3/{dashboard.dashboard_id}"

print(f"✅  Lakeview Dashboard created & published!")
print(f"    Name : {DASHBOARD_NAME}")
print(f"    ID   : {dashboard.dashboard_id}")
print(f"    URL  : {dashboard_url}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Fail the notebook if any task failed

# COMMAND ----------

failed = [r for r in results if r["status"] != "PASS"]
if failed:
    summary = "\n".join(
        f"  - [{r['task_key']}] {r['demo_name']}: {r['status']} ({r['result_state']}) — {r['run_page_url']}"
        for r in failed
    )
    raise RuntimeError(
        f"{len(failed)} of {len(results)} task(s) failed:\n{summary}"
    )

print(f"All {len(results)} tasks passed.")
dbutils.notebook.exit(json.dumps({
    "total":  len(results),
    "passed": len(results),
    "failed": 0,
}))
