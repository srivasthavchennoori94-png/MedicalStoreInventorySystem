import streamlit as st
import datetime
import random
from utils.file_handler import load_medicines, load_sales, record_sale
from utils.validations import validate_sale
from utils.helper import format_currency

st.title("🛒 Sales & Checkout Module")
st.markdown("Record retail transactions, generate invoices, and automatically deduct stock counts.")

df_meds = load_medicines()
df_sales = load_sales()

# Filter out medicines with zero stock
in_stock_meds = df_meds[df_meds["Quantity"] > 0] if not df_meds.empty else pd.DataFrame()

if in_stock_meds.empty:
    st.error("🚨 Zero stock available in inventory. Please add medicines or update stock levels before making sales.")
else:
    # Build options for select box
    med_choices = {f"{row['Medicine ID']} - {row['Medicine Name']} (Available: {row['Quantity']})": row['Medicine ID'] for idx, row in in_stock_meds.iterrows()}
    
    # Session state to store printable invoice after sale
    if "invoice_data" not in st.session_state:
        st.session_state.invoice_data = None
        
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Invoice Details")
        
        # Form
        with st.form("sales_transaction_form"):
            # Auto-generated Invoice Number
            next_inv_num = len(df_sales) + 1 if not df_sales.empty else 1
            suggested_inv = f"INV{1000 + next_inv_num}"
            
            invoice_num = st.text_input("Invoice Number *", value=suggested_inv, help="Unique receipt ID")
            
            selected_choice = st.selectbox("Select Medicine to Sell *", options=list(med_choices.keys()))
            selected_med_id = med_choices[selected_choice]
            
            # Load active medicine info
            med_row = in_stock_meds[in_stock_meds["Medicine ID"] == selected_med_id].iloc[0]
            max_qty = int(med_row["Quantity"])
            unit_price = float(med_row["Unit Price"])
            
            customer_name = st.text_input("Customer Name", value="Walk-in Customer", help="Name of client purchasing medicines")
            
            col_in1, col_in2 = st.columns(2)
            with col_in1:
                qty_sold = st.number_input("Quantity to Sell *", min_value=1, max_value=max_qty, value=1, step=1)
            with col_in2:
                selling_price = st.number_input("Selling Unit Price (₹) *", min_value=0.0, value=unit_price, step=5.0)
                
            sale_date = st.date_input("Sale Date *", value=datetime.date(2026, 7, 10))
            
            submit_sale = st.form_submit_button("💳 Process Transaction & Generate Bill")
            
        if submit_sale:
            # Validate Invoice Number Uniqueness
            if not df_sales.empty and invoice_num in df_sales["Invoice Number"].values:
                st.error(f"❌ Invoice Number '{invoice_num}' has already been processed in database.")
                st.stop()
                
            # Business validations
            is_valid, err_msg = validate_sale(max_qty, int(qty_sold), float(selling_price))
            if is_valid:
                total_amt = int(qty_sold) * float(selling_price)
                
                # Assemble Sale Record
                sale_record = {
                    "Invoice Number": invoice_num.strip(),
                    "Medicine ID": selected_med_id,
                    "Medicine Name": med_row["Medicine Name"],
                    "Quantity Sold": int(qty_sold),
                    "Selling Price": float(selling_price),
                    "Customer Name": customer_name.strip(),
                    "Sale Date": sale_date.strftime("%Y-%m-%d"),
                    "Total Amount": total_amt
                }
                
                success = record_sale(sale_record)
                if success:
                    st.success("🎉 Transaction completed successfully! Stock deducted.")
                    st.session_state.invoice_data = sale_record
                    st.rerun()
                else:
                    st.error("❌ Transaction failed. Stock level might have changed or file is locked.")
            else:
                st.error(f"⚠️ Validation Error: {err_msg}")
                
    with col2:
        st.subheader("Invoice Receipt")
        
        # Display session invoice
        if st.session_state.invoice_data:
            inv = st.session_state.invoice_data
            
            # Print styled invoice HTML box
            st.markdown(
                f"""<div style="background-color: #ffffff; color: #000000; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 2rem; font-family: 'Courier New', Courier, monospace; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
<div style="text-align: center; margin-bottom: 20px;">
<h3 style="margin: 0; font-weight: bold; color: #0d9488;">MEDIFLOW PHARMACY</h3>
<p style="margin: 3px 0; font-size: 0.8rem; color: #475569;">123 Healthcare Rd, Medical City</p>
<p style="margin: 3px 0; font-size: 0.8rem; color: #475569;">Phone: 9876543210</p>
</div>
<hr style="border-top: 1px dashed #cbd5e1; margin: 15px 0;">
<div style="font-size: 0.85rem; line-height: 1.5; color: #334155;">
<b>Invoice:</b> {inv['Invoice Number']}<br>
<b>Date:</b> {inv['Sale Date']}<br>
<b>Customer:</b> {inv['Customer Name']}<br>
</div>
<hr style="border-top: 1px dashed #cbd5e1; margin: 15px 0;">
<table style="width: 100%; font-size: 0.85rem; color: #334155; border-collapse: collapse;">
<thead>
<tr style="border-bottom: 1px solid #e2e8f0;">
<th style="text-align: left; padding: 4px 0;">Item Description</th>
<th style="text-align: right; padding: 4px 0;">Qty</th>
<th style="text-align: right; padding: 4px 0;">Price</th>
<th style="text-align: right; padding: 4px 0;">Total</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding: 8px 0; max-width: 150px; word-break: break-all;">{inv['Medicine Name']}</td>
<td style="text-align: right; padding: 8px 0;">{inv['Quantity Sold']}</td>
<td style="text-align: right; padding: 8px 0;">₹{inv['Selling Price']:.2f}</td>
<td style="text-align: right; padding: 8px 0;">₹{inv['Total Amount']:.2f}</td>
</tr>
</tbody>
</table>
<hr style="border-top: 1px dashed #cbd5e1; margin: 15px 0;">
<div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 1rem; color: #0f172a; margin-top: 10px;">
<span>Grand Total:</span>
<span>₹{inv['Total Amount']:.2f}</span>
</div>
<div style="text-align: center; margin-top: 30px; font-size: 0.75rem; color: #64748b;">
Thank you for visiting! Get well soon.<br>
*** Computer Generated Receipt ***
</div>
</div>""", 
                unsafe_allow_html=True
            )
            
            # Button to clear receipt
            if st.button("Close Receipt"):
                st.session_state.invoice_data = None
                st.rerun()
        else:
            st.info("No transaction has been processed in this session yet. Complete the form to view receipt.")
