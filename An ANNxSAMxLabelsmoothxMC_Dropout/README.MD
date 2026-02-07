# Robust Equipment Failure Prediction  
### ANN + SAM + Label Smoothing + Monte Carlo Dropout

---

## 📌 Project Overview

This project builds a **robust, calibrated, and uncertainty-aware machine learning model** to predict **equipment failure** in an industrial (steel plant–like) setup.

Instead of focusing only on accuracy, the model is designed to support **risk-aware decision-making**, where **wrong predictions are costly** and **data is noisy and limited**.

The final output is **not just a prediction**, but:

> **Failure Probability ± Uncertainty**,  
along with lower and upper confidence bounds.

---

## 🎯 Problem Statement

We want to predict whether equipment is likely to fail soon.

- **Target**
  - `1` → Failure likely  
  - `0` → Normal operation  

- **Input Sensors**
  - Temperature  
  - Pressure  
  - Vibration  
  - Load  

### Constraints
- Small dataset
- Noisy and correlated sensor signals
- High risk of overfitting
- High cost of false alarms and missed failures

---

## 🧠 Modeling Philosophy

Instead of building a brittle, overconfident model, we prioritize:

- **Robustness** → Stable under noise  
- **Calibration** → Probabilities that mean what they say  
- **Uncertainty Awareness** → Knowing when the model is unsure  

This makes the system suitable for **industrial decision-making**, not just offline evaluation.

---

## 🏗️ Architecture & Techniques Used

### 1️⃣ Artificial Neural Network (ANN)
- Captures **non-linear interactions** between sensors
- Two hidden layers with ReLU activations
- Dropout for regularization

Limitation addressed:
- ANNs can overfit and become overconfident

---

### 2️⃣ Label Smoothing
Instead of hard labels:

We use:
Failure = 0.9
Not Failure = 0.1


Benefits:
- Reduces overconfidence
- Improves probability calibration
- Produces more realistic risk scores

---

### 3️⃣ Sharpness-Aware Minimization (SAM)
SAM modifies the training objective to prefer **flat minima** over sharp ones.

Intuition:
- Sharp minima → fragile → overfit
- Flat minima → stable → generalize better

SAM performs a **two-step optimization**:
1. Tests the worst-case nearby loss (sharpness probe)
2. Updates parameters to minimize that worst-case loss

Result:
- Strong resistance to noise
- Better generalization on small datasets

---

### 4️⃣ Monte Carlo Dropout (Uncertainty Estimation)
Dropout is kept **ON during inference**, and the model is run multiple times.

This produces a **distribution of predictions** instead of a single value.

From this we compute:
- **Mean probability** → prediction
- **Standard deviation** → uncertainty (epistemic)

Final output example:
Failure Probability = 0.37 ± 0.03


---

## 📊 Output Dataset (Final Deliverable)

The final dataset contains:

| Column | Description |
|------|-------------|
| temperature | Sensor reading |
| pressure | Sensor reading |
| vibration | Sensor reading |
| load | Sensor reading |
| failure_probability | Mean predicted probability |
| uncertainty | Model uncertainty (MC Dropout std) |
| failure_prob_lower | Lower bound (mean − uncertainty) |
| failure_prob_upper | Upper bound (mean + uncertainty) |
| predicted_label | Binary decision |
| risk_level | LOW / MEDIUM / HIGH risk |

This turns raw model output into **decision-ready intelligence**.

---

## 🧠 How to Interpret Results

- **Low probability + Low uncertainty**  
  → Safe, automated decision

- **High probability + Low uncertainty**  
  → Schedule maintenance

- **Low probability + High uncertainty**  
  → Human review recommended

- **High probability + High uncertainty**  
  → Conservative action / inspection

Uncertainty is treated as a **first-class signal**, not noise.

---

## 🔍 Why Feature Attribution (SHAP) Was Not Used

- Input features are correlated
- Feature attribution under correlation can be misleading
- The project prioritizes **decision-level explainability** over per-feature explanations

Explainability is provided through:
- calibrated probabilities
- uncertainty bounds
- robustness guarantees

This is a **deliberate modeling choice**, not an omission.

---

## 🛠️ Tech Stack

- **Python**
- **PyTorch** (modeling & optimization)
- **scikit-learn** (preprocessing)
- **NumPy / Pandas** (data handling)

## ✅ Key Takeaway

This project demonstrates how to move from:

❌ *Point predictions*  
to  
✅ *Risk-aware, uncertainty-informed decisions*

It is designed for **real-world industrial AI**, not just benchmark performance.

---

## 📌 Future Extensions

- Conformal Prediction for formal coverage guarantees

- Time-series extension for predictive maintenance
- Deployment as a monitoring service

---

**Author** 

Susnata 
Built with a focus on robustness, calibration, and trustworthiness in AI systems.
