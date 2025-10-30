Human Multiple Disease Detection System
AI-powered web application for early detection of Diabetes, Heart Disease, and Kidney Disease using Machine Learning.

**Abstract** This project presents an AI-powered web application designed for early detection of three critical diseases: Diabetes, Heart Disease, and Kidney Disease. The system leverages Machine Learning algorithms (Random Forest and risk-based scoring) to analyze health parameters and provide instant predictions.
Built using Python and Streamlit, the platform offers a user-friendly interface where patients can input their health data and receive immediate results along with visual analytics. The system analyzes 8 parameters for Diabetes, 13 parameters for Heart Disease, and 24 parameters for Kidney Disease to generate accurate predictions.
Key features include secure user authentication, interactive health graphs, nearby doctor recommendations using Google Maps API, personalized health precautions, and prediction history tracking. All user data is securely stored in an SQLite database with encrypted passwords.
The primary objective is to promote early disease detection and raise health awareness by making medical predictions accessible to everyone. The system achieves approximately 90-95% accuracy across all three disease predictions, making it a reliable tool for preliminary health assessment.

Project members
Sakshi Jha [Team Leader]
Anshika Shukla
Saifee Humaira
Khan Zaara

🎯 Features

🔬 Disease Prediction - Predict 3 major diseases using ML models
📊 Health Analytics - Visual graphs and parameter analysis
🏥 Doctor Finder - Locate nearby specialists via Google Maps API
🛡️ Health Precautions - Diet plans, tips, and warning signs
📈 User Dashboard - Track prediction history and analytics
🔐 Secure Login - User authentication with encrypted passwords


🛠️ Tech Stack

Frontend: Streamlit, HTML/CSS
Backend: Python 3.8+, SQLite
ML: Scikit-learn, NumPy, Pandas
APIs: Google Maps API, Geocoder
Visualization: Matplotlib


📦 Installation
1. Clone Repository
bashgit clone https://github.com/yourusername/disease-detection-system.git
cd disease-detection-system
2. Install Dependencies
bashpip install -r requirements.txt
3. Set Up Environment
Create .env file:
envGOOGLE_API_KEY=your_api_key_here
4. Add ML Models
Place these files in root directory:

diabetes.pkl
heart.pkl
kidney.pkl

5. Run Application
   python -m streamlit run app.py
Open browser at http://localhost:8501

📋 Requirements
txtstreamlit==1.28.0
streamlit-option-menu==0.3.6
scikit-learn==1.3.0
pandas==2.0.3
matplotlib==3.7.2
bcrypt==4.0.1
python-dotenv==1.0.0
geocoder==1.38.1
requests==2.31.0

🚀 Usage

Login/Signup - Create account or login
Select Disease - Choose from Diabetes, Heart, or Kidney
Enter Parameters - Input health data
Get Results - View prediction, graphs, and recommendations
Find Doctors - Locate nearby specialists
View Analytics - Track your health history


🧠 Disease Models
DiseaseParametersAlgorithmDiabetes8Random Forest + Polynomial FeaturesHeart Disease13Random Forest ClassifierKidney Disease24Risk-based Scoring System# Multiple_Disease_Prediction
