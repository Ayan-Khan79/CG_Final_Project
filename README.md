# 🚀 RetailX: Enterprise Multi-Agent Retail Intelligence Platform

![Status](https://img.shields.io/badge/Status-Production%20Ready-success) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![Framework](https://img.shields.io/badge/Framework-FastAPI%20%7C%20Streamlit-orange) ![AI](https://img.shields.io/badge/AI-Azure%20OpenAI%20%7C%20CrewAI-purple) ![Cloud](https://img.shields.io/badge/Cloud-Azure%20Web%20Apps-blue)

An enterprise-grade AI-powered analytical ecosystem engineered to solve complex supply chain challenges, warehouse compliance visibility issues, and demand misalignments.

---

# 📌 Project Overview

**RetailX** transitions traditional, reactive ERP systems into a proactive intelligence matrix. The platform leverages a **Multi-Agent Swarm** to make data-driven decisions autonomously.

The RetailX Platform is designed to:
- ✅ Forecast inventory demand using a 131MB Machine Learning model.
- ✅ Ensure warehouse storage compliance (temperature/humidity) via RAG.
- ✅ Automate operational reports using Multi-Agent AI (CrewAI).
- ✅ Dynamically sync heavy ML assets from Azure Blob Storage.
- ✅ Deploy seamlessly using Docker + GitHub Actions + Azure Web Apps.

This project demonstrates a complete enterprise AI architecture using modern cloud-native technologies and strict security guardrails.

---

# 🌐 Complete System Architecture

```text
                    ┌─────────────────────┐
                    │  STREAMLIT UI       │
                    │  (User / Manager)   │
                    └─────────┬───────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │      FASTAPI SERVER    │
                  │   (Azure App Service)  │
                  └─────────┬──────────────┘
                            │
        ┌───────────────────┴────────────────────┐
        │                                        │
        ▼                                        ▼
┌────────────────┐                     ┌────────────────┐
│ INTENT GUARD   │                     │ CLOUD SYNC     │
│ (Azure OpenAI) │                     │ (Azure Blob)   │
└──────┬─────────┘                     └────────┬───────┘
       │                                        │
       ▼                                        ▼
┌───────────────────────────────────────────────────────┐
│           MASTER AUTONOMOUS SWARM ORCHESTRATOR        │
└───────────────────────┬───────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ DOCUMENT AGENT│ │ FORECAST AGENT│ │ RISK SUPERVISOR │
│ (RAG Search)  │ │ (ML Execution)│ │ (Synthesis)     │
└───────────────┘ └───────────────┘ └───────────────┘
```

---

# 🧩 Technology Stack

| Technology | Operational Function |
|---|---|
| **Streamlit** | Frontend Data Dashboard & Chat UI |
| **FastAPI / Uvicorn** | Asynchronous API routing and high-concurrency handling |
| **Azure OpenAI (GPT-4o)** | Intent Verification Guardrails & Natural Language Generation |
| **CrewAI** | Multi-Agent Swarm Orchestration |
| **Scikit-Learn** | Machine Learning Demand Forecasting |
| **Azure Blob Storage** | Dynamic syncing of heavy `.pkl` models and rulebooks |
| **Git LFS** | Large File Storage for 100MB+ models |
| **Docker** | Containerized Application Bundling |
| **GitHub Actions** | Multi-Stage CI/CD Automation |
| **Azure Web Apps** | Zero-touch Continuous Cloud Deployment |

---

# 📂 Project Structure Matrix

To maintain a production-ready environment, heavy and sensitive files are strictly isolated:

```text
RetailX_Core/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # Multi-stage CI/CD via Azure Publish Profiles
│
├── app/
│   ├── agents/
│   │   ├── orchestrator.py       # Core Swarm Router & Intent Gatekeeper
│   │   ├── anomaly_agent.py
│   │   ├── forecasting_agent.py
│   │   └── support_agent.py
│   │
│   ├── data/
│   │   └── warehouse_compliance.txt # Source rules for RAG
│   │
│   ├── models/
│   │   ├── demand_forecast_model.pkl # 131MB ML Model (Git LFS)
│   │   └── native_vector_rag.pkl     # Pre-computed semantic embeddings
│   │
│   ├── main.py                   # FastAPI Application Core
│   └── azure_storage.py          # Cloud Asset Sync Engine
│
├── Dockerfile                    # Optimized Python 3.12 Image Blueprint
├── .dockerignore / .gitignore    # Security nodes blocking local credentials
└── requirements.txt
```

---

# 🤖 Multi-Agent Swarm Architecture (CrewAI Layer)

# What is Swarm Intelligence?
Instead of a single LLM attempting to answer complex multi-domain queries, RetailX splits the workload across specialized AI workers operating in a sequential pipeline.

## 🧠 Swarm Workflow Diagram

```text
                     USER QUERY
                          │
                          ▼
               ┌──────────────────┐
               │ INTENT GATEKEEPER│
               │ (Blocks Off-Topic)│
               └────────┬─────────┘
                        │
                        ▼
               ┌──────────────────┐
               │ SWARM ORCHESTRATOR│
               └────────┬─────────┘
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ DOCUMENT AGENT │ │ FORECAST AGENT │ │ RISK SUPERVISOR│
│ (RAG Compliance│ │ (Runs ML Model)│ │ (Synthesizes   │
│  Extraction)   │ │                │ │  Final Output) │
└────────┬───────┘ └────────┬───────┘ └────────┬───────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │ Corporate Markdown │
                 │ Actionable Report  │
                 └────────────────────┘
```

## Available Agents

| Agent Identity | Core Responsibility |
|---|---|
| **Document Assistant (Compliance)** | Extracts strict climate thresholds (e.g., < 25°C) from `warehouse_compliance.txt` via RAG. |
| **Forecasting Agent (Data Science)**| Executes `demand_forecast_model.pkl` to predict inventory velocities and target turnovers. |
| **Risk Supervisor (Orchestrator)** | Accepts outputs from both sub-agents, evaluates stockout hazards, and drafts operational recommendations. |

---

# 📚 Retrieval-Augmented Generation (RAG) Architecture

RetailX ensures that the AI does not hallucinate logistics parameters by forcing it to read internal documents before answering.

## RAG Data Flow

```text
                  USER COMPLIANCE QUESTION
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Vector Search Engine  │
                 │ (native_vector_rag.pkl)│
                 └───────────┬───────────┘
                             │
             [Extracts Top-K Relevant Text Chunks]
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Azure OpenAI Endpoint │
                 │ (GPT-4o Evaluation)   │
                 └───────────┬───────────┘
                             │
                             ▼
                 Grounded Compliance Output
```

---

# ⚙️ Enterprise CI/CD Pipeline

The platform features a **Zero-Touch Multi-Stage Deployment** architecture. No manual server SSH or configuration is required post-commit.

## 🔄 CI/CD Workflow Diagram

```text
Developer (Git Push)
          │
          ▼
┌─────────────────────┐
│ GitHub Repository   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ GitHub Actions      │
│ (Triggered)         │
└─────────┬───────────┘
          │
      [Stage 1]
          ▼
┌─────────────────────┐
│ PyTest Validation & │
│ Docker Image Build  │
└─────────┬───────────┘
          │
      [Stage 2]
          ▼
┌─────────────────────┐
│ Docker Hub Push     │
│ (Explicit Tagging)  │
└─────────┬───────────┘
          │
      [Stage 3]
          ▼
┌─────────────────────┐
│ Azure App Service   │
│ (Direct Publish)    │
└─────────┬───────────┘
          │
          ▼
   🚀 Live Deployment
```

---

# 💎 Core Business Value (Impact)

1. **🚨 Zero Stockout Risks:** By mapping localized demand curves against active stock, structural supply chain gaps are exposed before revenue is lost.
2. **⚖️ Absolute Legal Compliance:** Ensures high-value electronic inventory adheres to non-negotiable ambient storage controls via real-time RAG audits.
3. **🛡️ Guardrail Security:** The Intent Gatekeeper neutralizes out-of-domain conversational queries, saving computational token costs and preventing system abuse.
4. **🚀 Developer Velocity:** The automated CI/CD pipeline ensures feature updates reach production within minutes without operational downtime.
