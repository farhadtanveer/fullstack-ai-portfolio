# FastAPI — Learning Notes

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
  - [Things That Confused Me](#things-that-confused-me)
  - [Useful Commands](#useful-commands)

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

This creates a `.venv` folder inside your project directory. The dot prefix keeps it hidden from directory listings — that is intentional.

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

Once active, your terminal prompt will show `(.venv)` at the start — that is your confirmation.

```
(.venv) your-name\my-fastapi-project>   # Windows
(.venv) your-name@machine:~/project$    # macOS / Linux
```

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

> The quotes around `"fastapi[standard]"` are required — some terminals misinterpret the brackets without them.

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

What each part does:

```python
app = FastAPI()
# Creates your application instance — everything attaches to this object

@app.get("/")
# Registers read_root() as the handler for GET requests at the root URL

item_id: int
# FastAPI reads this type hint and validates the incoming value is an integer
# If someone passes "abc", FastAPI returns a 422 error automatically

q: str | None = None
# Optional query parameter — the endpoint works with or without it
# Example: /items/5?q=hello  or just  /items/5
```

**Start the development server:**

```bash
fastapi dev main.py
```

The `dev` command starts the server with auto-reload enabled. Any time you save a file, the server picks up the changes immediately.

**Open these in your browser:**

| URL                           | What you get                                             |
| ----------------------------- | -------------------------------------------------------- |
| `http://127.0.0.1:8000`       | Your API returning raw JSON                              |
| `http://127.0.0.1:8000/docs`  | **Swagger UI** — interactive, click-to-test API explorer |
| `http://127.0.0.1:8000/redoc` | **ReDoc** — clean, read-only documentation view          |

The `/docs` page is generated entirely from your type hints and function signatures. You write zero documentation code and still get a fully functional API explorer with input fields, example responses, and status codes.

To stop the server: `CTRL + C`

---

### Things That Confused Me

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

## Resources

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Pydantic v2 Docs](https://docs.pydantic.dev/)
- [Uvicorn Docs](https://www.uvicorn.org/)
- [Python venv — Official Docs](https://docs.python.org/3/library/venv.html)
