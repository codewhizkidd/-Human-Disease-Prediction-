import streamlit as st
import pickle
import sqlite3
import bcrypt
from streamlit_option_menu import option_menu
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import geocoder
import requests
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# ===================== MODERN UI STYLING =====================
def inject_modern_css():
    st.markdown("""
    <style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Global Reset */
    * {
        font-family: 'Inter', 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #f3e7f5 0%, #e8d5f0 50%, #dcc3eb 100%);
        background-attachment: fixed;
    }
    
    /* Main Content Area */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin-top: 2rem;
    }
    
    /* Headers */
    h1 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        color: #2d3748;
        margin-top: 2rem;
    }
    
    /* Greeting Card */
    .greeting-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .greeting-card h2 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .greeting-card p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    
    /* Date/Time Card */
    .datetime-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        display: inline-block;
        margin-top: 1rem;
    }
    
    .datetime-card .date {
        font-size: 0.9rem;
        color: #718096;
        margin-bottom: 0.25rem;
    }
    
    .datetime-card .time {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Labels */
    .stNumberInput label, .stTextInput label, .stSelectbox label {
        font-weight: 600 !important;
        color: #2d3748 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.5rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Input Fields */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        color: #2d3748 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #718096;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    .metric-unit {
        font-size: 1rem;
        color: #a0aec0;
        margin-left: 0.5rem;
    }
    
    /* Status Indicators */
    .status-normal {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .status-abnormal {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    /* Alert Boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #667eea;
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Success/Info Messages */
    .custom-success {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
    }
    
    .custom-warning {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(237, 137, 54, 0.3);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f7fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Remove top padding */
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    /* Doctor Card */
    .doctor-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .doctor-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ===================== MODERN COMPONENTS =====================
def show_greeting_card(username):
    """Modern greeting card with date/time"""
    now = datetime.now()
    hour = now.hour
    
    if hour < 12:
        greeting = "Good Morning"
        emoji = "🌅"
    elif hour < 18:
        greeting = "Good Afternoon"
        emoji = "☀️"
    else:
        greeting = "Good Evening"
        emoji = "🌙"
    
    st.markdown(f"""
    <div class="greeting-card">
        <h2>{greeting}, {username}! {emoji}</h2>
        <p>Happiness is nothing more than good health</p>
        <div class="datetime-card">
            <div class="date">📅 {now.strftime('%A, %B %d, %Y')}</div>
            <div class="time">🕐 {now.strftime('%I:%M %p')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_metric_card(label, value, unit="", status="normal"):
    """Modern metric card with status indicator"""
    status_class = "status-normal" if status == "normal" else "status-abnormal"
    status_text = "✓ Normal" if status == "normal" else "⚠ Abnormal"
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div>
            <span class="metric-value">{value}</span>
            <span class="metric-unit">{unit}</span>
        </div>
        <div style="margin-top: 0.75rem;">
            <span class="{status_class}">{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_modern_result(result, prediction_type):
    """Modern result display"""
    if "No" in result or "Non" in result:
        st.markdown(f"""
        <div class="custom-success">
            <h3 style="margin: 0; color: white;">✓ Great News!</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">{result}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="custom-warning">
            <h3 style="margin: 0; color: white;">⚠ Attention Required</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">{result}</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Please consult with a healthcare professional</p>
        </div>
        """, unsafe_allow_html=True)

def show_modern_doctors(prediction_label):
    """Modern doctor recommendation display"""
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.markdown("### 🏥 Recommended Specialists")
    
    user_lat, user_lng = 19.0760, 72.8777
    radius = 5000
    api_key_env = os.environ.get("GOOGLE_API_KEY")
    
    if "heart" in prediction_label.lower():
        doctor_type = "cardiologist"
    elif "kidney" in prediction_label.lower():
        doctor_type = "nephrologist"
    elif "diabet" in prediction_label.lower():
        doctor_type = "diabetologist"
    else:
        doctor_type = "doctor"
    
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={user_lat},{user_lng}&radius={radius}"
        f"&keyword={doctor_type}&key={api_key_env}"
    )
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            for place in data["results"][:3]:
                name = place["name"]
                address = place.get("vicinity", "Address not available")
                rating = place.get("rating", "N/A")
                lat = place["geometry"]["location"]["lat"]
                lng = place["geometry"]["location"]["lng"]
                maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
                
                st.markdown(f"""
                <div class="doctor-card">
                    <h4 style="margin: 0 0 0.5rem 0; color: #2d3748;">🩺 {name}</h4>
                    <p style="margin: 0; color: #718096; font-size: 0.9rem;">📍 {address}</p>
                    <p style="margin: 0.5rem 0; color: #718096; font-size: 0.9rem;">⭐ Rating: {rating}</p>
                    <a href="{maps_link}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600;">
                        🗺️ View on Google Maps →
                    </a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No nearby doctors found")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_modern_graph(values, labels, normal_ranges):
    """Modern health parameter visualization"""
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Health Parameters Activity Graph")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f7fafc')
    
    y_pos = np.arange(len(labels))
    colors = ['#48bb78' if normal_ranges[i][0] <= values[i] <= normal_ranges[i][1] 
              else '#f56565' for i in range(len(values))]
    
    bars = ax.barh(y_pos, values, color=colors, alpha=0.8, height=0.6)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10, fontweight='500')
    ax.invert_yaxis()
    ax.set_xlabel('Value', fontsize=11, fontweight='600')
    ax.set_title('Health Indicators Overview', fontsize=14, fontweight='700', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    max_value = max(values)
    max_range = max([high for low, high in normal_ranges])
    x_limit = max(max_value, max_range) * 1.4
    ax.set_xlim(0, x_limit)
    
    for i, (bar, (low, high)) in enumerate(zip(bars, normal_ranges)):
        ax.text(values[i] + (x_limit * 0.01), i, f"{values[i]}", 
                va='center', fontsize=10, fontweight='bold')
        
        range_text = f"Normal: {low}-{high}"
        color = '#f56565' if values[i] < normal_ranges[i][0] or values[i] > normal_ranges[i][1] else '#718096'
        ax.text(values[i] + (x_limit * 0.1), i, range_text, 
                va='center', fontsize=9, color=color, style='italic')
    
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== HIGHLIGHT ABNORMAL PARAMETERS =====================
def highlight_out_of_range(value, min_val, max_val, label):
    """Original function - kept for compatibility"""
    if value < min_val or value > max_val:
        status = "abnormal"
    else:
        status = "normal"
    return status

# ===================== DATABASE & AUTH SETUP =====================
st.set_page_config(
    page_title="Health Prediction Platform",
    layout="wide",
    page_icon="🩺"
)

inject_modern_css()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""

conn = sqlite3.connect('user_data.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS user_activity (
    username TEXT,
    activity_type TEXT,
    result TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    disease_type TEXT,
    result TEXT,
    input_json TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

def get_user(username):
    c.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    return c.fetchone()

def add_user(username, password_plaintext):
    hashed = bcrypt.hashpw(password_plaintext.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
    conn.commit()

def verify_password(password_plaintext, hashed_str):
    return bcrypt.checkpw(password_plaintext.encode('utf-8'), hashed_str.encode('utf-8'))

# Load models
diabetes_model = pickle.load(open('diabetes.pkl', 'rb'))
heart_disease_model = pickle.load(open('heart.pkl', 'rb'))
kidney_disease_model = pickle.load(open('kidney.pkl', 'rb'))

# ===================== SIDEBAR =====================
with st.sidebar:
    selected = option_menu(
        "Health Prediction",
        [
            "Home", "User Login", "Diabetes Prediction",
            "Heart Disease Prediction", "Kidney Disease Prediction",
            "Precautions", "About", "Contact Us", "User Graphs", "Exit"
        ],
        icons=['house', 'person', 'capsule', 'heart', 'droplet', 'shield-check', 'info-circle',
               'envelope', 'bar-chart', 'x-circle'],
        default_index=0
    )

def check_login():
    if not st.session_state.get('logged_in'):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 2rem; border-radius: 20px; color: white; text-align: center;
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);">
            <h2>🔒 Authentication Required</h2>
            <p style="font-size: 1.1rem; margin-top: 1rem;">Please login to access prediction tools</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# ===================== USER LOGIN =====================
if selected == "User Login":
    # Custom CSS for styling
    st.markdown("""
    <style>
    .login-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .login-header h1 {
        margin: 0;
        font-size: 2.5em;
        font-weight: bold;
    }
    .login-header p {
        margin: 10px 0 0 0;
        font-size: 1.1em;
        opacity: 0.9;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
                
    .success-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
        font-weight: bold;
        animation: slideIn 0.5s ease;
    }
    .error-message {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
        font-weight: bold;
        animation: shake 0.5s ease;
    }
    .warning-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
        font-weight: bold;
    }
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    .feature-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="login-header">
        <h1>🔐 Welcome Back!</h1>
        <p>Access your personalized health prediction dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div', unsafe_allow_html=True)
        st.markdown('<h3>🔒 Login to Your Account</h3>', unsafe_allow_html=True)
        
        login_user = st.text_input("Username", key="login_user", placeholder="Enter your username")
        login_pass = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Login", use_container_width=True, type="primary"):
                user = get_user(login_user)
                if user and verify_password(login_pass, user[1]):
                    st.markdown(f'<div class="success-message">✅ Welcome back, {login_user}!</div>', unsafe_allow_html=True)
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = login_user
                    
                    # log login
                    c.execute("INSERT INTO user_activity (username, activity_type, result) VALUES (?, ?, ?)",
                              (login_user, 'Login', 'Success'))
                    conn.commit()
                    st.balloons()
                elif user:
                    st.markdown('<div class="error-message">❌ Incorrect password. Please try again.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Username not found. Please signup first.</div>', unsafe_allow_html=True)
        
        with col_btn2:
            if st.session_state.get('logged_in'):
                if st.button("🚪 Logout", use_container_width=True):
                    # log logout
                    c.execute("INSERT INTO user_activity (username, activity_type, result) VALUES (?, ?, ?)",
                              (st.session_state['username'], 'Logout', 'Success'))
                    conn.commit()
                    st.session_state['logged_in'] = False
                    st.session_state['username'] = ""
                    st.markdown('<div class="success-message">👋 Logged out successfully!</div>', unsafe_allow_html=True)
        
        if st.session_state.get('logged_in'):
            st.markdown(f"""
            <div class="feature-box">
                <h4>👤 Logged in as: <strong>{st.session_state['username']}</strong></h4>
                <p>You now have access to all prediction tools!</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div>', unsafe_allow_html=True)
        st.markdown('<h3>✨ Create New Account</h3>', unsafe_allow_html=True)
        
        new_user = st.text_input("New Username", key="new_user", placeholder="Choose a unique username")
        new_pass = st.text_input("New Password", type="password", key="new_pass", placeholder="Create a strong password")
        
        if st.button("🎉 Create Account", use_container_width=True, type="primary"):
            if not new_user or not new_pass:
                st.markdown('<div class="warning-message">⚠️ Please enter both username and password.</div>', unsafe_allow_html=True)
            elif get_user(new_user):
                st.markdown('<div class="warning-message">⚠️ Username already exists. Choose another one.</div>', unsafe_allow_html=True)
            else:
                add_user(new_user, new_pass)
                c.execute("INSERT INTO user_activity (username, activity_type, result) VALUES (?, ?, ?)",
                          (new_user, 'Signup', 'Success'))
                conn.commit()
                st.markdown('<div class="success-message">🎊 Account created successfully! Please login now.</div>', unsafe_allow_html=True)
                st.snow()
        
        st.markdown("""
        <div class="feature-box">
            <h4>🌟 Why Create an Account?</h4>
            <div style="display: flex; justify-content: space-around; margin-top: 10px;">
                <span>✓ Save predictions</span>
                <span>✓ Track history</span>
            </div>
            <div style="display: flex; justify-content: space-around; margin-top: 8px;">
                <span>✓ Get insights</span>
                <span>✓ Secure data</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                border-radius: 15px; margin-top: 20px;">
        <h3>🥼 Advanced Health Prediction System</h3>
        <p>Our AI-powered platform provides predictions for multiple diseases including:</p>
        <p><strong>💉 Diabetes</strong> • <strong>❤️ Heart Disease</strong> • <strong>🩺 Kidney Disease</strong></p>
        <p style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
            Secure • Accurate • Confidential
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================== HOME =====================
if selected == "Home":
    st.title("🏠 HUMAN MULTIPLE DISEASE DETECTION SYSTEM")
    st.markdown("""
    <div style="font-family:'Roboto', sans-serif; line-height:1.6;">
    <h3>Welcome to the Multiple Disease Prediction System 🔬</h3>
    <p>This platform helps you detect Diabetes, Heart Disease, and Kidney Disease** early using advanced machine learning models trained on medical datasets.</p>
    
    <h4>✅ Supported Diseases:</h4>
    <ul>
        <li><b>Diabetes Detection:</b> Analyze your glucose, insulin, BMI, age, and other health parameters.</li>
        <li><b>Heart Disease Detection:</b> Evaluate heart risk based on blood pressure, cholesterol, ECG, exercise habits, and more.</li>
        <li><b>Kidney Disease Detection:</b> Assess kidney function using multiple biochemical and physical indicators.</li>
    </ul>

    <h4>💡 Features:</h4>
    <ul>
        <li>User Login & Signup for personalized tracking</li>
        <li>Prediction results stored in database</li>
        <li>Nearby doctors & health precautions suggestions</li>
        <li>User activity graphs and analytics</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ===================== DIABETES PREDICTION =====================
if selected == "Diabetes Prediction":
    check_login()
    
    show_greeting_card(st.session_state['username'])
    
    st.title("Diabetes Prediction")
    
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### Enter Health Parameters")
    
    col1, col2, col3 = st.columns(3)
    with col1: Pregnancies = st.number_input("Number of Pregnancies", min_value=0)
    with col2: Glucose = st.number_input("Glucose Level", min_value=0)
    with col3: BloodPressure = st.number_input("Blood Pressure", min_value=0)
    with col1: SkinThickness = st.number_input("Skin Thickness", min_value=0)
    with col2: Insulin = st.number_input("Insulin Level", min_value=0)
    with col3: BMI = st.number_input("BMI", min_value=0.0, format="%.2f")
    with col1: DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0, format="%.3f")
    with col2: Age = st.number_input("Age", min_value=0)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔍 Predict Diabetes", use_container_width=True):
        input_data = np.array([
            Pregnancies, Glucose, BloodPressure, SkinThickness,
            Insulin, BMI, DiabetesPedigreeFunction, Age
        ]).reshape(1, -1)
        poly = PolynomialFeatures(degree=2, include_bias=False)
        input_poly = poly.fit_transform(input_data)[:, :18]
        prediction = diabetes_model.predict(input_poly)
        result = "Diabetic" if prediction[0] == 1 else "Non-Diabetic"
        
        show_modern_result(f"The person is {result}", "diabetes")
        
        st.markdown("### Health Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status = "normal" if 70 <= Glucose <= 140 else "abnormal"
            show_metric_card("Glucose", Glucose, "mg/dL", status)
        with col2:
            status = "normal" if 80 <= BloodPressure <= 120 else "abnormal"
            show_metric_card("Blood Pressure", BloodPressure, "mmHg", status)
        with col3:
            status = "normal" if 18.5 <= BMI <= 24.9 else "abnormal"
            show_metric_card("BMI", BMI, "", status)
        with col4:
            status = "normal" if 18 <= Age <= 60 else "abnormal"
            show_metric_card("Age", Age, "years", status)
        
        show_modern_doctors("diabetes")
        
        show_modern_graph(
            [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age],
            ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", "Insulin", "BMI", "DPF", "Age"],
            [(0, 5), (70, 140), (60, 120), (10, 40), (15, 166), (18, 25), (0.1, 2.5), (20, 60)]
        )

# ===================== HEART DISEASE PREDICTION =====================
if selected == "Heart Disease Prediction":
    check_login()
    
    show_greeting_card(st.session_state['username'])
    
    st.title(" Heart Disease Prediction")
    
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### Enter Health Parameters")
    
    col1, col2, col3 = st.columns(3)
    with col1: age = st.number_input("Age", min_value=0)
    with col2: sex = st.number_input("Sex (1=male,0=female)", min_value=0, max_value=1)
    with col3: cp = st.number_input("Chest Pain Type (0-3)", min_value=0, max_value=3)
    with col1: trestbps = st.number_input("Resting Blood Pressure", min_value=0)
    with col2: chol = st.number_input("Serum Cholesterol", min_value=0)
    with col3: fbs = st.number_input("Fasting Blood Sugar >120 (1=yes,0=no)", min_value=0, max_value=1)
    with col1: restecg = st.number_input("Resting ECG (0-2)", min_value=0, max_value=2)
    with col2: thalach = st.number_input("Max Heart Rate Achieved", min_value=0)
    with col3: exang = st.number_input("Exercise Induced Angina (1=yes,0=no)", min_value=0, max_value=1)
    with col1: oldpeak = st.number_input("ST Depression", min_value=0.0, format="%.2f")
    with col2: slope = st.number_input("Slope of ST segment (1-3)", min_value=1, max_value=3)
    with col3: ca = st.number_input("Major Vessels (0-3)", min_value=0, max_value=3)
    with col1: thal = st.number_input("Thalassemia (1=normal,2=fixed,3=reversible)", min_value=1, max_value=3)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔍 Predict Heart Disease", use_container_width=True):
        input_data = [age, sex, cp, trestbps, chol, fbs,
                      restecg, thalach, exang, oldpeak, slope, ca, thal]
        prediction = heart_disease_model.predict([input_data])
        result = "Heart Disease" if prediction[0] == 1 else "No Heart Disease"
        
        show_modern_result(f"The person has {result}", "heart")
        
        st.markdown("### Health Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status = "normal" if 18 <= age <= 65 else "abnormal"
            show_metric_card("Age", age, "years", status)
        with col2:
            status = "normal" if 90 <= trestbps <= 120 else "abnormal"
            show_metric_card("Resting BP", trestbps, "mmHg", status)
        with col3:
            status = "normal" if 125 <= chol <= 200 else "abnormal"
            show_metric_card("Cholesterol", chol, "mg/dL", status)
        with col4:
            status = "normal" if 60 <= thalach <= 100 else "abnormal"
            show_metric_card("Max Heart Rate", thalach, "bpm", status)
        
        show_modern_doctors("heart disease")
        
        show_modern_graph(
            [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal],
            ["Age", "Sex", "Chest Pain", "Resting BP", "Cholesterol", 
             "Fasting BS", "Resting ECG", "Max HR", "Exercise Angina", 
             "Oldpeak", "ST Slope", "Ca", "Thal"],
            [(18, 65), (0, 1), (0, 1), (90, 120), (125, 200), 
             (0, 99), (0, 0), (60, 100), (0, 0), 
             (0, 1.0), (2, 2), (0, 0), (2, 2)]
        )

# ===================== KIDNEY DISEASE PREDICTION =====================
if selected == "Kidney Disease Prediction":
    check_login()
    
    show_greeting_card(st.session_state['username'])
    
    st.title(" Kidney Disease Prediction")
    
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### Enter Health Parameters")
    
    cols = st.columns(3)
    
    # Numeric inputs
    with cols[0]: age = st.number_input("Age", min_value=0, step=1)
    with cols[1]: bp = st.number_input("Blood Pressure", min_value=0, step=1)
    with cols[2]: sg = st.number_input("Specific Gravity", min_value=1.000, max_value=1.030, step=0.001, format="%.3f", value=1.020)
    with cols[0]: al = st.number_input("Albumin", min_value=0, max_value=5, step=1)
    with cols[1]: su = st.number_input("Sugar", min_value=0, max_value=5, step=1)
    
    # Categorical inputs using radio buttons in horizontal layout
    with cols[2]: 
        st.write("**Red Blood Cells**")
        rbc = st.radio("rbc_label", ["normal", "abnormal"], horizontal=True, label_visibility="collapsed", key="rbc")
    
    with cols[0]: 
        st.write("**Pus Cell**")
        pc = st.radio("pc_label", ["normal", "abnormal"], horizontal=True, label_visibility="collapsed", key="pc")
    
    with cols[1]: 
        st.write("**Pus Cell Clumps**")
        pcc = st.radio("pcc_label", ["notpresent", "present"], horizontal=True, label_visibility="collapsed", key="pcc")
    
    with cols[2]: 
        st.write("**Bacteria**")
        ba = st.radio("ba_label", ["notpresent", "present"], horizontal=True, label_visibility="collapsed", key="ba")
    
    # More numeric inputs
    with cols[0]: bgr = st.number_input("Blood Glucose Random", min_value=0.0, step=0.1)
    with cols[1]: bu = st.number_input("Blood Urea", min_value=0.0, step=0.1)
    with cols[2]: sc = st.number_input("Serum Creatinine", min_value=0.0, step=0.1, format="%.2f")
    with cols[0]: sod = st.number_input("Sodium", min_value=0.0, step=0.1)
    with cols[1]: pot = st.number_input("Potassium", min_value=0.0, step=0.1, format="%.2f")
    with cols[2]: hemo = st.number_input("Hemoglobin", min_value=0.0, step=0.1)
    with cols[0]: pcv = st.number_input("Packed Cell Volume", min_value=0, step=1)
    with cols[1]: wc = st.number_input("White Blood Cell Count", min_value=0, step=100)
    with cols[2]: rc = st.number_input("Red Blood Cell Count", min_value=0.0, step=0.1)
    
    # More categorical inputs using radio buttons
    with cols[0]: 
        st.write("**Hypertension**")
        htn = st.radio("htn_label", ["no", "yes"], horizontal=True, label_visibility="collapsed", key="htn")
    
    with cols[1]: 
        st.write("**Diabetes Mellitus**")
        dm = st.radio("dm_label", ["no", "yes"], horizontal=True, label_visibility="collapsed", key="dm")
    
    with cols[2]: 
        st.write("**Coronary Artery Disease**")
        cad = st.radio("cad_label", ["no", "yes"], horizontal=True, label_visibility="collapsed", key="cad")
    
    with cols[0]: 
        st.write("**Appetite**")
        appet = st.radio("appet_label", ["good", "poor"], horizontal=True, label_visibility="collapsed", key="appet")
    
    with cols[1]: 
        st.write("**Pedal Edema**")
        pe = st.radio("pe_label", ["no", "yes"], horizontal=True, label_visibility="collapsed", key="pe")
    
    with cols[2]: 
        st.write("**Anemia**")
        ane = st.radio("ane_label", ["no", "yes"], horizontal=True, label_visibility="collapsed", key="ane")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔍 Predict Kidney Disease", use_container_width=True):
        # Risk-based prediction logic
        risk = 0
        alerts = []
        
        # Numeric thresholds
        if bp > 140: risk += 1; alerts.append("High Blood Pressure")
        if sg < 1.015: risk += 1; alerts.append("Low Urine Specific Gravity")
        if al > 1: risk += 1; alerts.append("Protein in Urine (Albumin)")
        if su > 1: risk += 1; alerts.append("Sugar in Urine")
        if bgr > 150: risk += 1; alerts.append("High Blood Glucose")
        if bu > 20: risk += 1; alerts.append("High Blood Urea")
        if sc > 1.2: risk += 1; alerts.append("High Serum Creatinine")
        if sod < 135: risk += 1; alerts.append("Low Sodium Level")
        if pot > 5.0: risk += 1; alerts.append("High Potassium Level")
        if hemo < 12: risk += 1; alerts.append("Low Hemoglobin")
        if pcv < 36: risk += 1; alerts.append("Low Packed Cell Volume")
        if wc > 11000: risk += 1; alerts.append("High WBC Count")
        if rc < 4.2: risk += 1; alerts.append("Low RBC Count")
        
        # Categorical rules
        if rbc == "abnormal": risk += 1; alerts.append("Abnormal RBC")
        if pc == "abnormal": risk += 1; alerts.append("Abnormal Pus Cells")
        if pcc == "present": risk += 1; alerts.append("Pus Cell Clumps Present")
        if ba == "present": risk += 1; alerts.append("Bacteria in Urine")
        if htn == "yes": risk += 1; alerts.append("Hypertension")
        if dm == "yes": risk += 1; alerts.append("Diabetes Mellitus")
        if cad == "yes": risk += 1; alerts.append("Coronary Artery Disease")
        if appet == "poor": risk += 1; alerts.append("Poor Appetite")
        if pe == "yes": risk += 1; alerts.append("Pedal Edema")
        if ane == "yes": risk += 1; alerts.append("Anemia")
        
        # Final Decision
        if risk >= 4:
            result = "Kidney Disease"
            show_modern_result(f"⚠️ High Risk of Chronic Kidney Disease! (Risk Score: {risk})", "kidney")
            st.markdown("### 🚨 Abnormal Findings:")
            for alert in alerts:
                st.markdown(f"""
                <div style="background: #fff5f5; padding: 0.8rem; margin: 0.5rem 0; 
                            border-left: 4px solid #f56565; border-radius: 8px; color: #c53030;">
                    • {alert}
                </div>
                """, unsafe_allow_html=True)
        elif risk == 2 or risk == 3:
            result = "Moderate Risk"
            show_modern_result(f"⚠️ Moderate Risk. Medical checkup recommended. (Risk Score: {risk})", "kidney")
            st.markdown("### ⚠️ Possible Concerns:")
            for alert in alerts:
                st.markdown(f"""
                <div style="background: #fffbeb; padding: 0.8rem; margin: 0.5rem 0; 
                            border-left: 4px solid #f59e0b; border-radius: 8px; color: #92400e;">
                    • {alert}
                </div>
                """, unsafe_allow_html=True)
        else:
            result = "No Kidney Disease"
            show_modern_result(f"✅ Likely No Kidney Disease (Risk Score: {risk})", "kidney")
            st.success("Health parameters appear normal ✅")
        
        # Health Indicators
        st.markdown("### 🩺 Health Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status = "normal" if 60 <= bp <= 80 else "abnormal"
            show_metric_card("Blood Pressure", bp, "mmHg", status)
        with col2:
            status = "normal" if 0.6 <= sc <= 1.2 else "abnormal"
            show_metric_card("Creatinine", sc, "mg/dL", status)
        with col3:
            status = "normal" if 7 <= bu <= 20 else "abnormal"
            show_metric_card("Blood Urea", bu, "mg/dL", status)
        with col4:
            status = "normal" if 12 <= hemo <= 17 else "abnormal"
            show_metric_card("Hemoglobin", hemo, "g/dL", status)
        
        show_modern_doctors("kidney disease")
        
        show_modern_graph(
            [age, bp, sg, al, su, bgr, bu, sc, sod, pot, hemo, pcv, wc, rc],
            [
                "Age", "Blood Pressure", "Specific Gravity", "Albumin", "Sugar", 
                "Blood Glucose", "Blood Urea", "Serum Creatinine", "Sodium", 
                "Potassium", "Hemoglobin", "Packed Cell Vol", "WBC Count", "RBC Count"
            ],
            [
                (18, 65), (60, 80), (1.010, 1.025), (0, 0), (0, 0), 
                (70, 99), (7, 20), (0.6, 1.2), (136, 145), 
                (3.5, 5.0), (12, 17), (36, 48), (4000, 11000), (4.5, 5.5)
            ]
        )

# ===================== PRECAUTIONS =====================
if selected == "Precautions":
    check_login()
    
    show_greeting_card(st.session_state['username'])
    
    st.title("🛡️ Health Precautions & Lifestyle Guide")
    
    # Disease selection with better styling
    st.markdown("### Select Disease Type")
    disease = st.selectbox("Choose a disease to view personalized health recommendations", 
                           ["Diabetes", "Heart Disease", "Kidney Disease"],
                           label_visibility="collapsed")
    
    precautions = {
        "Diabetes": {
            "precautions": [
                "Eat balanced meals with less sugar and refined carbs",
                "Exercise at least 30 minutes daily (walking, cycling, swimming)",
                "Check blood sugar levels regularly as advised by doctor",
                "Avoid junk food, sugary drinks, and processed foods",
                "Maintain healthy weight (BMI 18.5-24.9)",
                "Stay hydrated - drink 8-10 glasses of water daily"
            ],
            "diet": [
                "Whole grains (brown rice, oats, quinoa)",
                "Leafy vegetables (spinach, kale, broccoli)",
                "Lean proteins (chicken, fish, legumes)",
                "Low-fat dairy products",
                "Nuts and seeds (almonds, walnuts)",
                "Avoid: White bread, pastries, candy, sodas"
            ],
            "warning_signs": [
                "Frequent urination",
                "Excessive thirst",
                "Unexplained weight loss",
                "Blurred vision",
                "Slow healing wounds"
            ],
            "tests": [
                "Fasting Blood Sugar (FBS) - Every 3 months",
                "HbA1c Test - Every 3-6 months",
                "Lipid Profile - Annually"
            ]
        },
        "Heart Disease": {
            "precautions": [
                "Completely avoid smoking and limit alcohol consumption",
                "Eat a heart-healthy diet rich in fruits and vegetables",
                "Control cholesterol levels (LDL < 100 mg/dL)",
                "Monitor and maintain healthy blood pressure (<120/80)",
                "Reduce stress through meditation, yoga, or hobbies",
                "Get 7-8 hours of quality sleep every night"
            ],
            "diet": [
                "Omega-3 rich foods (salmon, mackerel, walnuts)",
                "Fresh fruits (berries, oranges, apples)",
                "Vegetables (tomatoes, carrots, bell peppers)",
                "Whole grains and oats",
                "Olive oil and avocados",
                "Avoid: Trans fats, excess salt, red meat, fried foods"
            ],
            "warning_signs": [
                "Chest pain or discomfort",
                "Shortness of breath",
                "Pain in arms, neck, or jaw",
                "Irregular heartbeat",
                "Extreme fatigue"
            ],
            "tests": [
                "ECG (Electrocardiogram) - Annually",
                "Lipid Profile - Every 6 months",
                "Blood Pressure - Weekly monitoring",
                "Stress Test - As recommended"
            ]
        },
        "Kidney Disease": {
            "precautions": [
                "Drink adequate water (6-8 glasses) but avoid overhydration",
                "Limit salt intake to less than 5g per day",
                "Reduce protein intake if advised by doctor",
                "Monitor and control blood pressure and sugar levels",
                "Avoid self-medication, especially painkillers (NSAIDs)",
                "Regular kidney function tests as prescribed"
            ],
            "diet": [
                "Fresh vegetables (cauliflower, cabbage, onions)",
                "Fruits with low potassium (apples, berries, grapes)",
                "Egg whites (limit egg yolks)",
                "Fish in moderation",
                "Rice and pasta",
                "Avoid: Processed foods, canned items, bananas, oranges, nuts"
            ],
            "warning_signs": [
                "Swelling in feet and ankles",
                "Frequent or reduced urination",
                "Foamy or bloody urine",
                "Persistent fatigue",
                "Loss of appetite"
            ],
            "tests": [
                "Serum Creatinine - Every 3 months",
                "Blood Urea Nitrogen (BUN) - Every 3 months",
                "Urine Analysis - Every 3-6 months",
                "Kidney Ultrasound - Annually"
            ]
        }
    }
    
    specialists = {
        "Diabetes": "Endocrinologist",
        "Heart Disease": "Cardiologist",
        "Kidney Disease": "Nephrologist"
    }
    
    disease_emojis = {
        "Diabetes": "💉",
        "Heart Disease": "❤️",
        "Kidney Disease": "🩺"
    }
    
    # Main content with tabs
    st.markdown("---")
    
    # Disease header card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 1.5rem 0;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);">
        <h2 style="margin: 0; color: white;">{disease_emojis[disease]} {disease}</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            Recommended Specialist: <strong>{specialists[disease]}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["✅ Precautions", "🍽️ Diet Plan", "⚠️ Warning Signs", "🔬 Medical Tests"])
    
    with tab1:
        st.markdown('<div class="graph-card">', unsafe_allow_html=True)
        st.markdown("### Daily Precautions & Lifestyle Tips")
        for i, precaution in enumerate(precautions[disease]["precautions"], 1):
            st.markdown(f"""
            <div style="background: #f7fafc; padding: 1rem; margin: 0.5rem 0; 
                        border-left: 4px solid #667eea; border-radius: 8px;">
                <strong style="color: #667eea;">{i}.</strong> {precaution}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="graph-card">', unsafe_allow_html=True)
        st.markdown("### 🥗 Recommended Diet Plan")
        st.markdown("**Foods to Include:**")
        col1, col2 = st.columns(2)
        for i, food in enumerate(precautions[disease]["diet"][:len(precautions[disease]["diet"])-1]):
            if i % 2 == 0:
                col1.markdown(f"✓ {food}")
            else:
                col2.markdown(f"✓ {food}")
        
        st.markdown("---")
        st.markdown(f"**⚠️ {precautions[disease]['diet'][-1]}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="graph-card">', unsafe_allow_html=True)
        st.markdown("### ⚠️ Warning Signs - Seek Immediate Medical Attention")
        st.warning("If you experience any of these symptoms, consult a doctor immediately:")
        
        for sign in precautions[disease]["warning_signs"]:
            st.markdown(f"""
            <div style="background: #fff5f5; padding: 0.8rem; margin: 0.5rem 0; 
                        border-left: 4px solid #f56565; border-radius: 8px; color: #c53030;">
                🚨 {sign}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="graph-card">', unsafe_allow_html=True)
        st.markdown("### 🔬 Recommended Medical Tests")
        st.info("Regular health checkups are essential for early detection and management")
        
        for test in precautions[disease]["tests"]:
            test_parts = test.split(" - ")
            st.markdown(f"""
            <div style="background: #e6f7ff; padding: 1rem; margin: 0.5rem 0; 
                        border-left: 4px solid #1890ff; border-radius: 8px;">
                <strong style="color: #1890ff;">🧪 {test_parts[0]}</strong><br>
                <span style="color: #595959; font-size: 0.9rem;">Frequency: {test_parts[1]}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Find nearby doctors section
    st.markdown("---")
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.markdown("### 🏥 Find Specialists Near You")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"Looking for a {specialists[disease]}? Click the button to find specialists near your location.")
    with col2:
        if st.button("🔍 Find Doctors", use_container_width=True):
            show_modern_doctors(disease.lower())
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Emergency contact card
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; margin-top: 2rem;
                box-shadow: 0 4px 15px rgba(245, 101, 101, 0.3);">
        <h4 style="margin: 0; color: white;">🚨 Emergency Contact</h4>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            In case of medical emergency, call: <strong>108 (Ambulance)</strong> or <strong>102 (Medical Emergency)</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
# ===================== ABOUT =====================
if selected == "About":
    st.title("ℹ️ About This Project")
    st.markdown("""
    <div style="font-family:'Roboto', sans-serif; line-height:1.6;">
    <p>This project, <b>Human Multiple Disease Detection System</b>, is designed to help users detect three major diseases—<b>Diabetes</b>, <b>Heart Disease</b>, and <b>Kidney Disease</b>—at an early stage using <b>machine learning models</b> trained on real medical datasets.</p>

    <h4>🔬 Features:</h4>
    <ul>
        <li>Predicts <b>Diabetes</b>, <b>Heart Disease</b>, and <b>Kidney Disease</b> accurately using trained ML models.</li>
        <li>Provides health precautions for each disease to improve lifestyle and prevent complications.</li>
        <li>Suggests nearby specialists automatically based on your location.</li>
        <li>Maintains user login, history of predictions, and analytics of usage.</li>
        <li>Interactive and user-friendly interface built with <b>Streamlit</b>.</li>
    </ul>

    <h4>💡 Purpose:</h4>
    <p>This system is developed to raise awareness about early detection of common diseases and empower users with actionable health insights. It helps both patients and caregivers to monitor health conditions efficiently.</p>

    <h4>🥼 Supported Diseases:</h4>
    <ul>
        <li>✅ Diabetes Detection</li>
        <li>✅ Heart Disease Detection</li>
        <li>✅ Kidney Disease Detection</li>
    </ul>

    <p>By integrating <b>AI & ML</b> with healthcare, this project aims to make health monitoring accessible and easy for everyone.</p>
    </div>
    """, unsafe_allow_html=True)

# ===================== CONTACT =====================
if selected == "Contact Us":
    st.title("📬 Contact Us")
    st.markdown("""
<div style="
    background-color: #f0f8ff; 
    padding: 20px; 
    border-radius: 10px; 
    color: #1a1a1a; 
    font-family:'Roboto', sans-serif;
    line-height:1.6;
">
    <h4>📧 Email Addresses:</h4>
    <ul>
        <li><b>Zaara Khan:</b> <a href="mailto:zaarakhn07@eng.rizvi.edu.in">zaarakhn07@eng.rizvi.edu.in</a> - Backend & Database Management</li>
        <li><b>Anshika Shukla:</b> <a href="mailto:shuklaanshika@eng.rizvi.edu.in">shuklaanshika@eng.rizvi.edu.in</a> - Frontend & UI Developer</li>
        <li><b>Sakshi Jha:</b> <a href="mailto:jhasakshi18@eng.rizvi.edu.in">jhasakshi18@eng.rizvi.edu.in</a> - API Integration,UI Designing and Performance optimization [Team leader]</li>
        <li><b>Humaira Saifee:</b> <a href="mailto:humairasaifee25@gmail.com">humairasaifee25@gmail.com</a> - Machine Learning & AI Specialist</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ===================== USER GRAPHS =====================
if selected == "User Graphs":
    check_login()
    st.title("📊 User Graphs and Analytics")
    
    try:
        df = pd.read_sql_query("SELECT * FROM user_activity ORDER BY timestamp", conn, parse_dates=['timestamp'])
    except Exception as e:
        st.error(f"Database error: {e}")
        st.stop()
    
    if df.empty:
        st.info("No activity data yet.")
    else:
        # ✅ Filter out non-disease activities
        disease_keywords = ['diabetes', 'heart', 'kidney']
        disease_df = df[df['activity_type'].str.lower().str.contains('|'.join(disease_keywords), na=False)]
        
        if disease_df.empty:
            st.info("No disease prediction data yet.")
            st.stop()
        
        disease_df['timestamp'] = pd.to_datetime(disease_df['timestamp'], errors='coerce')
        
        # ✅ Optional: Admin-only access to raw data
        with st.expander("View Raw Activity Data (Admin Only)"):
            if st.session_state.get('username') == "admin":
                st.dataframe(disease_df)
            else:
                st.warning("You don't have permission to view this data.")
        
        st.markdown("### Disease Prediction Overview")
        
        # ✅ Count of predictions per disease type
        st.subheader("📈 Predictions per Disease Type")
        prediction_counts = (
            disease_df['activity_type']
            .replace({
                'Diabetes Prediction': 'Diabetes',
                'Heart Prediction': 'Heart Disease',
                'Kidney Disease Prediction': 'Kidney Disease'
            })
            .value_counts()
            .reindex(['Diabetes', 'Heart Disease', 'Kidney Disease'], fill_value=0)
        )
        
        fig1, ax1 = plt.subplots()
        prediction_counts.plot(kind='bar', ax=ax1, color=['#2B7A78', '#3AAFA9', '#17252A'], edgecolor='black')
        ax1.set_xlabel("Disease Type")
        ax1.set_ylabel("Number of Predictions")
        ax1.set_title("Disease-wise Prediction Count")
        st.pyplot(fig1)
        
        # ✅ Prediction results pie chart
        st.subheader("🎯 Prediction Result Distribution")
        if 'result' in disease_df.columns:
            result_counts = disease_df['result'].value_counts()
            fig2, ax2 = plt.subplots()
            result_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax2, colors=['#3AAFA9', '#DEF2F1'])
            ax2.set_ylabel('')
            ax2.set_title("Prediction Outcomes")
            st.pyplot(fig2)
        
        # ✅ Dashboard summary metrics
        st.markdown("### 📊 Summary Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Predictions", len(disease_df))
        col3.metric("Diseases Covered", prediction_counts[prediction_counts > 0].count())

# ===================== EXIT =====================
if selected == "Exit":
    st.title("👋 Thank You!")
    st.markdown("""
    <div class="greeting-card">
        <h2>Thank you for using our Health Prediction Platform!</h2>
        <p>Stay healthy and take care of yourself 💙</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()