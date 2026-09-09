import pandas as pd
import numpy as np
from faker import Faker
import random
import os
from datetime import datetime, timedelta

fake = Faker()

# -----------------------------
# Configuration
# -----------------------------
NUM_FILES = 70                # Number of CSV files
RECORDS_PER_FILE = 1000000  # Records per CSV
OUTPUT_FOLDER = "/Volumes/iics/casemix/history/csv_files_test/"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# Random Data Lists
# -----------------------------
CASE_TYPES = [
    "INPATIENT",
    "OUTPATIENT",
    "EMERGENCY",
    "DAY SURGERY"
]

FACILITIES = [
    "General Hospital",
    "City Medical Center",
    "National Hospital",
    "Health Care Clinic",
    "Community Hospital"
]

DIAG_TYPES = [
    "PRIMARY",
    "SECONDARY",
    "PROVISIONAL"
]

PREFIXES = ["MR", "MS", "MRS", "DR"]

ARE = ["A", "B", "C", "D", "E"]
ARCL = ["X1", "Y2", "Z3", "P4", "Q5"]


def random_date(start_year=2020):
    """Generate a random date between start_year and today."""
    start = datetime(start_year, 1, 1)
    end = datetime.now()

    return (
        start
        + timedelta(
            seconds=random.randint(
                0,
                int((end - start).total_seconds())
            )
        )
    ).date()


def generate_dataframe(start_id, num_records):

    end_id = start_id + num_records

    case_ids = np.arange(start_id, end_id, dtype=np.int64)

    patient_ids = np.random.randint(
        1000000,
        9999999,
        num_records,
        dtype=np.int64
    )

    patient_acc_surr = np.random.randint(
        100000,
        999999,
        num_records,
        dtype=np.int64
    )

    los = np.random.randint(1, 31, num_records)

    htp = np.round(np.random.uniform(0, 100, num_records), 1)
    ltp = np.round(np.random.uniform(0, 100, num_records), 1)

    # -----------------------------
    # Generate Created & Updated Dates
    # Ensures Updated >= Created
    # -----------------------------
    created_dates = [
        random_date()
        for _ in range(num_records)
    ]

    today = datetime.now().date()

    updated_dates = datetime.now().date()
    data = {
        "CASE_SURR_ID": case_ids,
        "PATIENT_SURR_ID": patient_ids,
        "CASE_TYPE": np.random.choice(CASE_TYPES, num_records),
        "HEALTHCARE_FACILITY": np.random.choice(FACILITIES, num_records),

        "PATIENT_AC_NO": [
            fake.bothify("ACC########")
            for _ in range(num_records)
        ],

        "DIAG_CODE": [
            fake.bothify("D###")
            for _ in range(num_records)
        ],

        "DIAG_TYPE": np.random.choice(DIAG_TYPES, num_records),

        "MDC": [
            fake.bothify("M##")
            for _ in range(num_records)
        ],

        "DRG": [
            fake.bothify("DRG###")
            for _ in range(num_records)
        ],

        "DISCH_DATE": [
            random_date()
            for _ in range(num_records)
        ],

        "LOS": los,
        "HTP": htp,
        "LTP": ltp,

        "DH_CREATED_DATE": created_dates,
        "DH_UPDATED_DATE": updated_dates,

        "ORDER_NUMBER": [
            fake.bothify("ORD########")
            for _ in range(num_records)
        ],

        "PRFX": np.random.choice(PREFIXES, num_records),
        "ARE": np.random.choice(ARE, num_records),
        "ARCL": np.random.choice(ARCL, num_records),

        "DRG_ICD10": [
            fake.bothify("D10###")
            for _ in range(num_records)
        ],

        "MDC_ICD10": [
            fake.bothify("M10##")
            for _ in range(num_records)
        ],

        "DIAG_CODE_ICD10": [
            fake.bothify("ICD10###")
            for _ in range(num_records)
        ],

        "PATIENT_ACC_SURR_ID": patient_acc_surr
    }

    return pd.DataFrame(data)


# -----------------------------
# Generate Files
# -----------------------------
current_case_id = 1

for file_no in range(1, NUM_FILES + 1):

    print(f"Generating File {file_no}/{NUM_FILES}...")

    df = generate_dataframe(
        current_case_id,
        RECORDS_PER_FILE
    )

    file_name = os.path.join(
        OUTPUT_FOLDER,
        f"case_data_{file_no:03}.csv"
    )

    df.to_csv(file_name, index=False)

    current_case_id += RECORDS_PER_FILE

    print(f"Saved {file_name}")

print("Completed Successfully!")