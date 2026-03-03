# Vision Transformer (ViT) from Scratch – MNIST Classification

## 📖 Project Overview

This project implements a Vision Transformer (ViT) architecture from scratch using PyTorch and applies it to the MNIST handwritten digit classification dataset.

The implementation includes:

- Patch Embedding using Conv2D
- Learnable CLS Token
- Learnable Positional Embedding
- Transformer Encoder Blocks
- Multi-Head Self Attention
- MLP Head for classification
- Training and Validation pipeline
- GPU support

---

## 🧠 Architecture Flow

1. Input Image (28x28)
2. Patch Embedding (Image → Patches)
3. Flatten to Sequence
4. Add CLS Token
5. Add Positional Embedding
6. Pass through Transformer Encoder layers
7. Extract CLS token
8. MLP Head → Class logits
9. CrossEntropy Loss

---

## ⚙️ Training Details

- Optimizer: Adam
- Loss Function: CrossEntropyLoss
- Epochs: 5
- Dataset: MNIST
- Device: GPU (if available)

---

## 📊 Results

- Final Training Accuracy: ~94%
- Validation Accuracy: ~94.55%

The model demonstrates stable learning and good generalization performance.

---

## 🚀 Key Learnings

- How Vision Transformers convert images into token sequences
- Importance of CLS token in classification tasks
- Role of LayerNorm and residual connections
- Difference between training mode and evaluation mode
- Handling GPU tensors during visualization

---

## 📌 Future Improvements

- Increase embedding dimension
- Increase number of encoder layers
- Use data augmentation
- Try CIFAR-10 dataset
- Implement learning rate scheduling

---

## Susnata

Implemented from scratch as a deep learning practice project.
