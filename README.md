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
venv/bin/uvicorn main:app --reload

# Production
venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
```

Server runs at `http://localhost:8000`. 
- **Web UI**: `http://localhost:8000/` (HTMX + Jinja2)
- **API docs**: `http://localhost:8000/docs` (Swagger UI)

## API Endpoints

### Add Item
```bash
POST /items/
Content-Type: application/json

{
  "name": "CNC Machine",
  "description": "5-axis CNC milling machine",
  "quantity": 2
}
```

### List Items
```bash
GET /items/?skip=0&limit=100
```

### Delete Item
```bash
DELETE /items/{item_id}
```

### Delete Item by Name
```bash
DELETE /items/name/{item_name}
```

## Example Usage (curl)

```bash
# Add item
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "CNC Machine", "description": "5-axis CNC milling machine", "quantity": 2}'

# List items
curl http://localhost:8000/items/

# Delete item
curl -X DELETE http://localhost:8000/items/1
```

## Web UI Features

The web UI at `/` provides:
- **Table view** of all inventory items (ID, Name, Description, Quantity)
- **Add item form** with name, description, and quantity fields
- **Delete buttons** with confirmation dialog for each item
- **HTMX-powered** interactions (no page reloads)
- **Pico.css** for lightweight styling

## Database

- SQLite file: `inventory.db` (auto-created)
- Table: `items` (id, name, description, quantity)

## Project Structure

```
.
├── main.py              # FastAPI application
├── inventory.db         # SQLite database
├── static/
│   ├── htmx.min.js      # HTMX library (local)
│   └── pico.min.css     # Pico.css framework (local)
├── templates/
│   ├── base.html        # Base template
│   ├── index.html       # Main page
│   └── partials/
│       ├── item_row.html    # Table row partial
│       └── item_form.html   # Add item form partial
└── test_api.py          # API test script
```

## Frontend Stack

- **HTMX** - Hypermedia-driven interactions
- **Jinja2** - Server-side templating
- **Pico.css** - Minimal CSS framework
- All static assets served locally (no CDN dependencies)