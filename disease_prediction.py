import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

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

    st.success("✅ Form submitted. Here’s the final input:")
    st.json(user_input)
