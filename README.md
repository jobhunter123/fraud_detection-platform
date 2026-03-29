# 🛡️ AI-Powered Fraud Detection & Attack Simulation Platform

A real-time financial fraud detection system combining rule-based heuristics with unsupervised ML anomaly detection, JWT-secured APIs, adversarial attack simulation, and LLM-generated investigation reports.

> Built with FastAPI · scikit-learn · SQLAlchemy · Chart.js

---

## 🚀 Live Demo

- **API Docs:** https://your-app.railway.app/docs
- **Dashboard:** Open `frontend/index.html` in your browser

---

## 🎯 What It Does

Every incoming transaction is passed through a two-layer fraud analysis pipeline:

1. **Rule Engine** — flags large amounts, new devices, geo-location changes, rapid velocity
2. **ML Model (Isolation Forest)** — detects statistical outliers invisible to rules

Combined into a **risk score 0–100** with an explainability layer that tells analysts *why* a transaction was flagged, plus an **LLM-generated investigation report** for flagged transactions.

---

## 🔥 Key Features

| Feature | Description |
|---|---|
| JWT Authentication | Secure register/login with bcrypt hashed passwords |
| Hybrid Fraud Detection | Rule engine + Isolation Forest anomaly detection |
| Explainability Layer | `risk_reasons` array on every response |
| LLM Investigation Reports | Claude AI generates analyst-ready fraud reports |
| Attack Simulator | Generates realistic fraud patterns for testing |
| Live Dashboard | Real-time charts, fraud highlighting, report viewer |
| REST API | Clean endpoints any payment gateway can integrate with |

---

## 📁 Project Structure

```
fraud-detection-platform/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI routes
│   │   ├── auth.py            # JWT authentication
│   │   ├── models.py          # SQLAlchemy ORM models
│   │   ├── schemas.py         # Pydantic validation
│   │   ├── database.py        # DB connection
│   │   ├── risk_engine.py     # Hybrid fraud scoring
│   │   ├── ml_model.py        # Isolation Forest
│   │   ├── attack_simulator.py# Adversarial generator
│   │   └── llm_reporter.py    # Claude AI reports
│   ├── requirements.txt
│   ├── Procfile
│   └── railway.toml
└── frontend/
    └── index.html             # Dashboard UI
```

---

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/fraud-detection-platform.git
cd fraud-detection-platform/backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables (optional for LLM reports)
# Windows PowerShell:
$env:ANTHROPIC_API_KEY="your-key-here"

# 5. Run the server
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to test the API.
Open `frontend/index.html` in your browser for the dashboard.

---

## 🔐 API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/register` | ❌ | Create account |
| POST | `/login` | ❌ | Get JWT token |
| POST | `/transaction` | ✅ | Submit & score transaction |
| GET | `/transactions` | ✅ | All transaction logs |
| GET | `/fraud` | ✅ | Flagged transactions only |
| GET | `/simulate_attack` | ✅ | Generate attack scenario |
| GET | `/stats` | ✅ | Fraud analytics summary |

---

## 🧠 How the Risk Score Works

```
Final Risk Score = Rule Score (60%) + ML Score (40%), capped at 100

Rules:
  Amount > ₹10,000      → +30
  New device            → +20
  Location change       → +25
  Rapid transactions    → +25

ML (Isolation Forest):
  Anomaly detected      → +40
  
Threshold: score > 70 → flagged as FRAUD 🚨
```

---

## 🌐 Deployment

Deployed on **Railway** — see [Deployment Guide](#) for steps.

---

## 📄 License

MIT