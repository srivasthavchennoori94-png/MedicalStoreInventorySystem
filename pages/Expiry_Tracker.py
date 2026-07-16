import streamlit as st
import datetime
import pandas as pd
from utils.file_handler import load_medicines
from utils.helper import render_styled_table

st.title("⏳ Expiry & Compliance Tracker")
st.markdown("Track and filter medicines that have expired or are expiring within the next 30 days to ensure safety compliance.")

df_meds = load_medicines()

if df_meds.empty:
    st.info("No medicine inventory records found.")
else:
    today = datetime.date(2026, 7, 10)
    
    # Pre-parse dates for sorting and comparison
    df_meds["_Expiry_Date_Obj"] = pd.to_datetime(df_meds["Expiry Date"]).dt.date
    
    # 1. Expired Items
    expired_df = df_meds[df_meds["_Expiry_Date_Obj"] < today].copy()
    expired_df = expired_df.drop(columns=["_Expiry_Date_Obj"])
    
    # 2. Expiring in 30 Days
    expiring_soon_df = df_meds[
        (df_meds["_Expiry_Date_Obj"] >= today) & 
        (df_meds["_Expiry_Date_Obj"] <= today + datetime.timedelta(days=30))
    ].copy()
    expiring_soon_df = expiring_soon_df.drop(columns=["_Expiry_Date_Obj"])
    
    # Clean temporary column
    df_meds = df_meds.drop(columns=["_Expiry_Date_Obj"])
    
    # ------------------ Metrics Header ------------------
    col1, col2 = st.columns(2)
    with col1:
        st.error(f"🚨 **Total Expired Medicines**: {len(expired_df)}")
    with col2:
        st.warning(f"⏳ **Expiring within 30 Days**: {len(expiring_soon_df)}")
        
    st.markdown("---")
    
    # ------------------ Tabbed lists ------------------
    tab1, tab2 = st.tabs(["❌ Expired Products", "⚠️ Expiring Soon (<30 Days)"])
    
    with tab1:
        st.subheader("Expired Medicines list")
        if not expired_df.empty:
            st.markdown(render_styled_table(expired_df), unsafe_allow_html=True)
            
            # Export to CSV
            csv_expired = expired_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Expired List to CSV",
                data=csv_expired,
                file_name="expired_medicines_report.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ Awesome! No expired medicines found in inventory.")
            
    with tab2:
        st.subheader("Medicines Expiring within 30 Days")
        if not expiring_soon_df.empty:
            st.markdown(render_styled_table(expiring_soon_df), unsafe_allow_html=True)
            
            # Export to CSV
            csv_expiring = expiring_soon_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Expiring Soon List to CSV",
                data=csv_expiring,
                file_name="expiring_soon_report.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ Good! No medicines are expiring in the next 30 days.")
