# FastAPI Learning Notes

> Personal notes as I work through Projects 01 and 02.

---

## Core Concepts

### Pydantic Models
FastAPI uses Pydantic for data validation. If the incoming JSON doesn't match your model, FastAPI returns a 422 error automatically.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float          # Required
    description: str | None = None  # Optional
```

### Path vs Query Parameters
```python
# Path parameter — part of the URL
@app.get("/items/{item_id}")
def get_item(item_id: int):  # FastAPI converts string -> int automatically
    ...

# Query parameter — after the ?
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    # /items/?skip=0&limit=10
    ...
```

### HTTPException
```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Item not found")
```

---

## Things That Confused Me (And The Answer)

**Q: What's the difference between `response_model` and return type hints?**
A: `response_model` filters and validates the OUTPUT. Return type hints are just for your IDE.

**Q: Why does TestClient need `httpx`?**
A: TestClient is built on top of httpx. Always add it to requirements.txt.

---

## Useful Commands

```bash
# Start dev server with auto-reload
uvicorn app.main:app --reload

# Run all tests verbosely
pytest tests/ -v

# Check test coverage
pytest tests/ --cov=app --cov-report=html
```

---

## Resources
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Pydantic v2 Docs](https://docs.pydantic.dev/)
