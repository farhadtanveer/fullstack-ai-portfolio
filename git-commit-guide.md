# Git Commit Message Guide

## Format
```
<type>: <short description>

[optional body — explain WHY, not WHAT]
```

## Types

| Type | When to use |
|------|------------|
| `feat` | New feature or endpoint |
| `fix` | Bug fix |
| `test` | Adding or fixing tests |
| `docs` | README or comment updates |
| `refactor` | Code change that doesn't fix or add anything |
| `chore` | Dependency updates, config changes |
| `style` | Formatting only (Black, Ruff) |

## Good Examples

```
feat: add POST /items endpoint with Pydantic validation

fix: return 404 when item_id not in database

test: add tests for create and delete item endpoints

docs: update project 01 README with API table

chore: pin fastapi to 0.111.0 in requirements.txt

feat: add JWT auth middleware to project 02

feat: serve sentiment model via /predict endpoint
```

## Bad Examples (avoid these)

```
update               ← Too vague
fixed stuff          ← What stuff?
WIP                  ← Never commit this to main
final version        ← Nothing is ever final
asdf                 ← You know better
```

## Branch Naming

```
feat/add-prediction-endpoint
fix/cors-error-on-frontend
docs/update-project-03-readme
```
