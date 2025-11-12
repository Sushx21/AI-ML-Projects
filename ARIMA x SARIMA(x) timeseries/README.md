# ✈️ Time Series Forecasting using SARIMAX (with Log Transformation + Exogenous Variable)

## 📘 Overview
This project demonstrates **SARIMAX (Seasonal AutoRegressive Integrated Moving Average with eXogenous variables)** modeling 
on an airline passenger dataset.  
The goal is to forecast future air travel demand while accounting for both **seasonality** and an **external factor** (`is_summer`) 
representing higher air traffic during summer months.

---

##  Steps Involved

1. **Data Loading**  
   - The dataset contains `month`, `air` (passenger counts), and `is_summer` (0 or 1).
   - Missing values were checked and the date column was set as the time index.

2. **Log Transformation**  
   - Applied to stabilize variance and convert multiplicative seasonality into an additive form.

3. **Stationarity Testing**  
   - Performed **ADF (Augmented Dickey–Fuller)** and **KPSS (Kwiatkowski–Phillips–Schmidt–Shin)** tests.  
   - Both tests confirmed the log-transformed series is **non-stationary** (expected due to trend and seasonality).

4. **Decomposition**  
   - The series was decomposed into **Trend**, **Seasonal**, and **Residual** components.  
   - The decomposition plot shows a clear annual cycle and upward trend.

5. **Model Selection using Auto-ARIMA**  
   - Auto-ARIMA automatically determined the optimal `(p,d,q)` and seasonal `(P,D,Q,m)` values:
     ```
     (0,1,1) × (0,1,1,12)
     ```
   - Differencing terms `(d=1, D=1)` ensure the series becomes stationary internally.

6. **Model Training (SARIMAX)**  
   - Fitted the SARIMAX model on the training data, using `is_summer` as an **exogenous regressor**.  
   - The model learns a seasonal β coefficient that boosts forecasts during summer months.

7. **Model Validation**  
   - Forecasted the next 12 months and compared them with actuals.  
   - Achieved **low MAE** and **MAPE**, confirming good predictive performance.

8. **Final Forecasting (Full Model)**  
   - Re-fitted the model on the full 3-year dataset.  
   - Forecasted the next **36 months** (3 years).  
   - Future forecasts correctly capture both trend and seasonality.

---

## 📈 Results Summary

| Metric | Value |
|--------|-------|
| **MAE** | ~13.26 |
| **MAPE** | ~2.90% |

✅ The model successfully learned both **trend** and **seasonal patterns**,  
producing realistic forecasts with **exogenous influence** from summer months.

---

## ⚙️ Technologies Used
- Python  
- Pandas  
- Statsmodels  
- pmdarima  
- Matplotlib  

---

## 🧠 Key Insights
- Log transformation doesn’t make data stationary but makes it **well-behaved** for SARIMAX.  
- ADF & KPSS together confirm the need for differencing.  
- Exogenous variables (like summer months) allow **contextual seasonality adjustment**.  
- SARIMAX extends ARIMA’s capabilities by combining **trend, seasonality, and external drivers**.

---

## 🐺 Author
**Susnata **  