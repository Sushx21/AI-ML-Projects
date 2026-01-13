# 🔧 Susnata's Predictive Maintenance with Calibrated XGBoost  
### Rare-Event Risk Modeling for Industrial Equipment

## 📌 Problem Statement
In steel plants, unexpected equipment failures lead to:
- Production loss
- Safety hazards
- High repair and downtime costs

This project frames predictive maintenance as a **rare-event binary classification problem**, similar to **credit risk and fraud detection**, where the objective is **not accuracy**, but **reliable, calibrated probabilities for decision-making**.

---

## 🎯 Business Objective
The primary goal is to support **maintenance decision-making**, not raw prediction.

**Optimized for:**
- Minimizing downtime
- Avoiding unnecessary maintenance stops
- Protecting expensive equipment

**Explicitly NOT optimized for:**
- Accuracy (misleading under imbalance)

---

## 🏌️‍♂️ Dataset
- **AI4I 2020 Predictive Maintenance Dataset**
- Industrial sensor telemetry
- Rare machine failures (~3.4%)

Source:  
https://www.kaggle.com/datasets/stephanmatzka/predictive-maintenance-dataset-ai4i-2020

---

## 🧠 Modeling Philosophy
This project mirrors **credit risk modeling practices**:

| Concept | Purpose |
|------|--------|
| MCC(matthews correlation coefficient) | Robust decision evaluation under imbalance |
| Brier Score | Probability quality |
| Calibration | Control overconfidence |
| Ranking metrics | Maintenance prioritization |

Accuracy is intentionally de-emphasized.

---

## 🔍 Exploratory Data Analysis (EDA)
Key insights from EDA:
- **Torque** and **Tool Wear** are dominant failure drivers
- Failures cluster in **high torque + low RPM** regimes
- Temperature variables act as secondary amplifiers
- No single feature causes failure → **interactions matter**

This justifies the use of **tree-based and boosting models**.

---

## 🧪 Feature Treatment
- Outliers retained as they often represent **early warning signals**
- **Winsorization (1%–99%)** applied to heavy-tailed risk features
- **RobustScaler** used to preserve signal while maintaining stability

This approach aligns with industry practice in predictive maintenance and risk modeling.

---

## 🤖 Models Trained
1. Logistic Regression (baseline, interpretable reference)
2. Random Forest (interaction learning)
3. XGBoost (final model)

XGBoost achieved:
- ROC-AUC ≈ 0.97
- MCC ≈ 0.65
- Brier ≈ 0.02

---

## 🎯 Probability Calibration
Both Random Forest and XGBoost were calibrated using **Platt scaling**.

Calibration was required because:
- Failures are rare
- Decisions depend on probability thresholds
- Costs are asymmetric

Calibrated XGBoost demonstrated the most stable and reliable probabilities and was selected as the final model.

---

## 🚦 Decision Policy
- **Business-defined intervention threshold:** 0.7
- Threshold selection prioritizes **high-confidence alerts**
- Statistical optimum (Youden’s J) evaluated but not adopted due to operational cost constraints

---

## 📊 Decision Diagnostics
Key diagnostics:
- **MCC:** Balanced decision quality
- **Actual Failure Rate:** Baseline risk
- **Predicted Failure Rate:** Maintenance workload
- **Bias:** Intervention aggressiveness

The final model exhibits **conservative behavior**, which is desirable in cost-sensitive industrial environments.

---

## 🔎 Explainability (SHAP)
SHAP analysis confirms:
- Torque and Tool Wear are the strongest contributors
- RPM impact is contextual and interaction-driven
- Temperature acts as a secondary stress amplifier

The model aligns with real mechanical failure mechanisms.

---

## 🧪 Robustness & Stress Testing
A controlled stress test (+5% torque) was applied:
- Minimal change in Brier score
- Stable probability outputs

This confirms **robust, non-fragile behavior** under realistic operating variation.

---

## 📈 Ranking Power
- Gini coefficient ≈ 0.94
- Concordance ≈ 97%

This demonstrates strong ability to **prioritize failing machines above healthy ones**, which is critical for maintenance scheduling.

---

## 📦 Deployment Artifacts
The project outputs:
- `xgb_predictive_maintenance.pkl` → Model + decision policy
- `model_metadata.json` → Metrics, costs, configuration
- `maintenance_predictions_with_confidence.csv` → Inference-ready output

The CSV includes:
- Failure probability
- Confidence (stability under stress)
- Binary intervention decision

---

## 🏁 Conclusion
This project delivers a **production-ready predictive maintenance decision system**, validated for probability honesty, stability, cost sensitivity, and ranking reliability. The approach bridges machine learning with real industrial decision-making and is suitable for deployment in high-stakes manufacturing environments.

---

## 🐺 Author
**Susnata**  
Applied ML | Risk Modeling | Industrial AI
