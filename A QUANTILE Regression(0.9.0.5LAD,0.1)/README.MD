# Quantile Regression for Risk-Aware Demand Forecasting 🐺

## Problem Statement
Traditional demand forecasting models focus on predicting a single average outcome.  
While useful for reporting, this approach fails in operational settings where demand is uncertain and the cost of errors is asymmetric.

- Underestimating demand → stockouts, lost revenue, SLA breaches  
- Overestimating demand → idle inventory, unnecessary operational cost  

Despite this, classical regression models penalize both errors equally.

---

## Solution Overview
This project reframes demand forecasting as a **decision-making problem under uncertainty** using **Quantile Regression**.

Instead of predicting a single number, we estimate multiple conditional demand quantiles, allowing planners to choose strategies based on risk:
- conservative
- balanced
- safety-first

---

## Dataset
- Bike Sharing Demand dataset (Kaggle)
- Target variable: `count` (number of bikes rented)
- Features used:
  - temperature
  - humidity
  - windspeed  

Discrete variables such as hour, season, and holiday were intentionally excluded to isolate **weather-driven uncertainty**.

---

## Modeling Approach
Multiple quantile models were trained, each representing a different planning strategy:

| Quantile | Interpretation | Business Use |
|--------|---------------|-------------|
| 0.10 | Lower bound | Cost-cutting planner |
| 0.50 | Median | Typical-day planner |
| 0.90 | Upper bound | Safety-first / SLA planner |

All models are linear and interpretable, but optimized using **quantile-specific loss functions**.

At `q = 0.5`, quantile regression reduces to **Least Absolute Deviations (LAD)** regression.

---

## Why Quantile Regression?
Quantile regression minimizes **asymmetric absolute loss (Pinball Loss)**, enabling:

- Explicit modeling of uncertainty
- Natural handling of heteroskedastic demand
- Asymmetric penalties for over- and under-prediction
- Decision-aligned forecasting rather than accuracy-only optimization

---

## Why Not RMSE or R²?
Traditional metrics are misaligned with quantile objectives:

- **RMSE** assumes symmetric error costs and optimizes the mean  
- **R²** measures variance around the mean, not quantile coverage  

Instead, models are evaluated using:
- coverage (e.g., 90th percentile should cover ~90% of outcomes)
- pinball loss
- prediction interval width

---

## Key Visual Insights
- Median residual plots show stable typical demand but large tail risk
- 90th percentile planning plots demonstrate effective safety buffers
- Near-constant predictions indicate limited explanatory power of weather for central demand, while tail risk remains significant

These results show that **risk resides in the extremes, not in the average**.

---

## Interpretability
Each quantile has its own coefficient vector, allowing analysis of how features affect:
- normal demand
- extreme demand  

Regularization was disabled (`alpha = 0`) to retain interpretability.

---

## Key Takeaways
- Average demand is relatively stable
- Extreme demand varies significantly
- Mean/median-based planning hides operational risk
- Quantile regression enables risk-aware, decision-first planning
- A 90th percentile forecast acts as insurance, not a point prediction

---

## Tools & Libraries
- Python
- pandas, numpy
- scikit-learn (`QuantileRegressor`)
- matplotlib

---

In future enhancements i will upgrade this to Nonlinear quantile models
Like GradientBoostingRegressor and create a cost matrix 


## Author
**Susnata**  
