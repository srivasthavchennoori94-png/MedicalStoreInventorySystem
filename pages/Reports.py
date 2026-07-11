import streamlit as st
import datetime
import pandas as pd
from utils.file_handler import load_medicines, load_sales

st.title("📈 Reports Generator")
st.markdown("Compile, preview, and download custom Excel-compatible CSV reports for compliance and auditing.")

# Load datasets
df_meds = load_medicines()
df_sales = load_sales()

# Report Selector
report_options = [
    "Current Inventory Status",
    "Low Stock Alert Report (<20)",
    "Expired Medicines Audit",
    "Monthly Sales & Revenue Report",
    "Category-wise Stock Distribution"
]

report_choice = st.selectbox("Select Report to Generate", options=report_options)

st.markdown("---")

today = datetime.date(2026, 7, 10)
report_df = pd.DataFrame()
report_title = ""
report_desc = ""

# 1. Current Inventory Status
if report_choice == "Current Inventory Status":
    report_title = "Current_Inventory_Report"
    report_desc = "Complete list of medicines currently registered in the database, including batch and supplier details."
    report_df = df_meds.copy()

# 2. Low Stock Alert Report
elif report_choice == "Low Stock Alert Report (<20)":
    report_title = "Low_Stock_Report"
    report_desc = "Products whose current quantities have fallen below the critical threshold of 20 units."
    if not df_meds.empty:
        report_df = df_meds[df_meds["Quantity"] < 20].copy()

# 3. Expired Medicines Audit
elif report_choice == "Expired Medicines Audit":
    report_title = "Expired_Medicines_Report"
    report_desc = "Medicines in stock whose expiration dates are in the past. Action required: Disposal."
    if not df_meds.empty:
        df_meds["_Expiry_Obj"] = pd.to_datetime(df_meds["Expiry Date"]).dt.date
        report_df = df_meds[df_meds["_Expiry_Obj"] < today].copy()
        report_df = report_df.drop(columns=["_Expiry_Obj"])

# 4. Monthly Sales & Revenue Report
elif report_choice == "Monthly Sales & Revenue Report":
    report_title = "Monthly_Sales_Report"
    report_desc = "Summary of products sold, unit prices, invoices, and cumulative transaction volumes."
    
    if not df_sales.empty:
        # User input for Month selection
        df_sales["Sale Date Obj"] = pd.to_datetime(df_sales["Sale Date"])
        df_sales["YearMonth"] = df_sales["Sale Date Obj"].dt.strftime("%Y-%m")
        
        available_months = sorted(df_sales["YearMonth"].unique().tolist())
        selected_month = st.selectbox("Select Billing Month", options=available_months)
        
        report_df = df_sales[df_sales["YearMonth"] == selected_month].copy()
        report_df = report_df.drop(columns=["Sale Date Obj", "YearMonth"])

# 5. Category-wise Stock Distribution
elif report_choice == "Category-wise Stock Distribution":
    report_title = "Category_Wise_Stock_Report"
    report_desc = "Aggregated stock volume, unique brand count, and value evaluation per medical category."
    
    if not df_meds.empty:
        df_meds["Stock Value"] = df_meds["Quantity"] * df_meds["Unit Price"]
        report_df = df_meds.groupby("Category").agg(
            Unique_Brands=("Medicine ID", "count"),
            Total_Stock_Quantity=("Quantity", "sum"),
            Total_Inventory_Value=("Stock Value", "sum")
        ).reset_index()
        df_meds = df_meds.drop(columns=["Stock Value"])

# Display and Download Option
if report_df.empty:
    st.warning("⚠️ The generated report contains no records or data files are empty.")
else:
    st.subheader("📋 Report Preview")
    st.caption(report_desc)
    
    # Custom formatters
    format_rules = {}
    if "Unit Price" in report_df.columns:
        format_rules["Unit Price"] = lambda x: f"₹{x:.2f}"
    if "Quantity" in report_df.columns:
        format_rules["Quantity"] = lambda x: f"{x:,} units"
    if "Total Amount" in report_df.columns:
        format_rules["Total Amount"] = lambda x: f"₹{x:.2f}"
    if "Selling Price" in report_df.columns:
        format_rules["Selling Price"] = lambda x: f"₹{x:.2f}"
    if "Total_Inventory_Value" in report_df.columns:
        format_rules["Total_Inventory_Value"] = lambda x: f"₹{x:.2f}"
        
    st.dataframe(
        report_df.style.format(format_rules),
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = report_df.to_csv(index=False)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    st.download_button(
        label="📥 Download Report as CSV",
        data=csv,
        file_name=f"{report_title}_{timestamp}.csv",
        mime="text/csv",
        use_container_width=True
    )
