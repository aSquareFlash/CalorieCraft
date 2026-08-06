import streamlit as st
# App initialized

import pandas as pd
import plotly.express as px
import plotly.graph_objects as gg
import plotly.graph_objects as go
from datetime import date, datetime, timedelta

# Import database module
import db

# Set Streamlit page configuration
st.set_page_config(
    page_title="CalorieCraft | Nutrition & Exercise Tracker",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injected Custom CSS for sleek aesthetics
st.markdown("""
    <style>
    /* Main Background & Font Styling */
    .main {
        background-color: #0F172A;
    }
    
    /* Card Container Styling */
    .custom-card {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Header Aesthetics */
    .app-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 5px;
    }
    
    .app-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }
    
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 15px 20px;
        border-radius: 10px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: #10B981;
        transform: translateY(-2px);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    /* Button Styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    
    /* Database Warning Banner */
    .db-alert {
        background-color: #451A03;
        color: #FDBA74;
        border: 1px solid #9A3412;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    /* Modern Sidebar Base (Image 1 & Image 2 style) */
    section[data-testid="stSidebar"] {
        background-color: #0D1322 !important;
        border-right: 1px solid #1E293B !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* COLLAPSED MINI RAIL OVERRIDE (Image 2 style) */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0 !important;
        width: 78px !important;
        min-width: 78px !important;
        max-width: 78px !important;
        transform: none !important;
    }

    /* Main content margin adjustment when sidebar is collapsed mini rail */
    section[data-testid="stSidebar"][aria-expanded="false"] + section.main {
        margin-left: 78px !important;
    }

    /* Hide text elements in collapsed state */
    section[data-testid="stSidebar"][aria-expanded="false"] .sidebar-text-expand,
    section[data-testid="stSidebar"][aria-expanded="false"] .sidebar-profile-info {
        display: none !important;
    }

    /* Section Header and Divider in Collapsed State */
    section[data-testid="stSidebar"][aria-expanded="false"] .sidebar-section-title {
        display: none !important;
    }
    section[data-testid="stSidebar"][aria-expanded="false"] .sidebar-section-divider {
        display: block !important;
        border: 0 !important;
        border-top: 1px solid #1E293B !important;
        margin: 16px auto !important;
        width: 36px !important;
    }

    /* Sidebar st.button navigation styling (Image 1 & Image 2 style) */
    div[data-testid="stSidebar"] div.stButton > button {
        border-radius: 10px !important;
        padding: 12px 14px !important;
        margin-bottom: 4px !important;
        font-size: 0.98rem !important;
        font-weight: 600 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
        border: 1px solid transparent !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Inactive Sidebar Buttons (Secondary) */
    div[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-secondary"] {
        background-color: transparent !important;
        color: #94A3B8 !important;
        border-color: transparent !important;
    }

    div[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #F8FAFC !important;
    }

    /* Active Sidebar Button (Primary - Solid White Card like Image 1 & 2) */
    div[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"] {
        background-color: #FFFFFF !important;
        color: #0D1322 !important;
        font-weight: 700 !important;
        border-color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
    }

    div[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        background-color: #F8FAFC !important;
        color: #0D1322 !important;
    }

    div[data-testid="stSidebar"] div.stButton > button p {
        color: inherit !important;
        margin: 0 !important;
        font-weight: inherit !important;
        font-size: inherit !important;
    }

    /* COLLAPSED MINI RAIL BUTTON ADJUSTMENTS (Image 2 style) */
    section[data-testid="stSidebar"][aria-expanded="false"] div.stButton > button {
        padding: 10px 0 !important;
        justify-content: center !important;
        width: 44px !important;
        height: 44px !important;
        margin: 0 auto 6px auto !important;
        border-radius: 10px !important;
    }

    section[data-testid="stSidebar"][aria-expanded="false"] div.stButton > button p {
        width: 1.4em !important;
        overflow: hidden !important;
        display: inline-block !important;
        text-align: center !important;
        font-size: 1.25rem !important;
        white-space: nowrap !important;
    }
    </style>
""", unsafe_allow_html=True)

# Helper exercise MET calories burn dictionary per minute (at ~70kg average weight)
EXERCISE_MET_CALORIES_PER_MIN = {
    "Running (Moderate pace)": 10.0,
    "Running (Fast pace)": 13.5,
    "Walking (Brisk pace)": 4.5,
    "Weight Training / Gym": 6.0,
    "Cycling (Moderate)": 8.0,
    "Swimming (Laps)": 9.5,
    "HIIT / Circuit Training": 11.0,
    "Yoga / Stretching": 3.5,
    "Jump Rope": 12.0,
    "Rowing Machine": 8.5,
    "Basketball / Football": 9.0
}

# Initialize session state page navigation & user authentication
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Daily Logger"

if "user" not in st.session_state:
    st.session_state["user"] = None

page = st.session_state["current_page"]
current_user = st.session_state["user"]

# Ensure Supabase database connection status check
db_ready = db.is_db_connected()

# Sidebar Navigation Header & Menu (Pure Buttons driven by session state)
with st.sidebar:
    # 1. Brand Logo Header
    st.markdown("""
        <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 22px; padding: 4px 0;'>
            <div style='display: flex; align-items: center; gap: 12px; margin: 0 auto;'>
                <div style='background: linear-gradient(135deg, #6366F1, #8B5CF6); border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; color: #FFFFFF; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35); flex-shrink: 0;'>
                    🥗
                </div>
                <div class='sidebar-text-expand'>
                    <h3 style='color: #F8FAFC; font-weight: 800; margin: 0; font-size: 1.15rem; line-height: 1.2;'>CalorieCraft</h3>
                    <p style='color: #64748B; font-size: 0.76rem; margin: 0; font-weight: 500;'>Nutrition & Fitness</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. Section Header Label
    st.markdown("<p class='sidebar-section-title' style='color: #64748B; font-weight: 700; font-size: 0.72rem; letter-spacing: 1.5px; margin-bottom: 10px; padding-left: 6px;'>MAIN MENU</p>", unsafe_allow_html=True)
    st.markdown("<hr class='sidebar-section-divider' style='display: none;'>", unsafe_allow_html=True)
    
    # Render Pure st.button navigation items
    nav_items = [
        ("Daily Logger", "📝", "Daily Logger"),
        ("Daily Summary", "📊", "Daily Summary"),
        ("Analytics & History", "📈", "Analytics"),
        ("Manage Food Master", "🍎", "Manage Food")
    ]
    
    for label, icon, key_val in nav_items:
        is_active = (key_val in st.session_state["current_page"])
        btn_type = "primary" if is_active else "secondary"
        if st.button(f"{icon}   {label}", key=f"nav_btn_{key_val}", use_container_width=True, type=btn_type):
            st.session_state["current_page"] = key_val
            st.rerun()
    
    st.markdown("<hr style='border: 0; border-top: 1px solid #1E293B; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # 3. User Authentication / Profile Section
    user_initials = (current_user["username"][:2].upper()) if current_user and current_user.get("username") else "CU"
    display_name = current_user["username"] if current_user else "Guest User"
    display_email = current_user["email"] if current_user else ("● Connected" if db_ready else "○ Disconnected")
    
    st.markdown(f"""
        <div style='background: #FFFFFF; border-radius: 12px; padding: 10px 12px; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
            <div style='background: linear-gradient(135deg, #10B981, #059669); color: #F8FAFC; font-weight: 800; border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; flex-shrink: 0; margin: 0 auto;'>
                {user_initials}
            </div>
            <div class='sidebar-profile-info' style='flex: 1; overflow: hidden;'>
                <p style='color: #0B1120; font-weight: 800; font-size: 0.86rem; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{display_name}</p>
                <p style='color: {"#10B981" if current_user or db_ready else "#EF4444"}; font-size: 0.74rem; margin: 0; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>
                    {display_email}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    
    # User Account Expander / Modal
    if current_user:
        if st.button("🚪 Logout Account", key="btn_logout", use_container_width=True):
            st.session_state["user"] = None
            st.toast("Logged out successfully!", icon="👋")
            st.rerun()
    else:
        with st.expander("👤 User Account / Sign In", expanded=False):
            tab_signup, tab_login = st.tabs(["✨ Create Account", "🔑 Login"])
            
            with tab_signup:
                st.caption("Register a new CalorieCraft Account")
                new_uname = st.text_input("Username", key="reg_uname_input")
                new_email = st.text_input("Email ID", key="reg_email_input")
                new_pwd = st.text_input("Password", type="password", key="reg_pwd_input")
                
                if st.button("✨ Create Account", key="btn_do_register", use_container_width=True, type="primary"):
                    if not new_uname.strip() or not new_email.strip() or not new_pwd.strip():
                        st.error("Please fill in Username, Email, and Password.")
                    elif "@" not in new_email:
                        st.error("Please enter a valid Email ID.")
                    elif len(new_pwd) < 4:
                        st.error("Password must be at least 4 characters long.")
                    else:
                        reg_res = db.create_user_account(new_uname, new_email, new_pwd)
                        if reg_res["success"]:
                            st.session_state["user"] = reg_res["user"]
                            st.toast(reg_res["message"], icon="🎉")
                            st.rerun()
                        else:
                            st.error(reg_res["message"])
                            
            with tab_login:
                st.caption("Log in to your account")
                login_id = st.text_input("Username or Email", key="login_id_input")
                login_pwd = st.text_input("Password", type="password", key="login_pwd_input")
                
                if st.button("🔑 Sign In", key="btn_do_login", use_container_width=True, type="primary"):
                    if not login_id.strip() or not login_pwd.strip():
                        st.error("Please enter Username/Email and Password.")
                    else:
                        login_res = db.authenticate_user(login_id, login_pwd)
                        if login_res["success"]:
                            st.session_state["user"] = login_res["user"]
                            st.toast(login_res["message"], icon="🔑")
                            st.rerun()
                        else:
                            st.error(login_res["message"])
                            
    if not db_ready:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.error("⚠️ Supabase Credentials Not Configured")
        st.info("Please set `SUPABASE_URL` and `SUPABASE_KEY` in `.streamlit/secrets.toml`.")
        with st.expander("🛠️ View Database Setup Script"):
            st.code(open("schema.sql").read() if True else "", language="sql")

# Main Header Display
st.markdown("<h1 class='app-header'>🥗 CalorieCraft Tracker</h1>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>Track your macros, stay on top of workouts, and monitor weight goals with Supabase.</div>", unsafe_allow_html=True)

if not db_ready:
    st.markdown("""
        <div class='db-alert'>
            <strong>⚠️ Database Connection Notice:</strong><br/>
            Supabase is not connected yet. Please add your credentials to <code>.streamlit/secrets.toml</code> to enable data saving.
            <br/><br/>
            <strong>Example <code>.streamlit/secrets.toml</code>:</strong>
            <pre style="color: #FDBA74; margin-top: 5px;">
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
            </pre>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 1: DAILY LOGGER
# ==============================================================================
if "Daily Logger" in page:
    st.subheader("📝 Daily Activity Logger")
    
    selected_date = st.date_input("Select Date for Logging", value=date.today())
    date_str = selected_date.strftime("%Y-%m-%d")
    
    col1, col2 = st.columns(2, gap="medium")
    
    # ------------------ FOOD LOGGING SECTION ------------------
    with col1:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 🍲 Log Food Intake")
        
        # Fetch food master list from Supabase
        food_master_items = db.fetch_food_master()
        
        if food_master_items:
            food_options = {item["food_name"]: item for item in food_master_items}
            selected_food_name = st.selectbox("Select Food Item", options=list(food_options.keys()))
            quantity = st.number_input("Quantity / Servings", min_value=0.1, max_value=50.0, value=1.0, step=0.5)
            
            # Retrieve macros for selected food
            food_data = food_options[selected_food_name]
            calc_calories = round(food_data["calories"] * quantity, 1)
            calc_protein = round(food_data["protein"] * quantity, 1)
            calc_carbs = round(food_data["carbs"] * quantity, 1)
            calc_fat = round(food_data["fat"] * quantity, 1)
            
            # Display Macro Preview
            st.markdown("##### Calculated Preview:")
            p_col1, p_col2, p_col3, p_col4 = st.columns(4)
            p_col1.metric("Calories", f"{calc_calories} kcal")
            p_col2.metric("Protein", f"{calc_protein}g")
            p_col3.metric("Carbs", f"{calc_carbs}g")
            p_col4.metric("Fat", f"{calc_fat}g")
            
            if st.button("➕ Log Food Entry", use_container_width=True, type="primary"):
                if db_ready:
                    success = db.add_food_log_entry(
                        log_date=date_str,
                        food_name=selected_food_name,
                        quantity=quantity,
                        calories=calc_calories,
                        protein=calc_protein,
                        carbs=calc_carbs,
                        fat=calc_fat
                    )
                    if success:
                        st.toast(f"Logged {quantity}x {selected_food_name} for {date_str}!", icon="✅")
                        st.rerun()
                else:
                    st.error("Database connection missing. Unable to save log.")
        else:
            st.info("No items in Food Master List yet. Add items in 'Manage Food Master List' or check database connection.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ EXERCISE LOGGING SECTION ------------------
    with col2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 🏃‍♂️ Log Exercise & Workout")
        
        exercise_type = st.selectbox("Exercise Type", options=list(EXERCISE_MET_CALORIES_PER_MIN.keys()))
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=30, step=5)
        
        # Calculate estimated burn
        estimated_burn_rate = EXERCISE_MET_CALORIES_PER_MIN.get(exercise_type, 7.0)
        calc_burned = round(estimated_burn_rate * duration, 1)
        
        st.markdown("##### Calculated Preview:")
        st.metric("Estimated Calories Burned", f"{calc_burned} kcal")
        
        if st.button("🔥 Log Exercise Entry", use_container_width=True, type="primary"):
            if db_ready:
                success = db.add_exercise_log_entry(
                    log_date=date_str,
                    exercise_name=exercise_type,
                    duration_minutes=duration,
                    calories_burned=calc_burned
                )
                if success:
                    st.toast(f"Logged {exercise_type} ({duration} mins) for {date_str}!", icon="✅")
                    st.rerun()
            else:
                st.error("Database connection missing. Unable to save log.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ WEIGHT LOGGING SECTION ------------------
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("### ⚖️ Log Body Weight")
    w_col1, w_col2 = st.columns([3, 1], gap="medium")
    with w_col1:
        weight_val = st.number_input("Weight (KG)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
    with w_col2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("⚖️ Save Weight", use_container_width=True):
            if db_ready:
                success = db.add_or_update_weight_log(log_date=date_str, weight_kg=weight_val)
                if success:
                    st.toast(f"Weight {weight_val} kg saved for {date_str}!", icon="✅")
                    st.rerun()
            else:
                st.error("Database connection missing. Unable to save weight.")
    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# PAGE 2: DAILY SUMMARY
# ==============================================================================
elif "Daily Summary" in page:
    st.subheader("📊 Daily Calorie & Nutrition Summary")
    
    summary_date = st.date_input("Select Date", value=date.today())
    summary_date_str = summary_date.strftime("%Y-%m-%d")
    
    # Fetch logs for selected date
    food_logs = db.fetch_food_logs(log_date=summary_date_str) if db_ready else []
    exercise_logs = db.fetch_exercise_logs(log_date=summary_date_str) if db_ready else []
    
    # Calculations
    total_calories_consumed = sum(item["calories"] for item in food_logs)
    total_protein = sum(item["protein"] for item in food_logs)
    total_carbs = sum(item["carbs"] for item in food_logs)
    total_fat = sum(item["fat"] for item in food_logs)
    total_calories_burned = sum(item["calories_burned"] for item in exercise_logs)
    net_calories = total_calories_consumed - total_calories_burned
    
    # Top Overview Metrics
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Calories Consumed", f"{total_calories_consumed:.0f} kcal")
    m2.metric("Calories Burned", f"{total_calories_burned:.0f} kcal")
    m3.metric("Net Balance", f"{net_calories:.0f} kcal", delta=f"{net_calories:.0f} kcal", delta_color="inverse")
    m4.metric("Protein", f"{total_protein:.1f} g")
    m5.metric("Carbs", f"{total_carbs:.1f} g")
    m6.metric("Fat", f"{total_fat:.1f} g")
    
    st.markdown("---")
    
    col_chart, col_details = st.columns([1, 1], gap="medium")
    
    # Donut Chart for Macro Breakdown
    with col_chart:
        st.markdown("### 🥗 Macro Breakdown")
        if total_protein > 0 or total_carbs > 0 or total_fat > 0:
            labels = ['Protein (g)', 'Carbs (g)', 'Fat (g)']
            values = [total_protein, total_carbs, total_fat]
            colors = ['#10B981', '#3B82F6', '#F59E0B']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.55,
                marker=dict(colors=colors),
                textinfo='label+percent',
                insidetextorientation='radial'
            )])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#F8FAFC'),
                showlegend=True,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No food logged for this date to generate macro distribution.")

    with col_details:
        st.markdown("### 📋 Quick Stats")
        st.write(f"- **Food Items Logged:** {len(food_logs)}")
        st.write(f"- **Exercises Logged:** {len(exercise_logs)}")
        if total_protein > 0 or total_carbs > 0 or total_fat > 0:
            protein_cal = total_protein * 4
            carbs_cal = total_carbs * 4
            fat_cal = total_fat * 9
            total_macro_cal = protein_cal + carbs_cal + fat_cal
            st.write(f"- **Protein Calories:** {protein_cal:.0f} kcal ({protein_cal/total_macro_cal*100:.1f}%)")
            st.write(f"- **Carbs Calories:** {carbs_cal:.0f} kcal ({carbs_cal/total_macro_cal*100:.1f}%)")
            st.write(f"- **Fat Calories:** {fat_cal:.0f} kcal ({fat_cal/total_macro_cal*100:.1f}%)")
            
    st.markdown("---")
    
    # Detailed Food Logs Table with Delete Option
    st.markdown("### 🍲 Food Entries for Selected Date")
    if food_logs:
        df_food = pd.DataFrame(food_logs)
        df_food_display = df_food[['id', 'food_name', 'quantity', 'calories', 'protein', 'carbs', 'fat']].copy()
        df_food_display.columns = ['ID', 'Food Item', 'Quantity', 'Calories (kcal)', 'Protein (g)', 'Carbs (g)', 'Fat (g)']
        
        # Display editable/deletable table
        st.dataframe(df_food_display, use_container_width=True)
        
        del_col1, del_col2 = st.columns([3, 1])
        with del_col1:
            food_to_delete = st.selectbox("Select Food Log to Delete", options=food_logs, format_func=lambda x: f"ID {x['id']}: {x['food_name']} ({x['quantity']}x)")
        with del_col2:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🗑️ Delete Selected Food Log", use_container_width=True):
                if db_ready and food_to_delete:
                    if db.delete_food_log_entry(food_to_delete['id']):
                        st.toast("Food log entry deleted!", icon="🗑️")
                        st.rerun()
    else:
        st.info("No food entries logged for this date.")

    # Detailed Exercise Logs Table with Delete Option
    st.markdown("### 🏃‍♂️ Exercise Entries for Selected Date")
    if exercise_logs:
        df_ex = pd.DataFrame(exercise_logs)
        df_ex_display = df_ex[['id', 'exercise_name', 'duration_minutes', 'calories_burned']].copy()
        df_ex_display.columns = ['ID', 'Exercise', 'Duration (mins)', 'Calories Burned (kcal)']
        
        st.dataframe(df_ex_display, use_container_width=True)
        
        del_ex1, del_ex2 = st.columns([3, 1])
        with del_ex1:
            ex_to_delete = st.selectbox("Select Exercise Log to Delete", options=exercise_logs, format_func=lambda x: f"ID {x['id']}: {x['exercise_name']} ({x['duration_minutes']} mins)")
        with del_ex2:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🗑️ Delete Selected Exercise Log", use_container_width=True):
                if db_ready and ex_to_delete:
                    if db.delete_exercise_log_entry(ex_to_delete['id']):
                        st.toast("Exercise log entry deleted!", icon="🗑️")
                        st.rerun()
    else:
        st.info("No exercise entries logged for this date.")


# ==============================================================================
# PAGE 3: ANALYTICS & HISTORY
# ==============================================================================
elif "Analytics" in page:
    st.subheader("📈 Historical Trends & Performance Analytics")
    
    # Filter selection
    filter_option = st.radio("Select Date Filter", options=["Last 7 Days", "Last 30 Days", "Custom Date Range"], horizontal=True)
    
    today_val = date.today()
    if filter_option == "Last 7 Days":
        start_d = today_val - timedelta(days=6)
        end_d = today_val
    elif filter_option == "Last 30 Days":
        start_d = today_val - timedelta(days=29)
        end_d = today_val
    else:
        col_sd, col_ed = st.columns(2)
        start_d = col_sd.date_input("Start Date", value=today_val - timedelta(days=14))
        end_d = col_ed.date_input("End Date", value=today_val)
        
    start_str = start_d.strftime("%Y-%m-%d")
    end_str = end_d.strftime("%Y-%m-%d")
    
    if db_ready:
        all_food_logs = db.fetch_food_logs(start_date=start_str, end_date=end_str)
        all_ex_logs = db.fetch_exercise_logs(start_date=start_str, end_date=end_str)
        all_weight_logs = db.fetch_weight_logs(start_date=start_str, end_date=end_str)
        
        # Build unified daily dataframe
        date_range = pd.date_range(start=start_d, end=end_d)
        df_daily = pd.DataFrame({'log_date': [d.strftime("%Y-%m-%d") for d in date_range]})
        
        # Process food
        if all_food_logs:
            df_f = pd.DataFrame(all_food_logs)
            df_f_agg = df_f.groupby('log_date')['calories'].sum().reset_index()
            df_daily = pd.merge(df_daily, df_f_agg, on='log_date', how='left').fillna({'calories': 0})
            df_daily.rename(columns={'calories': 'calories_consumed'}, inplace=True)
        else:
            df_daily['calories_consumed'] = 0.0
            
        # Process exercise
        if all_ex_logs:
            df_e = pd.DataFrame(all_ex_logs)
            df_e_agg = df_e.groupby('log_date')['calories_burned'].sum().reset_index()
            df_daily = pd.merge(df_daily, df_e_agg, on='log_date', how='left').fillna({'calories_burned': 0})
        else:
            df_daily['calories_burned'] = 0.0
            
        # Metrics summary
        avg_calories = df_daily['calories_consumed'].mean()
        total_burned = df_daily['calories_burned'].sum()
        
        # Weight calculations
        weight_change_str = "N/A"
        if all_weight_logs:
            df_w = pd.DataFrame(all_weight_logs)
            initial_weight = df_w.iloc[0]['weight_kg']
            final_weight = df_w.iloc[-1]['weight_kg']
            delta_weight = final_weight - initial_weight
            weight_change_str = f"{delta_weight:+.1f} kg"
            
        an_col1, an_col2, an_col3 = st.columns(3)
        an_col1.metric("Average Daily Calorie Intake", f"{avg_calories:.0f} kcal/day")
        an_col2.metric("Total Calories Burned in Period", f"{total_burned:.0f} kcal")
        an_col3.metric("Weight Change in Period", weight_change_str)
        
        st.markdown("---")
        
        # 1. Calorie Intake vs Burned Chart
        st.markdown("### 📊 Daily Calorie Intake vs. Burned")
        fig_cal = go.Figure()
        fig_cal.add_trace(go.Bar(
            x=df_daily['log_date'],
            y=df_daily['calories_consumed'],
            name='Calories Consumed',
            marker_color='#10B981'
        ))
        fig_cal.add_trace(go.Bar(
            x=df_daily['log_date'],
            y=df_daily['calories_burned'],
            name='Calories Burned',
            marker_color='#EF4444'
        ))
        fig_cal.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'),
            xaxis=dict(title='Date', gridcolor='#334155'),
            yaxis=dict(title='Calories (kcal)', gridcolor='#334155'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_cal, use_container_width=True)
        
        # 2. Weight Trend Chart
        st.markdown("### ⚖️ Body Weight Progress Trend")
        if all_weight_logs:
            df_w = pd.DataFrame(all_weight_logs)
            fig_w = px.line(
                df_w,
                x='log_date',
                y='weight_kg',
                markers=True,
                title="Weight Progression (KG)",
                labels={'log_date': 'Date', 'weight_kg': 'Weight (KG)'}
            )
            fig_w.update_traces(line_color='#3B82F6', line_width=3, marker_size=8)
            fig_w.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#F8FAFC'),
                xaxis=dict(gridcolor='#334155'),
                yaxis=dict(gridcolor='#334155')
            )
            st.plotly_chart(fig_w, use_container_width=True)
        else:
            st.info("No weight logs available for the selected period.")


# ==============================================================================
# PAGE 4: MANAGE FOOD MASTER LIST
# ==============================================================================
elif "Manage Food" in page:
    st.subheader("🍎 Manage Food Master Database")
    
    col_add, col_list = st.columns([1, 1.2], gap="large")
    
    with col_add:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### ➕ Add New Food Item")
        
        with st.form("add_food_form", clear_on_submit=True):
            new_name = st.text_input("Food Name & Serving Unit (e.g. Oats 100g, Banana 1 medium)")
            new_calories = st.number_input("Calories (kcal)", min_value=0.0, max_value=2000.0, value=100.0, step=5.0)
            new_protein = st.number_input("Protein (g)", min_value=0.0, max_value=200.0, value=0.0, step=0.5)
            new_carbs = st.number_input("Carbs (g)", min_value=0.0, max_value=200.0, value=0.0, step=0.5)
            new_fat = st.number_input("Fat (g)", min_value=0.0, max_value=200.0, value=0.0, step=0.5)
            
            submit_btn = st.form_submit_button("✨ Save to Food Master List", use_container_width=True, type="primary")
            
            if submit_btn:
                if not new_name.strip():
                    st.error("Please enter a valid food name.")
                elif db_ready:
                    success = db.add_food_master_item(
                        food_name=new_name,
                        calories=new_calories,
                        protein=new_protein,
                        carbs=new_carbs,
                        fat=new_fat
                    )
                    if success:
                        st.toast(f"Added {new_name} to Food Master database!", icon="🎉")
                        st.rerun()
                else:
                    st.error("Database connection missing. Unable to save item.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_list:
        st.markdown("### 📜 Existing Food Master Items")
        master_items = db.fetch_food_master() if db_ready else []
        
        if master_items:
            df_master = pd.DataFrame(master_items)
            df_master_display = df_master[['id', 'food_name', 'calories', 'protein', 'carbs', 'fat']].copy()
            df_master_display.columns = ['ID', 'Food Name', 'Calories (kcal)', 'Protein (g)', 'Carbs (g)', 'Fat (g)']
            
            search_query = st.text_input("🔍 Search Food Master Items", "")
            if search_query:
                df_master_display = df_master_display[df_master_display['Food Name'].str.contains(search_query, case=False)]
                
            st.dataframe(df_master_display, use_container_width=True, height=350)
            
            # Deletion block
            st.markdown("##### 🗑️ Delete Item from Master List")
            del_m1, del_m2 = st.columns([3, 1])
            with del_m1:
                item_to_delete = st.selectbox(
                    "Select item to delete",
                    options=master_items,
                    format_func=lambda x: f"ID {x['id']}: {x['food_name']}"
                )
            with del_m2:
                st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                if st.button("Delete Item", use_container_width=True):
                    if db_ready and item_to_delete:
                        if db.delete_food_master_item(item_to_delete['id']):
                            st.toast(f"Deleted {item_to_delete['food_name']}!", icon="🗑️")
                            st.rerun()
        else:
            st.info("No items found in food_master table.")
