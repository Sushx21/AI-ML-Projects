# 🔍 Fraud-Investigator LLM — Refund Decision Intelligence (Fine-Tuned GPT-2)

This project demonstrates how a **fine-tuned Large Language Model (LLM)** can support **fraud detection** and **refund-decision workflows**—similar to what frontline associates do manually in large e-commerce operations.

The goal is to convert customer behavioral signals into natural-language summaries and train a model to output **Low / Medium / High risk** decisions. This creates a lightweight AI assistant that brings consistency, speed, and structure to refund investigation.

---

## 🧠 Project Motivation
Frontline associates analyze multiple signals before approving or denying refunds:
- Order and payment history
- Device & IP patterns
- Customer claim behavior
- Account overlap and risk indicators

This project captures such reasoning patterns using a fine-tuned GPT-2 model so that the system can assist humans during refund or abuse evaluations.

---

## 🏗️ Workflow Overview

### **1️⃣ Data Preparation**
- Loaded raw CSV file
- Applied feature engineering
- Converted rows into natural-language case summaries
- Generated risk labels (responses)
- Saved dataset in JSONL format for Hugging Face compatibility

Each line in the dataset:
```json
{
  "text_summary": "Customer using device X placed 2 orders... behavior appears legitimate.",
  "abuse": "Low risk. Approve refund normally."
}
```

---

## 📚 Libraries & Tech Stack
- **Unsloth** (fast fine-tuning)
- **Hugging Face Transformers**
- **TRL (Supervised Fine-Tuning)**
- **LoRA (PEFT)**
- **GPT-2 Medium**
- **Pandas**
- **Google Colab GPU**

---

## ⚙️ LoRA Configuration
Targeted LoRA adapters applied to:
- `c_attn` (Q/K/V projection)
- `c_fc` (MLP expansion)
- `c_proj` (attention & MLP projection)

This ensures efficient domain adaptation while keeping training lightweight.

---

## 📈 Training Details
**Hyperparameters:**
- Learning rate: `2e-4`
- Max steps: `100`
- Warmup: `5`
- Optimizer: `adamw_8bit`
- Batch size effective: `8`
- Precision: 8-bit + bf16

**Results:**
- **Final Loss:** `0.7582`
- **Perplexity:** `2.1344`

Low perplexity indicates a confident and stable model.

---

## 🤖 Example Inference
**Prompt:**
```
### Case: Customer using device z8x31pq... Payment method changed twice.
### Response:
```

**Model Prediction:**
```
Low risk. Approve refund with issue noted.
```

---

## 🚀 Future Extensions
This model is the foundation for a larger **agentic fraud investigation system**, including:
- Human-in-the-loop workflows
- CRM integrations
- Automated refund decision pipelines
- Dashboard population using API calls

This pushes the vision toward operational automation, where AI assists humans with accountability and consistency.

---

## 📁 Folder Structure
```
📁 fraud-investigator-llm
 ├── fraud_cases.json
 ├── fine_tuning.ipynb
 ├── fraud_investigator_model/
 └── README.md
```

---

## 🐺 Closing Note
This project blends machine intelligence with human reasoning to build smarter refund evaluation workflows. A small but strong step toward operational AI in trust & safety.