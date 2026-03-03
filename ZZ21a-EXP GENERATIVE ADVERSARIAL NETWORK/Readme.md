# GAN Experimentation – MNIST (Experimental Notebook)

This project is an **experimental exploration** of Generative Adversarial Networks (GANs) using the MNIST handwritten digits dataset.  
The goal of this notebook was **not** to build a perfect GAN, but to:

- Understand the basic architecture of a Vanilla GAN  
- Experiment with generator + discriminator training dynamics  
- Observe concepts like **adversarial training**, **noise sampling**, and **mode collapse**  
- Document real outcomes, even when the model does not perform ideally  

### 🚀 What This Experiment Shows
During training, the model experienced **mode collapse** — the generator repeatedly produced similar images instead of diverse digits.  
This is a *common and expected* behavior when experimenting with basic GANs.

Instead of hiding the result, this notebook intentionally includes:
- The collapsed outputs  
- Generator and discriminator loss logs  
- Observations on how GAN instability happens  
- Notes on noise sampling and GAN objectives  

### 🎯 Purpose of This Repository
This repository is meant to serve as:
- A **learning log** of foundational GAN behavior  
- A reference for concepts like generator loss, discriminator loss, and adversarial dynamics  
- A stepping stone for future experiments (e.g., CIFAR-10 GAN, DCGAN,etc.)  

### 🧪  Disclaimer
This is **not** a production-ready GAN.

GAN is highly resource and data intensive 

DCGANs will be added in next iteration
This is an **experimental notebook** designed for learning, debugging, and building intuition about how GANs behave.

More advanced and stable GAN variants will be added over time.

---

Feel free to explore, experiment, and improve 🐺 
Susnata
