import streamlit as st 
import pickle 
import os
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Mulitple Disease Prediction",layout="wide", page_icon="👨‍🦰🤶")

working_dir = os.path.dirname(os.path.abspath(__file__))


diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes.pkl','rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart.pkl','rb'))
kidney_disease_model = pickle.load(open(f'{working_dir}/saved_models/kindey.pkl','rb'))

NewBMI_Overweight=0
NewBMI_Underweight=0
NewBMI_Obesity_1=0
NewBMI_Obesity_2=0 
NewBMI_Obesity_3=0
NewInsulinScore_Normal=0 
NewGlucose_Low=0
NewGlucose_Normal=0 
NewGlucose_Overweight=0
NewGlucose_Secret=0

with st.sidebar:
    selected = option_menu("Mulitple Disease Prediction", 
                ['Home',
                'Diabetes Prediction',
                 'Heart Disease Prediction',
                 'Kidney Disease Prediction',
                 'about',
                 'developer',
                 'contact us',
                 'Exit'],
                 menu_icon='hospital-fill',
                 icons=['house','activity','heart', 'person' , 'info-circle', 'person-circle', 'envelope', 'x-circle'],
                 default_index=0)
    

# ---------------------- Home Section ---------------------- #
if(selected=='Home'):
    
    #page title
    st.title('HUMAN MULTIPLE DISEASE DETECTION SYSTEM')
    #st.image("C:\Users
    
    \OneDrive\Desktop\Multiple_Disease_Prediction-main\healthcare.jpg")
    st.markdown("""
    # Welcome to the Human Multiple Disease Detection System! 🔍
                
    Your health matters, and early detection can make all the difference. Many diseases progress silently, and timely detection can lead to more effective treatment. Our system is designed to assist in identifying multiple human diseases efficiently using **state-of-the-art machine learning techniques**. With just a few simple steps, you can analyze medical data and gain valuable insights into potential health risks.

    This AI-powered system utilizes deep learning and advanced medical data analysis techniques to help users detect diseases early, providing a **fast, reliable, and user-friendly experience**.

    ---
    
    ## How It Works ⚙️
    1. **Provide Health Information:** Navigate to the **Any Disease Recognition** page and input the relevant test data for the suspected disease.
    2. **Advanced AI-Powered Analysis:** Our machine learning model processes the data using deep learning techniques to detect patterns and identify potential diseases.
    3. **Instant Results & Recommendations:** View a detailed breakdown of the results, along with potential next steps for medical consultation and treatment.

    ---
    
    ## Why Choose Us? 🌟
    - **🔬 High Accuracy:** Our system leverages advanced machine learning models trained on large medical datasets to ensure precise disease detection.
    - **🖥️ User-Friendly Interface:** Designed for ease of use, making it accessible for healthcare professionals and general users alike.
    - **⚡ Fast and Efficient:** Receive results in seconds, enabling prompt decision-making and proactive health management.
    - **🩺 Multi-Disease Detection:** Detect a range of diseases with a single system, improving diagnostic efficiency and reliability.
    - **🔒 Secure & Private:** We prioritize user data privacy and security, ensuring that all uploaded medical data is processed securely and not stored.

    ---
    
    ## Get Started 🚀
    Click on the **Any Disease Recognition** page in the sidebar to upload your test results or input relevant data. Experience the power of AI-driven disease detection and take control of your health today!
    
    Supported diseases:
    - ✅ Diabetes Detection
    - ✅ kidney Detection
    - ✅ Heart Disease Detection
    - ✅ More diseases coming soon!
    
    ---
    
    ## About Us 📖
    Want to know more about how this system works? Visit the **About** page to explore details about our machine learning models, medical datasets, and research methodologies powering this innovative disease detection platform.
    
    **Your health is our priority. Let’s work together to ensure a healthier future! 💙🌍**
    """)

#About Page
if(selected=="about"):
    st.title("About")
    
    st.markdown("""
                ## 🏥 About This Web Application
                
                This Web Application is created by **CODEWHIZZKID** to assist in disease prediction using machine learning models trained on various medical datasets. 
                The application is designed to provide **accurate** 🧠 and **efficient** ⏳ predictions for different diseases based on patient data, enhancing early diagnosis and decision-making.

                ### 📊 About the Dataset
                The datasets used in this project have been **preprocessed and standardized** 📌 to ensure high accuracy and reliability. 
                The original datasets have undergone transformations such as **normalization**, **feature scaling**, and **handling missing values** to improve model performance.
                The dataset is divided into an **80/20 ratio** ⚖️ for training and testing while maintaining the original directory structure.

                ### ⚡ Features of This Application:
                - 🖥️ **User-Friendly Interface**: Easy navigation and seamless user experience.
                - 🏥 **Multiple Disease Prediction**: Supports classification for **Diabetes, Heart Disease, kidney Disease**.
                - 🔍 **Data Standardization & Preprocessing**: Ensures improved model accuracy by handling missing values and normalizing input features.
                - 🔒 **Secure & Efficient Processing**: Data is processed securely, and results are provided instantly.
                - 🚀 **Real-Time Predictions**: Users can upload patient data and receive **immediate** predictions based on the trained model.

                ### 📂 Datasets Used:
                The following datasets have been used in training the models:

                1. **Diabetes Dataset** - [📥 Download](https://www.dropbox.com/scl/fi/0uiujtei423te1q4kvrny/diabetes.csv?rlkey=20xvytca6xbio4vsowi2hdj8e&e=1&dl=0)
                4. **Heart Disease Dataset** - [📥 Download](https://drive.google.com/file/d/1CEql-OEexf9p02M5vCC1RDLXibHYE9Xz/view)
                5. **kidney Disease Dataset** - [📥 Download](https://www.kaggle.com/datasets/francismon/curated-colon-dataset-for-deep-learning)
   
                ### 🔮 Future Enhancements:
                - 🔗 Adding more **disease datasets** to expand prediction capabilities.
                - 🧠 Implementing a **Deep Learning model** to improve accuracy.
                - 📝 Enabling **real-time patient data input** via forms for better usability.

                This application aims to **leverage machine learning for improving healthcare predictions** and assisting medical professionals in decision-making. ❤️‍🩹
                """)

#developer 
if(selected=="developer"):
    st.title("About Humaira Saifee 👨‍💻")
    st.header("Your AI & ML Engineer")
    
    st.subheader("Meet the Developer")
    st.write("""
    Hello, I'm **Humaira Saifee**, your AI and Machine Learning Engineer with 1 years of experience in the field. I am passionate about harnessing the power of technology to make a positive impact on people's lives. Allow me to share a bit about my journey in the world of artificial intelligence and machine learning.
    """)

    st.subheader("My Expertise")
    st.write("""
    With a strong academic background in computer science and a deep fascination for AI and ML, I embarked on a journey that has taken me across the globe, working on diverse and innovative projects. Over the years, I've had the privilege of collaborating on international projects that have pushed the boundaries of what's possible in AI and ML.
    """)

    st.subheader("A Commitment to Excellence")
    st.write("""
    My work is driven by a commitment to excellence and a belief that technology should be accessible and beneficial to everyone. Whether it's developing predictive models, creating intelligent algorithms, or designing user-friendly interfaces, I strive for solutions that are both cutting-edge and user-centric.
    """)

    st.subheader("Passion for Health Tech")
    st.write("""
    The development of **Multiple disease prediction using machine learning** represents a convergence of my passion for AI and my dedication to improving healthcare accessibility. I believe that AI has the potential to transform the way we approach healthcare, making it more personalized and informative. This platform is a testament to that vision.
    """)

    st.subheader("Join Me on this Journey")
    st.write("""
    I invite you to explore **Multiple disease prediction using machine learning** and experience firsthand the fusion of AI and healthcare. Together, we can empower individuals with knowledge, promote well-being, and contribute to a brighter and healthier future.
    """)

#About Page
if(selected=="contact us"):
    st.title("📞 Contact Us")
    st.write("Have questions or need assistance? We're here to help!")

    st.subheader("Customer Support")
    st.write("""
    Our dedicated customer support team is available to assist you with any inquiries or issues you may have. Whether it's a technical question, feedback, or a general inquiry, we're just a message away.
    """)

    st.subheader("Get in Touch")
    st.write("""
    Feel free to reach out to us via email or through the contact form below. We value your feedback and are committed to providing you with the best possible experience.
    """)
    st.markdown("📧 **Email:** humairasaifee25@gmail.com")
    st.markdown("📞 **Phone:** 9152858705")

    st.subheader("Stay Connected")
    st.write("""
    Stay up-to-date with the latest news, updates, and health tips by following us on social media. Connect with us on **Facebook** or **Instagram** to join our growing community.
    """)

    st.subheader("📍 Location")
    st.write("Mumbai, Maharashtra - 400050")




if selected == 'Diabetes Prediction':
    st.title("Diabetes Prediction Using Machine Learning")

    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input("Number of Pregnancies")
    with col2:
        Glucose = st.text_input("Glucose Level")
    with col3:
        BloodPressure = st.text_input("BloodPressure Value")
    with col1:
        SkinThickness = st.text_input("SkinThickness Value")
    with col2:
        Insulin = st.text_input("Insulin Value")
    with col3:
        BMI = st.text_input("BMI Value")
    with col1:
        DiabetesPedigreeFunction = st.text_input("DiabetesPedigreeFunction Value")
    with col2:
        Age = st.text_input("Age")

    diabetes_result = ""

    # Check if all inputs are filled before enabling submit
    all_inputs = [Pregnancies, Glucose, BloodPressure, SkinThickness,
                  Insulin, BMI, DiabetesPedigreeFunction, Age]
    
    if st.button("Diabetes Test Result"):
        if all(x.strip() != "" for x in all_inputs):
            # Initialize all derived feature variables
            NewBMI_Underweight = NewBMI_Overweight = NewBMI_Obesity_1 = 0
            NewBMI_Obesity_2 = NewBMI_Obesity_3 = 0
            NewInsulinScore_Normal = 0
            NewGlucose_Low = NewGlucose_Normal = NewGlucose_Overweight = NewGlucose_Secret = 0

            # BMI categories
            if float(BMI) <= 18.5:
                NewBMI_Underweight = 1
            elif 18.5 < float(BMI) <= 24.9:
                pass  # Normal BMI
            elif 24.9 < float(BMI) <= 29.9:
                NewBMI_Overweight = 1
            elif 29.9 < float(BMI) <= 34.9:
                NewBMI_Obesity_1 = 1
            elif 34.9 < float(BMI) <= 39.9:
                NewBMI_Obesity_2 = 1
            elif float(BMI) > 39.9:
                NewBMI_Obesity_3 = 1

            # Insulin score
            if 16 <= float(Insulin) <= 166:
                NewInsulinScore_Normal = 1

            # Glucose levels
            if float(Glucose) <= 70:
                NewGlucose_Low = 1
            elif 70 < float(Glucose) <= 99:
                NewGlucose_Normal = 1
            elif 99 < float(Glucose) <= 126:
                NewGlucose_Overweight = 1
            elif float(Glucose) > 126:
                NewGlucose_Secret = 1

            # Final user input for model
            user_input = [float(Pregnancies), float(Glucose), float(BloodPressure),
                          float(SkinThickness), float(Insulin), float(BMI),
                          float(DiabetesPedigreeFunction), float(Age),
                          NewBMI_Underweight, NewBMI_Overweight, NewBMI_Obesity_1,
                          NewBMI_Obesity_2, NewBMI_Obesity_3, NewInsulinScore_Normal,
                          NewGlucose_Low, NewGlucose_Normal, NewGlucose_Overweight,
                          NewGlucose_Secret]

            prediction = diabetes_model.predict([user_input])
            if prediction[0] == 1:
                diabetes_result = "The person is diabetic"
            else:
                diabetes_result = "The person is not diabetic"
        else:
            st.warning("⚠️ Please fill in all the fields before submitting.")

    st.success(diabetes_result)

# heart disease 
if selected == 'Heart Disease Prediction':
    st.title("💓 Heart Disease Prediction Using Machine Learning")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input("Age")
    with col2:
        sex = st.text_input("Sex (0 = Female, 1 = Male)")
    with col3:
        cp = st.text_input("Chest Pain Type (0–3)")
    with col1:
        trestbps = st.text_input("Resting Blood Pressure (mm Hg)")
    with col2:
        chol = st.text_input("Serum Cholesterol (mg/dl)")
    with col3:
        fbs = st.text_input("Fasting Blood Sugar > 120 mg/dl (1 = True, 0 = False)")
    with col1:
        restecg = st.text_input("Resting ECG (0–2)")
    with col2:
        thalach = st.text_input("Maximum Heart Rate Achieved")
    with col3:
        exang = st.text_input("Exercise Induced Angina (1 = Yes, 0 = No)")
    with col1:
        oldpeak = st.text_input("ST Depression Induced by Exercise")
    with col2:
        slope = st.text_input("Slope of Peak Exercise ST Segment (0–2)")
    with col3:
        ca = st.text_input("Major Vessels Colored by Fluoroscopy (0–3)")
    with col1:
        thal = st.text_input("Thal (1 = Normal, 2 = Fixed Defect, 3 = Reversible Defect)")

    heart_disease_result = ""

    if st.button("Get Heart Disease Prediction"):
        try:
            user_input = list(map(float, [
                age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                exang, oldpeak, slope, ca, thal
            ]))
            prediction = heart_disease_model.predict([user_input])
            if prediction[0] == 1:
                heart_disease_result = "🚨 This person **has heart disease.**"
            else:
                heart_disease_result = "✅ This person **does not have heart disease.**"
        except ValueError:
            st.error("❌ Please enter valid numerical values in all fields.")

    if heart_disease_result:
        st.success(heart_disease_result)


if selected == 'Kidney Disease Prediction':
    st.title("🧪 Kidney Disease Prediction Using Machine Learning")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        age = st.text_input('Age')
    with col2:
        blood_pressure = st.text_input('Blood Pressure')
    with col3:
        specific_gravity = st.text_input('Specific Gravity')
    with col4:
        albumin = st.text_input('Albumin')
    with col5:
        sugar = st.text_input('Sugar')

    with col1:
        red_blood_cells = st.text_input('Red Blood Cells (0 = Normal, 1 = Abnormal)')
    with col2:
        pus_cell = st.text_input('Pus Cell (0 = Normal, 1 = Abnormal)')
    with col3:
        pus_cell_clumps = st.text_input('Pus Cell Clumps (0 = No, 1 = Yes)')
    with col4:
        bacteria = st.text_input('Bacteria (0 = No, 1 = Yes)')
    with col5:
        blood_glucose_random = st.text_input('Blood Glucose Random')

    with col1:
        blood_urea = st.text_input('Blood Urea')
    with col2:
        serum_creatinine = st.text_input('Serum Creatinine')
    with col3:
        sodium = st.text_input('Sodium')
    with col4:
        potassium = st.text_input('Potassium')
    with col5:
        hemoglobin = st.text_input('Hemoglobin')

    with col1:
        packed_cell_volume = st.text_input('Packed Cell Volume')
    with col2:
        white_blood_cell_count = st.text_input('White Blood Cell Count')
    with col3:
        red_blood_cell_count = st.text_input('Red Blood Cell Count')
    with col4:
        hypertension = st.text_input('Hypertension (0 = No, 1 = Yes)')
    with col5:
        diabetes_mellitus = st.text_input('Diabetes Mellitus (0 = No, 1 = Yes)')

    with col1:
        coronary_artery_disease = st.text_input('Coronary Artery Disease (0 = No, 1 = Yes)')
    with col2:
        appetite = st.text_input('Appetite (0 = Good, 1 = Poor)')
    with col3:
        peda_edema = st.text_input('Pedal Edema (0 = No, 1 = Yes)')
    with col4:
        anemia = st.text_input('Anemia (0 = No, 1 = Yes)')

    kidney_disease_result = ""

    if st.button("Get Kidney Disease Prediction"):
        try:
            user_input = list(map(float, [
                age, blood_pressure, specific_gravity, albumin, sugar,
                red_blood_cells, pus_cell, pus_cell_clumps, bacteria,
                blood_glucose_random, blood_urea, serum_creatinine, sodium,
                potassium, hemoglobin, packed_cell_volume,
                white_blood_cell_count, red_blood_cell_count, hypertension,
                diabetes_mellitus, coronary_artery_disease, appetite,
                peda_edema, anemia
            ]))

            prediction = kidney_disease_model.predict([user_input])

            if prediction[0] == 1:
                kidney_disease_result = "🚨 This person **has kidney disease.**"
            else:
                kidney_disease_result = "✅ This person **does not have kidney disease.**"
        except ValueError:
            st.error("❌ Please enter valid numerical values in all fields.")

    if kidney_disease_result:
        st.success(kidney_disease_result)



if selected == 'Exit':
    st.title("Exit Confirmation 🛑")
    st.write("Are you sure you want to exit now?")
    
    st.markdown(
        """
        <a href="http://localhost:5501/index.html" target="_self">
            <button style="background-color: #f44336; color: white; padding: 12px 20px; border: none; border-radius: 8px; font-size: 16px;">
                ❌ Exit to Homepage
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

