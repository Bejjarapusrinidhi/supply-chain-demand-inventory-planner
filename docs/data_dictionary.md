# Data Dictionary – Supply Chain Demand & Inventory Planner

## 1. Overview

This document describes the datasets used in the Supply Chain Demand & Inventory Planner, including their columns, purposes, and relationships.

The project uses CSV files to store supply chain master data, planning data, and calculated outputs.

## 2. Master Data Tables

### 2.1 skus.csv

Stores product or Stock Keeping Unit (SKU) information.

| Column | Description |
|---|---|
| sku_id | Unique identifier for each SKU |
| sku_name | Name of the product |
| category | Product category |
| unit_of_measure | Measurement unit used for the product |

Primary Key: `sku_id`

### 2.2 locations.csv

Stores information about supply chain locations.

| Column | Description |
|---|---|
| location_id | Unique location identifier |
| location_name | Name of the location |
| location_type | Type of location |

Primary Key: `location_id`

### 2.3 suppliers.csv

Stores supplier information and ordering constraints.

| Column | Description |
|---|---|
| supplier_id | Unique supplier identifier |
| supplier_name | Supplier name |
| minimum_order_quantity | Minimum quantity required per order |
| maximum_weekly_capacity | Maximum weekly supply capacity |

Primary Key: `supplier_id`

## 3. Planning and Transaction Tables

### 3.1 inventory.csv

Stores the opening inventory available for each SKU at each location.

| Column | Description |
|---|---|
| sku_id | SKU identifier |
| location_id | Location identifier |
| on_hand_quantity | Available opening inventory quantity |

Composite Primary Key: `sku_id`, `location_id`

### 3.2 forecast_demand.csv

Stores weekly forecast demand for each SKU and location.

| Column | Description |
|---|---|
| demand_id | Unique demand record identifier |
| sku_id | SKU identifier |
| location_id | Location identifier |
| week | Planning week |
| forecast_quantity | Expected demand quantity |

Primary Key: `demand_id`

### 3.3 supplier_capacity.csv

Stores the available supplier capacity for each week.

| Column | Description |
|---|---|
| supplier_id | Supplier identifier |
| week | Planning week |
| available_capacity | Available supply capacity |

Composite Primary Key: `supplier_id`, `week`

### 3.4 lead_times.csv

Stores estimated delivery lead times for supplier-location combinations.

| Column | Description |
|---|---|
| supplier_id | Supplier identifier |
| location_id | Destination location identifier |
| lead_time_days | Estimated delivery time in days |

Composite Primary Key: `supplier_id`, `location_id`

### 3.5 purchase_orders.csv

Stores purchase order information.

| Column | Description |
|---|---|
| purchase_order_id | Unique purchase order identifier |
| sku_id | SKU identifier |
| location_id | Destination location |
| supplier_id | Supplier identifier |
| order_week | Week in which the order is placed |
| order_quantity | Quantity ordered |
| status | Purchase order status |

Primary Key: `purchase_order_id`

## 4. Calculated Output Tables

### 4.1 inventory_projection.csv

Stores the calculated weekly inventory position.

| Column | Description |
|---|---|
| demand_id | Related demand record |
| sku_id | SKU identifier |
| location_id | Location identifier |
| week | Planning week |
| forecast_quantity | Forecast demand |
| on_hand_quantity | Opening inventory reference |
| incoming_quantity | Expected incoming purchase order quantity |
| opening_inventory | Inventory available at the beginning of the week |
| projected_balance | Calculated inventory after demand |
| shortage_quantity | Quantity of unmet demand |

### 4.2 shortage_report.csv

Stores identified shortages and their priority information.

| Column | Description |
|---|---|
| demand_id | Related demand record |
| sku_id | SKU identifier |
| location_id | Location identifier |
| week | Planning week |
| forecast_quantity | Expected demand |
| on_hand_quantity | Opening inventory reference |
| incoming_quantity | Expected incoming quantity |
| opening_inventory | Inventory at the beginning of the week |
| projected_balance | Projected inventory balance |
| shortage_quantity | Unmet demand quantity |
| shortage_rate | Shortage as a proportion of forecast demand |
| severity | Shortage severity classification |
| priority_score | Numeric priority score |
| priority_rank | Relative priority ranking |

### 4.3 mitigation_options.csv

Stores suggested actions for identified shortages.

| Column | Description |
|---|---|
| mitigation_id | Unique mitigation identifier |
| shortage_id | Related shortage identifier |
| sku_id | SKU identifier |
| location_id | Location identifier |
| week | Week of the shortage |
| mitigation_type | Type of suggested action |
| supplier_id | Suggested supplier, if applicable |
| recommended_quantity | Suggested quantity |
| estimated_capacity | Supplier capacity reference, if available |
| status | Status of the recommendation |

## 5. Entity Relationships

The main relationships are:

- One SKU can have multiple forecast demand records.
- One SKU can have inventory records at multiple locations.
- One location can have multiple inventory and forecast records.
- One supplier can have multiple purchase orders.
- One supplier can have capacity records for multiple weeks.
- Supplier lead time is recorded for each supplier-location combination.
- Each forecast demand record can produce an inventory projection record.
- Inventory projection records with shortages can produce shortage report records.
- Each shortage can have multiple mitigation suggestions.

## 6. Important Notes

- Identifiers are used to connect related datasets.
- Inventory projection, shortage reports, and mitigation options are derived outputs.
- The current implementation uses CSV files rather than a relational database.
- Composite keys describe the intended uniqueness of records.
- Full database constraints and all relationship rules are not yet enforced.
