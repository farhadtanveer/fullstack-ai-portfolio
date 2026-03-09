from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# ── Data model (Pydantic validates input automatically) ───────────────
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True


# ── In-memory "database" for learning purposes ────────────────────────
fake_db: dict[int, Item] = {
    1: Item(name="Sensor A", description="Temperature sensor", price=29.99),
    2: Item(name="Relay Module", price=9.99, in_stock=False),
}
next_id = 3


# ── CRUD Endpoints ────────────────────────────────────────────────────
@router.get("/", response_model=dict[int, Item])
def list_items():
    """Return all items."""
    return fake_db


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    """Return a single item by ID."""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@router.post("/", response_model=Item, status_code=201)
def create_item(item: Item):
    """Create a new item."""
    global next_id
    fake_db[next_id] = item
    next_id += 1
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, updated: Item):
    """Replace an existing item."""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_db[item_id] = updated
    return updated


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]
