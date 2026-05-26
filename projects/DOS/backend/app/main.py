import os
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=True)
    fecha_limite = Column(String(50), nullable=True)
    prioridad = Column(String(20), default="media")  # baja, media, alta
    estado = Column(String(20), default="pendiente") # pendiente, completada
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskLiteJota — Gestor de Tareas", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class TaskCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None
    fecha_limite: Optional[str] = None
    prioridad: str = Field(default="media")

    @validator('prioridad')
    def validate_prioridad(cls, v):
        if v not in ["baja", "media", "alta"]:
            raise ValueError("La prioridad debe ser: baja, media o alta.")
        return v

class TaskEdit(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None
    fecha_limite: Optional[str] = None
    prioridad: str = Field(default="media")
    estado: str = Field(default="pendiente")

    @validator('prioridad')
    def validate_prioridad(cls, v):
        if v not in ["baja", "media", "alta"]:
            raise ValueError("La prioridad debe ser: baja, media o alta.")
        return v

    @validator('estado')
    def validate_estado(cls, v):
        if v not in ["pendiente", "completada"]:
            raise ValueError("El estado debe ser: pendiente o completada.")
        return v

class TaskResponse(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_limite: Optional[str] = None
    prioridad: str
    estado: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Helper to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/tasks", response_model=List[TaskResponse])
def get_tasks(
    estado: Optional[str] = Query(None),
    prioridad: Optional[str] = Query(None)
):
    db = SessionLocal()
    query = db.query(TaskDB)
    
    if estado:
        query = query.filter(TaskDB.estado == estado)
    if prioridad:
        query = query.filter(TaskDB.prioridad == prioridad)
        
    tasks = query.order_by(TaskDB.created_at.desc()).all()
    db.close()
    return tasks

@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    # Additional manual check for safety
    if len(task.titulo.strip()) < 3 or len(task.titulo.strip()) > 100:
        raise HTTPException(status_code=422, detail="El título debe tener entre 3 y 100 caracteres.")
        
    db = SessionLocal()
    db_task = TaskDB(
        titulo=task.titulo.strip(),
        descripcion=task.descripcion,
        fecha_limite=task.fecha_limite,
        prioridad=task.prioridad,
        estado="pendiente",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    db.close()
    return db_task

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskEdit):
    db = SessionLocal()
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        db.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
    if len(task_data.titulo.strip()) < 3 or len(task_data.titulo.strip()) > 100:
        db.close()
        raise HTTPException(status_code=422, detail="El título debe tener entre 3 y 100 caracteres.")
        
    db_task.titulo = task_data.titulo.strip()
    db_task.descripcion = task_data.descripcion
    db_task.fecha_limite = task_data.fecha_limite
    db_task.prioridad = task_data.prioridad
    db_task.estado = task_data.estado
    db_task.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_task)
    db.close()
    return db_task

@app.put("/api/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int):
    db = SessionLocal()
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        db.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
    db_task.estado = "completada"
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    db.close()
    return db_task

@app.put("/api/tasks/{task_id}/reopen", response_model=TaskResponse)
def reopen_task(task_id: int):
    db = SessionLocal()
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        db.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
    db_task.estado = "pendiente"
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    db.close()
    return db_task

@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    db = SessionLocal()
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        db.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(db_task)
    db.commit()
    db.close()
    return {"status": "deleted", "id": task_id}