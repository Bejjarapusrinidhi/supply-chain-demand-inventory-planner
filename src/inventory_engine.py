
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. LOAD PROJECT DATA
# --------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_FOLDER / "data"



def load_data():

    inventory = pd.read_csv(DATA_FOLDER / "inventory.csv")
    forecast = pd.read_csv(DATA_FOLDER / "forecast_demand.csv")
    purchase_orders = pd.read_csv(DATA_FOLDER / "purchase_orders.csv")
    lead_times = pd.read_csv(DATA_FOLDER / "lead_times.csv")

    return inventory, forecast, purchase_orders, lead_times



# --------------------------------------------------
# 2. CALCULATE INCOMING STOCK
# --------------------------------------------------


def calculate_incoming(purchase_orders, lead_times):

    # Orders already received are excluded.
    # We assume their quantities are reflected in opening inventory.
    incoming_orders = purchase_orders[
        purchase_orders["status"].isin(["Open", "In Transit"])
    ].copy()

    # Attach the supplier's lead time for the destination
    incoming_orders = incoming_orders.merge(
        lead_times,
        on=["supplier_id", "location_id"],
        how="left"
    )

    if incoming_orders["lead_time_days"].isna().any():
        raise ValueError("Some purchase orders have no matching lead time.")

    # Extract the week number from values such as 2026W01
    order_week_number = (
        incoming_orders["order_week"]
        .str.extract(r"W(\d+)")[0]
        .astype(int)
    )

    # Estimate arrival week using lead time
    weeks_to_arrival = (
        (incoming_orders["lead_time_days"] + 6) // 7
    )

    incoming_orders["arrival_week_number"] = (
        order_week_number + weeks_to_arrival
    )

    # Keep arrivals within our 12-week planning horizon
    incoming_orders = incoming_orders[
        incoming_orders["arrival_week_number"] <= 12
    ].copy()

    incoming_orders["arrival_week"] = (
        "2026W"
        + incoming_orders["arrival_week_number"].astype(str).str.zfill(2)
    )

    incoming = incoming_orders.groupby(
        ["sku_id", "location_id", "arrival_week"]
    )["order_quantity"].sum().reset_index()

    incoming = incoming.rename(columns={
        "arrival_week": "week",
        "order_quantity": "incoming_quantity"
    })

    return incoming

# --------------------------------------------------
# 3. CALCULATE INVENTORY PROJECTION
# --------------------------------------------------

def calculate_inventory_projection(
    inventory,
    forecast,
    incoming
):
    projection = forecast.merge(
        inventory,
        on=["sku_id", "location_id"],
        how="left"
    )

    projection = projection.merge(
        incoming,
        on=["sku_id", "location_id", "week"],
        how="left"
    )

    projection["incoming_quantity"] = (
        projection["incoming_quantity"].fillna(0)
    )

    projection = projection.sort_values(
        ["sku_id", "location_id", "week"]
    )

    projection["opening_inventory"] = 0
    projection["projected_balance"] = 0
    projection["shortage_quantity"] = 0

    # Calculate balance separately for each SKU and location
    for (sku, location), group in projection.groupby(
        ["sku_id", "location_id"]
    ):
        balance = group["on_hand_quantity"].iloc[0]

        for index in group.index:
            opening = balance
            incoming_quantity = projection.loc[
                index, "incoming_quantity"
            ]
            demand = projection.loc[
                index, "forecast_quantity"
            ]

            balance = (
                opening
                + incoming_quantity
                - demand
            )

            projection.loc[index, "opening_inventory"] = opening

            projection.loc[index, "projected_balance"] = max(
                balance, 0
            )

            projection.loc[index, "shortage_quantity"] = max(
                -balance, 0
            )

            # Carry balance forward to next week
            balance = max(balance, 0)

    return projection


# --------------------------------------------------
# 4. RUN THE INVENTORY ENGINE
# --------------------------------------------------

def main():
    print("Loading supply chain data...")

    inventory, forecast, purchase_orders, lead_times = load_data()

    incoming = calculate_incoming(purchase_orders, lead_times)

    projection = calculate_inventory_projection(
        inventory,
        forecast,
        incoming
    )

    output_file = DATA_FOLDER / "inventory_projection.csv"

    projection.to_csv(output_file, index=False)

    shortages = projection[
        projection["shortage_quantity"] > 0
    ]

    print("\nInventory projection completed!")
    print(f"Total records: {len(projection)}")
    print(f"Shortage records: {len(shortages)}")
    print(
        f"Total shortage quantity: "
        f"{shortages['shortage_quantity'].sum()}"
    )

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
