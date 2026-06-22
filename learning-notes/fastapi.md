# FastAPI — Personal Learning Notes

> A structured, chapter-by-chapter reference I built while learning FastAPI from scratch.
> Updated as I go. Written to be useful both as a quick reference and as a readable guide.

---

## Table of Contents

- [Chapter 01 — Introduction & Setup](#chapter-01--introduction--setup)
  - [Why FastAPI](#why-fastapi)
  - [How FastAPI Works Under the Hood](#how-fastapi-works-under-the-hood)
  - [Virtual Environments](#virtual-environments)
  - [Installation](#installation)
  - [Your First FastAPI App](#your-first-fastapi-app)
  - [Things That Confused Me](#things-that-confused-me-chapter-01)
  - [Useful Commands](#useful-commands)
- [Chapter 02 — Path Parameters & Query Parameters](#chapter-02--path-parameters--query-parameters)
  - [How FastAPI Decides Where a Parameter Comes From](#how-fastapi-decides-where-a-parameter-comes-from)
  - [Path Parameters](#path-parameters)
  - [Query Parameters](#query-parameters)
  - [Combining Path and Query Parameters](#combining-path-and-query-parameters)
  - [Enum — Predefined Valid Values](#enum--predefined-valid-values)
  - [Things That Confused Me](#things-that-confused-me-chapter-02)
- [Resources](#resources)

---

## Chapter 01 — Introduction & Setup

### Why FastAPI

I picked FastAPI over Django and Flask for API work because it hits the right balance between performance, developer experience, and built-in features.

| What matters      | What FastAPI offers                                               |
| ----------------- | ----------------------------------------------------------------- |
| Performance       | On par with Node.js and Go — one of the fastest Python frameworks |
| Development speed | Roughly 200–300% faster feature development                       |
| Fewer bugs        | Around 40% fewer developer-induced errors                         |
| Documentation     | Auto-generated from your code — no extra work needed              |
| Standards         | Fully compatible with OpenAPI and JSON Schema                     |

**Quick framework comparison:**

| Use case                              | Best choice |
| ------------------------------------- | ----------- |
| Pure API / backend service            | **FastAPI** |
| Full website with templates and admin | Django      |
| Minimal script-level web app          | Flask       |

---

### How FastAPI Works Under the Hood

FastAPI does not do everything itself. It stands on two solid libraries:

```
FastAPI
├── Starlette  →  Handles the web layer (routing, requests, responses, middleware)
└── Pydantic   →  Handles data validation using Python type hints
```

This is why when you write `item_id: int` in a function signature, FastAPI automatically validates that the incoming value is an integer. If it is not, it returns a clean `422 Unprocessable Entity` error — without you writing any validation logic.

---

### Virtual Environments

#### Why You Need One

When you install a package globally with `pip install`, it goes into your entire system's Python. That is fine until two projects need different versions of the same library — then they conflict and things break in ways that are hard to debug.

A virtual environment is an isolated Python installation scoped to one project. Each project gets its own packages and versions. Nothing leaks between them.

```
# Without venv — conflict waiting to happen
your-computer (global)
├── fastapi==0.100   ← Project A needs this
└── fastapi==0.80    ← Project B needs this  ✗ cannot coexist

# With venv — clean isolation
your-computer/
├── project-a/
│   └── .venv/    ← fastapi==0.100 lives here
└── project-b/
    └── .venv/    ← fastapi==0.80 lives here, no conflict
```

**Rule I follow:** Create a virtual environment before writing a single line of code in any Python project.

#### Creating and Managing a venv

**Create:**

```bash
python -m venv .venv
```

> Requires Python 3.10 or higher. Python 3.12 or 3.13 is recommended for new projects.
> Check your version with: `python --version`

**Activate:**

On **Windows:**

```bash
.venv\Scripts\activate
```

> PowerShell only — if you get a permissions error, run this once first:
>
> ```
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

On **macOS / Linux:**

```bash
source .venv/bin/activate
```

Once active, your terminal prompt will show `(.venv)` at the start.

**Deactivate:**

```bash
deactivate
```

**Never commit `.venv` to Git.** Add this to your `.gitignore`:

```
.venv/
__pycache__/
*.pyc
```

---

### Installation

With the virtual environment active:

```bash
pip install "fastapi[standard]"
```

The `[standard]` extra installs FastAPI plus everything needed to run it:

| Package    | Purpose                               |
| ---------- | ------------------------------------- |
| `fastapi`  | The core framework                    |
| `uvicorn`  | ASGI server — runs your app           |
| `pydantic` | Data validation                       |
| `httpx`    | Required for the built-in test client |

**Verify the installation:**

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

---

### Your First FastAPI App

Create a file called `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**Start the development server:**

```bash
fastapi dev main.py
```

**Open these in your browser:**

| URL                           | What you get                                             |
| ----------------------------- | -------------------------------------------------------- |
| `http://127.0.0.1:8000`       | Your API returning raw JSON                              |
| `http://127.0.0.1:8000/docs`  | **Swagger UI** — interactive, click-to-test API explorer |
| `http://127.0.0.1:8000/redoc` | **ReDoc** — clean, read-only documentation view          |

To stop the server: `CTRL + C`

---

### Things That Confused Me (Chapter 01)

**Q: Do I need to install `uvicorn` separately?**
A: No. `fastapi[standard]` already includes it. Only install it separately if you need a specific version.

**Q: What is the difference between `fastapi dev` and `uvicorn main:app --reload`?**
A: They do the same thing in development. `fastapi dev` is the newer, recommended command introduced in the FastAPI CLI. Use it — it is simpler.

**Q: Is `str | None` the same as `Optional[str]`?**
A: Yes. `str | None` is the modern Python 3.10+ syntax. `Optional[str]` from `typing` is the older equivalent. Both work in FastAPI — prefer `str | None` in new code.

---

### Useful Commands

```bash
# Create virtual environment
python -m venv .venv

# Activate — Windows
.venv\Scripts\activate

# Activate — macOS / Linux
source .venv/bin/activate

# Deactivate
deactivate

# Install FastAPI with standard extras
pip install "fastapi[standard]"

# Verify FastAPI version
python -c "import fastapi; print(fastapi.__version__)"

# Start development server with auto-reload
fastapi dev main.py

# Alternative (older style, still works)
uvicorn main:app --reload

# Save current dependencies to a file
pip freeze > requirements.txt

# Install from requirements file (e.g. after cloning a project)
pip install -r requirements.txt
```

---

## Chapter 02 — Path Parameters & Query Parameters

Every URL carries data. The question is _where_ in the URL that data lives. FastAPI gives you two clean mechanisms — path parameters and query parameters — and uses your function signature alone to tell them apart.

### How FastAPI Decides Where a Parameter Comes From

This is the single most important rule in this chapter:

- If a function parameter name appears inside `{}` in the route path → it is a **path parameter**
- If it does not appear in the path → FastAPI automatically treats it as a **query parameter**

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    ...
```

```
/items/{item_id}   →  item_id is in the path   →  path parameter
                       q is not in the path     →  query parameter (automatic)
```

No extra import or decorator needed. FastAPI figures it out from the route string.

---

### Path Parameters

A path parameter is a variable embedded directly inside the URL path, marked with curly braces `{}`.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

**What happens at the HTTP layer:**

```
Request:  GET /users/42
FastAPI:  extracts "42" from the URL (it arrives as a string at HTTP level)
          sees user_id: int
          converts "42" → 42 (Python int)
          passes 42 into get_user()

Request:  GET /users/abc
FastAPI:  tries to convert "abc" → int
          fails → returns 422 Unprocessable Entity automatically
```

#### Multiple path parameters

You can have more than one path parameter in the same route. FastAPI maps them by name, not by position.

```python
@app.get("/users/{user_id}/posts/{post_id}")
def get_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}

# GET /users/3/posts/17  →  {"user_id": 3, "post_id": 17}
```

#### Route order matters

FastAPI matches routes top to bottom. If you have a fixed path and a dynamic path that could overlap, always declare the fixed one first.

```python
# ✅ Correct order — /users/me is declared before /users/{user_id}
@app.get("/users/me")
def get_current_user():
    return {"user": "the current user"}

@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}
```

```python
# ✗ Wrong order — /users/me would be caught by /users/{user_id} first
# user_id would receive the string "me"
@app.get("/users/{user_id}")
def get_user(user_id: str):
    ...

@app.get("/users/me")   # this route would never be reached
def get_current_user():
    ...
```

---

### Query Parameters

Any function parameter that is **not** part of the URL path is automatically treated as a query parameter. Query parameters appear after `?` in the URL, separated by `&`.

```python
from fastapi import FastAPI

app = FastAPI()

fake_db = [{"name": "Foo"}, {"name": "Bar"}, {"name": "Baz"}]


@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    return fake_db[skip : skip + limit]
```

```
GET /items/            →  skip=0, limit=10  (defaults used)
GET /items/?skip=1     →  skip=1, limit=10
GET /items/?skip=1&limit=2  →  {"name": "Bar"}, {"name": "Baz"}
```

#### Optional query parameters

Set the default to `None` to make a parameter optional. FastAPI will not require it from the client.

```python
@app.get("/items/{item_id}")
def get_item(item_id: int, detail: str | None = None):
    result = {"item_id": item_id}
    if detail:
        result.update({"detail": detail})
    return result

# GET /items/5           →  {"item_id": 5}
# GET /items/5?detail=full  →  {"item_id": 5, "detail": "full"}
```

#### Required query parameters

Remove the default value entirely to make a query parameter required. FastAPI will return a `422` error if the client does not send it.

```python
@app.get("/search/")
def search(q: str):           # no default → required
    return {"query": q}

# GET /search/         →  422 Unprocessable Entity (q is missing)
# GET /search/?q=hello →  {"query": "hello"}
```

#### Boolean query parameters

FastAPI handles boolean conversion intelligently. These all evaluate to `True`:

```
?active=true  ?active=True  ?active=1  ?active=on  ?active=yes
```

And these to `False`:

```
?active=false  ?active=False  ?active=0  ?active=off  ?active=no
```

```python
@app.get("/items/{item_id}")
def get_item(item_id: int, active: bool = True):
    return {"item_id": item_id, "active": active}

# GET /items/3?active=false  →  {"item_id": 3, "active": false}
```

---

### Combining Path and Query Parameters

Path and query parameters can coexist freely in the same endpoint. FastAPI sorts them out by checking the route string.

```python
@app.get("/users/{user_id}/items/{item_id}")
def get_user_item(
    user_id: int,
    item_id: str,
    detail: bool = False,
    limit: int = 10,
):
    result = {"user_id": user_id, "item_id": item_id, "limit": limit}
    if detail:
        result.update({"detail": "some extra information"})
    return result
```

```
user_id  →  path parameter  (in the route string)
item_id  →  path parameter  (in the route string)
detail   →  query parameter (not in the route string, has a default)
limit    →  query parameter (not in the route string, has a default)
```

```
GET /users/1/items/hammer?detail=true&limit=5
→  {"user_id": 1, "item_id": "hammer", "limit": 5, "detail": "some extra information"}
```

---

### Enum — Predefined Valid Values

When a path parameter should only accept a specific set of values, use Python's `Enum`. FastAPI will validate against the allowed values and show them as a dropdown in `/docs`.

```python
from enum import Enum
from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet  = "resnet"
    lenet   = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model": model_name, "message": "LeCNN all the images"}
    return {"model": model_name, "message": "Have some residuals"}
```

```
GET /models/alexnet  →  200 OK
GET /models/resnet   →  200 OK
GET /models/pytorch  →  422 Unprocessable Entity  (not in the Enum)
```

Note that `ModelName` inherits from both `str` and `Enum`. The `str` inheritance is what allows FastAPI to serialize it in JSON responses and render it correctly in the docs.

---

### Things That Confused Me (Chapter 02)

**Q: What is the difference between a path parameter and a query parameter semantically — not just syntactically?**
A: Path parameters _identify_ a specific resource. Query parameters _modify_ how that resource is returned. `/users/42` identifies user 42. `/users/42?format=short` modifies how user 42's data is presented. Mixing them up produces APIs that are confusing to maintain and hard to cache correctly.

**Q: What happens if I forget to include a parameter in the `{}` path string?**
A: FastAPI silently treats it as a query parameter — no error, no warning. This is a subtle bug. If you intend something to be a required part of the URL path, double-check that the parameter name exists inside `{}` in the route decorator.

**Q: Can query parameters have no default and no `| None` — making them truly required?**
A: Yes. If you declare `q: str` with no default value and no `| None`, FastAPI requires it. The client must send it or receive a `422`. This is intentional and useful for things like search endpoints where a query string is always expected.

**Q: Does parameter order in the function signature matter?**
A: Not to FastAPI — it maps by name, not position. However, Python itself has a rule that parameters with defaults must come after parameters without defaults. If you run into ordering conflicts with `Path()` and `Query()`, the modern solution is to use `Annotated` (covered in a later chapter).

---

## Resources

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [FastAPI — Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [FastAPI — Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [Pydantic v2 Docs](https://docs.pydantic.dev/)
- [Uvicorn Docs](https://www.uvicorn.org/)
- [Python venv — Official Docs](https://docs.python.org/3/library/venv.html)
- [Python Enum — Official Docs](https://docs.python.org/3/library/enum.html)

---

_Part of my FastAPI learning series — one focused chapter at a time._
