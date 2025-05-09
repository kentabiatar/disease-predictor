import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import joblib
from streamlit_echarts import st_echarts

load_dotenv()
API_KEY = st.secrets["api"]["weather_key"]

indonesia_cities = [
    "Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Palembang", "Makassar",
    "Batam", "Pekanbaru", "Yogyakarta", "Malang", "Denpasar", "Manado", "Padang",
    "Balikpapan", "Banjarmasin", "Samarinda", "Pontianak", "Kupang", "Jayapura"
]

st.set_page_config(page_title="Disease Prediction", layout="wide")
st.title("🩺 Disease Prediction Form")

# --- AGE & GENDER ---
col1, col2 = st.columns(2)

with col1:
    age = st.selectbox("Select Age", list(range(1, 101)))

with col2:
    gender_text = st.selectbox("Select Gender", ["Male", "Female"])
    gender = 1 if gender_text == "Male" else 0  # 1 = Male, 0 = Female

# --- WEATHER DATA PLACEHOLDER ---
st.markdown("### 🌦️ Current Weather Data")
city = st.selectbox("📍 Select your city in Indonesia:", indonesia_cities)

# Default values (in case API fails)
temperature = 0.0
humidity = 0.0
wind_speed = 0.0

if city:
    # --- WeatherAPI Call ---
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = round(data["current"]["temp_c"], 2)
        humidity = round(data["current"]["humidity"], 2)
        wind_speed = round(data["current"]["wind_kph"], 2)


    else:
        st.error("❌ Failed to fetch weather data. Check your API key or try again later.")

col3, col4, col5 = st.columns(3)

with col3:
    temperature = round(st.number_input("Temperature (°C)", value=float(temperature), step=0.01), 2)

with col4:
    humidity = round(st.number_input("Humidity (%)", value=float(humidity), step=0.01), 2)

with col5:
    wind_speed = round(st.number_input("Wind Speed (km/h)", value=float(wind_speed), step=0.01), 2)

# --- SYMPTOM CHECKBOXES ---
st.markdown("### ✅ Check the box if you feel any of the following:")

symptom_labels = [
    "nausea", "joint_pain", "abdominal_pain", "high_fever", "chills",
    "fatigue", "runny_nose", "pain_behind_the_eyes", "dizziness", "headache",
    "chest_pain", "vomiting", "cough", "shivering", "asthma_history",
    "high_cholesterol", "diabetes", "obesity", "hiv_aids", "nasal_polyps",
    "asthma", "high_blood_pressure", "severe_headache", "weakness",
    "trouble_seeing", "fever", "body_aches", "sore_throat", "sneezing",
    "diarrhea", "rapid_breathing", "rapid_heart_rate", "swollen_glands",
    "rashes", "sinus_headache", "facial_pain", "shortness_of_breath",
    "reduced_smell_and_taste", "skin_irritation", "itchiness",
    "throbbing_headache", "confusion", "back_pain", "knee_ache"
]

symptom_labels.sort()

# Responsive columns for symptoms
cols = st.columns(4)

symptoms = {}
for i, label in enumerate(symptom_labels):
    with cols[i % 4]:
        symptoms[label] = 1 if st.checkbox(label.replace("_", " ").title()) else 0

# --- SUBMIT ---
if st.button("Submit"):
    user_input = {
        "age": age,
        "gender": gender,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        **symptoms
    }

    user_input_df = pd.DataFrame([user_input])
    user_input_df.rename(columns={"gender" : "gender_Male"}, inplace=True)
    
    # Load the model
    model = joblib.load("xgboost_model.pkl")
    y_encoder = joblib.load("label_encoder.pkl")
    feature_cols = joblib.load("feature_columns.pkl")
    user_input_df = user_input_df.reindex(columns=feature_cols, fill_value=0)

    st.success("✅ Form submitted.")
    probas = model.predict_proba(user_input_df)[0]
    top5_idx = probas.argsort()[-5:][::-1]
    top5_diseases = y_encoder.classes_[top5_idx]
    top5_probs = probas[top5_idx]
    
    left, right = st.columns(2, vertical_alignment="center")
    
    with left:
        options = {
            "tooltip": {"trigger": "item"},
            "legend": {"top": "5%", "left": "center", "textStyle": {
                                                        "color": "#fff"
                                                    }},
            "series": [
                {
                    "name": "result",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "avoidLabelOverlap": False,
                    "itemStyle": {
                        "borderRadius": 10,
                        "borderColor": "#fff",
                        "borderWidth": 2,
                    },
                    "label": {"show": False, "position": "center", "color": "#FFF"},
                    "emphasis": {
                        "label": {"show": True, "fontSize": "25", "fontWeight": "bold", "color": "#FFF"}
                    },
                    "labelLine": {"show": False},
                    "data": [
                        {"value": float(top5_probs[0]*100), "name": top5_diseases[0]},
                        {"value": float(top5_probs[1]*100), "name": top5_diseases[1]},
                        {"value": float(top5_probs[2]*100), "name": top5_diseases[2]},
                        {"value": float(top5_probs[3]*100), "name": top5_diseases[3]},
                        {"value": float(top5_probs[4]*100), "name": top5_diseases[4]},
                    ],
                }
            ],
        }
        
        st_echarts(
            options=options, height="500px",
        )
        
    with right:
        st.markdown("### 🧠 Prediction Result")
        st.markdown("You most likely have one of the following conditions, based on your input:")
        for i in range(5):
            st.markdown(f"**Top {i+1} Prediction:** {top5_diseases[i]} — {top5_probs[i]*100:.2f}%")

        # st.json(user_input)