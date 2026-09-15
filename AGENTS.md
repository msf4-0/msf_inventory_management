# MSF Inventory Management - Agent Guidelines

## Project State
- Windows (PowerShell) project
- Early-stage Python project
- Virtual environment at `venv/` (system Python 3.14.0)
- FastAPI backend with SQLite database
- HTMX + Jinja2 web UI
- Source: `main.py`

## Commands
- Create venv: `python -m venv venv`
- Activate venv: `venv\Scripts\Activate.ps1`
- Python: `venv\Scripts\python`
- Pip: `venv\Scripts\pip`
- Run server: `venv\Scripts\uvicorn main:app --reload`
- Run server (prod): `venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8000`

## API Endpoints
- GET `/` - Web UI (HTMX + Jinja2)
- POST `/items/` - Add item (JSON or form)
- GET `/items/` - List items (query: skip, limit)
- DELETE `/items/{item_id}` - Delete item by ID
- DELETE `/items/name/{item_name}` - Delete item by name

## Web UI
- Served at `/` (root path)
- HTMX for dynamic interactions (no page reloads)
- Jinja2 server-side templating
- Pico.css for styling (served locally)
- Static assets in `static/` (htmx.min.js, pico.min.css)
- Templates in `templates/` with partials in `templates/partials/`

## Database
- SQLite: `inventory.db` (auto-created)
- Table: `items` (id, name, description, quantity)

## Rules & Constraints
- Do not read or edit the Exercise.md file.