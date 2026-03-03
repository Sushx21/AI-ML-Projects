# streamlit run streamlit_app.py
import streamlit as st
import requests

API_URL = "http://localhost:9000/predict_premium"

st.set_page_config(
    page_title="Susnata Health Premium Predictor",
    page_icon="💊",
    layout="wide"
)

st.title("Susnata Health Premium Cost Predictor")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", 1, 100, 30)
    number_of_dependants = st.number_input("Dependants", 0, 10, 0)
    income_lakhs = st.number_input("Income (Lakhs)", 0.0, 1000.0, 10.0)

with col2:
    insurance_plan = st.selectbox("Insurance Plan", ["Bronze", "Silver", "Gold"])
    genetical_risk = st.number_input("Genetical Risk", 0.0, 1.0, 0.0)
    employment_status = st.selectbox("Employment Status", ["Salaried", "Self Employed", "Unemployed"])

with col3:
    gender = st.selectbox("Gender", ["Male", "Female"])
    marital_status = st.selectbox("Marital Status", ["Unmarried", "Married"])
    bmi_category = st.selectbox("BMI Category", ["Underweight", "Normal", "Overweight"])
    smoking_status = st.selectbox("Smoking Status", ["No Smoking", "Smoking"])

region = st.selectbox("Region", ["East", "West", "North", "South"])
normalized_risk_score = st.slider("Normalized Risk Score", 0.0, 1.0, 0.2)

if st.button("Predict"):
    payload = {
        "age": age,
        "number_of_dependants": number_of_dependants,
        "income_lakhs": income_lakhs,
        "insurance_plan": insurance_plan,
        "genetical_risk": genetical_risk,
        "normalized_risk_score": normalized_risk_score,
        "gender": gender,
        "region": region,
        "marital_status": marital_status,
        "bmi_category": bmi_category,
        "smoking_status": smoking_status,
        "employment_status": employment_status
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Premium: ₹ {result['predicted_premium']:.2f}")
        else:
            st.error(f"API Error: {response.text}")
    except Exception as e:
        st.error(f"Error connecting to API: {e}")