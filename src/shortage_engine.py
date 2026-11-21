
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. PROJECT PATH
# --------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_FOLDER / "data"


# --------------------------------------------------
# 2. LOAD INVENTORY PROJECTION
# --------------------------------------------------

def load_projection():
    file_path = DATA_FOLDER / "inventory_projection.csv"

    return pd.read_csv(file_path)


# --------------------------------------------------
# 3. IDENTIFY SHORTAGES
# --------------------------------------------------

def identify_shortages(projection):
    shortages = projection[
        projection["shortage_quantity"] > 0
    ].copy()

    return shortages


# --------------------------------------------------
# 4. CALCULATE SHORTAGE SEVERITY
# --------------------------------------------------

def calculate_severity(shortages):

    shortages["shortage_rate"] = (
        shortages["shortage_quantity"]
        / shortages["forecast_quantity"]
    )

    shortages["shortage_rate"] = (
        shortages["shortage_rate"].fillna(0)
    )

    shortages["severity"] = "Low"

    shortages.loc[
        shortages["shortage_rate"] >= 0.25,
        "severity"
    ] = "Medium"

    shortages.loc[
        shortages["shortage_rate"] >= 0.50,
        "severity"
    ] = "High"

    shortages.loc[
        shortages["shortage_rate"] >= 1.00,
        "severity"
    ] = "Critical"

    return shortages


# --------------------------------------------------
# 5. ASSIGN PRIORITY SCORES
# --------------------------------------------------

def assign_priority(shortages):

    priority_scores = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4
    }

    shortages["priority_score"] = (
        shortages["severity"].map(priority_scores)
    )

    shortages = shortages.sort_values(
        by=["priority_score", "shortage_quantity"],
        ascending=[False, False]
    )

    shortages["priority_rank"] = range(
        1, len(shortages) + 1
    )

    return shortages


# --------------------------------------------------
# 6. SAVE SHORTAGE REPORT
# --------------------------------------------------

def main():

    print("Starting shortage prioritization...")

    projection = load_projection()

    shortages = identify_shortages(projection)

    shortages = calculate_severity(shortages)

    shortages = assign_priority(shortages)

    output_file = DATA_FOLDER / "shortage_report.csv"

    shortages.to_csv(output_file, index=False)

    print("\nShortage analysis completed!")
    print(f"Total shortage records: {len(shortages)}")

    if not shortages.empty:

        print(
            "\nShortages by severity:"
        )

        print(
            shortages["severity"].value_counts()
        )

        print(
            "\nTotal shortage quantity:",
            shortages["shortage_quantity"].sum()
        )

        print("\nTop 10 prioritized shortages:")

        print(
            shortages[
                [
                    "sku_id",
                    "location_id",
                    "week",
                    "forecast_quantity",
                    "shortage_quantity",
                    "severity",
                    "priority_rank"
                ]
            ].head(10).to_string(index=False)
        )

    else:
        print("No shortages identified.")

    print(f"\nSaved report to: {output_file}")


if __name__ == "__main__":
    main()
