# Supply Chain Demand & Inventory Planner

## 1. Project Overview

The Supply Chain Demand & Inventory Planner is a Python-based application designed to monitor inventory, forecast demand, identify potential shortages, prioritize shortage risks, and recommend mitigation actions.

It includes a Streamlit dashboard to help users understand inventory conditions and review shortage-related information.

## 2. Key Features

- Generate sample supply chain datasets.
- Project weekly inventory using forecast demand and incoming purchase orders.
- Consider supplier lead times when estimating purchase order arrival weeks.
- Identify inventory shortages.
- Classify shortages into Low, Medium, High, and Critical severity levels.
- Generate suggested mitigation options.
- Validate important data quality rules.
- Display KPIs, charts, filters, and reports through a Streamlit dashboard.

## 3. Technology Stack

- Python
- Pandas
- Streamlit
- Plotly
- CSV

## 4. Project Structure

```text
supply_chain_planner/
│
├── data/
│   ├── skus.csv
│   ├── locations.csv
│   ├── suppliers.csv
│   ├── inventory.csv
│   ├── forecast_demand.csv
│   ├── supplier_capacity.csv
│   ├── lead_times.csv
│   ├── purchase_orders.csv
│   ├── inventory_projection.csv
│   ├── shortage_report.csv
│   └── mitigation_options.csv
│
├── src/
│   ├── generator.py
│   ├── inventory_engine.py
│   ├── shortage_engine.py
│   ├── mitigation_engine.py
│   ├── validation.py
│   └── dashboard.py
│
├── docs/
├── prompts/
├── exports/
├── README.md
└── .gitignore
```

## 5. Setup Instructions

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd supply_chain_planner
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install pandas streamlit plotly
```

## 6. How to Run the Project

Run the following commands in order from the project root directory.

### Step 1: Generate sample data

```bash
python src/generator.py
```

### Step 2: Validate the generated data

```bash
python src/validation.py
```

### Step 3: Run inventory projection

```bash
python src/inventory_engine.py
```

### Step 4: Prioritize shortages

```bash
python src/shortage_engine.py
```

### Step 5: Generate mitigation options

```bash
python src/mitigation_engine.py
```

### Step 6: Launch the dashboard

```bash
streamlit run src/dashboard.py
```

## 7. Current Starter Dataset

The current prototype uses:

- 100 SKUs
- 5 locations
- 20 suppliers
- 12 planning weeks
- 6,000 forecast records
- 500 inventory records

The data generator uses a fixed random seed (`20261022`) to support repeatable dataset generation.

## 8. Business Logic

### Inventory Projection

Projected inventory is calculated using:

Opening Inventory + Incoming Quantity - Forecast Demand

Shortages are identified when projected available inventory is insufficient to meet forecast demand.

### Lead Time

Purchase order arrival weeks are estimated using supplier lead times. Lead times are rounded up to whole weeks.

### Shortage Prioritization

Shortages are classified according to the shortage quantity as a percentage of forecast demand:

- Low: below 25%
- Medium: 25% to below 50%
- High: 50% to below 100%
- Critical: 100% or more

### Mitigation Options

The prototype generates suggested additional supplier orders and demand reallocation options for identified shortages.

## 9. Current Limitations

- The current dataset is a starter dataset and does not yet cover the complete target scale.
- Inventory projection uses weekly planning buckets.
- Shortage quantities are not carried forward as backorders into later weeks.
- Supplier capacity and SKU compatibility are not fully enforced when generating mitigation suggestions.
- Demand reallocation is currently a placeholder recommendation.
- Production planning, bill of materials, and substitute SKU approval are not yet implemented.
- Validation covers initial data quality checks but not every business rule in the challenge.

Mitigation options should therefore be treated as suggestions rather than confirmed feasible actions.

## 10. Future Improvements

- Expand the dataset to the full target scale.
- Add production planning and bill of materials.
- Enforce supplier capacity and minimum order quantities.
- Add approved substitute SKU relationships.
- Improve shortage and backorder calculations.
- Add SQL and JSON exports.
- Add more comprehensive validation and reproducibility checks.

## 11. AI Assistance

AI tools were used as development assistance for understanding requirements, planning the application, debugging, and improving documentation. The relevant prompt history is maintained separately in the `prompts/` directory.
