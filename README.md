# 🚀 RetailX: Enterprise Multi-Agent Retail Intelligence Platform

![Status](https://img.shields.io/badge/Status-Production%20Ready-success) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![Framework](https://img.shields.io/badge/Framework-FastAPI%20%7C%20Streamlit-orange) ![AI](https://img.shields.io/badge/AI-Azure%20OpenAI%20%7C%20CrewAI-purple)

**RetailX** is an advanced, AI-driven enterprise analytical ecosystem engineered to solve complex supply chain challenges, warehouse compliance visibility issues, and demand misalignments. Unlike traditional reactive ERP systems, RetailX leverages a **Multi-Agent Swarm Matrix** to make proactive, data-driven decisions.

---

## 🎯 Project Overview
Managing stockouts, overstocking, and strict warehouse compliance (like temperature and humidity controls for high-value goods) is highly complex in the retail industry. RetailX automates this entire cognitive process.

By integrating **CrewAI** and **Azure OpenAI**, the platform deploys **Autonomous Digital Workers (Agents)**. These agents communicate with each other, parse internal compliance manuals, execute Machine Learning models for demand forecasting, and synthesize the data into a cohesive, actionable corporate report.

---

## 🏗️ Core Architecture & Flow

The system is built on a secure, decoupled microservices architecture where the frontend, backend, cloud storage, and AI agents operate in seamless isolated layers.

```text
[ 🖥️ Streamlit UI ]  👉 Sends Query
        │
        ▼
[ 🟢 FastAPI Backend (Azure App Service) ]
        │
        ├─► 🛡️ Gatekeeper (Intent Boundary): Evaluates if the query is retail-relevant.
        │       (Automatically blocks out-of-domain queries)
        │
        ▼ (If Valid Local Data is Requested)
[ 🧠 Master Autonomous Swarm Orchestrator ] ─── Auto-syncs assets from [ ☁️ Azure Blob ]
        │
        ├──► 🕵️ Document Assistant Agent  (Reads warehouse_compliance.txt via RAG)
        ├──► 📈 ML Forecasting Agent      (Executes 131MB demand_forecast_model.pkl)
        └──► 👔 Risk Supervisor Agent     (Synthesizes data & drafts final report)
        │
        ▼
[ 📤 Final Corporate Output Returned to User UI ]
```

---

## 🛠️ Technology Stack

* **Frontend:** Streamlit (For a clean, interactive data and chat dashboard)
* **Backend:** FastAPI & Uvicorn (High-performance, asynchronous API routing)
* **AI & LLM:** Azure OpenAI (GPT-4o) & CrewAI Framework
* **Storage & Models:** Azure Blob Storage & Git LFS (Large File Storage)
* **DevOps & CI/CD:** Docker, GitHub Actions, Azure Web Apps (100% Zero-Touch Automation)

---

## 📂 Project Structure & External Assets
To maintain a production-ready environment, heavy and sensitive files are strictly isolated:

* 📄 **`app/data/warehouse_compliance.txt`**: The core source text containing company storage thresholds and safety rules. Queried by the RAG system.
* 📦 **`app/models/demand_forecast_model.pkl`**: A 131.90 MB Machine Learning model tracking dynamic inventory velocities. Handled explicitly via **Git LFS**.
* 🧠 **`app/models/native_vector_rag.pkl`**: Pre-computed numerical vector embeddings for immediate semantic document retrieval.
* ⚙️ **`.github/workflows/ci-cd.yml`**: A multi-stage pipeline that triggers on every `git push` to run tests, build the Docker image (bypassing cache), and deploy live to Azure.
* 🛡️ **`.gitignore` & `.dockerignore`**: Security nodes preventing local credentials (`.env`) and cache files from leaking into remote environments.

---

## 💎 Core Platform Benefits (Business Impact)

1. **🚨 Zero Stockout Risks:** The ML model continuously tracks live demand against actual shelf stock, neutralizing stockout hazards before high-demand business cycles.
2. **⚖️ 100% Legal Compliance:** The Document Assistant ensures high-value inventory (e.g., electronics) strictly adheres to environmental parameters (like < 25°C and < 40% humidity), preventing product degradation.
3. **🤖 Automated Swarm Intelligence:** Eliminates manual report cross-referencing. The Supervisor Agent autonomously processes multi-disciplinary data to deliver immediate operational recommendations.
4. **🚀 Zero-Touch Continuous Deployment:** Completely automated infrastructure. A single `git push` triggers a full test, build, and cloud deployment cycle without manual server intervention.
