import streamlit as st
import pandas as pd
from utils.file_handler import reset_database, load_suppliers, save_suppliers
from utils.helper import render_styled_table

st.title("⚙️ System Settings & Tools")
st.markdown("Configure system parameters, manage supplier details, and perform database resets.")

tab1, tab2, tab3 = st.tabs(["🤝 Suppliers Directory", "🚨 Database Administration", "ℹ️ System Info"])

# ----------------- Tab 1: Supplier Directory -----------------
with tab1:
    st.subheader("Manage Suppliers")
    df_sups = load_suppliers()
    
    col_s1, col_s2 = st.columns([3, 2])
    
    with col_s1:
        st.markdown("**Registered Suppliers**")
        if not df_sups.empty:
            st.markdown(render_styled_table(df_sups), unsafe_allow_html=True)
        else:
            st.info("No suppliers registered.")
            
    with col_s2:
        st.markdown("**Add New Supplier**")
        with st.form("add_supplier_form", clear_on_submit=True):
            next_sup_id = len(df_sups) + 1 if not df_sups.empty else 1
            sup_id = st.text_input("Supplier ID *", value=f"SUP{next_sup_id:03d}")
            sup_name = st.text_input("Supplier Name *")
            contact_person = st.text_input("Contact Person")
            phone = st.text_input("Phone Number")
            email = st.text_input("Email ID")
            address = st.text_area("Postal Address")
            
            submit_sup = st.form_submit_button("Add Supplier")
            
        if submit_sup:
            if not sup_name.strip() or not sup_id.strip():
                st.error("⚠️ Supplier ID and Supplier Name are mandatory fields.")
            elif not df_sups.empty and sup_id.strip() in df_sups["Supplier ID"].values:
                st.error(f"❌ Supplier ID '{sup_id}' already exists.")
            else:
                new_sup = {
                    "Supplier ID": sup_id.strip(),
                    "Supplier Name": sup_name.strip(),
                    "Contact Person": contact_person.strip(),
                    "Phone": phone.strip(),
                    "Email": email.strip(),
                    "Address": address.strip()
                }
                
                df_sups = pd.concat([df_sups, pd.DataFrame([new_sup])], ignore_index=True)
                if save_suppliers(df_sups):
                    st.success(f"✅ Supplier '{sup_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save supplier.")

# ----------------- Tab 2: Database Administration -----------------
with tab2:
    st.subheader("Database Backups & Reset")
    st.warning(
        "⚠️ **CRITICAL WARNING**: Resetting the database will overwrite all your medicines, sales invoices, "
        "and supplier files with default sample records. All your customized inputs will be permanently lost."
    )
    
    confirm_reset = st.checkbox("I understand the consequences and wish to completely reset the system data.")
    reset_btn = st.button("🚨 Reset Database to Default State", type="primary")
    
    if reset_btn:
        if confirm_reset:
            with st.spinner("Rebuilding database records..."):
                if reset_database():
                    st.success("✅ Database reset complete. Streamlit application will now refresh!")
                    st.rerun()
                else:
                    st.error("❌ Database reset failed. Verify file system write permissions.")
        else:
            st.error("⚠️ Please confirm by checking the safety checkbox before running a reset.")

# ----------------- Tab 3: System Info -----------------
with tab3:
    st.subheader("Application Specifications")
    st.markdown(
        """
        - **System Name**: MediFlow IMS
        - **Project Type**: Degree College Mini Project
        - **OS Compatibility**: Windows 10/11, macOS, Linux
        - **Core Stack**: Python, Streamlit, Pandas, Plotly
        - **Data Store**: Flat File CSV (Multi-table)
        - **Framework Version**: Streamlit 1.35+ Page Navigation Router
        
        #### 👨‍💻 Student Notes
        This project has been developed with **Object-Oriented Programming (OOP)** conventions and modular design logic. 
        It demonstrates data analytics, validation patterns, stock state machines, and file serialization inside standard Python frameworks.
        """
    )
