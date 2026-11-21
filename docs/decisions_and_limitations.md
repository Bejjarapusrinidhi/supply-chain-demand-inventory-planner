# Business Decisions and Limitations

## 1. Project Approach

The Supply Chain Demand & Inventory Planner was developed as a modular Python application.

The project separates data generation, inventory projection, shortage prioritization, mitigation recommendations, validation, and dashboard visualization into individual modules.

This makes the application easier to understand, test, and improve.

## 2. Business Decisions

### 2.1 Inventory Projection

The inventory projection uses the following calculation:

Projected Balance = Opening Inventory + Incoming Quantity - Forecast Demand

If the projected balance is negative, the shortage quantity represents the unmet demand.

The current implementation prevents negative inventory from being carried forward as a negative balance.

### 2.2 Supplier Lead Time

Supplier lead time is stored in days.

For weekly planning, lead time is rounded up to the nearest whole week:

Weeks to Arrival = Ceiling(Lead Time in Days / 7)

Estimated Arrival Week = Order Week + Weeks to Arrival

Orders arriving outside the 12-week planning horizon are excluded from the projection.

This is a weekly approximation rather than an exact calendar-date calculation.

### 2.3 Shortage Prioritization

Shortage rate is calculated as:

Shortage Rate = Shortage Quantity / Forecast Quantity

Severity is assigned using these rules:

| Shortage Rate | Severity |
|---|---|
| Below 25% | Low |
| 25% to below 50% | Medium |
| 50% to below 100% | High |
| 100% or more | Critical |

A numeric priority score is assigned based on severity, and shortages are ranked for review.

These thresholds are prototype business rules and can be adjusted based on business requirements.

### 2.4 Mitigation Recommendations

The system currently generates two suggestion types:

- Additional Supplier Order
- Demand Reallocation

These recommendations help demonstrate possible responses to shortages.

They are suggestions only and should not be treated as confirmed procurement or allocation decisions.

## 3. Data Generation Decisions

- The starter dataset is generated using Python and Pandas.
- A fixed random seed of 20261022 is used for repeatability.
- The current dataset contains 100 SKUs, 5 locations, 20 suppliers, and 12 planning weeks.
- Generated CSV files are used as the application's input and output data.

## 4. Validation Decisions

The validation module performs initial checks for:

- Duplicate identifiers and composite keys.
- Missing values.
- Invalid foreign key references.
- Negative or missing quantities.
- Invalid purchase order statuses.

The current validation module does not yet cover every business constraint or lifecycle rule.

## 5. Current Limitations

1. The current starter dataset is smaller than the full target scale of 3,000 SKUs, 50 locations, and 500 suppliers.
2. Production planning and bill of materials are not implemented.
3. Substitute SKU approval and substitution logic are not implemented.
4. Supplier capacity and minimum order quantities are not fully enforced in mitigation recommendations.
5. Supplier-SKU compatibility is not checked when suggesting additional supplier orders.
6. Demand reallocation is currently a placeholder suggestion.
7. Shortage quantities are not carried forward as backorders into later weeks.
8. The current implementation uses CSV files rather than a fully constrained relational database.
9. Received purchase orders are excluded from incoming quantities under the assumption that they are reflected in opening inventory. The generated data does not fully reconcile these quantities.
10. Lead time is approximated using weekly buckets.

## 6. Future Improvements

- Expand the generator to the complete challenge dataset scale.
- Introduce a relational database with primary and foreign key constraints.
- Implement production capacity and bill of materials planning.
- Add approved substitute SKU relationships.
- Enforce supplier capacity, minimum order quantities, and SKU compatibility.
- Improve backorder and inventory balance calculations.
- Add exact date-based delivery planning.
- Improve data validation and automated testing.
- Add SQL and JSON data exports.

## 7. Conclusion

The current project demonstrates an end-to-end prototype for demand and inventory planning, shortage identification, prioritization, and mitigation suggestions.

The modular design provides a foundation for extending the system with more advanced supply chain planning capabilities.
