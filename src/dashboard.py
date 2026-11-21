
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Supply Chain Planner",
    page_icon="📦",
    layout="wide"
)

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_FOLDER / "data"


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    inventory = pd.read_csv(
        DATA_FOLDER / "inventory.csv"
    )

    forecast = pd.read_csv(
        DATA_FOLDER / "forecast_demand.csv"
    )

    projection = pd.read_csv(
        DATA_FOLDER / "inventory_projection.csv"
    )

    shortages = pd.read_csv(
        DATA_FOLDER / "shortage_report.csv"
    )

    mitigations = pd.read_csv(
        DATA_FOLDER / "mitigation_options.csv"
    )

    return inventory, forecast, projection, shortages, mitigations


inventory, forecast, projection, shortages, mitigations = load_data()


# --------------------------------------------------
# 3. DASHBOARD TITLE
# --------------------------------------------------

st.title("📦 Supply Chain Demand & Inventory Planner")

st.markdown(
    "Monitor inventory, forecast demand, identify shortages, "
    "and review recommended mitigation actions."
)


# --------------------------------------------------
# 4. SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

locations = sorted(projection["location_id"].unique())

selected_location = st.sidebar.selectbox(
    "Select Warehouse",
    ["All Locations"] + locations
)

weeks = sorted(projection["week"].unique())

selected_week = st.sidebar.selectbox(
    "Select Week",
    ["All Weeks"] + weeks
)


# --------------------------------------------------
# 5. APPLY FILTERS
# --------------------------------------------------

filtered_projection = projection.copy()
filtered_shortages = shortages.copy()
filtered_mitigations = mitigations.copy()

if selected_location != "All Locations":

    filtered_projection = filtered_projection[
        filtered_projection["location_id"] == selected_location
    ]

    filtered_shortages = filtered_shortages[
        filtered_shortages["location_id"] == selected_location
    ]

    filtered_mitigations = filtered_mitigations[
        filtered_mitigations["location_id"] == selected_location
    ]


if selected_week != "All Weeks":

    filtered_projection = filtered_projection[
        filtered_projection["week"] == selected_week
    ]

    filtered_shortages = filtered_shortages[
        filtered_shortages["week"] == selected_week
    ]

    filtered_mitigations = filtered_mitigations[
        filtered_mitigations["week"] == selected_week
    ]


# --------------------------------------------------
# 6. KPI METRICS
# --------------------------------------------------

total_skus = filtered_projection["sku_id"].nunique()

inventory_for_kpi = inventory.copy()

if selected_location != "All Locations":
    inventory_for_kpi = inventory_for_kpi[
        inventory_for_kpi["location_id"] == selected_location
    ]

total_inventory = inventory_for_kpi["on_hand_quantity"].sum()

total_demand = filtered_projection[
    "forecast_quantity"
].sum()

total_shortage = filtered_shortages[
    "shortage_quantity"
].sum()

shortage_count = len(filtered_shortages)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total SKUs",
    f"{total_skus:,}"
)

col2.metric(
    "Inventory",
    f"{total_inventory:,.0f} units"
)

col3.metric(
    "Forecast Demand",
    f"{total_demand:,.0f} units"
)

col4.metric(
    "Shortage Quantity",
    f"{total_shortage:,.0f} units"
)


st.divider()


# --------------------------------------------------
# 7. SHORTAGE SEVERITY CHART
# --------------------------------------------------

st.subheader("Shortage Analysis")

if not filtered_shortages.empty:

    severity_counts = (
        filtered_shortages["severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = [
        "Severity",
        "Count"
    ]

    fig_severity = px.bar(
        severity_counts,
        x="Severity",
        y="Count",
        color="Severity",
        title="Shortages by Severity"
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True
    )

else:

    st.success("No shortages found for the selected filters.")


# --------------------------------------------------
# 8. DEMAND VS INVENTORY CHART
# --------------------------------------------------

st.subheader("Weekly Demand vs Inventory")

weekly_data = (
    filtered_projection
    .groupby("week", as_index=False)
    .agg({
        "forecast_quantity": "sum",
        "projected_balance": "sum"
    })
)

if not weekly_data.empty:

    fig_weekly = px.line(
        weekly_data,
        x="week",
        y=[
            "forecast_quantity",
            "projected_balance"
        ],
        markers=True,
        title="Weekly Forecast Demand vs Projected Inventory"
    )

    st.plotly_chart(
        fig_weekly,
        use_container_width=True
    )


# --------------------------------------------------
# 9. TOP PRIORITY SHORTAGES
# --------------------------------------------------

st.subheader("Top Priority Shortages")

if not filtered_shortages.empty:

    top_shortages = filtered_shortages.sort_values(
        "priority_rank"
    ).head(10)

    st.dataframe(
        top_shortages[
            [
                "sku_id",
                "location_id",
                "week",
                "forecast_quantity",
                "shortage_quantity",
                "severity",
                "priority_rank"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No shortage records available.")


# --------------------------------------------------
# 10. MITIGATION RECOMMENDATIONS
# --------------------------------------------------

st.subheader("Recommended Mitigation Actions")

if not filtered_mitigations.empty:

    st.dataframe(
        filtered_mitigations[
            [
                "sku_id",
                "location_id",
                "week",
                "mitigation_type",
                "supplier_id",
                "recommended_quantity",
                "status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No mitigation recommendations available.")


# --------------------------------------------------
# 11. DOWNLOAD REPORTS
# --------------------------------------------------

st.subheader("Download Reports")

col1, col2 = st.columns(2)

with col1:

    st.download_button(
        label="Download Shortage Report",
        data=filtered_shortages.to_csv(index=False),
        file_name="shortage_report.csv",
        mime="text/csv"
    )

with col2:

    st.download_button(
        label="Download Inventory Projection",
        data=filtered_projection.to_csv(index=False),
        file_name="inventory_projection.csv",
        mime="text/csv"
    )


st.caption(
    "Supply Chain Planner | Prototype | "
    "Generated from seeded sample data"
)
