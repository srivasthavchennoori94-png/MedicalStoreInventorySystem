import streamlit as st
import datetime
from utils.file_handler import add_medicine, load_medicines, load_suppliers
from utils.validations import validate_medicine

st.title("➕ Add Medicine to Inventory")
st.markdown("Enter details below to register a new medicine batch in the database.")

# Load dynamic select options
df_meds = load_medicines()
df_sups = load_suppliers()

categories = sorted(df_meds["Category"].unique().tolist()) if not df_meds.empty else []
default_categories = ["Analgesics", "Antibiotics", "Antidiabetics", "Antihypertensives", "Antivirals", "Vitamins", "Antihistamines", "Cardiovascular"]
for cat in default_categories:
    if cat not in categories:
        categories.append(cat)
categories.append("Other (Specify New)")

suppliers = sorted(df_sups["Supplier Name"].unique().tolist()) if not df_sups.empty else []
if not suppliers:
    suppliers = ["Apex Pharmaceuticals", "Sun Distributors", "MedLife Wholesale", "Cipla Trade Services", "Global Medicals Ltd"]
suppliers.append("Other (Specify New)")

# Form layout
with st.form("add_medicine_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        # Generate Suggested Medicine ID
        next_id_num = len(df_meds) + 1 if not df_meds.empty else 1
        suggested_id = f"MED{next_id_num:03d}"
        
        med_id = st.text_input("Medicine ID *", value=suggested_id, help="Unique identifier (e.g. MED001)")
        med_name = st.text_input("Medicine Name *", help="Brand name & strength (e.g. Paracetamol 500mg)")
        
        category_sel = st.selectbox("Category *", options=categories)
        new_category = st.text_input("New Category", help="Fill this only if 'Other' is selected above")
        
        manufacturer = st.text_input("Manufacturer *", help="Company manufacturing the medicine")
        batch_number = st.text_input("Batch Number *", help="Batch manufacturing tag (e.g. BCH1082)")
        
    with col2:
        purchase_date = st.date_input("Purchase Date *", value=datetime.date(2026, 7, 10))
        expiry_date = st.date_input("Expiry Date *", value=datetime.date(2027, 7, 10))
        
        quantity = st.number_input("Stock Quantity *", min_value=0, value=100, step=10, help="Initial stock quantity")
        unit_price = st.number_input("Unit Price (₹) *", min_value=0.0, value=50.0, step=5.0, help="Cost per unit")
        
        supplier_sel = st.selectbox("Supplier Name *", options=suppliers)
        new_supplier = st.text_input("New Supplier Name", help="Fill this only if 'Other' is selected above")

    st.markdown("<small style='color: #64748b;'>* Fields marked with asterisk are mandatory.</small>", unsafe_allow_html=True)
    
    submit_button = st.form_submit_button("Add Medicine Record")

if submit_button:
    # Resolve 'Other' inputs
    category = new_category.strip() if category_sel == "Other (Specify New)" else category_sel
    supplier = new_supplier.strip() if supplier_sel == "Other (Specify New)" else supplier_sel
    
    # Prepare payload
    medicine_data = {
        "Medicine ID": med_id.strip(),
        "Medicine Name": med_name.strip(),
        "Category": category,
        "Manufacturer": manufacturer.strip(),
        "Batch Number": batch_number.strip(),
        "Purchase Date": purchase_date.strftime("%Y-%m-%d"),
        "Expiry Date": expiry_date.strftime("%Y-%m-%d"),
        "Quantity": int(quantity),
        "Unit Price": float(unit_price),
        "Supplier Name": supplier
    }
    
    # Validate payload
    is_valid, error_msg = validate_medicine(medicine_data)
    
    if is_valid:
        success = add_medicine(medicine_data)
        if success:
            st.success(f"✅ Medicine '{medicine_data['Medicine Name']}' added successfully with ID '{medicine_data['Medicine ID']}'!")
        else:
            st.error("❌ Failed to save record. Please check file write permissions or if the Medicine ID was duplicated.")
    else:
        st.error(f"⚠️ Validation Failed: {error_msg}")
