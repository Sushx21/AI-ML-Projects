# Susnata Agent App

A lightweight **Lovable-style application builder** that converts natural language prompts into full, ready-to-run mini applications. This system uses **LangGraph**, **structured planning agents**, and **file‑level tool execution** to generate project folders containing HTML, CSS, JavaScript, and documentation.

---

## 🚀 What This Project Does

This app takes a user prompt like:

> *"Build me a calculator app or a todo list or anything"*

and automatically generates:

* A **project folder** inside `susnata21_generated_project/`
* All required **files** (HTML, CSS, JS, or others based on the plan)
* A **multi‑agent workflow**:

  * **Planner Agent** → Converts the request into a high‑level project plan
  * **Architect Agent** → Breaks the plan into detailed technical tasks
  * **Coder Agent** → Creates and writes actual file content using tools

Everything runs through a LangGraph pipeline that ensures structured, deterministic app creation.

---

## 🧩 Core Components

### **1. Planner Agent** (`planner_prompt`)

* Converts the user's natural language request into:

  * App name
  * Description
  * Tech stack
  * Features
  * List of files required for the app
* Output is structured into the `Plan` Pydantic model.

### **2. Architect Agent** (`architect_prompt`)

* Takes the plan and breaks it down into **explicit engineering tasks**.
* Provides file‑level implementation steps.
* Ensures dependency ordering and integration.

### **3. Coder Agent**

* Executes one task at a time.
* Uses LangGraph's tool system to:

  * Read files
  * Write files
  * List project directories
  * Run shell commands
* Creates the full application inside the generated project folder.

---

## 🛠️ Tools Available

The system includes safe wrappers to avoid writing outside the project directory:

* **write_file** → Creates or updates files
* **read_file** → Reads existing files
* **list_files** → Lists project contents
* **get_current_directory** → Returns the project root
* **run_cmd** → Runs shell commands inside the project

These tools allow the agent to behave like a small automated developer.

---

## 🧠 LangGraph Workflow

```
User Prompt → Planner → Architect → Coder → Generated App
```

* The graph loops through "coder" until all tasks are completed.
* When no more steps remain, the flow returns **DONE**.

---

## 📂 Project Structure Example

After running a prompt (like "Build a Todo App"), the system generates:

```
susnata21_generated_project/
│
├── index.html
├── styles.css
├── script.js
└── README.md
```

The exact structure depends on the planner’s output.

---

## ▶️ How to Run

Inside `graph.py`, modify the `user_prompt` inside `__main__` and run:

```bash
python graph.py
```

Your generated app will appear inside the `susnata21_generated_project` folder.

---

## 🧾 Summary

This project is a **natural‑language‑powered mini app builder** that:

* Understands your prompt
* Plans the required system
* Breaks it into engineering tasks
* Writes all code files automatically

A simple and powerful foundation for building full Lovable‑style app generators using LangGraph.

---

🐺  Happy Building!

Susnata 
