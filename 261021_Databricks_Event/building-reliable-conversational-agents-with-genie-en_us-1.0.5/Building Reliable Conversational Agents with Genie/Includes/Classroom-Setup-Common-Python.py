# Databricks notebook source
## Determines if in Vocareum or Other Workspace and sets up the catalog
## Usage: my_catalog = build_user_catalog() within your demo/lab setup.

import re
from typing import Optional

def _safe_uc_name(value: str) -> str:
    # UC identifiers are generally safest with letters, numbers, underscores
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_]", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "user"


def _current_user_email() -> str:
    """
    Get the user's name and email address.
    """
    return spark.sql("SELECT current_user()").first()[0]


def _get_workspace_catalogs():
    """
    Returns a set of Catalogs visible to that user.
    """
    list_of_catalogs_in_workspace = [row["catalog"].strip().lower() for row in spark.sql("SHOW CATALOGS").collect()]
    return list_of_catalogs_in_workspace


def _catalog_exists(name: str, catalogs: set[str]) -> bool:
    """
    Catalog checker to see if the catalog already exists for that user.
    """
    catalog_exists = name.lower() in catalogs
    return catalog_exists


def build_user_catalog(prefix: str = "labuser", catalog_forced = None) -> str:
    """
    Returns a UC catalog name for the current user.

    Parameters
    ----------
    prefix: str
        Prefix for the catalog name. Default is 'labuser'.
    catalog_forced: str
        Uses this catalog name if specified. Otherwise uses the prefix and user's name.

    Vocareum behavior:
      - If a catalog equals the user's 'labuserxxx' name and already exists,
        assume you are in Vocareum and use it.
      - Assumes users have a catalog by default in Vocareum.

    Other workspaces:
      - Use <prefix>_<user> and create it if possible for that user.
    """

    # Obtain user's email and user name name
    user_email = _current_user_email()
    user_name = user_email.split("@")[0]

    # Make the user name safe if it's not in Vocareum
    safe_user_name = _safe_uc_name(user_name)


    # VOCAREUM CHECKER: Catalog is just the username (already provisioned)
    # and starts with 'labuser'
    vocareum_catalog_name = safe_user_name

    if user_email.lower().endswith("@vocareum.com"):
        print("✅ Vocareum Workspace check. Learner is using a Vocareum Workspace.")

        if _catalog_exists(
            name=vocareum_catalog_name,
            catalogs=_get_workspace_catalogs()
        ):
            print(
                f"✅ Catalog check. User catalog '{vocareum_catalog_name}' already exists in Vocareum. Using this catalog."
            )
            return vocareum_catalog_name
        else:
            raise ValueError(
                f"❌ Catalog '{vocareum_catalog_name}' does not exist in this Vocareum workspace. "
                "Please create the catalog or verify the catalog name before continuing."
            )

    # OTHER WORKSPACE SETUP
    else:    
        print("Learner is not using a Databricks Academy provided Vocareum Workspace.")

        # Setting catalog for workspaces outside of Vocareum using the provided prefix and user name
        # Limit the user's name to 19 characters. THis is done because there is a limit to the catalog.schema.object name (64 characters). For someone with a long name this could cause issus. Using 19 because that is the general size of the vocareum user name
        safe_user_name_char_restrict = safe_user_name[:19]

        # If catalog_forced is set, will use that by default.
        if catalog_forced is None:
            catalog_name = f"{prefix}_{safe_user_name_char_restrict}"
            print(f'Using the default catalog name: {catalog_name}')
        else:
            catalog_name = catalog_forced
            print(f'Using learner set catalog: {catalog_name}')


        # Check if the user already has this catalog with the prefix_safeusername
        if _catalog_exists(name=catalog_name, catalogs=_get_workspace_catalogs()) == True:
            print(f"✅ Catalog '{catalog_name}' already exists in your Workspace. Using this catalog.")
            return catalog_name
        elif _catalog_exists(name=catalog_name, catalogs=_get_workspace_catalogs()) == False and catalog_forced is not None:
            raise RuntimeError(
                f"Your forced catalog name '{catalog_name}' does not exist in this workspace. "
                "Catalog forced assumes the catalog already exists. "
                "Create the catalog or reference an existing one, then rerun the notebook."
            )
        else:
            try:
                print(f"Catalog name '{catalog_name}' does not exist in your Workspace.")
                print(f"Creating catalog '{catalog_name}'...")
                spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog_name}")
                print(f"✅ Created catalog '{catalog_name}'.")
                return catalog_name
            except Exception as e:
                print(
                    f"⚠️ Could not create catalog '{catalog_name}'. "
                    "You may not have privileges to create catalogs in this workspace.\n"
                    f"Error: {e}"
                )

# COMMAND ----------

def setup_complete_msg():
  '''
  Prints a note in the output that the setup was complete.
  '''
  print('\n------------------------------------------------------------------------------')
  print('✅ SETUP COMPLETE!')
  print('------------------------------------------------------------------------------')

# COMMAND ----------

def display_config_values(config_values):
    """
    Displays list of key-value pairs as rows of HTML text and textboxes
    
    param config_values: 
        list of (key, value) tuples
        
    Returns
    ----------
    HTML output displaying the config values
    Example
    --------
    display_config_values([('catalog', 'your catalog'),('schema','your schema')])
    """
    html = """<table style="width:100%">"""
    for name, value in config_values:
        html += f"""
        <tr>
            <td style="white-space:nowrap; width:1em">{name}:</td>
            <td><input type="text" value="{value}" style="width: 100%"></td></tr>"""
    html += "</table>"
    displayHTML(html)

# COMMAND ----------

my_catalog = build_user_catalog(catalog_forced = None)
