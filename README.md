# MediFlow IMS - Medical Store Inventory System

MediFlow IMS is a modern, responsive, and fully-featured Pharmacy Inventory Management System built using Python and Streamlit. This application was designed as a Degree College Mini Project to demonstrate robust data structures, validation pipelines, analytical plotting, and transactional state updates using standard Python tools and flat CSV files (no SQL databases required).

---

## 🚀 Features

- **Responsive Analytics Dashboard**: High-level visual KPI metrics (total medicines, stock volumes, warning indicators for low/expired items, today's sales and revenues) and live Plotly visualizer charts.
- **Form-Validated Inventory Registration**: Prevent duplicate IDs, check purchase/expiration order, flag negative numbers, and auto-generate unique medicine keys.
- **Searchable Inventory Directory**: Real-time filtering by category, manufacturer, date range, search query terms, and interactive sorting columns. Includes direct edit/deletion forms.
- **Active Stock Controller**: Adjustment selectors for increasing, decreasing, or setting exact stock levels with real-time notifications for critical bounds.
- **Sales & Billing Module**: Log transactions, verify quantity margins, deduct quantities from CSV datasets, and print a formatted shop receipt on screen.
- **Expiry Compliance Tracker**: Highlight expired inventory, calculate batches expiring in the next 30 days, and export audit reports directly to Excel-compatible CSVs.
- **Report Manager**: Download filtered spreadsheets for current stock levels, low-stock warnings, monthly sales logs, or category value analyses.
- **Modern UI Styling**: Tailored CSS for card layouts, glassmorphic metrics, custom color palettes, brand logo rendering, and smooth sidebar layout.

---

## 📂 Project Structure

```text
medical_store_inventory/
│
├── app.py                      # Main router & Streamlit entrypoint
├── requirements.txt            # Python dependencies
├── README.md                   # Installation & usage documentation
│
├── data/                       # CSV databases (generated automatically)
│   ├── medicines.csv           # 100 sample medicine records
│   ├── sales.csv               # Historical sales records
│   └── suppliers.csv           # Registered wholesale suppliers
│
├── pages/                      # Page components
│   ├── Dashboard.py            # Overview statistics & Plotly trends
│   ├── Add_Medicine.py         # Registration portal
│   ├── View_Medicines.py       # Inventory directory & CRUD utilities
│   ├── Update_Stock.py         # Increase/decrease count sliders
│   ├── Sales.py                # Transaction logs & bill printing
│   ├── Expiry_Tracker.py       # Expired audits & CSV downloaders
│   ├── Reports.py              # Exporting custom compliance datasets
│   └── Settings.py             # Administrative panel & supplier directories
│
├── utils/                      # Business & Data Logic
│   ├── file_handler.py         # Read/write serialization & data resets
│   ├── analytics.py            # Math backend calculations for KPIs
│   ├── charts.py               # Plotly figure configurations
│   ├── validations.py          # Field syntax/value validations
│   └── helper.py               # Sidebar templates & metric layouts
│
├── assets/                     # Stylistic branding assets
│   ├── logo.png                # Vector medical brand icon
│   └── styles.css              # Custom font injections & card rules
│
└── images/                     # Screenshots directory
```

---

## 🛠️ Installation & Setup

Ensure you have **Python 3.8+** installed on your Windows machine. Follow these quick steps to set up and run the system locally:

### 1. Clone or Copy Workspace Files
Ensure all project folders (`pages/`, `utils/`, `assets/`, `data/`) are in a single directory named `MediFlow_IMS`.

### 2. Set Up a Virtual Environment (Recommended)
Open VS Code terminal inside the workspace directory and execute:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all package requirements automatically listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
Start the server:
```powershell
streamlit run app.py
```
This will automatically launch the browser and display the **MediFlow IMS Dashboard** on:
`http://localhost:8501`

---

## 💡 Notes for Demonstrating (Viva/Viva-Voce)
- **Flat File DB**: Point out that the system operates completely offline without external DB services (like SQLite or MySQL), making it highly portable and simple to deploy for mini-projects.
- **Mock Reset**: If you run out of sample stock or mess up during live demonstrations, go to **System Settings** > **Database Administration**, check the confirmation box, and click **Reset Database**. This rebuilds 100 fresh realistic medical records (with expired/low-stock/sales history) instantly.
- **Validation Layers**: Walk the examiner through `utils/validations.py` to show code quality standards.
