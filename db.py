import streamlit as st
from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from datetime import date, datetime
import hashlib

@st.cache_resource
def _get_client_from_secrets(url: str, key: str) -> Optional[Client]:
    try:
        url = url.rstrip('/')
        if url.endswith('/rest/v1'):
            url = url[:-len('/rest/v1')]
        return create_client(url, key)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        return None

def get_supabase_client() -> Optional[Client]:
    """
    Initialize Supabase client using Streamlit secrets.
    Returns None if secrets are not configured or invalid.
    """
    try:
        if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
            if url and key:
                return _get_client_from_secrets(url, key)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
    return None

def is_db_connected() -> bool:
    """Check if Supabase client is configured and operational."""
    client = get_supabase_client()
    return client is not None

def hash_password(password: str) -> str:
    """Generate SHA-256 hash for user password."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ==========================================
# USER AUTHENTICATION & REGISTRATION
# ==========================================

def create_user_account(username: str, email: str, password: str) -> Dict[str, Any]:
    """Create a new user account using Supabase Auth and database users table."""
    client = get_supabase_client()
    if not client:
        return {"success": False, "message": "Database is not connected. Check credentials."}
    
    username = username.strip()
    email = email.strip().lower()
    
    if not username or not email or not password:
        return {"success": False, "message": "Username, Email and Password are required."}
    
    # 1. Register user via Supabase Auth API
    try:
        client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"username": username}
            }
        })
    except Exception as e:
        print(f"Supabase Auth signup notice: {e}")

    # 2. Register/Insert into users table
    pwd_hash = hash_password(password)
    user_data = {
        "username": username,
        "email": email,
        "password_hash": pwd_hash
    }
    
    try:
        client.table("users").insert(user_data).execute()
        return {
            "success": True,
            "message": f"Account created successfully for {username}!",
            "user": {"username": username, "email": email}
        }
    except Exception as e:
        err_str = str(e)
        if "duplicate" in err_str.lower() or "unique" in err_str.lower() or "23505" in err_str:
            return {"success": False, "message": "Username or Email already registered. Please login."}
        elif "PGRST205" in err_str or "schema cache" in err_str.lower() or "users" in err_str.lower():
            return {
                "success": True,
                "message": f"Account registered for {username}! (Note: Run schema.sql in Supabase SQL Editor to enable user table)",
                "user": {"username": username, "email": email}
            }
        return {"success": False, "message": f"Failed to create account: {e}"}

def authenticate_user(email_or_username: str, password: str) -> Dict[str, Any]:
    """Authenticate user with email/username and password."""
    client = get_supabase_client()
    if not client:
        return {"success": False, "message": "Database not connected.", "user": None}
    
    identifier = email_or_username.strip()
    pwd_hash = hash_password(password)
    
    # 1. Try Supabase Auth API login if email format
    if "@" in identifier:
        try:
            auth_res = client.auth.sign_in_with_password({"email": identifier.lower(), "password": password})
            if auth_res and auth_res.user:
                meta = auth_res.user.user_metadata or {}
                uname = meta.get("username", identifier.split("@")[0])
                return {
                    "success": True,
                    "message": f"Welcome back, {uname}!",
                    "user": {"username": uname, "email": auth_res.user.email}
                }
        except Exception as e:
            print(f"Supabase Auth signin error: {e}")
            
    # 2. Try users table query
    try:
        query = client.table("users").select("*")
        if "@" in identifier:
            query = query.eq("email", identifier.lower())
        else:
            query = query.eq("username", identifier)
            
        res = query.execute()
        if res.data:
            matched_user = res.data[0]
            if matched_user.get("password_hash") == pwd_hash:
                return {
                    "success": True,
                    "message": f"Welcome back, {matched_user['username']}!",
                    "user": {"username": matched_user["username"], "email": matched_user["email"]}
                }
            else:
                return {"success": False, "message": "Incorrect password. Please try again.", "user": None}
        else:
            return {"success": False, "message": "User not found. Please check username/email or sign up.", "user": None}
    except Exception as e:
        err_str = str(e)
        if "PGRST205" in err_str or "users" in err_str.lower():
            return {"success": False, "message": "Users table missing. Please run schema.sql in Supabase SQL editor.", "user": None}
        return {"success": False, "message": f"Login failed: {e}", "user": None}

# ==========================================
# FOOD MASTER CRUD OPERATIONS
# ==========================================

def fetch_food_master() -> List[Dict[str, Any]]:
    """Fetch all food items from food_master."""
    client = get_supabase_client()
    if not client:
        return []
    try:
        response = client.table("food_master").select("*").order("food_name").execute()
        return response.data or []
    except Exception as e:
        st.cache_resource.clear()
        st.error(f"Database error fetching food master list: {e}")
        return []

def add_food_master_item(food_name: str, calories: float, protein: float, carbs: float, fat: float) -> bool:
    """Insert a new food item into food_master."""
    client = get_supabase_client()
    if not client:
        return False
    try:
        data = {
            "food_name": food_name.strip(),
            "calories": float(calories),
            "protein": float(protein),
            "carbs": float(carbs),
            "fat": float(fat)
        }
        client.table("food_master").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Failed to add food to master list: {e}")
        return False

def delete_food_master_item(item_id: int) -> bool:
    """Delete a food item from food_master by ID."""
    client = get_supabase_client()
    if not client:
        return False
    try:
        client.table("food_master").delete().eq("id", item_id).execute()
        return True
    except Exception as e:
        st.error(f"Failed to delete food master item: {e}")
        return False

# ==========================================
# FOOD LOG CRUD OPERATIONS
# ==========================================

def fetch_food_logs(log_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch food logs by specific date or date range."""
    client = get_supabase_client()
    if not client:
        return []
    try:
        query = client.table("food_log").select("*")
        if log_date:
            query = query.eq("log_date", str(log_date))
        if start_date and end_date:
            query = query.gte("log_date", str(start_date)).lte("log_date", str(end_date))
        
        response = query.order("id", desc=True).execute()
        return response.data or []
    except Exception as e:
        st.error(f"Database error fetching food logs: {e}")
        return []

def add_food_log_entry(log_date: str, food_name: str, quantity: float, calories: float, protein: float, carbs: float, fat: float) -> bool:
    """Insert a food log entry into food_log."""
    client = get_supabase_client()
    if not client:
        return False
    try:
        data = {
            "log_date": str(log_date),
            "food_name": food_name,
            "quantity": float(quantity),
            "calories": float(calories),
            "protein": float(protein),
            "carbs": float(carbs),
            "fat": float(fat)
        }
        client.table("food_log").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Failed to insert food log: {e}")
        return False

def delete_food_log_entry(log_id: int) -> bool:
    """Delete a food log entry by ID."""
    client = get_supabase_client()
    if not client:
        return False
    try:
        client.table("food_log").delete().eq("id", log_id).execute()
        return True
    except Exception as e:
        st.error(f"Failed to delete food log: {e}")
        return False

# ==========================================
# EXERCISE LOG CRUD OPERATIONS
# ==========================================

def fetch_exercise_logs(log_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch exercise logs by specific date or date range."""
    client = get_supabase_client()
    if not client:
        return []
    try:
        query = client.table("exercise_log").select("*")
        if log_date:
            query = query.eq("log_date", str(log_date))
        if start_date and end_date:
            query = query.gte("log_date", str(start_date)).lte("log_date", str(end_date))
        
        response = query.order("id", desc=True).execute()
        return response.data or []
    except Exception as e:
        st.error(f"Database error fetching exercise logs: {e}")
        return []

def add_exercise_log_entry(log_date: str, exercise_name: str, duration_minutes: float, calories_burned: float) -> bool:
    """Insert an exercise log entry into exercise_log."""
    client = get_supabase_client()
    if not client:
        return False
    try:
        data = {
            "log_date": str(log_date),
            "exercise_name": exercise_name,
            "duration_minutes": float(duration_minutes),
            "calories_burned": float(calories_burned)
        }
        client.table("exercise_log").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Failed to insert exercise log: {e}")
        return False

def delete_exercise_log_entry(log_id: int) -> bool:
    """Delete an exercise log entry by ID."""
    client = get_supabase_client()
    if not client:
        return False
    try:
        client.table("exercise_log").delete().eq("id", log_id).execute()
        return True
    except Exception as e:
        st.error(f"Failed to delete exercise log: {e}")
        return False

# ==========================================
# WEIGHT LOG CRUD OPERATIONS
# ==========================================

def fetch_weight_logs(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch weight logs sorted by date."""
    client = get_supabase_client()
    if not client:
        return []
    try:
        query = client.table("weight_log").select("*")
        if start_date and end_date:
            query = query.gte("log_date", str(start_date)).lte("log_date", str(end_date))
        
        response = query.order("log_date", desc=False).execute()
        return response.data or []
    except Exception as e:
        st.error(f"Database error fetching weight logs: {e}")
        return []

def add_or_update_weight_log(log_date: str, weight_kg: float) -> bool:
    """Insert or update weight log entry for a given date."""
    client = get_supabase_client()
    if not client:
        return False
    try:
        data = {
            "log_date": str(log_date),
            "weight_kg": float(weight_kg)
        }
        client.table("weight_log").upsert(data, on_conflict="log_date").execute()
        return True
    except Exception as e:
        st.error(f"Failed to log weight: {e}")
        return False

def delete_weight_log_entry(log_id: int) -> bool:
    """Delete a weight log entry by ID."""
    client = get_supabase_client()
    if not client:
        return False
    try:
        client.table("weight_log").delete().eq("id", log_id).execute()
        return True
    except Exception as e:
        st.error(f"Failed to delete weight log: {e}")
        return False
