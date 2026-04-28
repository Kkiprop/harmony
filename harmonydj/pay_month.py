import json
import csv
from collections import defaultdict
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================
INPUT_JSON_FILE = r"C:\Users\Admin\p24\harmonydj\harmonydj\Payroll_daily.json"
OUTPUT_CSV_FILE = r"C:\Users\Admin\p24\harmonydj\harmonydj\Payroll_monthly.csv"

START_MONTH = "2025-09"
END_MONTH   = "2026-04"

# =====================================================
# GENERATE MONTHS
# =====================================================
def generate_months(start_month, end_month):
    months = []
    current = datetime.strptime(start_month, "%Y-%m")
    end = datetime.strptime(end_month, "%Y-%m")

    while current <= end:
        months.append(current.strftime("%Y-%m"))

        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return months


months = generate_months(START_MONTH, END_MONTH)

# =====================================================
# LOAD JSON
# =====================================================
with open(INPUT_JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# =====================================================
# STORE DATA
# =====================================================
store_totals = defaultdict(lambda: defaultdict(float))
all_stores = set()

# =====================================================
# ALIAS NORMALIZATION
# =====================================================
def normalize_store(store_name):
    name = store_name.strip().lower()

    if name in [
        "apni mandi fulfillment centre",
        "amfc",
        "amf"
    ]:
        return "AMFC"

    return store_name.strip()


# =====================================================
# AGGREGATE DAILY INTO MONTHLY
# =====================================================
for doc in data:
    date_str = doc.get("date")
    payroll_data = doc.get("payroll_data", {})

    if not date_str:
        continue

    month = date_str[:7]

    if month not in months:
        continue

    for store, amount in payroll_data.items():

        if amount is None:
            continue

        store = normalize_store(store)

        all_stores.add(store)

        store_totals[store][month] += float(amount)

# =====================================================
# HANDLE PRIORITY RULE
# If both AMFC and old full name exist, keep AMFC only
# =====================================================
old_name = "Apni mandi fulfillment centre"

if old_name in store_totals:
    for month in months:

        old_val = store_totals[old_name][month]
        amfc_val = store_totals["AMFC"][month]

        # if both have values, keep AMFC only
        if old_val != 0 and amfc_val != 0:
            pass

        # if only old name has value, move it
        elif old_val != 0 and amfc_val == 0:
            store_totals["AMFC"][month] = old_val

    del store_totals[old_name]

if old_name in all_stores:
    all_stores.remove(old_name)

all_stores.add("AMFC")

# =====================================================
# WRITE CSV
# =====================================================
header = ["Store"] + months

with open(OUTPUT_CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for store in sorted(all_stores):
        row = [store]

        for month in months:
            value = round(store_totals[store][month], 2)
            row.append(value)

        writer.writerow(row)

print("CSV created successfully:")
print(OUTPUT_CSV_FILE)