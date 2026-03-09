# Project 01 — FastAPI Basics

> **Goal:** Learn FastAPI fundamentals — routing, Pydantic models, CRUD operations, and testing.

## What I Built
A simple Items API simulating an industrial parts inventory.
No database yet — uses an in-memory dict to keep focus on FastAPI concepts.

## Tech Stack
- Python 3.12
- FastAPI 0.111
- Pydantic v2 (data validation)
- pytest + TestClient (testing)

## How to Run

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment file
cp .env.example .env

# 4. Start the server
uvicorn app.main:app --reload

# 5. Open interactive API docs
# http://localhost:8000/docs
```

## Run Tests

```bash
pytest tests/ -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/items/` | List all items |
| GET | `/items/{id}` | Get single item |
| POST | `/items/` | Create item |
| PUT | `/items/{id}` | Update item |
| DELETE | `/items/{id}` | Delete item |

## What I Learned
- [ ] FastAPI project structure and routing
- [ ] Pydantic BaseModel for request/response validation
- [ ] HTTP status codes and error handling with HTTPException
- [ ] Writing tests with TestClient
