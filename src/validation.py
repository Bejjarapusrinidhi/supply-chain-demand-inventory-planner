
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. PROJECT PATH
# --------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_FOLDER / "data"


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

def load_data():

    files = [
        "skus",
        "locations",
        "suppliers",
        "inventory",
        "forecast_demand",
        "supplier_capacity",
        "lead_times",
        "purchase_orders"
    ]

    data = {}

    for file in files:
        data[file] = pd.read_csv(
            DATA_FOLDER / f"{file}.csv"
        )

    return data


# --------------------------------------------------
# 3. CHECK DUPLICATE RECORDS
# --------------------------------------------------

def check_duplicates(data):

    print("\nChecking duplicate records...")

    primary_keys = {
        "skus": ["sku_id"],
        "locations": ["location_id"],
        "suppliers": ["supplier_id"],
        "forecast_demand": ["demand_id"],
        "purchase_orders": ["purchase_order_id"]
    }

    for table, columns in primary_keys.items():

        duplicates = data[table].duplicated(
            subset=columns
        ).sum()

        print(f"{table}: {duplicates} duplicates")

    composite_keys = {
        "inventory": ["sku_id", "location_id"],
        "supplier_capacity": ["supplier_id", "week"],
        "lead_times": ["supplier_id", "location_id"]
    }

    for table, columns in composite_keys.items():

        duplicates = data[table].duplicated(
            subset=columns
        ).sum()

        print(f"{table}: {duplicates} duplicate combinations")


# --------------------------------------------------
# 4. CHECK MISSING VALUES
# --------------------------------------------------

def check_missing_values(data):

    print("\nChecking missing values...")

    for table, dataframe in data.items():

        missing = dataframe.isnull().sum().sum()

        print(f"{table}: {missing} missing values")


# --------------------------------------------------
# 5. CHECK FOREIGN KEYS
# --------------------------------------------------

def check_foreign_keys(data):

    print("\nChecking foreign key relationships...")

    sku_ids = set(data["skus"]["sku_id"])
    location_ids = set(data["locations"]["location_id"])
    supplier_ids = set(data["suppliers"]["supplier_id"])

    checks = {
        "inventory SKU": (
            data["inventory"]["sku_id"], sku_ids
        ),
        "inventory location": (
            data["inventory"]["location_id"], location_ids
        ),
        "forecast SKU": (
            data["forecast_demand"]["sku_id"], sku_ids
        ),
        "forecast location": (
            data["forecast_demand"]["location_id"], location_ids
        ),
        "purchase order SKU": (
            data["purchase_orders"]["sku_id"], sku_ids
        ),
        "purchase order location": (
            data["purchase_orders"]["location_id"], location_ids
        ),
        "purchase order supplier": (
            data["purchase_orders"]["supplier_id"], supplier_ids
        ),
        "capacity supplier": (
            data["supplier_capacity"]["supplier_id"], supplier_ids
        ),
        "lead time supplier": (
            data["lead_times"]["supplier_id"], supplier_ids
        ),
        "lead time location": (
            data["lead_times"]["location_id"], location_ids
        )
    }

    for name, (column, valid_ids) in checks.items():

        invalid = (~column.isin(valid_ids)).sum()

        print(f"{name}: {invalid} invalid references")


# --------------------------------------------------
# 6. CHECK QUANTITIES AND STATUSES
# --------------------------------------------------

def check_business_rules(data):

    print("\nChecking business rules...")

    quantity_columns = {
        "inventory": ["on_hand_quantity"],
        "forecast_demand": ["forecast_quantity"],
        "supplier_capacity": ["available_capacity"],
        "lead_times": ["lead_time_days"],
        "purchase_orders": ["order_quantity"]
    }

    for table, columns in quantity_columns.items():

        for column in columns:

            invalid = (
                (data[table][column] < 0)
                | data[table][column].isna()
            ).sum()

            print(
                f"{table}.{column}: "
                f"{invalid} invalid values"
            )

    valid_statuses = {
        "Open",
        "In Transit",
        "Received"
    }

    invalid_statuses = (
        ~data["purchase_orders"]["status"].isin(valid_statuses)
    ).sum()

    print(
        f"Invalid purchase order statuses: {invalid_statuses}"
    )


# --------------------------------------------------
# 7. RUN ALL VALIDATIONS
# --------------------------------------------------

def main():

    print("SUPPLY CHAIN DATA VALIDATION")

    data = load_data()

    check_duplicates(data)

    check_missing_values(data)

    check_foreign_keys(data)

    check_business_rules(data)

    print("\nValidation checks completed!")


if __name__ == "__main__":
    main()
