
import pandas as pd
import sqlite3
import json
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FOLDER = BASE_DIR / "data"
EXPORT_FOLDER = BASE_DIR / "exports"
JSON_FOLDER = EXPORT_FOLDER / "json"

# Create export folders
JSON_FOLDER.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = EXPORT_FOLDER / "supply_chain.db"


def export_json():

    print("Starting JSON export...")

    csv_files = list(DATA_FOLDER.glob("*.csv"))

    for file_path in csv_files:

        df = pd.read_csv(file_path)

        json_path = JSON_FOLDER / f"{file_path.stem}.json"

        df.to_json(
            json_path,
            orient="records",
            indent=2
        )

        print(f"Exported: {json_path.name}")


def export_sqlite():

    print("\nStarting SQLite export...")

    csv_files = list(DATA_FOLDER.glob("*.csv"))
    export_summary = []

    with sqlite3.connect(DATABASE_PATH) as connection:

        for file_path in csv_files:

            df = pd.read_csv(file_path)

            table_name = file_path.stem

            df.to_sql(
                table_name,
                connection,
                if_exists="replace",
                index=False
            )

            export_summary.append({
                "table_name": table_name,
                "row_count": len(df)
            })

            print(
                f"Created table: {table_name} "
                f"({len(df)} records)"
            )

        summary_df = pd.DataFrame(export_summary)

        summary_df.to_sql(
            "export_summary",
            connection,
            if_exists="replace",
            index=False
        )

    print(f"\nSQLite database saved: {DATABASE_PATH}")


def main():

    print("SUPPLY CHAIN DATA EXPORT")
    print("-" * 35)

    export_json()
    export_sqlite()

    print("\nAll exports completed successfully!")


if __name__ == "__main__":
    main()
