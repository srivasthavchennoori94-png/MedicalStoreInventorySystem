import os
import streamlit as st
import datetime
import pandas as pd
from typing import Dict, Any, List
from utils.file_handler import load_medicines, load_sales

def inject_custom_css():
    """Reads assets/styles.css and injects it into the Streamlit app page with theme support."""
    theme = st.session_state.get("theme", "dark")
    
    if theme == "dark":
        theme_vars = """
        :root {
            --bg-color: #0b0f19;
            --sidebar-bg: #0f172a;
            --sidebar-text: #f8fafc;
            --sidebar-border: #1e293b;
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(51, 65, 85, 0.8);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --hr-color: #334155;
            --input-bg: #1e293b;
            --input-border: #334155;
            --input-text: #f8fafc;
            
            --st-background-color: #0b0f19;
            --st-secondary-background-color: #0f172a;
            --st-text-color: #f8fafc;
        }
        """
    else:
        theme_vars = """
        :root {
            --bg-color: #f8fafc;
            --sidebar-bg: #ffffff;
            --sidebar-text: #0f172a;
            --sidebar-border: #cbd5e1;
            --card-bg: rgba(255, 255, 255, 0.85);
            --card-border: rgba(226, 232, 240, 0.85);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --hr-color: #cbd5e1;
            --input-bg: #ffffff;
            --input-border: #cbd5e1;
            --input-text: #0f172a;
            
            --st-background-color: #f8fafc;
            --st-secondary-background-color: #ffffff;
            --st-text-color: #0f172a;
        }
        """
        
    css_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css"))
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            css_content = f.read()
        full_css = theme_vars + "\n" + css_content
        st.markdown(f"<style>{full_css}</style>", unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found at " + css_path)

def render_sidebar_branding():
    """Renders the logo and company title in the Streamlit sidebar."""
    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png"))
    
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
    else:
        # Fallback text if logo image load fails
        st.sidebar.markdown("<h2 style='color:#0d9488;'>💊 MediFlow</h2>", unsafe_allow_html=True)
        
    st.sidebar.markdown(
        "<h3 style='text-align: center; margin-top: -10px; color: var(--text-secondary); font-size: 1.1rem; font-weight: 500;'>Inventory Management</h3>", 
        unsafe_allow_html=True
    )
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

def check_sidebar_notifications():
    """Calculates low stock and expired counts to show notice badges in the sidebar."""
    df_meds = load_medicines()
    if df_meds.empty:
        return
        
    today = datetime.date(2026, 7, 10) # Using active date context
    
    # 1. Low stock count (< 20)
    low_stock_count = len(df_meds[df_meds["Quantity"] < 20])
    
    # 2. Expired count
    expired_count = 0
    expiring_soon_count = 0
    
    for idx, row in df_meds.iterrows():
        try:
            exp_date = datetime.datetime.strptime(str(row["Expiry Date"]), "%Y-%m-%d").date()
            if exp_date < today:
                expired_count += 1
            elif (exp_date - today).days <= 30:
                expiring_soon_count += 1
        except Exception:
            pass
            
    # Draw badges in the sidebar
    st.sidebar.subheader("📢 Quick Alerts")
    
    if expired_count > 0:
        st.sidebar.error(f"🚨 {expired_count} Expired Products")
    if expiring_soon_count > 0:
        st.sidebar.warning(f"⚠️ {expiring_soon_count} Expiring in 30 Days")
    if low_stock_count > 0:
        st.sidebar.info(f"📦 {low_stock_count} Low Stock Items")
        
    if expired_count == 0 and expiring_soon_count == 0 and low_stock_count == 0:
        st.sidebar.success("✅ System check: All items OK")

def format_currency(amount: float) -> str:
    """Formats float to currency string (Rupees)."""
    return f"₹{amount:,.2f}"

def render_metric_card(title: str, value: str, icon: str, color: str = "#0d9488", trend: str = "", trend_type: str = "positive") -> str:
    """Generates HTML for a customized metric card with glassmorphism style."""
    trend_html = ""
    if trend:
        cls = "positive" if trend_type == "positive" else "negative"
        arrow = "↑" if trend_type == "positive" else "↓"
        trend_html = f"<div class='kpi-footer {cls}'><span>{arrow} {trend}</span></div>"
        
    html = f"""
    <div class="kpi-card" style="--accent-color: {color};">
        <div class="kpi-header">
            <span class="kpi-title">{title}</span>
            <span class="kpi-icon">{icon}</span>
        </div>
        <div class="kpi-value">{value}</div>
        {trend_html}
    </div>
    """
    return html
