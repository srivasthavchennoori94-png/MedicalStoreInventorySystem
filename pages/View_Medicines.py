import streamlit as st
import datetime
import pandas as pd
from utils.file_handler import load_medicines, update_medicine, delete_medicine, load_suppliers
from utils.validations import validate_medicine
from utils.helper import format_currency, render_styled_table

st.title("📋 View & Manage Medicines")
st.markdown("Search, sort, filter, update or delete medicine records from the inventory database.")

# Load active medicines
df_meds = load_medicines()

if df_meds.empty:
    st.info("No medicine inventory records found. Add some medicines first!")
else:
    # ------------------ Navigation Tabs ------------------
    tab1, tab2 = st.tabs(["🔍 Search & Filter", "🛠️ Edit / Delete Records"])
    
    with tab1:
        # Search & Filter Layout
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            search_query = st.text_input("Search by Medicine Name, ID or Supplier", placeholder="Type name, ID, batch, supplier...")
        with col2:
            categories = ["All"] + sorted(df_meds["Category"].unique().tolist())
            selected_category = st.selectbox("Filter Category", categories)
        with col3:
            manufacturers = ["All"] + sorted(df_meds["Manufacturer"].unique().tolist())
            selected_mfr = st.selectbox("Filter Manufacturer", manufacturers)
        with col4:
            expiry_options = ["All", "Expired", "Expiring Soon (<30d)", "Safe / Valid"]
            selected_exp = st.selectbox("Expiry Status", expiry_options)
            
        # Sorting Controls
        col_sort1, col_sort2, _ = st.columns([1, 1, 2])
        with col_sort1:
            sort_by = st.selectbox("Sort By", ["Medicine ID", "Medicine Name", "Expiry Date", "Quantity", "Unit Price"])
        with col_sort2:
            sort_order = st.selectbox("Order", ["Ascending", "Descending"])
            
        # Apply Search/Filters
        filtered_df = df_meds.copy()
        
        # 1. Text Search
        if search_query:
            q = search_query.lower()
            filtered_df = filtered_df[
                filtered_df["Medicine Name"].str.lower().str.contains(q) |
                filtered_df["Medicine ID"].str.lower().str.contains(q) |
                filtered_df["Batch Number"].str.lower().str.contains(q) |
                filtered_df["Supplier Name"].str.lower().str.contains(q)
            ]
            
        # 2. Category Filter
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["Category"] == selected_category]
            
        # 3. Manufacturer Filter
        if selected_mfr != "All":
            filtered_df = filtered_df[filtered_df["Manufacturer"] == selected_mfr]
            
        # 4. Expiry Filter
        today = datetime.date(2026, 7, 10)
        if selected_exp != "All":
            expiry_statuses = []
            for idx, row in filtered_df.iterrows():
                try:
                    exp_date = datetime.datetime.strptime(str(row["Expiry Date"]), "%Y-%m-%d").date()
                    if exp_date < today:
                        expiry_statuses.append("Expired")
                    elif (exp_date - today).days <= 30:
                        expiry_statuses.append("Expiring Soon (<30d)")
                    else:
                        expiry_statuses.append("Safe / Valid")
                except Exception:
                    expiry_statuses.append("Unknown")
                    
            filtered_df["_expiry_status"] = expiry_statuses
            
            if selected_exp == "Expired":
                filtered_df = filtered_df[filtered_df["_expiry_status"] == "Expired"]
            elif selected_exp == "Expiring Soon (<30d)":
                filtered_df = filtered_df[filtered_df["_expiry_status"] == "Expiring Soon (<30d)"]
            elif selected_exp == "Safe / Valid":
                filtered_df = filtered_df[filtered_df["_expiry_status"] == "Safe / Valid"]
                
            filtered_df = filtered_df.drop(columns=["_expiry_status"])
            
        # Apply Sorting
        ascending = (sort_order == "Ascending")
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
        
        # Display Table
        st.markdown(f"**Showing {len(filtered_df)} matches**")
        st.markdown(render_styled_table(filtered_df), unsafe_allow_html=True)
        
    with tab2:
        st.subheader("📝 Edit or Delete Selected Medicine")
        
        # Select medicine
        med_options = {f"{row['Medicine ID']} - {row['Medicine Name']} (Batch: {row['Batch Number']})": row['Medicine ID'] for idx, row in df_meds.iterrows()}
        selected_med_label = st.selectbox("Select Medicine to Edit or Delete", options=list(med_options.keys()))
        
        selected_med_id = med_options[selected_med_label]
        med_row = df_meds[df_meds["Medicine ID"] == selected_med_id].iloc[0]
        
        # Edit Form
        with st.form("edit_medicine_form"):
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                st.text_input("Medicine ID (Cannot change)", value=med_row["Medicine ID"], disabled=True)
                edit_name = st.text_input("Medicine Name", value=med_row["Medicine Name"])
                
                categories = sorted(df_meds["Category"].unique().tolist())
                edit_category = st.selectbox("Category", options=categories, index=categories.index(med_row["Category"]) if med_row["Category"] in categories else 0)
                
                edit_mfr = st.text_input("Manufacturer", value=med_row["Manufacturer"])
                edit_batch = st.text_input("Batch Number", value=med_row["Batch Number"])
                
            with col_e2:
                # Dates
                cur_pur_date = datetime.datetime.strptime(str(med_row["Purchase Date"]), "%Y-%m-%d").date()
                cur_exp_date = datetime.datetime.strptime(str(med_row["Expiry Date"]), "%Y-%m-%d").date()
                
                edit_pur_date = st.date_input("Purchase Date", value=cur_pur_date)
                edit_exp_date = st.date_input("Expiry Date", value=cur_exp_date)
                
                edit_qty = st.number_input("Quantity", min_value=0, value=int(med_row["Quantity"]))
                edit_price = st.number_input("Unit Price (₹)", min_value=0.0, value=float(med_row["Unit Price"]))
                
                df_sups = load_suppliers()
                suppliers = sorted(df_sups["Supplier Name"].unique().tolist()) if not df_sups.empty else []
                if med_row["Supplier Name"] not in suppliers:
                    suppliers.append(med_row["Supplier Name"])
                edit_supplier = st.selectbox("Supplier Name", options=suppliers, index=suppliers.index(med_row["Supplier Name"]) if med_row["Supplier Name"] in suppliers else 0)
                
            save_changes = st.form_submit_button("💾 Save Changes")
            
        if save_changes:
            edit_data = {
                "Medicine ID": selected_med_id,
                "Medicine Name": edit_name.strip(),
                "Category": edit_category,
                "Manufacturer": edit_mfr.strip(),
                "Batch Number": edit_batch.strip(),
                "Purchase Date": edit_pur_date.strftime("%Y-%m-%d"),
                "Expiry Date": edit_exp_date.strftime("%Y-%m-%d"),
                "Quantity": int(edit_qty),
                "Unit Price": float(edit_price),
                "Supplier Name": edit_supplier
            }
            
            is_valid, error_msg = validate_medicine(edit_data, is_edit=True)
            if is_valid:
                if update_medicine(selected_med_id, edit_data):
                    st.success(f"✅ Medicine '{edit_name}' (ID: {selected_med_id}) details updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update details.")
            else:
                st.error(f"⚠️ Validation error: {error_msg}")
                
        # Delete Operations
        st.markdown("---")
        st.subheader("🚨 Danger Zone")
        st.warning(f"Deleting this medicine will permanently erase '{med_row['Medicine Name']}' from inventory records.")
        
        confirm_del = st.checkbox("I confirm that I want to delete this medicine.")
        delete_btn = st.button("🗑️ Delete Medicine Permanently", type="primary")
        
        if delete_btn:
            if confirm_del:
                if delete_medicine(selected_med_id):
                    st.success(f"🗑️ Medicine '{med_row['Medicine Name']}' deleted successfully.")
                    st.rerun()
                else:
                    st.error("❌ Could not delete the medicine.")
            else:
                st.error("⚠️ Please check the confirmation checkbox first.")
