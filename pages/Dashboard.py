import streamlit as st
import datetime
from utils.analytics import get_kpi_metrics, get_recent_medicines
from utils.charts import plot_category_distribution, plot_stock_by_category, plot_sales_trend
from utils.file_handler import load_medicines, load_sales
from utils.helper import render_metric_card, format_currency, render_styled_table

# Page Title
st.title("📊 Pharmacy Dashboard")
st.markdown("Real-time operational summary of your pharmacy inventory and transactions.")

# Load active data
df_meds = load_medicines()
df_sales = load_sales()

# Fetch KPIs
kpis = get_kpi_metrics()

# ----------------- KPI Cards Grid (Row 1) -----------------
st.markdown("### Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        render_metric_card("Total Medicines", f"{kpis['total_medicines']}", "💊", "#0d9488"), 
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        render_metric_card("Total Categories", f"{kpis['total_categories']}", "📂", "#3b82f6"), 
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        render_metric_card("Total Stock Volume", f"{kpis['total_stock']:,}", "📦", "#8b5cf6"), 
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        render_metric_card("Total Revenue", format_currency(kpis['total_revenue']), "💰", "#10b981"), 
        unsafe_allow_html=True
    )

st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)

# ----------------- KPI Cards Grid (Row 2) -----------------
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown(
        render_metric_card("Low Stock Items", f"{kpis['low_stock']}", "⚠️", "#f59e0b" if kpis['low_stock'] > 0 else "#10b981"), 
        unsafe_allow_html=True
    )
with col6:
    st.markdown(
        render_metric_card("Expired Products", f"{kpis['expired']}", "🚨", "#ef4444" if kpis['expired'] > 0 else "#10b981"), 
        unsafe_allow_html=True
    )
with col7:
    st.markdown(
        render_metric_card("Expiring Soon (<30d)", f"{kpis['expiring_soon']}", "⏳", "#e11d48" if kpis['expiring_soon'] > 0 else "#10b981"), 
        unsafe_allow_html=True
    )
with col8:
    st.markdown(
        render_metric_card("Today's Sales", f"{kpis['today_sales']} ({format_currency(kpis['today_revenue'])})", "🛒", "#ec4899"), 
        unsafe_allow_html=True
    )

st.markdown("---")

# ----------------- Chart Columns -----------------
st.markdown("### Visual Insights")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_sales = plot_sales_trend(df_sales)
    if fig_sales:
        st.plotly_chart(fig_sales, use_container_width=True, theme=None)
    else:
        st.info("No transaction data available to plot sales trend.")

with chart_col2:
    fig_cat = plot_category_distribution(df_meds)
    if fig_cat:
        st.plotly_chart(fig_cat, use_container_width=True, theme=None)
    else:
        st.info("No medicine data available to plot categories.")

# Row of category stock volumes
fig_stock = plot_stock_by_category(df_meds)
if fig_stock:
    st.plotly_chart(fig_stock, use_container_width=True, theme=None)

st.markdown("---")

# ----------------- Recent Medicines Table -----------------
st.markdown("### 🆕 Recently Added Medicines")
df_recent = get_recent_medicines(5)

if not df_recent.empty:
    st.markdown(render_styled_table(df_recent), unsafe_allow_html=True)
else:
    st.info("No medicine inventory records found.")
