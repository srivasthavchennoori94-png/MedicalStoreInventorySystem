import datetime
import pandas as pd
from typing import Dict, Any, Tuple
from utils.file_handler import load_medicines, load_sales

def get_kpi_metrics() -> Dict[str, Any]:
    """Calculates all key statistics for dashboard visual cards."""
    df_meds = load_medicines()
    df_sales = load_sales()
    
    today = datetime.date(2026, 7, 10) # Set to the user's current date
    today_str = today.strftime("%Y-%m-%d")
    
    # 1. Total Medicines & Categories
    total_meds = len(df_meds) if not df_meds.empty else 0
    total_categories = df_meds["Category"].nunique() if not df_meds.empty else 0
    total_stock = df_meds["Quantity"].sum() if not df_meds.empty else 0
    
    # 2. Low Stock Count
    low_stock = len(df_meds[df_meds["Quantity"] < 20]) if not df_meds.empty else 0
    
    # 3. Expiry Calculations
    expired = 0
    expiring_soon = 0
    
    if not df_meds.empty:
        for idx, row in df_meds.iterrows():
            try:
                exp_date = datetime.datetime.strptime(str(row["Expiry Date"]), "%Y-%m-%d").date()
                if exp_date < today:
                    expired += 1
                elif 0 <= (exp_date - today).days <= 30:
                    expiring_soon += 1
            except Exception:
                pass
                
    # 4. Sales and Revenue
    today_sales_count = 0
    today_revenue = 0.0
    total_revenue = 0.0
    
    if not df_sales.empty:
        total_revenue = df_sales["Total Amount"].sum()
        
        # Today's sales
        df_today = df_sales[df_sales["Sale Date"] == today_str]
        today_sales_count = len(df_today)
        today_revenue = df_today["Total Amount"].sum()
        
    return {
        "total_medicines": total_meds,
        "total_categories": total_categories,
        "total_stock": total_stock,
        "low_stock": low_stock,
        "expired": expired,
        "expiring_soon": expiring_soon,
        "today_sales": today_sales_count,
        "today_revenue": today_revenue,
        "total_revenue": total_revenue
    }

def get_recent_medicines(limit: int = 5) -> pd.DataFrame:
    """Returns the most recently added medicines."""
    df = load_medicines()
    if df.empty:
        return df
        
    # Reverse rows so that the latest appended records appear first
    df_sorted = df.iloc[::-1]
    return df_sorted.head(limit)[["Medicine ID", "Medicine Name", "Category", "Quantity", "Unit Price", "Purchase Date"]]

def get_top_selling_medicines(limit: int = 5) -> pd.DataFrame:
    """Calculates top selling medicines based on quantities sold."""
    df_sales = load_sales()
    if df_sales.empty:
        return pd.DataFrame(columns=["Medicine Name", "Quantity Sold", "Revenue"])
        
    summary = df_sales.groupby("Medicine Name").agg(
        Quantity_Sold=("Quantity Sold", "sum"),
        Revenue=("Total Amount", "sum")
    ).reset_index()
    
    summary = summary.sort_values(by="Quantity_Sold", ascending=False)
    return summary.head(limit)
