import joblib
import numpy as np
import pandas as pd

# Loading model and scaler
model = joblib.load("artifacts/xgb_model.joblib")
scaler_data = joblib.load("artifacts/scaler_with_columns.joblib")

scaler = scaler_data["scaler"]
cols_to_scale = scaler_data["cols_to_scale}"] if "cols_to_scale}" in scaler_data else None # there was a small typo while saving name hence a extra}

# Inference  model feature names
FEATURES = getattr(model, "feature_names_in_", None)
if FEATURES is None:
    raise ValueError("Model does not contain feature_names_in_. You must save features during training.")

# Category maps
PLAN_MAP = {"Bronze": 1, "Silver": 2, "Gold": 3}

SMOKING_MAP = {
    "Not Smoking": "No Smoking",
    "Does Not Smoke": "No Smoking",
    "Smoking=0": "No Smoking",
    "Smoking": "Smoking",
    "No Smoking": "No Smoking"
}

NOMINAL_COLS = [
    "gender", "region", "marital_status",
    "bmi_category", "smoking_status", "employment_status"
]


def prepare_input(
    age,
    number_of_dependants,
    income_lakhs,
    insurance_plan,
    genetical_risk,
    normalized_risk_score,
    gender,
    region,
    marital_status,
    bmi_category,
    smoking_status,
    employment_status
):
    # Normalize category values
    plan_val = PLAN_MAP.get(insurance_plan, 2)  # default Silver
    smoking_val = SMOKING_MAP.get(smoking_status, smoking_status)

    data = {
        "age": age,
        "number_of_dependants": number_of_dependants,
        "income_lakhs": income_lakhs,
        "insurance_plan": plan_val,
        "genetical_risk": genetical_risk,
        "normalized_risk_score": normalized_risk_score,
        "gender": gender,
        "region": region,
        "marital_status": marital_status,
        "bmi_category": bmi_category,
        "smoking_status": smoking_val,
        "employment_status": employment_status
    }

    df = pd.DataFrame([data])

    # One hot encoding
    df = pd.get_dummies(df, columns=NOMINAL_COLS, drop_first=True, dtype=int)

    # Handling scaler columns
    if cols_to_scale:
        for col in cols_to_scale:
            if col not in df.columns:
                df[col] = 0
        df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # Align with model features
    for col in FEATURES:
        if col not in df.columns:
            df[col] = 0

    df = df[FEATURES]

    return df


def predict_premium(**kwargs):
    input_df = prepare_input(**kwargs)
    prediction = model.predict(input_df)[0]
    return float(prediction)