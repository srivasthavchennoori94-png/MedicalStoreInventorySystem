import datetime
from typing import Dict, Any, Tuple, Optional
import pandas as pd
from utils.file_handler import load_medicines

def validate_medicine(data: Dict[str, Any], is_edit: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validates the medicine entry form fields.
    Returns (True, None) if valid, otherwise (False, "Error Message").
    """
    # 1. Medicine Name Mandatory
    name = data.get("Medicine Name", "").strip()
    if not name:
        return False, "Medicine Name is a mandatory field."
        
    # 2. Medicine ID uniqueness (only for new records)
    med_id = data.get("Medicine ID", "").strip()
    if not med_id:
        return False, "Medicine ID is mandatory."
        
    if not is_edit:
        df = load_medicines()
        if med_id in df["Medicine ID"].values:
            return False, f"Medicine ID '{med_id}' already exists in inventory."
            
    # 3. Numeric Fields (Quantity, Unit Price)
    try:
        qty = int(data.get("Quantity", 0))
        if qty < 0:
            return False, "Quantity cannot be negative."
    except (ValueError, TypeError):
        return False, "Quantity must be an integer."
        
    try:
        price = float(data.get("Unit Price", 0.0))
        if price < 0:
            return False, "Unit Price cannot be negative."
    except (ValueError, TypeError):
        return False, "Unit Price must be a number."
        
    # 4. Date Validations
    p_date_str = data.get("Purchase Date")
    e_date_str = data.get("Expiry Date")
    
    try:
        if isinstance(p_date_str, str):
            p_date = datetime.datetime.strptime(p_date_str, "%Y-%m-%d").date()
        else:
            p_date = p_date_str
            
        if isinstance(e_date_str, str):
            e_date = datetime.datetime.strptime(e_date_str, "%Y-%m-%d").date()
        else:
            e_date = e_date_str
            
        if e_date <= p_date:
            return False, "Expiry Date must be after the Purchase Date."
    except Exception:
        return False, "Invalid date format. Dates must be in YYYY-MM-DD format."
        
    # 5. Other fields mandatory
    if not data.get("Category", "").strip():
        return False, "Please select a Category."
    if not data.get("Manufacturer", "").strip():
        return False, "Manufacturer is mandatory."
    if not data.get("Batch Number", "").strip():
        return False, "Batch Number is mandatory."
    if not data.get("Supplier Name", "").strip():
        return False, "Please select a Supplier Name."
        
    return True, None

def validate_sale(med_qty_available: int, qty_to_sell: int, price: float) -> Tuple[bool, Optional[str]]:
    """
    Validates a sales invoice transaction.
    """
    if qty_to_sell <= 0:
        return False, "Quantity sold must be greater than zero."
        
    if qty_to_sell > med_qty_available:
        return False, f"Insufficient stock. Available quantity is {med_qty_available}."
        
    if price < 0:
        return False, "Selling price cannot be negative."
        
    return True, None
