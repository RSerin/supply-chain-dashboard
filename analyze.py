import pandas as pd

# ── Load ──────────────────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding="latin-1")
print(f"  {len(df):,} rows loaded\n")

# ── Parse dates ───────────────────────────────────────────────────────────────
df["order_date"] = pd.to_datetime(df["order date (DateOrders)"], format="%m/%d/%Y %H:%M")
df["year_month"]  = df["order_date"].dt.to_period("M").astype(str)

# ── Shipping delay (positive = late, negative = early) ────────────────────────
df["ship_delay"] = df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]

# ═════════════════════════════════════════════════════════════════════════════
# KPI SUMMARY
# ═════════════════════════════════════════════════════════════════════════════
total          = len(df)
on_time        = (df["Delivery Status"] == "Shipping on time").sum()
late           = (df["Delivery Status"] == "Late delivery").sum()
cancelled      = (df["Delivery Status"] == "Shipping canceled").sum()
otd_rate       = round(on_time / total * 100, 2)
late_rate      = round(late    / total * 100, 2)
avg_delay      = round(df["ship_delay"].mean(), 2)
total_revenue  = round(df["Sales"].sum(), 2)
avg_profit     = round(df["Benefit per order"].mean(), 2)
late_risk_rate = round(df["Late_delivery_risk"].mean() * 100, 2)

print("=" * 45)
print("  SUPPLY CHAIN KPI SUMMARY")
print("=" * 45)
print(f"  Total Orders          : {total:,}")
print(f"  On-Time Delivery Rate : {otd_rate}%")
print(f"  Late Delivery Rate    : {late_rate}%")
print(f"  Cancelled Orders      : {cancelled:,}")
print(f"  Avg Shipping Delay    : {avg_delay} days")
print(f"  Late Delivery Risk    : {late_risk_rate}%")
print(f"  Total Revenue         : ${total_revenue:,.2f}")
print(f"  Avg Profit Per Order  : ${avg_profit:,.2f}")
print("=" * 45)
print()

# ═════════════════════════════════════════════════════════════════════════════
# EXPORT 1 — Clean master file (used in Power BI)
# ═════════════════════════════════════════════════════════════════════════════
keep_cols = [
    "order_date", "year_month",
    "Category Name", "Department Name", "Market", "Order Region",
    "Customer Segment", "Shipping Mode", "Delivery Status",
    "Late_delivery_risk", "ship_delay",
    "Order Item Quantity", "Sales", "Benefit per order",
    "Order Item Profit Ratio", "Order Item Discount Rate",
    "Days for shipping (real)", "Days for shipment (scheduled)"
]
clean = df[keep_cols].copy()
clean.columns = [
    "order_date", "year_month",
    "category", "department", "market", "region",
    "customer_segment", "shipping_mode", "delivery_status",
    "late_risk", "ship_delay",
    "quantity", "sales", "profit_per_order",
    "profit_ratio", "discount_rate",
    "actual_ship_days", "scheduled_ship_days"
]
clean.to_csv("clean_supply_chain.csv", index=False)
print("✓ Exported: clean_supply_chain.csv")

# ═════════════════════════════════════════════════════════════════════════════
# EXPORT 2 — Category summary (Power BI + SAP Excel sheet)
# ═════════════════════════════════════════════════════════════════════════════
cat = df.groupby("Category Name").agg(
    Total_Orders    = ("Order Item Quantity", "count"),
    Total_Revenue   = ("Sales", "sum"),
    Total_Profit    = ("Benefit per order", "sum"),
    Avg_Ship_Delay  = ("ship_delay", "mean"),
    Late_Risk_Pct   = ("Late_delivery_risk", "mean"),
    On_Time_Count   = ("Delivery Status", lambda x: (x == "Shipping on time").sum()),
    Late_Count      = ("Delivery Status", lambda x: (x == "Late delivery").sum()),
).reset_index()
cat["On_Time_Rate_Pct"] = (cat["On_Time_Count"] / cat["Total_Orders"] * 100).round(2)
cat["Late_Risk_Pct"]    = (cat["Late_Risk_Pct"] * 100).round(2)
cat["Avg_Ship_Delay"]   = cat["Avg_Ship_Delay"].round(2)
cat["Total_Revenue"]    = cat["Total_Revenue"].round(2)
cat["Total_Profit"]     = cat["Total_Profit"].round(2)
cat.to_csv("category_summary.csv", index=False)
print("✓ Exported: category_summary.csv")

# ═════════════════════════════════════════════════════════════════════════════
# EXPORT 3 — Region summary (Power BI map + bar charts)
# ═════════════════════════════════════════════════════════════════════════════
reg = df.groupby(["Market", "Order Region"]).agg(
    Total_Orders   = ("Order Item Quantity", "count"),
    Total_Revenue  = ("Sales", "sum"),
    Avg_Ship_Delay = ("ship_delay", "mean"),
    Late_Risk_Pct  = ("Late_delivery_risk", "mean"),
    On_Time_Count  = ("Delivery Status", lambda x: (x == "Shipping on time").sum()),
).reset_index()
reg["On_Time_Rate_Pct"] = (reg["On_Time_Count"] / reg["Total_Orders"] * 100).round(2)
reg["Late_Risk_Pct"]    = (reg["Late_Risk_Pct"] * 100).round(2)
reg["Avg_Ship_Delay"]   = reg["Avg_Ship_Delay"].round(2)
reg["Total_Revenue"]    = reg["Total_Revenue"].round(2)
reg.to_csv("region_summary.csv", index=False)
print("✓ Exported: region_summary.csv")

# ═════════════════════════════════════════════════════════════════════════════
# EXPORT 4 — Monthly trend (Power BI line chart)
# ═════════════════════════════════════════════════════════════════════════════
monthly = df.groupby("year_month").agg(
    Total_Orders   = ("Order Item Quantity", "count"),
    Total_Revenue  = ("Sales", "sum"),
    Avg_Ship_Delay = ("ship_delay", "mean"),
    Late_Risk_Pct  = ("Late_delivery_risk", "mean"),
    On_Time_Count  = ("Delivery Status", lambda x: (x == "Shipping on time").sum()),
).reset_index()
monthly["On_Time_Rate_Pct"] = (monthly["On_Time_Count"] / monthly["Total_Orders"] * 100).round(2)
monthly["Late_Risk_Pct"]    = (monthly["Late_Risk_Pct"] * 100).round(2)
monthly["Avg_Ship_Delay"]   = monthly["Avg_Ship_Delay"].round(2)
monthly["Total_Revenue"]    = monthly["Total_Revenue"].round(2)
monthly.to_csv("monthly_trend.csv", index=False)
print("✓ Exported: monthly_trend.csv")

# ═════════════════════════════════════════════════════════════════════════════
# EXPORT 5 — Shipping mode performance (Power BI clustered bar)
# ═════════════════════════════════════════════════════════════════════════════
ship = df.groupby("Shipping Mode").agg(
    Total_Orders   = ("Order Item Quantity", "count"),
    Avg_Ship_Delay = ("ship_delay", "mean"),
    Late_Risk_Pct  = ("Late_delivery_risk", "mean"),
    On_Time_Count  = ("Delivery Status", lambda x: (x == "Shipping on time").sum()),
).reset_index()
ship["On_Time_Rate_Pct"] = (ship["On_Time_Count"] / ship["Total_Orders"] * 100).round(2)
ship["Late_Risk_Pct"]    = (ship["Late_Risk_Pct"] * 100).round(2)
ship["Avg_Ship_Delay"]   = ship["Avg_Ship_Delay"].round(2)
ship.to_csv("shipping_mode_summary.csv", index=False)
print("✓ Exported: shipping_mode_summary.csv")

print()
print("All done! Open these 5 CSV files in Power BI and SAP Excel report.")
