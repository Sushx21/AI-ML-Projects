# 🚘 Susnata's Vehicle Damage Classification using Deep Learning (PyTorch)

A complete computer vision pipeline for **classifying vehicle damage types** using CNNs and Transfer Learning.  
Three models were developed, with **ResNet50** achieving the highest accuracy of **81.74%**.  
The goal is to build a production-style computer vision workflow.

---

## 📌 Overview

This project implements a deep learning system capable of:

- 🔍 Classifying front & rear vehicle damage  
- 🧠 Learning robust features through augmentation  
- 🏗️ Training custom CNN models from scratch  
- 🔄 Leveraging **Transfer Learning (ResNet50)** for best accuracy  
- 📊 Generating confusion matrix & classification reports  
- 🖼️ Running inference on any uploaded image  
- 💾 Saving & loading PyTorch models for deployment  

This simulates a production-grade automotive inspection system.

---

## 🗂️ Dataset Summary

- **Total Images:** 2300  
- **Classes (6):**
  - F_Breakage  
  - F_Crushed  
  - F_Normal  
  - R_Breakage  
  - R_Crushed  
  - R_Normal  

- **Split:** 75% train — 25% validation  
- Loaded using PyTorch `ImageFolder`.

---

## 🧪 Data Augmentation

Enhances generalization and prevents overfitting:

- Random Horizontal Flip  
- Random Rotation  
- Color Jitter  
- Resize to 224×224  
- Normalize with ImageNet mean/std  

These augmentations imitate real-world lighting & orientation variations.

---

## 🧱 Models Implemented

### 🧠 **Model 1: Custom CNN (Baseline)**  
A simple 3-layer CNN with MaxPooling and a fully connected classifier.  
**Validation Accuracy:** ~52%

---

### 🧠 **Model 2: CNN with Regularization**  
Added:
- BatchNorm  
- Dropout (0.5)  
- L2 Regularization  

**Validation Accuracy:** ~55%  
Better stability but still limited due to small dataset.

---

### 🏆 **Model 3: ResNet50 (Transfer Learning)**  
The best-performing model.

✔ Loaded pretrained ImageNet weights  
✔ Unfroze only final block (`layer4`) + `fc` layer  
✔ Replaced output layer with 6-class classifier  
✔ Added dropout  

**Final Validation Accuracy:** **81.74%** ⚡🔥

---

## 📊 Evaluation Metrics

Generated via scikit-learn:

- Precision  
- Recall  
- F1-score  
- Support  

ResNet50 outperformed both CNN models across all metrics.

---

## 🏋️ Training Pipeline

Training loop includes:

- Custom batch logging  
- CrossEntropyLoss  
- Adam optimizer  
- GPU acceleration (Colab T4)  
- Epoch-wise validation accuracy  
- Metric aggregation  

Total training time varies by model size.

---

## 🖼️ Confusion Matrix

Visualizes predictions vs ground truth for all 6 classes.  
Useful for spotting misclassification patterns.

---

## 🔍 Inference Pipeline

Model can classify any damage image:

1. Load image  
2. Apply inference transforms  
3. Run forward pass  
4. Display prediction + probability  
5. Show top-3 confidence scores  

Example Output:

Prediction: F_Breakage
Confidence: 99.92%

---

## 💾 Save & Load Model

### Save:
`torch.save(model.state_dict(), "susnatacnn_model.pth")`

### Load:
`model.load_state_dict(torch.load("susnatacnn_model.pth"))`

---

## 🧰 Tech Stack

| Component | Technology |
|----------|------------|
| Framework | PyTorch |
| Image Loader | TorchVision |
| Augmentation | torchvision.transforms |
| Metrics | scikit-learn |
| Visualization | Matplotlib |
| Environment | Google Colab (GPU) |

---

## 📁 Project Structure

📦 vehicle-damage-classification ┣ 📂 dataset/ ┣ 📄 training_notebook.ipynb ┣ 📄 model.py ┣ 📄 utils.py ┣ 📄 susnatacnn_model.pth ┗ 📄 README.md

---

## 🐺My Final Thoughts

Even with a small dataset, transfer learning **crushed** custom CNNs.  
ResNet50 delivered **81% accuracy**, proving its robustness for:

- Insurance claim automation  

- Damage severity triage  