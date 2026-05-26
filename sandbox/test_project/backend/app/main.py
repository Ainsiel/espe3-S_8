import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(250), nullable=True)
    cantidad = Column(Integer, default=0)
    precio = Column(Float, default=0.0)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Web Transaccional", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class ItemCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    descripcion: Optional[str] = None
    cantidad: int = Field(default=0, ge=0)
    precio: float = Field(default=0.0, ge=0.0)

class ItemResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    cantidad: int
    precio: float

    class Config:
        orm_mode = True

# Helper dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/items", response_model=List[ItemResponse])
def get_items():
    db = SessionLocal()
    items = db.query(ItemDB).all()
    db.close()
    return items

@app.post("/api/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = ItemDB(
        nombre=item.nombre,
        descripcion=item.descripcion,
        cantidad=item.cantidad,
        precio=item.precio
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

@app.delete("/api/items/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not db_item:
        db.close()
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(db_item)
    db.commit()
    db.close()
    return {"status": "deleted", "id": item_id}