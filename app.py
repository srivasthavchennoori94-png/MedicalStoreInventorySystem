import streamlit as st
from utils.file_handler import init_files
from utils.helper import inject_custom_css, render_sidebar_branding, check_sidebar_notifications

# Initialize database CSVs and generate sample data
init_files()

# Initialize session state for theme
if "theme_toggle" not in st.session_state:
    st.session_state.theme_toggle = True # Default is Dark Mode

st.session_state.theme = "dark" if st.session_state.theme_toggle else "light"

# Page Setup
st.set_page_config(
    page_title="MediFlow IMS",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject styling
inject_custom_css()

# Define Navigation using modern Streamlit Page routing
dashboard = st.Page("pages/Dashboard.py", title="Dashboard", icon="📊", default=True)
view_meds = st.Page("pages/View_Medicines.py", title="View Medicines", icon="📋")
add_med = st.Page("pages/Add_Medicine.py", title="Add Medicine", icon="➕")
update_stock = st.Page("pages/Update_Stock.py", title="Update Stock", icon="🔄")
sales = st.Page("pages/Sales.py", title="Sales & Invoicing", icon="🛒")
expiry = st.Page("pages/Expiry_Tracker.py", title="Expiry Tracker", icon="⏳")
reports = st.Page("pages/Reports.py", title="Reports Generator", icon="📈")
settings = st.Page("pages/Settings.py", title="System Settings", icon="⚙️")

# Route pages under logical sections
pg = st.navigation({
    "Overview": [dashboard],
    "Inventory Management": [view_meds, add_med, update_stock],
    "Sales & Transactions": [sales],
    "Expiry & Alerting": [expiry],
    "Reports & Settings": [reports, settings]
}, position="hidden")

# Build Custom Sidebar Layout (Branding at the top, followed by navigation links)
with st.sidebar:
    # Render Logo and Branding at the top
    render_sidebar_branding()
    
    # Theme Toggle Widget
    theme_col1, theme_col2 = st.columns([3, 1])
    with theme_col1:
        label_text = "🌙 Dark Mode" if st.session_state.theme_toggle else "☀️ Light Mode"
        st.markdown(f"<div style='font-size: 0.95rem; font-weight: 500; padding-top: 4px; color: var(--sidebar-text);'>{label_text}</div>", unsafe_allow_html=True)
    with theme_col2:
        st.toggle("Theme Toggle", key="theme_toggle", label_visibility="collapsed")
        
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    # Custom Navigation Links with category headers
    st.markdown("<div style='color: #64748b; font-size: 0.75rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.3rem; text-transform: uppercase; letter-spacing: 0.05em;'>Overview</div>", unsafe_allow_html=True)
    st.page_link(dashboard)
    
    st.markdown("<div style='color: #64748b; font-size: 0.75rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.3rem; text-transform: uppercase; letter-spacing: 0.05em;'>Inventory Management</div>", unsafe_allow_html=True)
    st.page_link(view_meds)
    st.page_link(add_med)
    st.page_link(update_stock)
    
    st.markdown("<div style='color: #64748b; font-size: 0.75rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.3rem; text-transform: uppercase; letter-spacing: 0.05em;'>Sales & Transactions</div>", unsafe_allow_html=True)
    st.page_link(sales)
    
    st.markdown("<div style='color: #64748b; font-size: 0.75rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.3rem; text-transform: uppercase; letter-spacing: 0.05em;'>Expiry & Alerting</div>", unsafe_allow_html=True)
    st.page_link(expiry)
    
    st.markdown("<div style='color: #64748b; font-size: 0.75rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.3rem; text-transform: uppercase; letter-spacing: 0.05em;'>Reports & Settings</div>", unsafe_allow_html=True)
    st.page_link(reports)
    st.page_link(settings)

# Run the selected page
pg.run()

# Sidebar notification warnings
st.sidebar.markdown("---")
check_sidebar_notifications()
st.sidebar.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.75rem; margin-top: 20px;'>"
    "MediFlow IMS v1.0.0<br>© 2026 MediFlow Inc."
    "</div>", 
    unsafe_allow_html=True
)
