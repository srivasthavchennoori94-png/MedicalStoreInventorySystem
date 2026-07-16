import streamlit as st
from utils.file_handler import init_files
from utils.helper import inject_custom_css, render_sidebar_branding, check_sidebar_notifications
from utils.auth import authenticate_user, register_user

# Initialize database CSVs and generate sample data
init_files()

# Initialize session state for theme
if "theme_toggle" not in st.session_state:
    st.session_state.theme_toggle = True # Default is Dark Mode

st.session_state.theme = "dark" if st.session_state.theme_toggle else "light"

# Initialize session state for auth
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Page Setup
st.set_page_config(
    page_title="MediFlow IMS",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject styling
inject_custom_css()

# Authentication Check
if st.session_state.authenticated:
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
        
        # User details profile block
        st.markdown(f"""
        <div style='background: rgba(13, 148, 136, 0.15); padding: 12px; border-radius: 8px; border-left: 4px solid #0d9488; margin-bottom: 15px;'>
            <div style='font-size: 0.75rem; color: var(--text-secondary); font-weight: 600; text-transform: uppercase;'>Logged in as</div>
            <div style='font-size: 1rem; font-weight: 600; color: var(--text-primary);'>{st.session_state.username}</div>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # Logout Section
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

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
else:
    # Render Login / Signup screen
    # Hide sidebar controls when unauthenticated
    st.markdown("""
        <style>
        [data-testid="collapsedControl"] {
            display: none;
        }
        section[data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 60px;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #0d9488; font-size: 3.2rem; margin-bottom: 0;'>💊 MediFlow IMS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--text-secondary); font-size: 1.15rem; margin-bottom: 35px;'>Pharmacy Inventory & Management System</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        auth_mode = st.tabs(["🔑 Sign In", "📝 Create Account"])
        
        with auth_mode[0]:
            st.markdown("<div style='background: var(--card-bg); border: 1px solid var(--card-border); padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top:0;'>Sign In to your Account</h3>", unsafe_allow_html=True)
            
            login_username = st.text_input("Username", key="login_username", placeholder="Enter username").strip()
            login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
            
            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
            if st.button("Sign In", type="primary", use_container_width=True):
                if not login_username or not login_password:
                    st.error("Please fill in all fields.")
                elif authenticate_user(login_username, login_password):
                    st.session_state.authenticated = True
                    st.session_state.username = login_username
                    st.toast("Successfully signed in!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with auth_mode[1]:
            st.markdown("<div style='background: var(--card-bg); border: 1px solid var(--card-border); padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top:0;'>Register New Account</h3>", unsafe_allow_html=True)
            
            signup_username = st.text_input("Username", key="signup_username", placeholder="Choose a username").strip()
            signup_email = st.text_input("Email Address", key="signup_email", placeholder="Enter email address").strip()
            signup_password = st.text_input("Password", type="password", key="signup_password", placeholder="Choose password")
            signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm", placeholder="Confirm your password")
            
            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
            if st.button("Register & Create Account", type="primary", use_container_width=True):
                if not signup_username or not signup_email or not signup_password or not signup_confirm:
                    st.error("Please fill in all fields.")
                elif signup_password != signup_confirm:
                    st.error("Passwords do not match!")
                elif len(signup_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif "@" not in signup_email or "." not in signup_email:
                    st.error("Please enter a valid email address.")
                else:
                    success, msg = register_user(signup_username, signup_password, signup_email)
                    if success:
                        st.success(msg)
                        st.balloons()
                    else:
                        st.error(msg)
            st.markdown("</div>", unsafe_allow_html=True)
