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

from dotenv import load_dotenv
import os

load_dotenv()  # loads values from .env
api_key = os.getenv("GOOGLE_API_KEY")

import streamlit as st

def highlight_out_of_range(value, min_val, max_val, label):
    """Highlights if parameter is outside normal range with professional styling."""
    
    # Determine status
    if value < min_val or value > max_val:
        status = "out"
        status_icon = "⚠"
        status_text = "Out of Range"
        status_color = "#ff4444"
        bg_color = "#ffe6e6"
        border_color = "#ff4444"
    else:
        status = "in"
        status_icon = "●"
        status_text = "Normal"
        status_color = "#00c851"
        bg_color = "#e8f5e9"
        border_color = "#00c851"
    
    # Create styled component
    st.markdown(f"""
    <div style="
        background: {bg_color};
        border-left: 5px solid {border_color};
        border-radius: 8px;
        padding: 15px 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s ease;
    " onmouseover="this.style.transform='translateX(5px)'" 
       onmouseout="this.style.transform='translateX(0)'">
        <div style="flex: 1;">
            <span style="
                font-weight: bold;
                font-size: 1.1em;
                color: #333;
            ">{label}:</span>
            <span style="
                background: white;
                padding: 4px 12px;
                border-radius: 5px;
                margin-left: 10px;
                font-family: monospace;
                font-size: 1.1em;
                font-weight: bold;
                color: {status_color};
            ">{value}</span>
        </div>
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            <span style="font-size: 1.3em;">{status_icon}</span>
            <span style="
                color: {status_color};
                font-weight: 600;
                font-size: 0.95em;
            ">{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return status
    
import requests
import streamlit as st
import os

def show_nearby_doctors(prediction_label):
    st.subheader("🏥 Nearby Doctors Recommendation")

    # Example static coordinates (Mumbai)
    user_lat, user_lng = 19.0760, 72.8777
    radius = 5000  # meters (5 km)
    api_key = os.environ.get("GOOGLE_API_KEY")

    # Match specialist based on predicted disease
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
        f"&keyword={doctor_type}&key={api_key}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            st.markdown(f"### 👨‍⚕️ Specialists Found: *{doctor_type.title()}s* Near You")
            
            for place in data["results"][:5]:
                name = place["name"]
                address = place.get("vicinity", "Address not available")
                rating = place.get("rating", "N/A")
                lat = place["geometry"]["location"]["lat"]
                lng = place["geometry"]["location"]["lng"]
                maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"

                st.markdown(f"""
                <div style="
                    background-color:#f0f8ff;
                    padding:15px;
                    margin:10px 0;
                    border-radius:10px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.1);
                ">
                    <h4 style="margin-bottom:5px;">🩺 {name}</h4>
                    <p style="margin:0;">📍 {address}</p>
                    <p style="margin:0;">⭐ Rating: {rating}</p>
                    <a href="{maps_link}" target="_blank" 
                       style="color:#0078ff; text-decoration:none;">📍 View on Google Maps</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No nearby doctors found. Try increasing the radius or check your API key.")
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def show_health_summary(values, labels, normal_ranges):
    st.subheader("📊 Health Summary Chart")
    fig, ax = plt.subplots(figsize=(10, 6))  # Increased figure size
    y_pos = np.arange(len(labels))
    
    # Determine colors based on normal ranges
    colors = ['#4CAF50' if normal_ranges[i][0] <= values[i] <= normal_ranges[i][1] 
              else '#FF5252' for i in range(len(values))]
    
    bars = ax.barh(y_pos, values, color=colors)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()  # highest value on top
    ax.set_xlabel('Value')
    ax.set_title('Health Parameters Overview')
    
    # Calculate appropriate x-axis limit to prevent overlap
    max_value = max(values)
    max_range = max([high for low, high in normal_ranges])
    x_limit = max(max_value, max_range) * 1.4  # Add 40% padding
    ax.set_xlim(0, x_limit)
    
    # Add value and normal range annotations
    for i, (bar, (low, high)) in enumerate(zip(bars, normal_ranges)):
        # Display value at the end of the bar
        ax.text(values[i] + (x_limit * 0.01), i, f"{values[i]}", 
                va='center', fontsize=10, fontweight='bold')
        
        # Display normal range to the right with more spacing
        range_text = f"(Normal: {low}-{high})"
        if values[i] < normal_ranges[i][0] or values[i] > normal_ranges[i][1]:
            color = '#FF5252'
        else:
            color = 'gray'
        
        ax.text(values[i] + (x_limit * 0.08), i, range_text, 
                va='center', fontsize=9, color=color)
    
    plt.tight_layout()
    st.pyplot(fig)

# ----------------------- Page Config -----------------------
st.set_page_config(
    page_title="Multiple Disease Prediction",
    layout="wide",
    page_icon="🩺"
)

# ----------------------- Session State -----------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""

# ----------------------- Database Setup -----------------------
conn = sqlite3.connect('user_data.db', check_same_thread=False)
c = conn.cursor()

# users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
''')

# user activity + predictions tables
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

# ----------------------- User Functions -----------------------
def get_user(username):
    c.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    return c.fetchone()

def add_user(username, password_plaintext):
    hashed = bcrypt.hashpw(password_plaintext.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
    conn.commit()

def verify_password(password_plaintext, hashed_str):
    return bcrypt.checkpw(password_plaintext.encode('utf-8'), hashed_str.encode('utf-8'))

# ----------------------- Load ML Models -----------------------
diabetes_model = pickle.load(open('diabetes.pkl', 'rb'))

heart_disease_model = pickle.load(open('heart.pkl', 'rb'))
kidney_disease_model = pickle.load(open('kidney.pkl', 'rb'))
# ----------------------- Custom CSS -----------------------
page_bg_color = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Poppins:wght@600;700&display=swap');

/* ------------------- Main App Background ------------------- */
.stApp {
    background: linear-gradient(135deg, #c3ecff 0%, #b3f0ff 100%);
    color: #1a1a1a;
    font-family: 'Roboto', sans-serif;
    transition: all 0.5s ease;
}

/* ------------------- Headings ------------------- */
h1, h2, h3, h4, h5, h6 {
    color: #0d1a26;
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    margin-bottom: 15px;
    transition: all 0.3s ease;
}

/* ------------------- Card Layout ------------------- */
.card {
    background: #ffffff;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

/* ------------------- Fade-in Animation ------------------- */
.fade-in {
    opacity: 0;
    animation: fadeIn 0.7s ease forwards;
}
@keyframes fadeIn {
    from { opacity:0; transform: translateY(20px); }
    to { opacity:1; transform: translateY(0); }
}

/* ------------------- Typing Animation ------------------- */
.typing {
  display: inline-block;
  border-right: 2px solid #0077b6;
  white-space: nowrap;
  overflow: hidden;
  animation: typing 2s steps(40, end), blink-caret 0.75s step-end infinite;
}
@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}
@keyframes blink-caret {
  50% { border-color: transparent; }
}

/* ------------------- Labels above input ------------------- */
.stNumberInput label, .stTextInput label {
    display: block !important;
    color: #003366 !important;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
    padding-bottom: 4px;
    font-size: 0.95rem;
    transition: all 0.3s ease;
}

/* ------------------- Input Boxes ------------------- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    color: #333333 !important;
    background-color: #e0f7fa !important;
    border: 1px solid #0099cc !important;
    border-radius: 10px !important;
    padding: 8px;
    font-weight: 500;
    font-family: 'Roboto', sans-serif;
    transition: all 0.3s ease-in-out;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border: 2px solid #0077b6 !important;
    box-shadow: 0 0 8px rgba(0,119,182,0.3);
    transform: scale(1.02);
}

/* ------------------- Buttons ------------------- */
.stButton > button {
    background-color: #0077b6 !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    padding: 10px 20px !important;
    font-family: 'Poppins', sans-serif;
    transition: all 0.3s ease-in-out;
}
.stButton > button:hover {
    background-color: #0096c7 !important;
    transform: scale(1.05) translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,119,182,0.3);
}

/* ------------------- Sidebar ------------------- */
.css-1d391kg {  
    background-color: #e6f2ff !important;
    font-family: 'Roboto', sans-serif;
}
.css-1v3fvcr {
    font-weight: 700 !important;
    font-size: 1.15rem !important;
}
.css-1d391kg .nav-item:hover {
    background-color: #0099cc;
    color: white;
    border-radius: 10px;
    transition: 0.3s;
}

/* ------------------- Tables / DataFrames ------------------- */
.stDataFrame, .css-1lcbmhc {
    font-family: 'Roboto', sans-serif;
    font-size: 0.95rem;
    border-radius: 10px;
    overflow: hidden;
}

/* ------------------- Alerts / Warnings ------------------- */
.stAlert {
    border-radius: 12px;
    font-weight: 600;
    padding: 8px;
    font-family: 'Poppins', sans-serif;
}

/* ------------------- Horizontal line ------------------- */
hr {
    border: 1px solid #0099cc;
}

/* ------------------- Selectbox / Dropdown ------------------- */
.css-1wy0on6 {
    font-family: 'Roboto', sans-serif;
    color: #003366;
    transition: all 0.3s ease;
}
.css-1wy0on6:hover {
    transform: scale(1.02);
}

/* ------------------- Text Highlight on Hover ------------------- */
p:hover, li:hover, h4:hover, h5:hover {
    color: #0077b6;
    transition: 0.3s ease;
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)



# ----------------------- Sidebar -----------------------
with st.sidebar:
    selected = option_menu(
        "Multiple Disease Prediction",
        [
            "Home", "User Login", "Diabetes Prediction",
            "Heart Disease Prediction", "Kidney Disease Prediction",
            "Precautions",  
            "About", "Developer", "Contact Us", "User Graphs", "Exit"
        ],
        icons=['house', 'person', 'capsule', 'heart', 'droplet', 'map', 'info-circle',
               'person-circle', 'envelope', 'bar-chart', 'x-circle'],
        default_index=0
    )

# ----------------------- Login Check -----------------------
def check_login():
    if not st.session_state.get('logged_in'):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px; border-radius: 10px; color: white; text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>🔒 Authentication Required</h3>
            <p>Please login first to access prediction tools.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# ----------------------- User Login / Signup -----------------------
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
    
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
                
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
        st.markdown('<h3>🔑 Login to Your Account</h3>', unsafe_allow_html=True)
        
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
        <h3>🏥 Advanced Health Prediction System</h3>
        <p>Our AI-powered platform provides predictions for multiple diseases including:</p>
        <p><strong>💉 Diabetes</strong> • <strong>❤️ Heart Disease</strong> • <strong>🩺 Kidney Disease</strong></p>
        <p style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
            Secure • Accurate • Confidential
        </p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------- Home -----------------------
if selected == "Home":
    st.title("🏠 HUMAN MULTIPLE DISEASE DETECTION SYSTEM")
    st.markdown("""
    <div style="font-family:'Roboto', sans-serif; line-height:1.6;">
    <h3>Welcome to the Multiple Disease Prediction System 🔍</h3>
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
# ----------------------- About -----------------------
if selected == "About":
    st.title("ℹ️ About This Project")
    st.markdown("""
    <div style="font-family:'Roboto', sans-serif; line-height:1.6;">
    <p>This project, <b>Human Multiple Disease Detection System</b>, is designed to help users detect three major diseases—<b>Diabetes</b>, <b>Heart Disease</b>, and <b>Kidney Disease</b>—at an early stage using <b>machine learning models</b> trained on real medical datasets.</p>

    <h4>🔍 Features:</h4>
    <ul>
        <li>Predicts <b>Diabetes</b>, <b>Heart Disease</b>, and <b>Kidney Disease</b> accurately using trained ML models.</li>
        <li>Provides health precautions for each disease to improve lifestyle and prevent complications.</li>
        <li>Suggests nearby specialists automatically based on your location.</li>
        <li>Maintains user login, history of predictions, and analytics of usage.</li>
        <li>Interactive and user-friendly interface built with <b>Streamlit</b>.</li>
    </ul>

    <h4>💡 Purpose:</h4>
    <p>This system is developed to raise awareness about early detection of common diseases and empower users with actionable health insights. It helps both patients and caregivers to monitor health conditions efficiently.</p>

    <h4>🏥 Supported Diseases:</h4>
    <ul>
        <li>✅ Diabetes Detection</li>
        <li>✅ Heart Disease Detection</li>
        <li>✅ Kidney Disease Detection</li>
    </ul>

    <p>By integrating <b>AI & ML</b> with healthcare, this project aims to make health monitoring accessible and easy for everyone.</p>
    </div>
    """, unsafe_allow_html=True)


# ----------------------- About / Developer -----------------------
if selected == "Developer":
    st.title("👨‍💻 About Developer Team")
    st.markdown("""
    <div style="font-family:'Roboto', sans-serif; line-height:1.6;">
    <p>This project is developed by a passionate team of AI & ML enthusiasts focusing on healthcare technology.</p>

    <h4>Team Members:</h4>

    <ul>
        <li><b>Zaara Khan:</b> Full Stack Developer, responsible for prediction models deployment and API integration. <br>Email: zaarakhn07@eng.rizvi.edu.in</li>
        <li><b>Anshika Shukla:</b> Frontend & UI/UX Developer, worked on Streamlit interface and visualization. <br>Email: shuklaanshika@eng.rizvi.edu.in</li>
        <li><b>Sakshi Jha:</b> Full Stack Developer, API Integrations and Backend logic. <br>Email: jhasakshi18@eng.rizvi.edu.in</li>
        <li><b>Humaira Saifee:</b> Lead AI & ML Engineer, specialized in healthcare predictive models. <br>Email: humairasaifee25@gmail.com</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
# ----------------------- Contact -----------------------
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
        <li><b>Sakshi Jha:</b> <a href="mailto:jhasakshi18@eng.rizvi.edu.in">jhasakshi18@eng.rizvi.edu.in</a> - Team leader</li>
        <li><b>Humaira Saifee:</b> <a href="mailto:humairasaifee25@gmail.com">humairasaifee25@gmail.com</a> - Machine Learning & AI Specialist</li>
    </ul>
</div>
""", unsafe_allow_html=True)



# ----------------------- Diabetes Prediction -----------------------
if selected == "Diabetes Prediction":
    check_login()
    st.title("Diabetes Prediction")
    col1, col2, col3 = st.columns(3)
    with col1: Pregnancies = st.number_input("Number of Pregnancies", min_value=0)
    with col2: Glucose = st.number_input("Glucose Level", min_value=0)
    with col3: BloodPressure = st.number_input("Blood Pressure", min_value=0)
    with col1: SkinThickness = st.number_input("Skin Thickness", min_value=0)
    with col2: Insulin = st.number_input("Insulin Level", min_value=0)
    with col3: BMI = st.number_input("BMI", min_value=0.0, format="%.2f")
    with col1: DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0, format="%.3f")
    with col2: Age = st.number_input("Age", min_value=0)

    if st.button("Predict Diabetes"):
        input_data = np.array([
            Pregnancies, Glucose, BloodPressure, SkinThickness,
            Insulin, BMI, DiabetesPedigreeFunction, Age
        ]).reshape(1, -1)
        poly = PolynomialFeatures(degree=2, include_bias=False)
        input_poly = poly.fit_transform(input_data)[:, :18]
        prediction = diabetes_model.predict(input_poly)
        result = "Diabetic" if prediction[0] == 1 else "Non-Diabetic"
        st.success(f"The person is {result}")

        # Highlight section 
        st.subheader("Health Parameter Check 🔍")
        highlight_out_of_range(Glucose, 70, 140, "Glucose Level")
        highlight_out_of_range(BloodPressure, 80, 120, "Blood Pressure")
        highlight_out_of_range(BMI, 18.5, 24.9, "BMI")
        highlight_out_of_range(Age, 18, 60, "Age")

        st.success(f"The person is {result}")
        show_nearby_doctors("diabetes")

        
    show_health_summary(
        [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age],
        ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", "Insulin", "BMI", "DPF", "Age"],
        [(0, 5), (70, 140), (60, 120), (10, 40), (15, 166), (18, 25), (0.1, 2.5), (20, 60)]
    )



# ----------------------- Heart Disease -----------------------
if selected == "Heart Disease Prediction":
    check_login()
    st.title("Heart Disease Prediction")
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

    if st.button("Predict Heart Disease"):
        input_data = [age, sex, cp, trestbps, chol, fbs,
                      restecg, thalach, exang, oldpeak, slope, ca, thal]
        prediction = heart_disease_model.predict([input_data])
        result = "Heart Disease" if prediction[0] == 1 else "No Heart Disease"
        st.success(f"The person has {result}")

        # Highlight abnormal heart parameters
        abnormal_params = []

        if age > 50:
            abnormal_params.append("Age (High)")
        if trestbps > 140:
            abnormal_params.append("Resting Blood Pressure (High)")
        if chol > 240:
            abnormal_params.append("Cholesterol (High)")
        if fbs == 1:
            abnormal_params.append("Fasting Blood Sugar (High)")
        if thalach < 100:
            abnormal_params.append("Maximum Heart Rate (Low)")
        if oldpeak > 2:
            abnormal_params.append("ST Depression (High)")

        if abnormal_params:
            st.warning("⚠️ Parameters out of optimal range:")
            for param in abnormal_params:
                st.write(f"- {param}")
        else:
            st.success("✅ All input parameters are within optimal range!")
        
        
        show_nearby_doctors("heart disease")

        show_health_summary(
        [age, sex, cp, trestbps, chol, fbs,restecg, thalach, exang, oldpeak, slope, ca, thal],
        ["Age", "Sex", "Chest Pain Type", "Resting BP", "Cholesterol", 
         "Fasting BS", "Resting ECG", "Max HR", "Exercise Angina", 
         "Oldpeak", "ST Slope", "Ca", "Thal"],
        [(18, 65), (0, 1), (0, 1), (90, 120), (125, 200), 
         (0, 99), (0, 0), (60, 100), (0, 0), 
         (0, 1.0), (2, 2), (0, 0), (2, 2)]
    )




# ----------------------- Kidney Disease -----------------------
if selected == "Kidney Disease Prediction":
    check_login()
    st.title("Kidney Disease Prediction")
    cols = st.columns(3)

    labels = [
        "Age", "Blood Pressure", "Specific Gravity", "Albumin", "Sugar",
        "Red Blood Cells (0/1)", "Pus Cell (0/1)", "Pus Cell Clumps (0/1)", "Bacteria (0/1)",
        "Blood Glucose Random", "Blood Urea", "Serum Creatinine", "Sodium", "Potassium",
        "Hemoglobin", "Packed Cell Volume", "White Blood Cell Count", "Red Blood Cell Count",
        "Hypertension (0/1)", "Diabetes Mellitus (0/1)", "Coronary Artery Disease (0/1)",
        "Appetite (0=poor,1=good)", "Pedal Edema (0/1)", "Anemia (0/1)"
    ]

    user_inputs = []

    # Input fields
    for i, label in enumerate(labels):
        col = cols[i % 3]

        if "0/1" in label or label in ["Albumin", "Sugar", "Specific Gravity"]:
            value = col.number_input(label, min_value=0, max_value=100, step=1, key=label)
        else:
            value = col.number_input(label, min_value=0.0, step=0.01, format="%.2f", key=label)

        user_inputs.append(value)

    # Prediction button (loop ke baad)
    if st.button("Predict Kidney Disease"):
        input_data = [float(x) for x in user_inputs]
        prediction = kidney_disease_model.predict([input_data])
        result = "Kidney Disease" if prediction[0] == 1 else "No Kidney Disease"
        st.success(f"The person has {result}")

        # Highlight abnormal kidney parameters
        abnormal_params = []

        if user_inputs[1] > 140:
            abnormal_params.append("Blood Pressure (High)")
        if user_inputs[2] < 1.005:
            abnormal_params.append("Specific Gravity (Low)")
        if user_inputs[3] > 4:
            abnormal_params.append("Albumin (High)")
        if user_inputs[4] > 3:
            abnormal_params.append("Sugar (High)")
        if user_inputs[11] > 1.5:
            abnormal_params.append("Serum Creatinine (High)")
        if user_inputs[10] > 40:
            abnormal_params.append("Blood Urea (High)")
        if user_inputs[14] < 12:
            abnormal_params.append("Hemoglobin (Low)")

        if abnormal_params:
            st.warning("⚠️ Parameters out of optimal range:")
            for param in abnormal_params:
                st.write(f"- {param}")
        else:
            st.success("✅ All input parameters are within optimal range!")

        show_nearby_doctors("kidney disease")

    show_health_summary(
        [
            user_inputs[0],  # Age
            user_inputs[1],  # Blood Pressure
            user_inputs[2],  # Specific Gravity
            user_inputs[3],  # Albumin
            user_inputs[4],  # Sugar
            user_inputs[9],  # Blood Glucose Random
            user_inputs[10], # Blood Urea
            user_inputs[11], # Serum Creatinine
            user_inputs[12], # Sodium
            user_inputs[13], # Potassium
            user_inputs[14], # Hemoglobin
            user_inputs[15], # Packed Cell Volume
            user_inputs[16], # White Blood Cell Count
            user_inputs[17], # Red Blood Cell Count
        ],
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


# ----------------------- Precautions -----------------------
if selected == "Precautions":
    check_login()
    st.title("⚠️Health Precautions")

    disease = st.selectbox("Select Disease", ["Diabetes", "Heart Disease", "Kidney Disease"])

    precautions = {
        "Diabetes": [
            "Eat balanced meals with less sugar.",
            "Exercise at least 30 minutes daily.",
            "Check blood sugar levels regularly.",
            "Avoid junk food and sugary drinks."
        ],
        "Heart Disease": [
            "Avoid smoking and alcohol.",
            "Eat more fruits and vegetables.",
            "Control your cholesterol and blood pressure.",
            "Reduce stress and get enough sleep."
        ],
        "Kidney Disease": [
            "Drink enough water but avoid overhydration.",
            "Avoid too much salt and protein intake.",
            "Monitor blood pressure and sugar levels.",
            "Do not self-medicate with painkillers."
        ]
    }

    specialists = {
        "Diabetes": "Endocrinologist",
        "Heart Disease": "Cardiologist",
        "Kidney Disease": "Nephrologist"
    }

    st.markdown(f"### 💉 Disease: {disease}")
    st.markdown(f"**Recommended Specialist:** {specialists[disease]}")
    st.markdown("#### ✅ Precautions:")
    for p in precautions[disease]:
        st.markdown(f"- {p}")

    st.markdown("---")

    # Detect location automatically
    g = geocoder.ip('me')
    if g.ok:
        location = g.city or "your area"
        st.success(f"📍 Your current location: **{location}**")
    else:
        location = "your city"
        st.warning("Could not detect location automatically.")

    if st.button("🔍 Find Nearby Doctors"):
        st.info("Fetching doctors near you...")

        GOOGLE_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"  # 🔑 Replace with your API key (optional)

        if GOOGLE_API_KEY != "YOUR_GOOGLE_MAPS_API_KEY":
            response = requests.get(
                f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={specialists[disease]}+near+{location}&key={GOOGLE_API_KEY}"
            )
            data = response.json()
            if "results" in data:
                st.subheader(f"👨‍⚕️ {specialists[disease]}s near {location}:")
                for place in data["results"][:5]:
                    st.markdown(f"- **{place['name']}** — {place.get('formatted_address', 'Address not available')}")
            else:
                st.warning("No nearby doctors found.")
        else:
            st.info(f"🔹 Example doctors near {location}:")
            dummy_docs = [
                f"Dr. A. Sharma - {specialists[disease]}",
                f"Dr. B. Patel - {specialists[disease]}",
                f"Dr. C. Khan - {specialists[disease]}"
            ]
            for doc in dummy_docs:
                st.markdown(f"- {doc}")

# ----------------------- User Graphs -----------------------
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
        st.write("### 📋 All Activity Data")
        st.dataframe(df)

        # Convert timestamp column to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        # -------- Activity Count Bar Graph --------
        st.subheader("📈 User Activity Count")
        if 'activity_type' in df.columns:
            activity_counts = df['activity_type'].value_counts()
            fig1, ax1 = plt.subplots()
            activity_counts.plot(kind='bar', ax=ax1, color='skyblue', edgecolor='black')
            ax1.set_xlabel("Activity Type")
            ax1.set_ylabel("Count")
            ax1.set_title("User Activity Distribution")
            st.pyplot(fig1)
        else:
            st.warning("No 'activity_type' column found in data.")

        # -------- Prediction Result Pie Chart --------
        st.subheader("🩺 Prediction Result Distribution")
        disease_df = df[df['activity_type'].str.contains('Prediction', case=False, na=False)]

        if not disease_df.empty and 'result' in disease_df.columns:
            result_counts = disease_df['result'].value_counts()
            fig2, ax2 = plt.subplots()
            result_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax2, startangle=90)
            ax2.set_ylabel('')
            ax2.set_title("Prediction Results")
            st.pyplot(fig2)
        else:
            st.info("No prediction data yet.")
