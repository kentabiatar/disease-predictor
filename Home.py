import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Page configuration
st.set_page_config(
    page_title="Health Forecast AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load Lottie animation
lottie_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_HpFqiS.json")

# Title and subtitle
st.title("🌦️ Health Forecast AI")
st.subheader("Predicting health risks using weather & gender data.")

left, right = st.columns(2, vertical_alignment="center")

# Display Lottie animation
with left:
    if lottie_animation:
        st_lottie(lottie_animation, height=300, key="health")

# Introduction
with right:
    st.markdown("""
    Our **XGBoost-powered model** helps anticipate potential health conditions by analyzing real-time **weather conditions** and **user demographics**. It's more than a tool—it's your personal health radar.
    """)

    # Expandable section: Why This Model Matters
    with st.expander("🌍 Why This Model Matters"):
        st.markdown("""
        - **Climate and health are deeply connected**: Rising humidity or cold snaps can trigger asthma, infections, joint pain, and more.
        - **Personalized healthcare**: Gender-based differences in symptom response are real. Our model personalizes predictions based on *you*.
        - **Preventive care**: Early warnings can lead to timely interventions, potentially saving lives.
        """)

    # Expandable section: How It Works
    with st.expander("🔬 How It Works"):
        st.markdown("""
        Our `model uses the **XGBoost algorithm**, trained on real health incident data, local weather patterns, and gender demographics. It analyzes:
        - Temperature, humidity, rainfall
        - Gender-specific health patterns
        - Feature importance optimization via gradient boosting

        It then returns a **risk level** for common diseases, helping users make informed decisions.
        """)
        
    if st.button("Try me out!"):
        st.switch_page("./pages/Health_Forecast.py")

# Footer
st.markdown("---")
st.markdown("© 2025 Health Forecast AI Team. All rights reserved. Developed by Priska, Dzaky, Fadzar, and Kent.")
