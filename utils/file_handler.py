import os
import pandas as pd
import datetime
import random
from typing import Dict, List, Any, Optional

# Constants for File Paths
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
MEDICINES_FILE = os.path.join(DATA_DIR, "medicines.csv")
SALES_FILE = os.path.join(DATA_DIR, "sales.csv")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.csv")

def ensure_directories():
    """Ensure the data folder exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def init_files(reset: bool = False):
    """Initialize CSV files with correct structures and populate with sample data if empty or reset."""
    ensure_directories()
    
    # 1. Suppliers File
    if reset or not os.path.exists(SUPPLIERS_FILE) or os.path.getsize(SUPPLIERS_FILE) == 0:
        sample_suppliers = [
            {"Supplier ID": "SUP001", "Supplier Name": "Apollo Pharmacy Distributors", "Contact Person": "Rajesh Kumar", "Phone": "9876543210", "Email": "sales@apollodist.in", "Address": "New Delhi, India"},
            {"Supplier ID": "SUP002", "Supplier Name": "MedPlus Wholesalers", "Contact Person": "Amit Sharma", "Phone": "9876543211", "Email": "info@medpluswholesale.in", "Address": "Hyderabad, India"},
            {"Supplier ID": "SUP003", "Supplier Name": "Cipla Trade Agency", "Contact Person": "Vikram Patel", "Phone": "9876543212", "Email": "orders@ciplatrade.in", "Address": "Mumbai, India"},
            {"Supplier ID": "SUP004", "Supplier Name": "Sun Distributors India", "Contact Person": "Suresh Nair", "Phone": "9876543213", "Email": "support@sundistributors.in", "Address": "Chennai, India"},
            {"Supplier ID": "SUP005", "Supplier Name": "Mankind Wholesale Services", "Contact Person": "Sanjay Deshmukh", "Phone": "9876543214", "Email": "contact@mankindwholesale.in", "Address": "Ahmedabad, India"}
        ]
        suppliers_df = pd.DataFrame(sample_suppliers, columns=[
            "Supplier ID", "Supplier Name", "Contact Person", "Phone", "Email", "Address"
        ])
        suppliers_df.to_csv(SUPPLIERS_FILE, index=False)
    
    # 2. Medicines File
    if reset or not os.path.exists(MEDICINES_FILE) or os.path.getsize(MEDICINES_FILE) == 0:
        sample_medicines = generate_sample_medicines()
        medicines_df = pd.DataFrame(sample_medicines, columns=[
            "Medicine ID", "Medicine Name", "Category", "Manufacturer", 
            "Batch Number", "Purchase Date", "Expiry Date", "Quantity", "Unit Price", "Supplier Name"
        ])
        medicines_df.to_csv(MEDICINES_FILE, index=False)
        
    # 3. Sales File
    if reset or not os.path.exists(SALES_FILE) or os.path.getsize(SALES_FILE) == 0:
        sample_sales = generate_sample_sales()
        sales_df = pd.DataFrame(sample_sales, columns=[
            "Invoice Number", "Medicine ID", "Medicine Name", 
            "Quantity Sold", "Selling Price", "Customer Name", "Sale Date", "Total Amount"
        ])
        sales_df.to_csv(SALES_FILE, index=False)

def generate_sample_medicines() -> List[Dict[str, Any]]:
    """Generates 100 realistic medicines, including low stock, expired, and expiring soon."""
    categories = ["Analgesics", "Antibiotics", "Antidiabetics", "Antihypertensives", "Antivirals", "Vitamins", "Antihistamines", "Cardiovascular"]
    manufacturers = ["Cipla", "Sun Pharma", "Dr. Reddy's", "Lupin", "Mankind Pharma", "Torrent Pharma", "Alkem Labs", "Zydus Life"]
    suppliers = ["Apollo Pharmacy Distributors", "MedPlus Wholesalers", "Cipla Trade Agency", "Sun Distributors India", "Mankind Wholesale Services"]
    
    med_templates = {
        "Analgesics": ["Crocin 650mg", "Dolo 650mg", "Combiflam", "Zerodol-SP", "Meftal-Spas", "Dynapar AQ"],
        "Antibiotics": ["Taxim-O 200", "Augmentin 625 Duo", "Monocef-O 200", "Azithral 500", "Ciplox 500", "Sporidex 500"],
        "Antidiabetics": ["Glycomet GP 1", "Janumet 50/500", "Galvus Met 50/500", "Ryzodeg", "Glucobay 50", "Teneliglide 20mg"],
        "Antihypertensives": ["Telma 40", "Amlokind 5", "Cilacar 10", "Concor 5", "Minipress XL", "Moxovas 0.2"],
        "Antivirals": ["Virovir 400", "Fabiflu 400", "Herpex 400", "Entecavir 0.5", "Viraday"],
        "Vitamins": ["Shelcal 500", "Becosules Capsule", "Neurobion Forte", "Limcee 500mg", "Evion 400", "Zincovit"],
        "Antihistamines": ["Allegra 120", "Avil 25", "Cetzip", "Okacet", "Montair-LC"],
        "Cardiovascular": ["Atorva 10", "Rosuvas 10", "Clopilet 75", "Ecospirin 75", "Cardace 5", "Lipvas 20"]
    }
    
    today = datetime.date(2026, 7, 10) # Set to the context time: July 10, 2026
    med_list = []
    
    # We need 100 medicines
    counter = 1
    for category in categories:
        templates = med_templates[category]
        for name in templates:
            # Create a base medicine record
            # Generate different batches
            for i in range(2):
                if counter > 100:
                    break
                    
                med_id = f"MED{counter:03d}"
                batch_num = f"BCH{random.randint(1000, 9999)}"
                
                # Purchase Date: random date in the past 6 months
                purchase_days_ago = random.randint(10, 180)
                purchase_date = today - datetime.timedelta(days=purchase_days_ago)
                
                # Setup specific expiry scenarios to fulfill the system indicators:
                if counter <= 10:
                    # Expired: Expiry date was in the past (e.g. 10 to 45 days ago)
                    expiry_date = today - datetime.timedelta(days=random.randint(10, 45))
                elif counter <= 25:
                    # Expiring Soon: Expiry date in the next 1 to 30 days
                    expiry_date = today + datetime.timedelta(days=random.randint(1, 30))
                else:
                    # Normal Expiry: Expiry date in 6 to 24 months
                    expiry_date = purchase_date + datetime.timedelta(days=random.randint(365, 730))
                
                # Setup specific stock scenarios:
                if counter % 8 == 0:
                    # Low stock threshold (< 20)
                    qty = random.randint(2, 19)
                else:
                    qty = random.randint(50, 500)
                    
                price = float(random.choice([15.0, 25.0, 45.0, 80.0, 120.0, 180.0, 250.0, 320.0, 480.0]))
                
                med_list.append({
                    "Medicine ID": med_id,
                    "Medicine Name": f"{name} (B-{i+1})",
                    "Category": category,
                    "Manufacturer": random.choice(manufacturers),
                    "Batch Number": batch_num,
                    "Purchase Date": purchase_date.strftime("%Y-%m-%d"),
                    "Expiry Date": expiry_date.strftime("%Y-%m-%d"),
                    "Quantity": qty,
                    "Unit Price": price,
                    "Supplier Name": random.choice(suppliers)
                })
                counter += 1
                
    # Fill up to 100 if we are short
    while len(med_list) < 100:
        med_id = f"MED{counter:03d}"
        category = random.choice(categories)
        name = random.choice(med_templates[category])
        batch_num = f"BCH{random.randint(1000, 9999)}"
        purchase_date = today - datetime.timedelta(days=random.randint(10, 180))
        expiry_date = purchase_date + datetime.timedelta(days=random.randint(365, 730))
        qty = random.randint(50, 300)
        price = float(random.choice([20.0, 50.0, 100.0, 150.0]))
        
        med_list.append({
            "Medicine ID": med_id,
            "Medicine Name": f"{name} Extra",
            "Category": category,
            "Manufacturer": random.choice(manufacturers),
            "Batch Number": batch_num,
            "Purchase Date": purchase_date.strftime("%Y-%m-%d"),
            "Expiry Date": expiry_date.strftime("%Y-%m-%d"),
            "Quantity": qty,
            "Unit Price": price,
            "Supplier Name": random.choice(suppliers)
        })
        counter += 1
        
    return med_list

def generate_sample_sales() -> List[Dict[str, Any]]:
    """Generates a small history of sales for visual graphs."""
    today = datetime.date(2026, 7, 10)
    sales = []
    
    # 20 sales over the last 15 days
    med_list = [
        ("MED011", "Augmentin 625 Duo (B-1)", 120.0),
        ("MED035", "Amlokind 5 (B-1)", 45.0),
        ("MED052", "Limcee 500mg (B-2)", 15.0),
        ("MED067", "Atorva 10 (B-1)", 80.0),
        ("MED081", "Glycomet GP 1 Extra", 50.0)
    ]
    
    customers = ["Rahul Sharma", "Priya Sharma", "Amit Patel", "Vikram Singh", "Sunita Rao", "Ramesh Verma", "Deepa Gupta", "Suresh Nair", "Neha Deshmukh", "Sanjay Joshi"]
    
    for i in range(1, 35):
        days_ago = random.randint(0, 14)
        sale_date = today - datetime.timedelta(days=days_ago)
        
        med = random.choice(med_list)
        qty_sold = random.randint(1, 5)
        price = med[2]
        total_amt = qty_sold * price
        
        sales.append({
            "Invoice Number": f"INV{1000 + i}",
            "Medicine ID": med[0],
            "Medicine Name": med[1],
            "Quantity Sold": qty_sold,
            "Selling Price": price,
            "Customer Name": random.choice(customers),
            "Sale Date": sale_date.strftime("%Y-%m-%d"),
            "Total Amount": total_amt
        })
        
    # Sort sales by date ascending
    sales.sort(key=lambda x: x["Sale Date"])
    return sales

# Load / Save Operations
def load_csv(file_path: str) -> pd.DataFrame:
    """Loads a CSV file into a DataFrame, ensuring it exists first."""
    init_files()
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV {file_path}: {e}")
        return pd.DataFrame()

def save_csv(df: pd.DataFrame, file_path: str) -> bool:
    """Saves a DataFrame to a CSV file."""
    try:
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        print(f"Error saving CSV {file_path}: {e}")
        return False

# Database Specific Callers
def load_medicines() -> pd.DataFrame:
    return load_csv(MEDICINES_FILE)

def save_medicines(df: pd.DataFrame) -> bool:
    return save_csv(df, MEDICINES_FILE)

def load_sales() -> pd.DataFrame:
    return load_csv(SALES_FILE)

def save_sales(df: pd.DataFrame) -> bool:
    return save_csv(df, SALES_FILE)

def load_suppliers() -> pd.DataFrame:
    return load_csv(SUPPLIERS_FILE)

def save_suppliers(df: pd.DataFrame) -> bool:
    return save_csv(df, SUPPLIERS_FILE)

# C.R.U.D. Operations for Medicines
def add_medicine(data: Dict[str, Any]) -> bool:
    """Adds a new medicine to medicines.csv."""
    df = load_medicines()
    if data["Medicine ID"] in df["Medicine ID"].values:
        return False # Duplicate ID
    
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    return save_medicines(df)

def update_medicine(med_id: str, data: Dict[str, Any]) -> bool:
    """Updates an existing medicine details."""
    df = load_medicines()
    if med_id not in df["Medicine ID"].values:
        return False
    
    # Locate index
    idx = df[df["Medicine ID"] == med_id].index[0]
    for key, val in data.items():
        if key in df.columns:
            df.at[idx, key] = val
            
    return save_medicines(df)

def delete_medicine(med_id: str) -> bool:
    """Deletes a medicine from the inventory."""
    df = load_medicines()
    if med_id not in df["Medicine ID"].values:
        return False
    
    df = df[df["Medicine ID"] != med_id]
    return save_medicines(df)

def update_stock(med_id: str, qty_change: int, set_absolute: bool = False) -> bool:
    """Increases, decreases, or sets absolute stock for a medicine."""
    df = load_medicines()
    if med_id not in df["Medicine ID"].values:
        return False
    
    idx = df[df["Medicine ID"] == med_id].index[0]
    current_qty = int(df.at[idx, "Quantity"])
    
    if set_absolute:
        new_qty = qty_change
    else:
        new_qty = current_qty + qty_change
        
    if new_qty < 0:
        return False # Cannot have negative stock
        
    df.at[idx, "Quantity"] = new_qty
    return save_medicines(df)

# Sales Logging
def record_sale(sale_data: Dict[str, Any]) -> bool:
    """Records a sale invoice and decreases stock accordingly."""
    df_sales = load_sales()
    
    # 1. Reduce Stock first
    success = update_stock(sale_data["Medicine ID"], -int(sale_data["Quantity Sold"]))
    if not success:
        return False # Not enough stock or ID not found
        
    # 2. Append to sales sheet
    new_sale = pd.DataFrame([sale_data])
    df_sales = pd.concat([df_sales, new_sale], ignore_index=True)
    return save_sales(df_sales)

# Resets
def reset_database() -> bool:
    """Clears and rebuilds the CSV tables to their default state."""
    init_files(reset=True)
    return True

if __name__ == "__main__":
    print("Initializing Database CSV files...")
    init_files(reset=True)
    print("Database directories and dummy data files successfully initialized!")
