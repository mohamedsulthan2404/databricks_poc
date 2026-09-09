import csv
import random
import os
from datetime import datetime, timedelta

# -----------------------------
# Configuration
# -----------------------------
NUM_FILES = 30
RECORDS_PER_FILE = 1_000_000
OUTPUT_FOLDER = "/Volumes/iics/casemix/history/csv_files_test/"

# -----------------------------
# Random Data Lists
# -----------------------------
CASE_TYPES = [
    "INPATIENT",
    "OUTPATIENT",
    "EMERGENCY",
    "DAY SURGERY",
]

FACILITIES = [
    "General Hospital",
    "City Medical Center",
    "National Hospital",
    "Health Care Clinic",
    "Community Hospital",
]

DIAG_TYPES = [
    "PRIMARY",
    "SECONDARY",
    "PROVISIONAL",
]

PREFIXES = ["MR", "MS", "MRS", "DR"]
ARE = ["A", "B", "C", "D", "E"]
ARCL = ["X1", "Y2", "Z3", "P4", "Q5"]

CSV_COLUMNS = [
    "CASE_SURR_ID",
    "PATIENT_SURR_ID",
    "CASE_TYPE",
    "HEALTHCARE_FACILITY",
    "PATIENT_AC_NO",
    "DIAG_CODE",
    "DIAG_TYPE",
    "MDC",
    "DRG",
    "DISCH_DATE",
    "LOS",
    "HTP",
    "LTP",
    "DH_CREATED_DATE",
    "DH_UPDATED_DATE",
    "ORDER_NUMBER",
    "PRFX",
    "ARE",
    "ARCL",
    "DRG_ICD10",
    "MDC_ICD10",
    "DIAG_CODE_ICD10",
    "PATIENT_ACC_SURR_ID",
]


def random_date(start_year=2020):
    """Generate a random date between start_year and today."""
    start = datetime(start_year, 1, 1)
    end = datetime.now()

    random_seconds = random.randint(
        0,
        int((end - start).total_seconds()),
    )

    return (start + timedelta(seconds=random_seconds)).date()


def random_digits(length):
    """Generate a numeric string with the requested number of digits."""
    return "".join(random.choices("0123456789", k=length))


def generate_record(case_id):
    """Generate one CSV record using only Python standard-library modules."""

    patient_id = random.randint(1_000_000, 9_999_999)
    patient_acc_surr_id = random.randint(100_000, 999_999)

    los = random.randint(1, 30)

    htp = round(random.uniform(0, 100), 1)
    ltp = round(random.uniform(0, 100), 1)

    created_date = random_date()
    updated_date = datetime.now().date()

    return [
        case_id,
        patient_id,
        random.choice(CASE_TYPES),
        random.choice(FACILITIES),
        "ACC" + random_digits(8),
        "D" + random_digits(3),
        random.choice(DIAG_TYPES),
        "M" + random_digits(2),
        "DRG" + random_digits(3),
        random_date(),
        los,
        htp,
        ltp,
        created_date,
        updated_date,
        "ORD" + random_digits(8),
        random.choice(PREFIXES),
        random.choice(ARE),
        random.choice(ARCL),
        "D10" + random_digits(3),
        "M10" + random_digits(2),
        "ICD10" + random_digits(3),
        patient_acc_surr_id,
    ]


def generate_csv(file_path, start_case_id, num_records):
    """Generate a CSV file by streaming records directly to disk."""

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8",
        buffering=1024 * 1024,
    ) as csv_file:

        writer = csv.writer(csv_file, delimiter="|")
        writer.writerow(CSV_COLUMNS)

        for i in range(num_records):
            case_id = start_case_id + i
            writer.writerow(generate_record(case_id))

            if (i + 1) % 100_000 == 0:
                print(
                    f"    {i + 1:,}/{num_records:,} records generated",
                    flush=True,
                )


def main():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    current_case_id = 1
    start_time = datetime.now()

    print("=" * 60)
    print("Dummy CSV Data Generator")
    print("=" * 60)
    print(f"Number of files       : {NUM_FILES:,}")
    print(f"Records per file      : {RECORDS_PER_FILE:,}")
    print(f"Total records         : {NUM_FILES * RECORDS_PER_FILE:,}")
    print(f"Output folder         : {OUTPUT_FOLDER}")
    print("Dependencies          : Python standard library only")
    print("=" * 60)

    for file_no in range(1, NUM_FILES + 1):

        print()
        print(f"Generating File {file_no}/{NUM_FILES}...")

        file_name = os.path.join(
            OUTPUT_FOLDER,
            f"case_data_{file_no:03}.csv",
        )

        file_start_time = datetime.now()

        generate_csv(
            file_name,
            current_case_id,
            RECORDS_PER_FILE,
        )

        current_case_id += RECORDS_PER_FILE

        elapsed = datetime.now() - file_start_time
        file_size_mb = os.path.getsize(file_name) / (1024 * 1024)

        print(f"Saved       : {file_name}")
        print(f"File size   : {file_size_mb:,.2f} MB")
        print(f"Time taken  : {elapsed}")

    total_elapsed = datetime.now() - start_time

    print()
    print("=" * 60)
    print("Completed Successfully!")
    print("=" * 60)
    print(f"Files generated  : {NUM_FILES:,}")
    print(f"Total records    : {NUM_FILES * RECORDS_PER_FILE:,}")
    print(f"Output folder    : {OUTPUT_FOLDER}")
    print(f"Total time       : {total_elapsed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
