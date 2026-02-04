# PCA Loadings Back-Mapping: From Components to Original Features

## 📌 Motivation (Why this exists)

Principal Component Analysis (PCA) is excellent for dimensionality reduction,  
but it creates a serious problem:

> Models trained on principal components lose direct interpretability in the original feature space.

This repository demonstrates how to **back-map PCA loadings and regression coefficients**
to recover **original-feature-level interpretability** — mathematically, cleanly, and explicitly.

This is not a PCA tutorial.  
This is **PCA done with intent**.

---

## 🧠 Notation & Mental Model

<p align="center">
  <img src="pca_loadings_backmapping/pca_notation_and_mental_map.jpg" width="600">
</p>

**Definitions used throughout:**

- **X** → Original feature matrix  
  *(temperature, pressure, oxygen, coal rate, etc.)*

- **W** → PCA loading matrix  
  *(weights defining how original features combine into PCs)*

- **Z** → Principal components  




Z = XW


- **βₚ𝚌ₐ** → Regression coefficients learned on principal components

- **βₒᵣᵢgᵢₙₐₗ** → Regression coefficients expressed in original feature space

Each principal component is a **weighted sum of original features**.  
Nothing mystical. Just linear algebra.

---

## 🔁 Step 1: PCA Projection (Feature Space → PC Space)

<p align="center">
<img src="pca_loadings_backmapping/pca_projection_and_pc_regression.jpg" width="600">
</p>

PCA performs a linear transformation:



This means:
- Original features are projected onto orthogonal directions
- Each PC captures variance as a weighted combination of features

At this stage:
- Interpretability is reduced
- But structure and signal are preserved

---

## 📐 Step 2: Regression on Principal Components

We train a linear model **on the PCs**, not on original features:

y = Z βₚ𝚌ₐ + ε

This is often done to:
- Reduce multicollinearity
- Stabilize coefficients
- Improve numerical behavior

However…

👉 These coefficients are **not interpretable in original feature units**.

So we back-map them.

---

## 🔄 Step 3: Back-Mapping PCA Loadings

<p align="center">
  <img src="pca_loadings_backmapping/pca_backmapping_derivation.jpg" width="600">
</p>

Substitute PCA projection into regression:

This is the **back-mapping of PCA loadings**.

No approximation.  
No heuristic.  
Pure linear algebra.

---

## 🔬 Step 4: Feature-Level Interpretation

<p align="center">
  <img src="pca_loadings_backmapping/feature_level_backmapped_coefficients.jpg" width="600">
</p>

For a specific original feature **j**:


This shows:

- Each original feature’s influence is a **sum of its contributions across PCs**
- PCA does not destroy interpretability — **it delays it**
- Back-mapping restores decision-ready coefficients

---

## 🎯 Why This Matters (Business + ML)

- I can explain PCA-based models to non-technical stakeholders
- I can rank original features even after dimensionality reduction
- I can combine PCA with SHAP or other explainability tools meaningfully
- I avoid the “black-box PCA” trap

This is **interpretability-first modeling**, not just compression.


