# 🚀 Getting Started

A step-by-step guide to get this repo running on a new machine.

---

## 1. Clone and Initial Setup

```bash
git clone https://github.com/YOUR_USERNAME/fullstack-ai-portfolio.git
cd fullstack-ai-portfolio
```

## 2. Install Pre-commit Hooks
This runs Black + Ruff automatically before every commit.

```bash
pip install pre-commit
pre-commit install
```

Done. Every `git commit` will now auto-format your code.

---

## 3. Run Project 01 (FastAPI Basics)

```bash
cd projects/01-fastapi-basics

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start server
uvicorn app.main:app --reload

# Open docs → http://localhost:8000/docs
# Run tests
pytest tests/ -v
```

---

## 4. Run Project 03 (AI Sentiment API)

```bash
cd projects/03-ai-sentiment
pip install -r requirements.txt

# Step 1: Train the model in Jupyter
jupyter notebook notebooks/train_model.ipynb
# → Run all cells → saves model to /model/sentiment_model.joblib

# Step 2: Start the API
uvicorn app.main:app --reload

# Test prediction
curl -X POST http://localhost:8000/predict/ \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is absolutely fantastic!"}'
```

---

## 5. Run Project 04 (Full Stack — Capstone)

```bash
cd projects/04-industrial-dashboard
cp .env.example .env
# Edit .env with your values

# Start everything with one command
docker-compose up --build

# Frontend → http://localhost:3000
# Backend API docs → http://localhost:8000/docs
```

---

## Useful Commands

```bash
# Format all Python code
black .

# Lint all Python code
ruff check .

# Run pre-commit on all files manually
pre-commit run --all-files
```
