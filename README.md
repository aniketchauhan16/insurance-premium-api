<div align="center">

# 🏥 Insurance Premium Predictor API

### Predict insurance premium categories using a FastAPI-served ML model — with a Streamlit UI on top.

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Demo](#-demo) • [Quick Start](#-quick-start) • [API Reference](#-api-reference) • [Architecture](#-architecture) • [Roadmap](#-roadmap)

</div>

---

## 📌 What is this?

A machine learning model — wrapped in a production-style FastAPI service — that predicts a person's **insurance premium category** (`High` / `Medium` / `Low`) based on basic profile inputs like age, BMI, city tier, and lifestyle risk.

This isn't just a notebook with `model.predict()` — it's the full pipeline:

```
Raw user input  →  Pydantic validation + computed features  →  Model inference  →  JSON response  →  Streamlit UI
```

Built as a hands-on project to learn how ML models actually get **served**, not just trained.

---

## 🎬 Demo

> 🚧 **Local-only for now** — AWS deployment is on the roadmap. Run it yourself in under 2 minutes (see Quick Start below).

| Swagger UI | Streamlit Frontend |
|:---:|:---:|
| `http://localhost:8000/docs` | `http://localhost:8501` |

---

## ⚡ Quick Start

### 1. Clone & set up

```bash
git clone https://github.com/<your-username>/insurance-premium-api.git
cd insurance-premium-api

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 2. Run the API

```bash
uvicorn main:app --reload
```
→ Open **http://localhost:8000/docs** for the interactive Swagger UI.

### 3. Run the frontend

```bash
streamlit run app.py
```
→ Open **http://localhost:8501** to use the web interface.

### 4. Or run with Docker 🐳

```bash
docker build -t insurance-premium-api -f Dockerfile.txt .
docker run -p 8000:8000 insurance-premium-api
```

---

## 🧠 API Reference

### `POST /predict`

Predicts the insurance premium category for a given patient profile.

<details>
<summary><b>📥 Request body</b></summary>

```json
{
  "id": "P001",
  "name": "Aniket",
  "city": "Delhi",
  "age": 21,
  "gender": "male",
  "height": 1.78,
  "weight": 70
}
```

</details>

<details>
<summary><b>📤 Response</b></summary>

```json
{
  "predicted_category": "Medium",
  "confidence": 0.82
}
```

</details>

<details>
<summary><b>🧮 Computed features (handled automatically via Pydantic)</b></summary>

| Field | Derived from | Logic |
|---|---|---|
| `bmi` | `height`, `weight` | `weight / (height ** 2)` |
| `age_group` | `age` | bucketed into ranges |
| `lifestyle_risk` | `bmi`, `age` | rule-based scoring |
| `city_tier` | `city` | mapped via lookup table |

</details>

---

## 🏗️ Architecture

```
┌──────────────┐      POST /predict      ┌───────────────┐      .pkl      ┌──────────────┐
│  Streamlit   │ ───────────────────────▶ │   FastAPI     │ ─────────────▶ │  RandomForest │
│  Frontend    │ ◀─────────────────────── │   + Pydantic  │ ◀───────────── │  Classifier   │
└──────────────┘     JSON response        └───────────────┘   prediction   └──────────────┘
```

**Why this stack:**
- **FastAPI** → async-ready, auto-generates OpenAPI docs, fast to build
- **Pydantic** → validates raw input *and* computes derived features (no manual feature engineering at request time)
- **Scikit-learn** → simple, interpretable model for a learning project
- **Streamlit** → zero-frontend-code UI to demo the API visually

---

## 📂 Project Structure

```
insurance-premium-api/
├── model/
│   └── model.pkl          # trained RandomForestClassifier
├── main.py                 # FastAPI app + /predict endpoint
├── app.py                  # Streamlit frontend
├── requirements.txt
├── Dockerfile.txt
├── .dockerignore
└── README.md
```

---

## 🛣️ Roadmap

- [x] Train model + export as `.pkl`
- [x] Build FastAPI endpoint with Pydantic validation
- [x] Build Streamlit frontend
- [x] Dockerize the app
- [ ] Deploy on AWS (ECS)
- [ ] Add request logging
- [ ] Add basic test suite (`pytest` + `httpx`)
- [ ] CI/CD with GitHub Actions

---

## 🙋 About This Project

Built while learning FastAPI + ML model serving as part of my AI engineering learning path. The modeling code (feature engineering, RandomForest training) was adapted from a CampusX tutorial — the focus of this project was the **API design, request validation, and deployment pipeline**, not the ML modeling itself.

---

<div align="center">

**[⬆ Back to top](#-insurance-premium-predictor-api)**

</div>
