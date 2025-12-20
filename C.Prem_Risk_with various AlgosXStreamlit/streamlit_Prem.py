# Streamlit → PredictionHelper → XGBoost → Streamlit



import streamlit as st
from PredictionHelper_Premium import predict_premium

st.set_page_config(page_title="Susnata Health Premium Predictor", page_icon="💊", layout="wide")

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
    try:
        premium = predict_premium(
            age=age,
            number_of_dependants=number_of_dependants,
            income_lakhs=income_lakhs,
            insurance_plan=insurance_plan,
            genetical_risk=genetical_risk,
            normalized_risk_score=normalized_risk_score,
            gender=gender,
            region=region,
            marital_status=marital_status,
            bmi_category=bmi_category,
            smoking_status=smoking_status,
            employment_status=employment_status
        )
        st.success(f"Predicted Premium: ₹ {premium:.2f}")
    except Exception as e:
        st.error(f"Error: {e}")