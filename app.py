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
diabetes_model = pickle.load(open(r'C:\Users\rajsh\OneDrive\Documents\Multi Desease Prediction\-Human-Disease-Prediction-\diabetes.pkl', 'rb'))
heart_disease_model = pickle.load(open(r'C:\Users\rajsh\OneDrive\Documents\Multi Desease Prediction\-Human-Disease-Prediction-\heart.pkl', 'rb'))
kidney_disease_model = pickle.load(open(r'C:\Users\rajsh\OneDrive\Documents\Multi Desease Prediction\-Human-Disease-Prediction-\kidney.pkl', 'rb'))
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
            "Nearby Doctors & Precautions",  # ✅ New
            "About", "Developer", "Contact Us", "User Graphs", "Exit"
        ],
        icons=['house', 'person', 'activity', 'heart', 'person', 'map', 'info-circle',
               'person-circle', 'envelope', 'bar-chart', 'x-circle'],
        default_index=0
    )

# ----------------------- Login Check -----------------------
def check_login():
    if not st.session_state.get('logged_in'):
        st.markdown("""
        <div style="padding:10px; border:1px solid #ccc; border-radius:5px;">
        Please login first to access prediction tools.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# ----------------------- User Login / Signup -----------------------
if selected == "User Login":
    st.title("🔐 User Login / Signup")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user = get_user(login_user)
            if user and verify_password(login_pass, user[1]):
                st.success(f"Welcome, {login_user}! ✅")
                st.session_state['logged_in'] = True
                st.session_state['username'] = login_user

                # log login
                c.execute("INSERT INTO user_activity (username, activity_type, result) VALUES (?, ?, ?)",
                          (login_user, 'Login', 'Success'))
                conn.commit()
            elif user:
                st.error("Incorrect password ❌")
            else:
                st.error("Username not found. Please signup first.")

        if st.session_state.get('logged_in'):
            if st.button("Logout"):
                # log logout
                c.execute("INSERT INTO user_activity (username, activity_type, result) VALUES (?, ?, ?)",
                          (st.session_state['username'], 'Logout', 'Success'))
                conn.commit()
                st.session_state['logged_in'] = False
                st.session_state['username'] = ""
                st.success("Logged out successfully.")

    with col2:
        st.subheader("Create a New Account")
        new_user = st.text_input("New Username", key="new_user")
        new_pass = st.text_input("New Password", type="password", key="new_pass")
        if st.button("Signup"):
            if not new_user or not new_pass:
                st.warning("Please enter username and password.")
            elif get_user(new_user):
                st.warning("Username already exists. Choose another.")
            else:
                add_user(new_user, new_pass)
                c.execute("INSERT INTO user_activity (username, activity_type, result) VALUES (?, ?, ?)",
                          (new_user, 'Signup', 'Success'))
                conn.commit()
                st.success("Account created successfully! Please login now.")

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
        <li><b>Sakshi Jha:</b> Backend & Database Developer, responsible for SQLite integration and user management. <br>Email: jhasakshi18@eng.rizvi.edu.in</li>
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

# ----------------------- Nearby Doctors & Precautions -----------------------
if selected == "Nearby Doctors & Precautions":
    check_login()
    st.title("🩺 Nearby Doctors & Health Precautions")

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

    st.markdown(f"### 🧠 Disease: {disease}")
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

    df = pd.read_sql_query("SELECT * FROM user_activity ORDER BY timestamp", conn, parse_dates=['timestamp'])
    if df.empty:
        st.info("No activity data yet.")
    else:
        st.write("### All Activity Data")
        st.dataframe(df)

        st.subheader("User Activity Count")
        activity_counts = df['activity_type'].value_counts()
        fig1, ax1 = plt.subplots()
        activity_counts.plot(kind='bar', ax=ax1)
        ax1.set_xlabel("Activity Type")
        ax1.set_ylabel("Count")
        st.pyplot(fig1)

        st.subheader("Prediction Result Distribution")
        disease_df = df[df['activity_type'].str.contains('Prediction')]
        if not disease_df.empty:
            result_counts = disease_df['result'].value_counts()
            fig2, ax2 = plt.subplots()
            result_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
            ax2.set_ylabel('')
            st.pyplot(fig2)
        else:
            st.info("No prediction data yet.")
