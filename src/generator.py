
import random
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. PROJECT SETTINGS
# --------------------------------------------------

SEED = 20261022
NUMBER_OF_SKUS = 100
NUMBER_OF_LOCATIONS = 5
NUMBER_OF_SUPPLIERS = 20
NUMBER_OF_WEEKS = 12
NUMBER_OF_PURCHASE_ORDERS = 200

rng = random.Random(SEED)

# Save generated CSV files in the project's data folder
PROJECT_FOLDER = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_FOLDER / "data"


# --------------------------------------------------
# 2. GENERATE SKUS (PRODUCTS)
# --------------------------------------------------

def generate_skus():
    records = []

    for i in range(1, NUMBER_OF_SKUS + 1):
        records.append({
            "sku_id": f"SKU-{i:06d}",
            "sku_name": f"Product {i}",
            "category": rng.choice(["Electronics", "Furniture", "Clothing"]),
            "unit_of_measure": "Each"
        })

    return pd.DataFrame(records)


# --------------------------------------------------
# 3. GENERATE LOCATIONS (WAREHOUSES)
# --------------------------------------------------

def generate_locations():
    records = []

    for i in range(1, NUMBER_OF_LOCATIONS + 1):
        records.append({
            "location_id": f"LOC-{i:03d}",
            "location_name": f"Warehouse {i}",
            "location_type": "Warehouse"
        })

    return pd.DataFrame(records)


# --------------------------------------------------
# 4. GENERATE SUPPLIERS
# --------------------------------------------------

def generate_suppliers():
    records = []

    for i in range(1, NUMBER_OF_SUPPLIERS + 1):
        records.append({
            "supplier_id": f"SUP-{i:03d}",
            "supplier_name": f"Supplier {i}",
            "minimum_order_quantity": rng.choice([10, 20, 50]),
            "maximum_weekly_capacity": rng.choice([500, 750, 1000])
        })

    return pd.DataFrame(records)


# --------------------------------------------------
# 5. GENERATE INVENTORY
# --------------------------------------------------

def generate_inventory(skus, locations):
    records = []

    for sku in skus["sku_id"]:
        for location in locations["location_id"]:
            records.append({
                "sku_id": sku,
                "location_id": location,
                "on_hand_quantity": rng.randint(50, 500)
            })

    return pd.DataFrame(records)


# --------------------------------------------------
# 6. GENERATE WEEKLY FORECAST DEMAND
# --------------------------------------------------

def generate_forecast(skus, locations):
    records = []

    for sku in skus["sku_id"]:
        for location in locations["location_id"]:
            for week in range(1, NUMBER_OF_WEEKS + 1):

                demand = rng.randint(20, 150)

                # Add occasional demand spikes
                if rng.random() < 0.05:
                    demand = demand * 2

                records.append({
                    "demand_id": f"DEM-{sku}-{location}-2026W{week:02d}",
                    "sku_id": sku,
                    "location_id": location,
                    "week": f"2026W{week:02d}",
                    "forecast_quantity": demand
                })

    return pd.DataFrame(records)


# --------------------------------------------------
# 7. GENERATE SUPPLIER WEEKLY CAPACITY
# --------------------------------------------------

def generate_supplier_capacity(suppliers):
    records = []

    for _, supplier in suppliers.iterrows():
        for week in range(1, NUMBER_OF_WEEKS + 1):
            records.append({
                "supplier_id": supplier["supplier_id"],
                "week": f"2026W{week:02d}",
                "available_capacity": supplier["maximum_weekly_capacity"]
            })

    return pd.DataFrame(records)


# --------------------------------------------------
# 8. GENERATE SUPPLIER LEAD TIMES
# --------------------------------------------------

def generate_lead_times(suppliers, locations):
    records = []

    for supplier in suppliers["supplier_id"]:
        for location in locations["location_id"]:
            records.append({
                "supplier_id": supplier,
                "location_id": location,
                "lead_time_days": rng.randint(3, 21)
            })

    return pd.DataFrame(records)


# --------------------------------------------------
# 9. GENERATE PURCHASE ORDERS
# --------------------------------------------------

def generate_purchase_orders(skus, locations, suppliers):
    records = []

    for i in range(1, NUMBER_OF_PURCHASE_ORDERS + 1):

        sku = rng.choice(skus["sku_id"].tolist())
        location = rng.choice(locations["location_id"].tolist())
        supplier = rng.choice(suppliers["supplier_id"].tolist())

        order_week = rng.randint(1, NUMBER_OF_WEEKS)
        quantity = rng.randint(20, 200)

        records.append({
            "purchase_order_id": f"PO-2026-{i:06d}",
            "sku_id": sku,
            "location_id": location,
            "supplier_id": supplier,
            "order_week": f"2026W{order_week:02d}",
            "order_quantity": quantity,
            "status": rng.choice(["Open", "In Transit", "Received"])
        })

    return pd.DataFrame(records)


# --------------------------------------------------
# 10. SAVE DATA AS CSV FILES
# --------------------------------------------------

def save_data(dataframes):
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    for file_name, dataframe in dataframes.items():
        file_path = DATA_FOLDER / f"{file_name}.csv"
        dataframe.to_csv(file_path, index=False)

        print(f"Created: {file_name}.csv ({len(dataframe)} rows)")


# --------------------------------------------------
# 11. MAIN FUNCTION
# --------------------------------------------------

def main():
    print("Starting supply chain data generation...")

    skus = generate_skus()
    locations = generate_locations()
    suppliers = generate_suppliers()

    dataframes = {
        "skus": skus,
        "locations": locations,
        "suppliers": suppliers,
        "inventory": generate_inventory(skus, locations),
        "forecast_demand": generate_forecast(skus, locations),
        "supplier_capacity": generate_supplier_capacity(suppliers),
        "lead_times": generate_lead_times(suppliers, locations),
        "purchase_orders": generate_purchase_orders(
            skus, locations, suppliers
        )
    }

    save_data(dataframes)

    print("\nData generation completed successfully!")


if __name__ == "__main__":
    main()
