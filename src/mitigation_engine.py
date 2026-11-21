
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_FOLDER / "data"


# --------------------------------------------------
# 2. LOAD SHORTAGE AND SUPPLIER DATA
# --------------------------------------------------

def load_data():

    shortages = pd.read_csv(
        DATA_FOLDER / "shortage_report.csv"
    )

    suppliers = pd.read_csv(
        DATA_FOLDER / "suppliers.csv"
    )

    return shortages, suppliers


# --------------------------------------------------
# 3. GENERATE MITIGATION OPTIONS
# --------------------------------------------------

def generate_mitigations(shortages, suppliers):

    records = []

    for _, shortage in shortages.iterrows():

        shortage_quantity = int(
            shortage["shortage_quantity"]
        )

        sku = shortage["sku_id"]
        location = shortage["location_id"]
        week = shortage["week"]

        shortage_id = (
            f"SHORT-{sku}-{location}-{week}"
        )

        # Option 1: Increase supply
        for _, supplier in suppliers.iterrows():

            capacity = int(
                supplier["maximum_weekly_capacity"]
            )

            if capacity >= shortage_quantity:

                records.append({
                    "mitigation_id": (
                        f"MIT-{shortage_id}-"
                        f"{supplier['supplier_id']}"
                    ),
                    "shortage_id": shortage_id,
                    "sku_id": sku,
                    "location_id": location,
                    "week": week,
                    "mitigation_type": "Additional Supplier Order",
                    "supplier_id": supplier["supplier_id"],
                    "recommended_quantity": shortage_quantity,
                    "estimated_capacity": capacity,
                    "status": "Suggested"
                })

                # Avoid generating too many options
                break

        # Option 2: Reduce demand impact
        records.append({
            "mitigation_id": f"MIT-{shortage_id}-DEMAND",
            "shortage_id": shortage_id,
            "sku_id": sku,
            "location_id": location,
            "week": week,
            "mitigation_type": "Demand Reallocation",
            "supplier_id": None,
            "recommended_quantity": shortage_quantity,
            "estimated_capacity": None,
            "status": "Suggested"
        })

    return pd.DataFrame(records)


# --------------------------------------------------
# 4. SAVE MITIGATION REPORT
# --------------------------------------------------

def main():

    print("Generating mitigation options...")

    shortages, suppliers = load_data()

    mitigations = generate_mitigations(
        shortages,
        suppliers
    )

    output_file = DATA_FOLDER / "mitigation_options.csv"

    mitigations.to_csv(output_file, index=False)

    print("\nMitigation analysis completed!")

    print(
        f"Total mitigation options: {len(mitigations)}"
    )

    if not mitigations.empty:

        print("\nOptions by type:")

        print(
            mitigations["mitigation_type"].value_counts()
        )

        print("\nSample mitigation options:")

        print(
            mitigations.head(5).to_string(index=False)
        )

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
