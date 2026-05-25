# Alfa Horizon: Income Prediction and Scoring MVP

Alfa Horizon is a team project for Alfa Hackathon 2025. The product prototype helps a bank manager estimate a client's income, inspect risk factors, and generate personalized product offers from a single dashboard.

My role: Data Analyst. I worked on the ML/data part of the solution: feature preparation, CatBoost validation, prediction service integration, and analytics artifacts for the dashboard.

## Highlights

- Built an income prediction pipeline with CatBoostRegressor for tabular client and transaction data.
- Prepared feature engineering flow for cleaned train/test datasets and model inference.
- Validated the model on a time-based holdout with WMAE as the target metric.
- Integrated the ML service with a FastAPI endpoint used by the Node.js backend and Vue dashboard.
- Added SHAP-based factor output in the Python service for explainable prediction cards.

## Model Result

| Metric | Value |
| --- | ---: |
| Validation metric | WMAE |
| Validation WMAE | 69,077.82 |
| Model | CatBoostRegressor |
| Feature set | 225 features |
| Categorical features | 27 |

The metric is stored in `ml/models/catboost_full_fe_meta.json` and was calculated on the internal validation split.

## Stack

- ML/Data: Python, pandas, NumPy, CatBoost, feature engineering, WMAE validation.
- API: FastAPI for model inference, Node.js/Express as an API layer.
- Frontend: Vue 3, TypeScript, Vite, Pinia, Chart.js.
- Product prototype: client dashboard, income prediction, product recommendation logic, PDF/Excel export.

## Architecture

```text
front/       Vue 3 dashboard and manager UI
back/        Node.js API layer and business logic
ml/          CatBoost training, feature processing, FastAPI inference
docs/        Contracts and supporting project notes
```

## Local Run

Requirements: Node.js 16+, Python 3.9+.

Start the ML service:

```bash
cd ml
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.service.app:app --reload --port 8000
```

Start the backend:

```bash
cd back
npm install
npm run dev
```

Start the frontend:

```bash
cd front
npm install
npm run dev
```

## Data and Model Files

The repository contains prepared hackathon artifacts required for the demo flow: cleaned data files, trained CatBoost models, generated submissions, and report files. In a production repository these files would normally be moved to object storage, Git LFS, or GitHub Releases.

## Team

Project for Alfa Hackathon 2025:

- Alexander Belyanchikov - Frontend Developer
- Lev Voziyanov - Data Analyst
- Denis Nguyen - Data Scientist
- Daniil Prelsky - Backend Developer
