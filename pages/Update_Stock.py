import streamlit as st
from utils.file_handler import load_medicines, update_stock

st.title("🔄 Stock Management")
st.markdown("Adjust inventory stock levels manually (increase/reduce stock count) and manage low stock warnings.")

df_meds = load_medicines()

if df_meds.empty:
    st.info("No medicine inventory records found. Add medicines to update stock.")
else:
    # Build options
    med_options = {f"{row['Medicine ID']} - {row['Medicine Name']} (Qty: {row['Quantity']})": row['Medicine ID'] for idx, row in df_meds.iterrows()}
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Adjust Medicine Stock")
        selected_med_label = st.selectbox("Select Medicine *", options=list(med_options.keys()))
        selected_med_id = med_options[selected_med_label]
        
        # Load active row details
        med_row = df_meds[df_meds["Medicine ID"] == selected_med_id].iloc[0]
        current_qty = int(med_row["Quantity"])
        
        # Action selector
        action = st.radio("Stock Adjustment Operation", ["Increase Stock (+)", "Reduce Stock (-)", "Set Exact Stock Value"])
        
        adjust_qty = st.number_input("Adjustment Quantity *", min_value=1, value=10, step=5, help="Number of items to add or subtract")
        
        submit_btn = st.button("Update Stock Levels", use_container_width=True)
        
    with col2:
        st.subheader("Inventory Status Card")
        
        # Determine status colors
        if current_qty == 0:
            status_text = "OUT OF STOCK"
            status_color = "red"
            badge_class = "badge-danger"
        elif current_qty < 20:
            status_text = "CRITICAL LOW STOCK"
            status_color = "orange"
            badge_class = "badge-warning"
        else:
            status_text = "STOCK HEALTHY"
            status_color = "green"
            badge_class = "badge-success"
            
        st.markdown(
            f"""
            <div style='background-color: rgba(255,255,255,0.05); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 1.5rem; text-align: center;'>
                <p style='color: #64748b; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 5px;'>Active Product</p>
                <h4 style='margin: 0; font-size: 1.25rem; font-weight: 600;'>{med_row['Medicine Name']}</h4>
                <p style='font-size: 0.8rem; color: #94a3b8; margin: 5px 0 15px 0;'>Batch: {med_row['Batch Number']} | Category: {med_row['Category']}</p>
                <hr style='margin: 10px 0;'>
                <p style='color: #64748b; margin-bottom: 5px;'>Current Quantity</p>
                <h2 style='font-size: 3rem; margin: 0; font-weight: 700; color: {status_color};'>{current_qty}</h2>
                <span class='badge {badge_class}' style='margin-top: 10px;'>{status_text}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if current_qty < 20:
            st.warning(f"⚠️ **Low Stock Alert**: The quantity of this medicine is below the threshold of 20. Please restock soon!")

    if submit_btn:
        qty_change = 0
        set_absolute = False
        
        if action == "Increase Stock (+)":
            qty_change = adjust_qty
        elif action == "Reduce Stock (-)":
            qty_change = -adjust_qty
            if current_qty - adjust_qty < 0:
                st.error("❌ Stock reduction failed. You cannot reduce stock below 0 units.")
                st.stop()
        elif action == "Set Exact Stock Value":
            qty_change = adjust_qty
            set_absolute = True
            
        success = update_stock(selected_med_id, qty_change, set_absolute=set_absolute)
        if success:
            st.success("✅ Stock level updated successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to update stock level. Please check file writing permissions.")
