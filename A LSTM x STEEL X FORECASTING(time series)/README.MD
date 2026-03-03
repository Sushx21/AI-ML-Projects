# ⛓️🔩 Steel Production Forecasting using LSTM 🐺

## Overview
This project explores **time-series forecasting of steel (industrial) production** using Long Short-Term Memory (LSTM) networks.  
The focus is not only on prediction, but on **understanding model behavior**, trade-offs, and limitations when applying deep learning to **macro-economic time series**.

---

## Objectives
- Forecast future steel production using historical monthly data  
- Understand how LSTMs model time, memory, and trends  
- Analyze why deep learning forecasts appear smooth for macro data  
- Compare level-based and differenced modeling approaches  

---

## Dataset
- **Source:** FRED (Federal Reserve Economic Data)  
- **Series:** Industrial Production Index (manufacturing / steel proxy)  
- **Frequency:** Monthly  
- **Time span:** ~100 years  

---

## Model 1 — Level-Based LSTM
**Prediction target:**  
Next month’s production level using the previous 12 months.

**Key observations:**
- Captures long-term trend effectively  
- Produces smooth, conservative forecasts  
- Under-reacts to sudden economic shocks (e.g., 2008 crisis, COVID-19)

**Why this happens:**
- MSE loss penalizes large deviations  
- Macro-economic data is trend-dominated  
- Autoregressive forecasting compounds smoothing effects  

**Primary use case:**  
Strategic, long-term baseline planning.

---

## Model 2 — Differenced LSTM (Second Refinement)
**Prediction target:**  
Month-to-month change in production:

\[
\Delta y_t = y_t - y_{t-1}
\]

**Why differencing is used:**
- Reduces trend dominance  
- Improves sensitivity to short-term movements  
- Mitigates lag bias observed in residual analysis  

Predicted differences are reconstructed back to production levels using cumulative summation.

**Observed behavior:**
- More reactive to local changes than the level-based model  
- Less smoothing, but slightly noisier predictions  
- Long-horizon forecasts may drift due to cumulative error accumulation  

**Primary use case:**  
Short-term monitoring and directional analysis.

---

## Why Not ARIMA / SARIMA?
ARIMA and SARIMA are strong classical baselines for time-series forecasting.  
However, they were **intentionally not used as the primary model in this project** for the following reasons:

- **Linear assumptions:**  
  ARIMA/SARIMA assume linear relationships, while macro-economic dynamics often exhibit non-linear behavior over long horizons.

- **Manual model specification:**  
  Selecting `(p, d, q)` and seasonal parameters requires repeated tuning and strong assumptions about stationarity and seasonality.

- **Limited adaptability:**  
  Classical models struggle to adapt smoothly across structural regime changes without frequent re-estimation.

- **Focus of this project:**  
  The goal was to **study deep learning behavior** (smoothing bias, lag effects, differencing impact) rather than optimize a single statistical baseline.

That said, ARIMA/SARIMA remain valuable:
- As benchmark models  
- For short-horizon forecasts  
- In hybrid approaches combined with neural networks  

---

## Key Insights
- Absolute loss values are not directly comparable across models with different targets  
- Smooth forecasts are expected for macro-economic time series  
- Differencing improves responsiveness but introduces reconstruction drift  
- No single model is optimal for all forecasting horizons  

---

## Limitations
- Univariate modeling (no exogenous economic indicators)  
- Structural shocks cannot be anticipated  
- Differenced models are best suited for short forecast horizons
- Error accumulation (recursive forecasting problem)
Let's say when  LSTM is used recursively, its own predictions are fed back as inputs, so small early errors compound and the forecast can drift or flatten. 
---

## Conclusion
This project demonstrates that **interpreting model behavior is as important as prediction accuracy**.  
By comparing level-based and differenced LSTM models, it highlights practical trade-offs encountered when applying deep learning to real-world economic time series.

---
