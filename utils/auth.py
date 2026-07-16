import os
import hashlib
import pandas as pd
import datetime
from typing import Tuple

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
USERS_EXCEL = os.path.join(DATA_DIR, "users.xlsx")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")

def ensure_data_dir():
    """Ensure the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_users_file():
    """Initializes the users storage file (Excel or CSV fallback) if it does not exist."""
    ensure_data_dir()
    
    # Check if either users.xlsx or users.csv exists
    if not os.path.exists(USERS_EXCEL) and not os.path.exists(USERS_CSV):
        # Create empty DataFrame
        df = pd.DataFrame(columns=["Username", "PasswordHash", "Email", "SignupDate"])
        
        # Try to save to Excel first
        try:
            df.to_excel(USERS_EXCEL, index=False)
        except Exception:
            # Fallback to CSV
            try:
                df.to_csv(USERS_CSV, index=False)
            except Exception:
                pass

def load_users() -> pd.DataFrame:
    """Loads users from Excel or CSV fallback."""
    init_users_file()
    
    # Try Excel first
    if os.path.exists(USERS_EXCEL):
        try:
            return pd.read_excel(USERS_EXCEL)
        except Exception:
            # Fallback to CSV if excel read fails
            if os.path.exists(USERS_CSV):
                try:
                    return pd.read_csv(USERS_CSV)
                except Exception:
                    pass
    
    # If Excel doesn't exist or failed, try CSV
    if os.path.exists(USERS_CSV):
        try:
            return pd.read_csv(USERS_CSV)
        except Exception:
            pass
            
    # Return empty DataFrame if both failed or don't exist
    return pd.DataFrame(columns=["Username", "PasswordHash", "Email", "SignupDate"])

def save_users(df: pd.DataFrame) -> bool:
    """Saves users DataFrame to Excel and CSV fallback."""
    ensure_data_dir()
    
    excel_success = False
    # Attempt to write to Excel
    try:
        df.to_excel(USERS_EXCEL, index=False)
        excel_success = True
    except Exception:
        # Fallback to CSV
        pass
        
    # Also write to CSV for fallback/redundancy
    try:
        df.to_csv(USERS_CSV, index=False)
        return True
    except Exception:
        return excel_success

def register_user(username: str, password: str, email: str) -> Tuple[bool, str]:
    """Registers a new user. Returns (Success, Message)."""
    username = username.strip()
    email = email.strip()
    
    if not username or not password or not email:
        return False, "All fields are required."
        
    df = load_users()
    
    # Check if username already exists (case-insensitive check)
    if not df.empty and username.lower() in df["Username"].astype(str).str.lower().values:
        return False, f"Username '{username}' is already taken."
        
    # Hash the password
    password_hash = hash_password(password)
    signup_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_user = pd.DataFrame([{
        "Username": username,
        "PasswordHash": password_hash,
        "Email": email,
        "SignupDate": signup_date
    }])
    
    df = pd.concat([df, new_user], ignore_index=True)
    if save_users(df):
        return True, "Registration successful! You can now log in."
    else:
        return False, "Error saving user credentials. Please try again."

def authenticate_user(username: str, password: str) -> bool:
    """Checks if the credentials are valid."""
    username = username.strip()
    if not username or not password:
        return False
        
    df = load_users()
    if df.empty:
        return False
        
    # Find matching username
    user_row = df[df["Username"].astype(str).str.lower() == username.lower()]
    if user_row.empty:
        return False
        
    # Check password hash
    stored_hash = user_row.iloc[0]["PasswordHash"]
    return stored_hash == hash_password(password)
