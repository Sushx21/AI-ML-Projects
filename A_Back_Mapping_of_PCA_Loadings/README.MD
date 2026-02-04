
# Susnata PCA Loadings Back-Mapping: From Components to Original Features

## 📌 Motivation (Why this exists)

Principal Component Analysis (PCA) is excellent for dimensionality reduction,  
but it introduces a critical limitation:

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
  *(weights defining how original features combine into principal components)*

- **Z** → Principal component matrix  

\[
Z = XW
\]

- **βₚ𝚌ₐ** → Regression coefficients learned on principal components  

- **βₒᵣᵢgᵢₙₐₗ** → Regression coefficients expressed in the original feature space  

Each principal component is a **weighted linear combination of original features**.  
Nothing mystical. Just linear algebra.

---

## 🔁 Step 1: PCA Projection (Feature Space → PC Space)

<p align="center">
  <img src="pca_loadings_backmapping/pca_projection_and_pc_regression.jpg" width="600">
</p>

PCA performs a linear transformation:

\[
Z = XW
\]

This means:
- Original features are projected onto orthogonal directions
- Each principal component captures variance as a weighted combination of features

At this stage:
- Interpretability is reduced
- But the underlying structure and signal are preserved

---

## 📐 Step 2: Regression on Principal Components

We train a linear model **on the principal components**, not on the original features:

\[
y = Z \beta_{\text{PCA}} + \varepsilon
\]

This is often done to:
- Reduce multicollinearity
- Stabilize coefficient estimates
- Improve numerical conditioning

However…

👉 These coefficients are **not interpretable in original feature units**.

So we back-map them.

---

## 🔄 Step 3: Back-Mapping PCA Loadings

<p align="center">
  <img src="pca_loadings_backmapping/pca_backmapping_derivation.jpg" width="600">
</p>

Substituting the PCA projection into the regression equation:

\[
Z = XW
\]

\[
y = (XW)\beta_{\text{PCA}} + \varepsilon
\]

Rearranging:

\[
y = X (W \beta_{\text{PCA}}) + \varepsilon
\]

This gives the key result:

\[
\beta_{\text{original}} = W \beta_{\text{PCA}}
\]

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

\[
\beta_{\text{original}}^{(j)} =
\sum_{k=1}^{K} W_{j,k} \cdot \beta_{\text{PCA}}^{(k)}
\]

This shows that:

- Each original feature’s influence is an **aggregation of its contributions across PCs**
- PCA does not destroy interpretability — **it delays it**
- Back-mapping restores decision-ready coefficients in the original feature space

---

## 🎯 Why This Matters (Business + ML)

- Enables explanation of PCA-based models to non-technical stakeholders
- Allows ranking of original features even after dimensionality reduction
- Makes PCA compatible with interpretability tools (e.g., SHAP)
- Avoids the “black-box PCA” trap

This is **interpretability-first modeling**, not just compression.

---

## 🐺 Takeaway

Most workflows stop at:

\[
Z = XW
\]

This work goes further:

\[
\beta_{\text{original}} = W \beta_{\text{PCA}}
\]

Dimensionality reduction is easy.  
**Reconstruction of meaning is mastery.**
