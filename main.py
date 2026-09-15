from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, field_validator
from typing import List, Optional

DATABASE_URL = "sqlite:///./inventory.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    quantity = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int = 0

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Item name cannot be blank")
        return v

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    quantity: int

    class Config:
        from_attributes = True

app = FastAPI(title="Inventory Management System")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    items = db.query(Item).order_by(func.lower(Item.name)).all()
    return templates.TemplateResponse(
        request, "index.html", {"items": items}
    )

def get_items_sorted(db: Session):
    return db.query(Item).order_by(func.lower(Item.name)).all()

@app.post("/items/", response_model=ItemResponse)
def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    existing = db.query(Item).filter(func.lower(Item.name) == item.name.lower()).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Item with name '{item.name}' already exists")
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.post("/items/form", response_class=HTMLResponse)
def add_item_form(
    request: Request,
    name: str = Form(...),
    description: str = Form(None),
    quantity: int = Form(0),
    db: Session = Depends(get_db)
):
    name = name.strip()
    if not name:
        return templates.TemplateResponse(
            request,
            "partials/error_message.html",
            {"message": "Item name cannot be blank."},
            headers={"HX-Retarget": "#form-error", "HX-Reswap": "innerHTML"},
        )
    existing = db.query(Item).filter(func.lower(Item.name) == name.lower()).first()
    if existing:
        return templates.TemplateResponse(
            request,
            "partials/error_message.html",
            {"message": f"Item '{name}' already exists."},
            headers={"HX-Retarget": "#form-error", "HX-Reswap": "innerHTML"},
        )
    db_item = Item(name=name, description=description, quantity=quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return templates.TemplateResponse(
        request, "partials/item_table.html", {"items": get_items_sorted(db)}
    )

@app.post("/items/{item_id}/adjust", response_class=HTMLResponse)
def adjust_item_quantity(
    request: Request,
    item_id: int,
    delta: int = Form(...),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.quantity = max(0, item.quantity + delta)
    db.commit()
    return templates.TemplateResponse(
        request, "partials/item_table.html", {"items": get_items_sorted(db)}
    )

@app.get("/items/", response_model=List[ItemResponse])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).order_by(func.lower(Item.name)).offset(skip).limit(limit).all()
    return items

@app.delete("/items/all")
def delete_all_items(request: Request, db: Session = Depends(get_db)):
    count = db.query(Item).delete()
    db.commit()
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request, "partials/item_table.html", {"items": get_items_sorted(db)}
        )
    return {"message": f"Deleted {count} items successfully"}

@app.delete("/items/{item_id}")
def delete_item_by_id(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request, "partials/item_table.html", {"items": get_items_sorted(db)}
        )
    return {"message": "Item deleted successfully"}

@app.delete("/items/name/{item_name}")
def delete_item_by_name(item_name: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.name == item_name).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}