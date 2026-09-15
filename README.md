# MSF Inventory Management

FastAPI backend for inventory management with SQLite database and HTMX + Jinja2 web UI.
This repo is used for teaching the AI-Assisted Coding module by SHRDC.

## Setup

```bash
# Create virtual env
python -m venv venv

# Install dependencies
venv/bin/pip install fastapi uvicorn sqlalchemy pydantic jinja2 
```

## Run Server

```bash
# Development (auto-reload)
venv/Scripts/uvicorn main:app --reload

# Production
venv/Scripts/uvicorn main:app --host 0.0.0.0 --port 8000
```

Server runs at `http://localhost:8000`. 
- **Web UI**: `http://localhost:8000/` (HTMX + Jinja2)
- **API docs**: `http://localhost:8000/docs` (Swagger UI)

