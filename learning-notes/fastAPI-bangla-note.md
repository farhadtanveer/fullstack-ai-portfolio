# FastAPI — সম্পূর্ণ বাংলা নোট

> **Stack:** FastAPI + SQLAlchemy + Pydantic + Alembic + MySQL/PostgreSQL

---

## সূচিপত্র

1. [FastAPI কী এবং এর মূল ভিত্তি](#১-fastapi-কী-এবং-এর-মূল-ভিত্তি)
2. [প্রজেক্ট স্ট্রাকচার](#২-প্রজেক্ট-স্ট্রাকচার)
3. [৫টি লেয়ার — বিস্তারিত](#৩-৫টি-লেয়ার--বিস্তারিত)
4. [Request Lifecycle](#৪-request-lifecycle)
5. [Core Concepts](#৫-core-concepts)
6. [নতুন Service তৈরির Step-by-Step](#৬-নতুন-service-তৈরির-step-by-step)
7. [Real Code Example](#৭-real-code-example--products-module)

---

## ১. FastAPI কী এবং এর মূল ভিত্তি

FastAPI হলো একটি Python web framework যেটা দিয়ে backend API বানানো যায়। React (frontend) থেকে request আসে, FastAPI সেটা handle করে database থেকে data নিয়ে response পাঠায়।

### FastAPI তিনটি জিনিসের উপর দাঁড়িয়ে আছে:

```
FastAPI = Starlette + Pydantic + Dependency Injection
```

| লাইব্রেরি        | কাজ                                      | React-এর সাথে তুলনা                    |
| ---------------- | ---------------------------------------- | -------------------------------------- |
| **Starlette**    | HTTP routing, middleware, server         | React Router এর মতো কিন্তু server-side |
| **Pydantic**     | Data validation এবং serialization        | PropTypes কিন্তু অনেক শক্তিশালী        |
| **FastAPI core** | এই দুটোকে একসাথে connect করে + DI system | —                                      |

### FastAPI তোমাকে বিনামূল্যে যা দেয়:

```
✅ Auto validation    — ভুল data আসলে নিজেই reject করে (422 error)
✅ Auto docs          — /docs এ গেলে Swagger UI পাবে, কোনো কাজ ছাড়াই
✅ Dependency injection — DB session, current user নিজেই inject করে
✅ Type safety        — Python type hints থেকে সব কিছু generate করে
```

### সবচেয়ে সহজ FastAPI app:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()   # এটাই পুরো application

class ProductIn(BaseModel):   # Pydantic — React কী পাঠাবে তার shape
    name: str
    price: float

@app.post("/products")        # Starlette — HTTP routing
async def create(data: ProductIn):   # FastAPI type hint পড়ে auto validate করে
    return {"id": 1, "name": data.name}
    # FastAPI নিজেই dict কে JSON বানিয়ে পাঠায়
```

---

## ২. প্রজেক্ট স্ট্রাকচার

জার্মান কোম্পানিগুলো (Celonis, Personio, CHECK24) **domain-driven** structure follow করে। মানে technical type অনুযায়ী না, **business feature** অনুযায়ী folder ভাগ করা হয়।

### পুরো প্রজেক্ট layout:

```
my-project/
├── backend/          ← FastAPI (এই নোট এটার জন্য)
├── frontend/         ← React
└── ai/               ← ভবিষ্যতে AI module
```

### backend/ এর ভেতরে:

```
backend/
├── main.py                      # App startup, middleware, router include
├── .env                         # Secrets — কখনো commit করবে না!
├── .env.example                 # Safe template — এটা commit করো
├── requirements.txt             # অথবা pyproject.toml (আরো modern)
├── alembic/                     # Database migrations
│   ├── env.py
│   └── versions/                # প্রতিটা migration file এখানে
│
└── app/
    ├── core/                    # সব module এটা use করে
    │   ├── config.py            # .env পড়ে (pydantic-settings দিয়ে)
    │   ├── security.py          # JWT encode/decode, password hashing
    │   ├── dependencies.py      # get_db(), get_current_user()
    │   └── exceptions.py        # Global HTTP error handlers
    │
    ├── db/
    │   ├── base.py              # SQLAlchemy Base class
    │   ├── session.py           # Engine + SessionLocal
    │   └── mixins.py            # TimestampMixin (created_at, updated_at)
    │
    ├── users/                   # ← একটা domain module
    │   ├── model.py             # User SQLAlchemy model (DB table)
    │   ├── schemas.py           # UserCreate, UserRead, UserUpdate
    │   ├── repository.py        # Raw DB queries
    │   ├── service.py           # Business logic
    │   ├── router.py            # HTTP endpoints
    │   ├── exceptions.py        # UserNotFound, UserAlreadyExists
    │   └── __init__.py
    │
    ├── products/                # একই structure
    │   ├── model.py
    │   ├── schemas.py
    │   ├── repository.py
    │   ├── service.py
    │   ├── router.py
    │   └── __init__.py
    │
    ├── auth/
    │   ├── router.py            # POST /auth/login, /auth/refresh
    │   ├── schemas.py           # TokenResponse, LoginRequest
    │   ├── service.py           # credentials verify, token issue
    │   └── __init__.py
    │
    └── api/
        └── v1/
            └── router.py        # সব router একসাথে — "switchboard"
```

### কেন domain-driven structure?

```
❌ Technical Structure (খারাপ):
   models/product.py
   schemas/product.py        → "product delete" করতে
   services/product_service.py  5টা folder খুলতে হবে!
   repositories/product_repo.py
   api/v1/products.py

✅ Domain Structure (ভালো):
   products/
   ├── model.py              → শুধু "products/" folder
   ├── schemas.py               খুললেই সব পাবে!
   ├── repository.py
   ├── service.py
   └── router.py
```

---

## ৩. ৫টি লেয়ার — বিস্তারিত

প্রতিটা module (users/, products/) এ ঠিক এই ৫টি layer থাকে। প্রতিটার একটাই কাজ।

### Layer Connection ফ্লোচার্ট:

```mermaid
flowchart TD
    React["🌐 React (Frontend)\naxios.post('/api/v1/products')"]
    Router["router.py\nHTTP endpoints only"]
    Service["service.py\nBusiness logic only"]
    Repo["repository.py\nDB queries only"]
    Model["model.py\nSQLAlchemy table"]
    DB["🗄️ Database\nMySQL / PostgreSQL"]
    Schema["schemas.py\nPydantic validation"]
    Deps["core/dependencies.py\nget_db, get_current_user"]

    React -->|"POST /products\n{name, price}"| Router
    Router -->|"validates via"| Schema
    Router -->|"calls"| Service
    Deps -.->|"Depends() inject"| Router
    Service -->|"business rules"| Repo
    Repo -->|"SQLAlchemy query"| Model
    Model -->|"INSERT/SELECT"| DB
    DB -->|"ORM object"| Repo
    Repo -->|"returns"| Service
    Service -->|"returns"| Router
    Router -->|"response_model filter"| Schema
    Schema -->|"JSON response"| React

    style React fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style Schema fill:#E1F5EE,stroke:#0F6E56,color:#085041
    style Deps fill:#FAEEDA,stroke:#854F0B,color:#633806
    style DB fill:#F1EFE8,stroke:#5F5E5A,color:#444441
```

---

### Layer 1 — `model.py` (Database Table)

**একমাত্র কাজ:** Database table define করা। Business logic নেই, validation নেই।

```python
# app/products/model.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.mixins import TimestampMixin

class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String(255), nullable=False)
    price   = Column(Integer, nullable=False)   # টাকা cent এ রাখো
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="products")
```

```python
# app/db/mixins.py
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
```

---

### Layer 2 — `schemas.py` (API Contract / Pydantic)

**একমাত্র কাজ:** React কী পাঠাবে এবং React কী পাবে তা define করা।

> ⚠️ **গুরুত্বপূর্ণ:** `model.py` আর `schemas.py` আলাদা কারণ — DB তে `password_hash` column থাকলেও React কে সেটা কখনো দেওয়া উচিত না। `response_model` দিয়ে সেটা filter হয়।

```python
# app/products/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):     # React এটা পাঠায়
    name: str = Field(min_length=2, max_length=255)
    price: int = Field(gt=0)        # 0 এর বেশি হতে হবে

class ProductUpdate(BaseModel):     # PATCH request এর জন্য
    name: Optional[str] = None      # সব field optional
    price: Optional[int] = None

class ProductRead(BaseModel):       # React এটা receive করে
    id: int
    name: str
    price: int
    created_at: datetime

    class Config:
        from_attributes = True      # ORM object → Pydantic convert করতে দেয়
```

**Pydantic auto validation উদাহরণ:**

```
React পাঠালো: {"name": "", "price": -5}

FastAPI নিজেই reject করে:
{
  "detail": [
    {"loc": ["body","name"], "msg": "String too short"},
    {"loc": ["body","price"], "msg": "Input should be greater than 0"}
  ]
}
তোমার কোড একটুও run হয়নি!
```

---

### Layer 3 — `repository.py` (Database Queries)

**একমাত্র কাজ:** SQL query লেখা। Business logic একদম নেই।

```python
# app/products/repository.py
from sqlalchemy.orm import Session
from app.products.model import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product)\
                      .filter(Product.id == product_id)\
                      .first()

    def get_all(self, skip: int = 0, limit: int = 20):
        return self.db.query(Product)\
                      .offset(skip).limit(limit).all()

    def create(self, name: str, price: int, user_id: int) -> Product:
        product = Product(name=name, price=price, user_id=user_id)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)   # DB থেকে নতুন id নিয়ে আসে
        return product

    def update(self, product: Product, data: dict) -> Product:
        for key, value in data.items():
            setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()
```

---

### Layer 4 — `service.py` (Business Logic)

**একমাত্র কাজ:** Business rules implement করা। HTTP জানে না, SQL জানে না।

> 💡 কোনো business rule পরিবর্তন হলে শুধু এই file বদলাও। বাকি কোথাও হাত দিতে হবে না।

```python
# app/products/service.py
from app.products.repository import ProductRepository
from app.products.schemas import ProductCreate, ProductUpdate
from app.products.exceptions import ProductNotFound, ProductNameTaken

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, data: ProductCreate, user_id: int):
        # Business rule: একই user এর একই নামে দুটো product থাকবে না
        existing = self.repo.get_by_name(data.name, user_id)
        if existing:
            raise ProductNameTaken(data.name)

        return self.repo.create(
            name=data.name,
            price=data.price,
            user_id=user_id
        )

    def get_or_404(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise ProductNotFound(product_id)  # domain exception
        return product

    def update_product(self, product_id: int, data: ProductUpdate, user_id: int):
        product = self.get_or_404(product_id)

        # Business rule: নিজের product ছাড়া অন্যেরটা edit করা যাবে না
        if product.user_id != user_id:
            raise PermissionDenied()

        update_data = data.model_dump(exclude_unset=True)  # None বাদ দেয়
        return self.repo.update(product, update_data)

    def delete_product(self, product_id: int, user_id: int):
        product = self.get_or_404(product_id)
        if product.user_id != user_id:
            raise PermissionDenied()
        self.repo.delete(product)
```

---

### Layer 5 — `router.py` (HTTP Endpoints)

**একমাত্র কাজ:** HTTP request → service call → HTTP response। Business logic একদম নেই।

```python
# app/products/router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.products.schemas import ProductCreate, ProductRead, ProductUpdate
from app.products.service import ProductService
from app.products.repository import ProductRepository
from app.users.model import User

router = APIRouter()

# Service inject করার helper
def get_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))

@router.post("/", response_model=ProductRead, status_code=201)
def create_product(
    data: ProductCreate,                              # Pydantic auto validate
    service: ProductService = Depends(get_service),  # DI inject
    current_user: User = Depends(get_current_user)   # JWT decode → User object
):
    return service.create_product(data, current_user.id)

@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_service)
):
    return service.get_or_404(product_id)

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.update_product(product_id, data, current_user.id)

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    service.delete_product(product_id, current_user.id)
```

---

### Layer Summary — কোথায় কী করবে না:

```mermaid
flowchart LR
    subgraph router["router.py ✅"]
        r1["HTTP method define"]
        r2["Pydantic schema declare"]
        r3["Depends() inject"]
        r4["Service call করো"]
    end

    subgraph service["service.py ✅"]
        s1["Business rules লেখো"]
        s2["Exception raise করো"]
        s3["Repository call করো"]
        s4["অন্য service call করো"]
    end

    subgraph repo["repository.py ✅"]
        rep1["SQL query লেখো"]
        rep2["db.add(), commit()"]
        rep3["filter(), join()"]
    end

    subgraph never["❌ কখনো না"]
        n1["router এ if/else logic"]
        n2["service এ SQL query"]
        n3["repo তে email পাঠানো"]
        n4["router এ db.query()"]
    end
```

---

## ৪. Request Lifecycle

React থেকে `POST /api/v1/products` call করলে ভেতরে কী হয়:

```mermaid
sequenceDiagram
    participant R as React
    participant M as Middleware
    participant D as Depends()
    participant P as Pydantic
    participant Ep as Endpoint fn
    participant S as Service
    participant Rp as Repository
    participant DB as Database

    R->>M: POST /api/v1/products<br/>{name, price}
    Note over M: CORS check<br/>Auth middleware
    M->>D: request পাস
    Note over D: get_db() → DB session খোলে<br/>get_current_user() → JWT decode → User fetch
    D->>P: validated dependencies পাস
    Note over P: ProductCreate validate<br/>ভুল হলে 422 return করে
    P->>Ep: typed data object পাস
    Ep->>S: service.create_product(data, user_id)
    Note over S: Business rules check<br/>name unique কিনা দেখে
    S->>Rp: repo.create(name, price, user_id)
    Rp->>DB: INSERT INTO products...
    DB-->>Rp: নতুন row return
    Rp-->>S: Product ORM object
    S-->>Ep: Product ORM object
    Note over Ep: response_model=ProductRead<br/>দিয়ে filter করে
    Ep-->>R: HTTP 201 + JSON<br/>{id, name, price, created_at}
    Note over D: finally: db.close() — session বন্ধ
```

---

## ৫. Core Concepts

### ক) `Depends()` — Dependency Injection

React এর `useContext` এর মতো, কিন্তু function এর জন্য। তুমি declare করো কী দরকার, FastAPI নিজেই দিয়ে দেয়।

```python
# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Generator function — এটাই magic
def get_db():
    db = SessionLocal()
    try:
        yield db        # ← এখানে endpoint চলে
    finally:
        db.close()      # ← সবসময় বন্ধ হয়, এমনকি error হলেও
```

```python
# app/core/dependencies.py
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.users.model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = decode_token(token)    # JWT decode
    user = db.query(User).get(payload["user_id"])
    if not user:
        raise HTTPException(status_code=401)
    return user   # ← endpoint এ inject হয়
```

```python
# Endpoint এ use:
@router.post("/products")
def create(
    data: ProductCreate,
    db: Session = Depends(get_db),              # DB session inject
    user: User = Depends(get_current_user)      # User object inject
):
    # db আর user দুটোই ready, তুমি শুধু ব্যবহার করো
```

---

### খ) Pydantic — Validation + Serialization

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    price: int = Field(gt=0, description="Price in cents")
    category: Optional[str] = None

    # Custom validator লেখা যায়
    @field_validator('name')
    @classmethod
    def name_must_not_be_url(cls, v):
        if 'http' in v:
            raise ValueError('Name cannot be a URL')
        return v.strip()   # whitespace remove করে
```

**Input vs Output Schema সবসময় আলাদা রাখো:**

```
ProductCreate  ← React পাঠায়    (id নেই, created_at নেই)
ProductUpdate  ← PATCH এ আসে   (সব field Optional)
ProductRead    ← React পায়     (id আছে, created_at আছে, password_hash নেই)
```

---

### গ) Exceptions — Error Handling

```python
# app/products/exceptions.py
class ProductNotFound(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id

class ProductNameTaken(Exception):
    def __init__(self, name: str):
        self.name = name

class PermissionDenied(Exception):
    pass
```

```python
# app/main.py — Global handlers register করো
from fastapi.responses import JSONResponse

@app.exception_handler(ProductNotFound)
def handle_product_not_found(request, exc: ProductNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Product {exc.product_id} not found"}
    )

@app.exception_handler(ProductNameTaken)
def handle_name_taken(request, exc: ProductNameTaken):
    return JSONResponse(
        status_code=409,
        content={"detail": f"Product name '{exc.name}' already exists"}
    )
```

---

### ঘ) Alembic — Database Migration

> Alembic হলো database এর জন্য git। Schema change কখনো manually করবে না।

```bash
# Initial setup
pip install alembic
alembic init alembic

# নতুন migration তৈরি (model change করার পর)
alembic revision --autogenerate -m "add products table"

# Migration apply করো
alembic upgrade head

# একধাপ পিছে যাও
alembic downgrade -1

# History দেখো
alembic history
```

```python
# alembic/env.py এ তোমার models import করতে হবে
from app.db.base import Base
from app.users.model import User      # ← import করো
from app.products.model import Product  # ← import করো

target_metadata = Base.metadata
```

---

### ঙ) `main.py` — সব একসাথে

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title="My API",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc"      # ReDoc UI
)

# CORS — React dev server কে allow করো
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React Vite port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# সব router include করো
app.include_router(api_router, prefix="/api/v1")
```

```python
# app/api/v1/router.py — Switchboard
from fastapi import APIRouter
from app.users.router import router as users_router
from app.products.router import router as products_router
from app.auth.router import router as auth_router

api_router = APIRouter()
api_router.include_router(users_router,    prefix="/users",    tags=["users"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(auth_router,     prefix="/auth",     tags=["auth"])
```

---

### চ) `async def` vs `def`

```python
# ✅ async use করো — External HTTP call এর জন্য
@router.get("/weather")
async def get_weather():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.weather.com/...")
    return response.json()

# ✅ regular def — SQLAlchemy sync DB queries এর জন্য
@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
    # FastAPI এটাকে threadpool এ run করে, block করে না

# 💡 Rule of thumb:
# httpx, aiohttp দিয়ে external call → async def
# SQLAlchemy (sync) DB query → regular def
# নিশ্চিত না? → regular def দিলেই চলে
```

---

### ছ) `config.py` — Environment Variables

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"   # .env file থেকে পড়ে

settings = Settings()   # singleton — সব জায়গায় এটা import করো
```

```bash
# .env
DATABASE_URL=mysql+pymysql://user:password@localhost/mydb
SECRET_KEY=your-super-secret-key-here
```

---

## ৬. নতুন Service তৈরির Step-by-Step

যেকোনো নতুন feature তৈরি করতে এই order follow করো:

```mermaid
flowchart TD
    A["Step 1️⃣\nAlembic migration লেখো\nalembic revision --autogenerate"]
    B["Step 2️⃣\nmodel.py লেখো\nSQLAlchemy table class"]
    C["Step 3️⃣\nschemas.py লেখো\nCreate, Update, Read Pydantic models"]
    D["Step 4️⃣\nexceptions.py লেখো\nDomain exceptions define করো"]
    E["Step 5️⃣\nrepository.py লেখো\nCRUD DB queries"]
    F["Step 6️⃣\nservice.py লেখো\nBusiness logic + repo call"]
    G["Step 7️⃣\nrouter.py লেখো\nHTTP endpoints + Depends()"]
    H["Step 8️⃣\napi/v1/router.py তে register করো\nএকটা line যোগ করো"]
    I["✅ Done!\n/docs এ গিয়ে test করো"]

    A --> B --> C --> D --> E --> F --> G --> H --> I

    style A fill:#FAEEDA,stroke:#854F0B,color:#633806
    style B fill:#FAEEDA,stroke:#854F0B,color:#633806
    style C fill:#E1F5EE,stroke:#0F6E56,color:#085041
    style D fill:#FCEBEB,stroke:#A32D2D,color:#791F1F
    style E fill:#E1F5EE,stroke:#0F6E56,color:#085041
    style F fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style G fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style H fill:#F1EFE8,stroke:#5F5E5A,color:#444441
    style I fill:#EAF3DE,stroke:#3B6D11,color:#27500A
```

---

## ৭. Real Code Example — Products Module

এখানে শুরু থেকে শেষ পর্যন্ত একটা পূর্ণ products module:

### Step 1: Migration

```bash
alembic revision --autogenerate -m "create products table"
alembic upgrade head
```

### Step 2 — model.py

```python
# app/products/model.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.mixins import TimestampMixin

class Product(TimestampMixin, Base):
    __tablename__ = "products"
    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String(255), nullable=False)
    price   = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user    = relationship("User", back_populates="products")
```

### Step 3 — schemas.py

```python
# app/products/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name:  str = Field(min_length=2, max_length=255)
    price: int = Field(gt=0)

class ProductUpdate(BaseModel):
    name:  Optional[str] = None
    price: Optional[int] = None

class ProductRead(BaseModel):
    id: int
    name: str
    price: int
    created_at: datetime
    class Config:
        from_attributes = True
```

### Step 4 — exceptions.py

```python
# app/products/exceptions.py
class ProductNotFound(Exception):
    def __init__(self, pid: int): self.pid = pid

class ProductNameTaken(Exception):
    def __init__(self, name: str): self.name = name
```

### Step 5 — repository.py

```python
# app/products/repository.py
from sqlalchemy.orm import Session
from app.products.model import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, pid: int):
        return self.db.query(Product).filter(Product.id == pid).first()

    def get_by_name(self, name: str, user_id: int):
        return self.db.query(Product).filter(
            Product.name == name, Product.user_id == user_id
        ).first()

    def create(self, name: str, price: int, user_id: int) -> Product:
        p = Product(name=name, price=price, user_id=user_id)
        self.db.add(p); self.db.commit(); self.db.refresh(p)
        return p

    def get_all(self, user_id: int, skip=0, limit=20):
        return self.db.query(Product)\
                      .filter(Product.user_id == user_id)\
                      .offset(skip).limit(limit).all()
```

### Step 6 — service.py

```python
# app/products/service.py
from app.products.repository import ProductRepository
from app.products.schemas import ProductCreate
from app.products.exceptions import ProductNotFound, ProductNameTaken

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create(self, data: ProductCreate, user_id: int):
        if self.repo.get_by_name(data.name, user_id):
            raise ProductNameTaken(data.name)
        return self.repo.create(data.name, data.price, user_id)

    def get_or_404(self, pid: int):
        product = self.repo.get_by_id(pid)
        if not product:
            raise ProductNotFound(pid)
        return product

    def list_mine(self, user_id: int):
        return self.repo.get_all(user_id)
```

### Step 7 — router.py

```python
# app/products/router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.products.schemas import ProductCreate, ProductRead
from app.products.service import ProductService
from app.products.repository import ProductRepository

router = APIRouter()

def get_service(db: Session = Depends(get_db)):
    return ProductService(ProductRepository(db))

@router.post("/", response_model=ProductRead, status_code=201)
def create(data: ProductCreate, svc=Depends(get_service), user=Depends(get_current_user)):
    return svc.create(data, user.id)

@router.get("/", response_model=list[ProductRead])
def list_all(svc=Depends(get_service), user=Depends(get_current_user)):
    return svc.list_mine(user.id)

@router.get("/{pid}", response_model=ProductRead)
def get_one(pid: int, svc=Depends(get_service)):
    return svc.get_or_404(pid)

@router.delete("/{pid}", status_code=204)
def delete(pid: int, svc=Depends(get_service), user=Depends(get_current_user)):
    product = svc.get_or_404(pid)
    svc.repo.delete(product)
```

### Step 8 — Register

```python
# app/api/v1/router.py এ যোগ করো
from app.products.router import router as products_router
api_router.include_router(products_router, prefix="/products", tags=["products"])
```

### Test করো:

```bash
uvicorn main:app --reload
# তারপর browser এ: http://localhost:8000/docs
```

---

## Quick Reference চিটশিট

```
HTTP Status Codes:
200 → OK (GET success)
201 → Created (POST success)
204 → No Content (DELETE success)
400 → Bad Request (তুমি ভুল পাঠিয়েছ)
401 → Unauthorized (login করোনি)
403 → Forbidden (permission নেই)
404 → Not Found (data নেই)
409 → Conflict (duplicate data)
422 → Validation Error (Pydantic reject)
500 → Server Error (backend এ bug)
```

```
Alembic Commands:
alembic revision --autogenerate -m "message"  → migration তৈরি
alembic upgrade head                          → latest migration apply
alembic downgrade -1                          → একধাপ পিছে
alembic history                               → migration list দেখো
alembic current                               → current version দেখো
```

```
Run করার command:
uvicorn main:app --reload          → development
uvicorn main:app --host 0.0.0.0   → production ready
```
