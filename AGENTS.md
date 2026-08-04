# MSF Inventory Management - Agent Guidelines

## Project State
- Early-stage Python 3.12 project
- Virtual environment at `venv/` (Python 3.12.3)
- FastAPI backend with SQLite database
- HTMX + Jinja2 web UI
- Source: `main.py`

## Commands
- Activate venv: `source venv/bin/activate`
- Python: `venv/bin/python`
- Pip: `venv/bin/pip`
- Run server: `venv/bin/uvicorn main:app --reload`
- Run server (prod): `venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000`

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