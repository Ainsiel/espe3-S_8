import os

class ImplementerAgent:
    def __init__(self, logger, usage_ledger):
        self.logger = logger
        self.usage_ledger = usage_ledger

    def execute(self, project_id, project_dir):
        self.logger.log_event("implementer_agent", "implement", "Iniciando implementación atómica de componentes de software", "success")
        
        # Simulate LLM usage
        self.usage_ledger.record_usage(
            agent_id="implementer_agent",
            phase="implement",
            skill_id="apply_patch",
            input_tokens=3000,
            output_tokens=4000
        )

        backend_dir = os.path.join(project_dir, "backend")
        frontend_dir = os.path.join(project_dir, "frontend")
        os.makedirs(os.path.join(backend_dir, "app"), exist_ok=True)
        os.makedirs(os.path.join(backend_dir, "tests"), exist_ok=True)
        os.makedirs(frontend_dir, exist_ok=True)

        if project_id.strip().upper() in ["UNO", "DOS", "TRES"]:
            # 1. Write TaskLiteJota backend/app/main.py
            main_py = """import os
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
"""
            with open(os.path.join(backend_dir, "app", "main.py"), "w", encoding="utf-8") as f:
                f.write(main_py.strip())

            # 2. Write TaskLiteJota backend/tests/test_main.py (Pytest suite)
            test_main_py = """import pytest
from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app, engine, Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

def test_create_task_success():
    response = client.post(
        "/api/tasks",
        json={"titulo": "Aprender FastAPI", "descripcion": "Leer la documentación", "prioridad": "alta"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Aprender FastAPI"
    assert data["prioridad"] == "alta"
    assert data["estado"] == "pendiente"
    assert data["id"] is not None

def test_create_task_invalid_title():
    # Title too short (< 3)
    response1 = client.post("/api/tasks", json={"titulo": "Hi", "prioridad": "baja"})
    assert response1.status_code == 422

    # Title empty
    response2 = client.post("/api/tasks", json={"titulo": "", "prioridad": "baja"})
    assert response2.status_code == 422

    # Title too long (> 100)
    response3 = client.post("/api/tasks", json={"titulo": "A" * 101, "prioridad": "alta"})
    assert response3.status_code == 422

def test_get_tasks_sorting():
    # Insert multiple tasks
    client.post("/api/tasks", json={"titulo": "Tarea 1"})
    client.post("/api/tasks", json={"titulo": "Tarea 2"})
    
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    # Check creation descending order (newest first)
    assert data[0]["titulo"] == "Tarea 2"
    assert data[1]["titulo"] == "Tarea 1"

def test_edit_task_success():
    resp_create = client.post("/api/tasks", json={"titulo": "Tarea Inicial", "prioridad": "baja"})
    task_id = resp_create.json()["id"]
    
    resp_edit = client.put(
        f"/api/tasks/{task_id}",
        json={"titulo": "Tarea Editada", "prioridad": "alta", "estado": "pendiente", "descripcion": "Nueva desc"}
    )
    assert resp_edit.status_code == 200
    data = resp_edit.json()
    assert data["titulo"] == "Tarea Editada"
    assert data["prioridad"] == "alta"
    assert data["descripcion"] == "Nueva desc"
    assert data["updated_at"] is not None

def test_toggle_status():
    resp_create = client.post("/api/tasks", json={"titulo": "Hacer Ejercicio"})
    task_id = resp_create.json()["id"]
    
    # Complete task
    resp_comp = client.put(f"/api/tasks/{task_id}/complete")
    assert resp_comp.status_code == 200
    assert resp_comp.json()["estado"] == "completada"
    
    # Reopen task
    resp_reop = client.put(f"/api/tasks/{task_id}/reopen")
    assert resp_reop.status_code == 200
    assert resp_reop.json()["estado"] == "pendiente"

def test_delete_task_success():
    resp_create = client.post("/api/tasks", json={"titulo": "Eliminar Tarea"})
    task_id = resp_create.json()["id"]
    
    resp_del = client.delete(f"/api/tasks/{task_id}")
    assert resp_del.status_code == 200
    
    # Verify 404 on get/edit/delete
    resp_get = client.delete(f"/api/tasks/{task_id}")
    assert resp_get.status_code == 404
"""
            with open(os.path.join(backend_dir, "tests", "test_main.py"), "w", encoding="utf-8") as f:
                f.write(test_main_py.strip())

            # 3. Write TaskLiteJota frontend/index.html (Bootstrap 5 Premium glassmorphism dark-mode client)
            index_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TaskLiteJota — Gestor Personal de Tareas</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #020617;
            --bg-glass: rgba(15, 23, 42, 0.65);
            --border-glass: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-purple: #8b5cf6;
            --accent-cyan: #06b6d4;
        }
        body {
            font-family: 'Outfit', sans-serif;
            background: radial-gradient(circle at top left, #0f172a 0%, #020617 80%);
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 50px;
        }
        .navbar-custom {
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-glass);
        }
        .logo-text {
            font-weight: 800;
            background: linear-gradient(135deg, #a78bfa 0%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        .glass-card {
            background: var(--bg-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .interactive-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(139,92,246,0.15);
            border-color: rgba(139,92,246,0.3);
        }
        .form-control, .form-select {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: var(--text-main) !important;
            border-radius: 10px;
        }
        .form-control:focus, .form-select:focus {
            box-shadow: 0 0 0 2px rgba(139,92,246,0.4) !important;
            border-color: var(--accent-purple) !important;
        }
        .btn-premium {
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
            border: none;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            transition: all 0.3s;
        }
        .btn-premium:hover {
            opacity: 0.95;
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(139,92,246,0.4);
            color: white;
        }
        .badge-priority-alta {
            background-color: rgba(239, 68, 68, 0.2);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }
        .badge-priority-media {
            background-color: rgba(245, 158, 11, 0.2);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }
        .badge-priority-baja {
            background-color: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }
        .badge-status-pendiente {
            background-color: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }
        .badge-status-completada {
            background-color: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            text-decoration: line-through;
        }
        .task-title-strike {
            text-decoration: line-through;
            color: var(--text-secondary);
        }
        .btn-action-icon {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            color: var(--text-main);
            transition: all 0.2s;
        }
        .btn-action-icon:hover {
            background: rgba(139, 92, 246, 0.2);
            border-color: var(--accent-purple);
            color: white;
        }
        .btn-action-delete:hover {
            background: rgba(239, 68, 68, 0.2);
            border-color: #ef4444;
            color: #f87171;
        }
        /* Custom modal dark theme */
        .modal-content {
            background-color: #0f172a;
            border: 1px solid var(--border-glass);
            border-radius: 16px;
        }
    </style>
</head>
<body>
    <!-- React Mount Root -->
    <div id="root"></div>

    <!-- React, ReactDOM, Babel UMD Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js" crossorigin></script>
    <script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
    <script src="https://cdn.jsdelivr.net/npm/@babel/standalone/babel.min.js"></script>

    <!-- React Client Application -->
    <script type="text/babel">
        const { useState, useEffect } = React;
        const API_BASE = 'http://localhost:8000/api/tasks';

        function App() {
            const [tasks, setTasks] = useState([]);
            const [filterEstado, setFilterEstado] = useState('');
            const [filterPrioridad, setFilterPrioridad] = useState('');
            
            // Form state
            const [titulo, setTitulo] = useState('');
            const [descripcion, setDescripcion] = useState('');
            const [prioridad, setPrioridad] = useState('media');
            const [fechaLimite, setFechaLimite] = useState('');
            
            // Editing state
            const [editTaskId, setEditTaskId] = useState(null);
            const [toastMessage, setToastMessage] = useState(null);
            const [toastType, setToastType] = useState('success');
            
            // Delete confirmation state
            const [deleteTaskId, setDeleteTaskId] = useState(null);

            useEffect(() => {
                fetchTasks();
            }, [filterEstado, filterPrioridad]);

            const showToast = (msg, type = 'success') => {
                setToastMessage(msg);
                setToastType(type);
                setTimeout(() => setToastMessage(null), 4000);
            };

            const fetchTasks = async () => {
                try {
                    let url = API_BASE;
                    const params = [];
                    if (filterEstado) params.push(`estado=${filterEstado}`);
                    if (filterPrioridad) params.push(`prioridad=${filterPrioridad}`);
                    if (params.length > 0) {
                        url += '?' + params.join('&');
                    }
                    
                    const res = await fetch(url);
                    if (!res.ok) throw new Error('Error al conectar con el servidor API');
                    const data = await res.json();
                    setTasks(data);
                } catch (err) {
                    showToast(err.message, 'danger');
                }
            };

            const handleSubmit = async (e) => {
                e.preventDefault();
                if (titulo.trim().length < 3 || titulo.trim().length > 100) {
                    showToast('El título debe tener entre 3 y 100 caracteres.', 'danger');
                    return;
                }

                const taskPayload = {
                    titulo: titulo.trim(),
                    descripcion: descripcion.trim() || null,
                    fecha_limite: fechaLimite || null,
                    prioridad: prioridad
                };

                try {
                    if (editTaskId) {
                        // We are editing. The edit endpoint expects TaskEdit schema including "estado"
                        const taskToEdit = tasks.find(t => t.id === editTaskId);
                        const editPayload = {
                            ...taskPayload,
                            estado: taskToEdit ? taskToEdit.estado : 'pendiente'
                        };

                        const res = await fetch(`${API_BASE}/${editTaskId}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(editPayload)
                        });
                        
                        if (!res.ok) {
                            const errData = await res.json();
                            throw new Error(errData.detail || 'Fallo al editar la tarea');
                        }
                        showToast('¡Tarea modificada correctamente!');
                        setEditTaskId(null);
                    } else {
                        // Creating new
                        const res = await fetch(API_BASE, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(taskPayload)
                        });
                        
                        if (!res.ok) {
                            const errData = await res.json();
                            throw new Error(errData.detail || 'Fallo al guardar la tarea');
                        }
                        showToast('¡Tarea creada correctamente!');
                    }

                    // Reset form
                    setTitulo('');
                    setDescripcion('');
                    setPrioridad('media');
                    setFechaLimite('');
                    fetchTasks();
                } catch (err) {
                    showToast(err.message, 'danger');
                }
            };

            const handleEditClick = (task) => {
                setEditTaskId(task.id);
                setTitulo(task.titulo);
                setDescripcion(task.descripcion || '');
                setPrioridad(task.prioridad);
                setFechaLimite(task.fecha_limite || '');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            };

            const cancelEdit = () => {
                setEditTaskId(null);
                setTitulo('');
                setDescripcion('');
                setPrioridad('media');
                setFechaLimite('');
            };

            const toggleStatus = async (task) => {
                try {
                    const endpoint = task.estado === 'pendiente' ? 'complete' : 'reopen';
                    const res = await fetch(`${API_BASE}/${task.id}/${endpoint}`, {
                        method: 'PUT'
                    });
                    if (!res.ok) throw new Error('Error al cambiar el estado de la tarea');
                    showToast(task.estado === 'pendiente' ? '¡Tarea completada!' : '¡Tarea reabierta!');
                    fetchTasks();
                } catch (err) {
                    showToast(err.message, 'danger');
                }
            };

            const triggerDelete = (id) => {
                setDeleteTaskId(id);
            };

            const confirmDelete = async () => {
                if (!deleteTaskId) return;
                try {
                    const res = await fetch(`${API_BASE}/${deleteTaskId}`, {
                        method: 'DELETE'
                    });
                    if (!res.ok) throw new Error('No se pudo borrar la tarea');
                    showToast('Tarea eliminada de forma permanente.', 'success');
                    setDeleteTaskId(null);
                    fetchTasks();
                } catch (err) {
                    showToast(err.message, 'danger');
                }
            };

            return (
                <div>
                    {/* Glassmorphism Navbar */}
                    <nav className="navbar navbar-dark navbar-custom mb-5 py-3">
                        <div className="container d-flex justify-content-between align-items-center">
                            <span className="navbar-brand d-flex align-items-center gap-2">
                                <i className="bi bi-check2-square fs-3 text-purple" style={{color: '#a78bfa'}}></i>
                                <span className="logo-text fs-3">TaskLiteJota</span>
                            </span>
                            <span className="badge bg-secondary py-2 px-3 border border-dark rounded-pill fs-7 d-flex align-items-center gap-1">
                                <i className="bi bi-hdd-network text-info"></i> v1.0.0 (SQLite Local)
                            </span>
                        </div>
                    </nav>

                    <div className="container">
                        {toastMessage && (
                            <div className={`alert alert-${toastType} d-flex align-items-center gap-2 border-0 rounded-4 py-3 shadow-lg mb-4`} role="alert">
                                <i className={`bi ${toastType === 'danger' ? 'bi-exclamation-triangle-fill' : 'bi-check-circle-fill'}`}></i>
                                <div className="fw-semibold">{toastMessage}</div>
                            </div>
                        )}

                        <div className="row">
                            {/* Left: Form Card */}
                            <div className="col-lg-4 mb-4">
                                <div className="glass-card p-4">
                                    <h4 className="mb-4 d-flex align-items-center gap-2">
                                        <i className={`bi ${editTaskId ? 'bi-pencil-square text-warning' : 'bi-plus-circle-fill text-purple'}`} style={{color: editTaskId ? '#fbbf24' : '#8b5cf6'}}></i>
                                        <span>{editTaskId ? 'Editar Tarea' : 'Nueva Tarea'}</span>
                                    </h4>

                                    <form onSubmit={handleSubmit}>
                                        <div className="mb-3">
                                            <label htmlFor="titulo" className="form-label fw-medium text-secondary">Título de la Tarea <span className="text-danger">*</span></label>
                                            <input 
                                                type="text" 
                                                className="form-control" 
                                                id="titulo" 
                                                value={titulo}
                                                onChange={(e) => setTitulo(e.target.value)}
                                                placeholder="Ej. Comprar viveres" 
                                                required
                                            />
                                            <div className="form-text text-muted" style={{fontSize: '0.8rem'}}>Debe contener entre 3 y 100 caracteres.</div>
                                        </div>

                                        <div className="mb-3">
                                            <label htmlFor="descripcion" className="form-label fw-medium text-secondary">Descripción</label>
                                            <textarea 
                                                className="form-control" 
                                                id="descripcion" 
                                                rows="3" 
                                                value={descripcion}
                                                onChange={(e) => setDescripcion(e.target.value)}
                                                placeholder="Escribe detalles sobre la tarea..."
                                            ></textarea>
                                        </div>

                                        <div className="row">
                                            <div className="col-md-6 mb-3">
                                                <label htmlFor="prioridad" className="form-label fw-medium text-secondary">Prioridad</label>
                                                <select 
                                                    className="form-select" 
                                                    id="prioridad"
                                                    value={prioridad}
                                                    onChange={(e) => setPrioridad(e.target.value)}
                                                >
                                                    <option value="baja">Baja</option>
                                                    <option value="media">Media</option>
                                                    <option value="alta">Alta</option>
                                                </select>
                                            </div>
                                            <div className="col-md-6 mb-3">
                                                <label htmlFor="fechaLimite" className="form-label fw-medium text-secondary">Fecha Límite</label>
                                                <input 
                                                    type="date" 
                                                    className="form-control" 
                                                    id="fechaLimite" 
                                                    value={fechaLimite}
                                                    onChange={(e) => setFechaLimite(e.target.value)}
                                                />
                                            </div>
                                        </div>

                                        <button type="submit" className="btn btn-premium w-100 py-2.5 mt-3 d-flex align-items-center justify-content-center gap-2">
                                            <i className="bi bi-save"></i> {editTaskId ? 'Guardar Cambios' : 'Registrar Tarea'}
                                        </button>

                                        {editTaskId && (
                                            <button type="button" onClick={cancelEdit} className="btn btn-outline-secondary w-100 py-2.5 mt-2 rounded-3 border-secondary">
                                                Cancelar Edición
                                            </button>
                                        )}
                                    </form>
                                </div>
                            </div>

                            {/* Right: List and Filters */}
                            <div className="col-lg-8">
                                {/* Filter Bar Card */}
                                <div className="glass-card p-4 mb-4">
                                    <div className="row align-items-center g-3">
                                        <div className="col-md-4">
                                            <h5 className="m-0 d-flex align-items-center gap-2">
                                                <i className="bi bi-filter-left text-cyan" style={{color: '#06b6d4'}}></i>
                                                <span>Filtros Operativos</span>
                                            </h5>
                                        </div>
                                        <div className="col-md-4">
                                            <select 
                                                className="form-select form-select-sm"
                                                value={filterEstado}
                                                onChange={(e) => setFilterEstado(e.target.value)}
                                            >
                                                <option value="">Estado: Todos</option>
                                                <option value="pendiente">Pendientes</option>
                                                <option value="completada">Completadas</option>
                                            </select>
                                        </div>
                                        <div className="col-md-4">
                                            <select 
                                                className="form-select form-select-sm"
                                                value={filterPrioridad}
                                                onChange={(e) => setFilterPrioridad(e.target.value)}
                                            >
                                                <option value="">Prioridad: Todas</option>
                                                <option value="alta">Alta</option>
                                                <option value="media">Media</option>
                                                <option value="baja">Baja</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                {/* Tasks List rendering */}
                                <div className="d-flex flex-column gap-3">
                                    {tasks.length === 0 ? (
                                        <div className="glass-card p-5 text-center">
                                            <i className="bi bi-clipboard-x fs-1 text-secondary mb-3 d-block"></i>
                                            <h5 className="text-secondary">Sin tareas pendientes o registradas</h5>
                                            <p className="text-muted small m-0">¡Añade una tarea usando el panel izquierdo para comenzar!</p>
                                        </div>
                                    ) : (
                                        tasks.map(task => (
                                            <div key={task.id} className={`glass-card interactive-card p-4 d-flex justify-content-between align-items-center gap-3 border-start border-4 ${task.prioridad === 'alta' ? 'border-danger' : task.prioridad === 'media' ? 'border-warning' : 'border-success'}`}>
                                                <div className="d-flex align-items-start gap-3">
                                                    {/* Circle status check toggle button */}
                                                    <button 
                                                        onClick={() => toggleStatus(task)} 
                                                        className="btn p-0 border-0 fs-4 text-purple mt-0.5"
                                                        style={{background: 'none', color: task.estado === 'completada' ? '#34d399' : '#94a3b8'}}
                                                    >
                                                        <i className={`bi ${task.estado === 'completada' ? 'bi-check-circle-fill text-success' : 'bi-circle'}`}></i>
                                                    </button>

                                                    <div>
                                                        <h5 className={`m-0 fw-bold ${task.estado === 'completada' ? 'task-title-strike' : ''}`}>
                                                            {task.titulo}
                                                        </h5>
                                                        {task.descripcion && (
                                                            <p className="text-secondary small mt-1 mb-2">
                                                                {task.descripcion}
                                                            </p>
                                                        )}
                                                        <div className="d-flex flex-wrap gap-2 mt-1 align-items-center">
                                                            <span className={`badge px-2.5 py-1 rounded-pill ${task.estado === 'completada' ? 'badge-status-completada' : 'badge-status-pendiente'}`}>
                                                                {task.estado === 'completada' ? 'Completada' : 'Pendiente'}
                                                            </span>
                                                            <span className={`badge px-2.5 py-1 rounded-pill badge-priority-${task.prioridad}`}>
                                                                Prioridad: {task.prioridad.toUpperCase()}
                                                            </span>
                                                            {task.fecha_limite && (
                                                                <span className="text-muted small d-flex align-items-center gap-1">
                                                                    <i className="bi bi-calendar-event"></i> Límite: {task.fecha_limite}
                                                                </span>
                                                            )}
                                                        </div>
                                                    </div>
                                                </div>

                                                {/* Action Buttons */}
                                                <div className="d-flex gap-2">
                                                    <button 
                                                        onClick={() => handleEditClick(task)}
                                                        className="btn btn-action-icon"
                                                        title="Editar tarea"
                                                    >
                                                        <i className="bi bi-pencil"></i>
                                                    </button>
                                                    <button 
                                                        onClick={() => triggerDelete(task.id)}
                                                        className="btn btn-action-icon btn-action-delete"
                                                        title="Eliminar tarea"
                                                    >
                                                        <i className="bi bi-trash"></i>
                                                    </button>
                                                </div>
                                            </div>
                                        ))
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Custom Bootstrap Dark Confirmation Modal */}
                    {deleteTaskId && (
                        <div className="modal fade show d-block" style={{background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)'}} tabIndex="-1" role="dialog">
                            <div className="modal-dialog modal-dialog-centered" role="document">
                                <div className="modal-content p-3">
                                    <div className="modal-header border-0">
                                        <h5 className="modal-title fw-bold text-danger d-flex align-items-center gap-2">
                                            <i className="bi bi-exclamation-triangle-fill"></i> Confirmar Eliminación
                                        </h5>
                                        <button type="button" onClick={() => setDeleteTaskId(null)} className="btn-close btn-close-white" aria-label="Close"></button>
                                    </div>
                                    <div className="modal-body border-0 py-2">
                                        <p className="text-secondary">¿Estás seguro de que deseas eliminar permanentemente esta tarea? Esta acción no se puede deshacer.</p>
                                    </div>
                                    <div className="modal-footer border-0 gap-2">
                                        <button type="button" onClick={() => setDeleteTaskId(null)} className="btn btn-outline-secondary px-4 rounded-3 border-secondary text-light">Cancelar</button>
                                        <button type="button" onClick={confirmDelete} className="btn btn-danger px-4 rounded-3">Confirmar y Borrar</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""
            with open(os.path.join(frontend_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(index_html.strip())

            self.logger.log_event("implementer_agent", "implement", "Estructura de backend y frontend de TaskLiteJota implementada con éxito", "success")
            return backend_dir, frontend_dir
        elif project_id.strip().upper() == "CUATRO":
            # 1. Write StockMaster ERP Lite backend/app/main.py
            main_py = """import os
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Models
class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(500), nullable=True)
    costo = Column(Float, default=0.0, nullable=False)
    precio = Column(Float, default=0.0, nullable=False)
    stock_disponible = Column(Integer, default=0, nullable=False)
    stock_minimo = Column(Integer, default=0, nullable=False)
    categoria = Column(String(100), nullable=True)
    marca = Column(String(100), nullable=True)
    unidad_medida = Column(String(50), default="unidades")

class WarehouseDB(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=True)
    encargado = Column(String(100), nullable=True)

class StockMovementDB(Base):
    __tablename__ = "stock_movements"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    tipo = Column(String(20), nullable=False) # entrada, salida, salida_transferencia, entrada_transferencia
    documento_referencia = Column(String(50), nullable=True)
    usuario = Column(String(100), default="admin")
    fecha = Column(DateTime, default=datetime.utcnow)
    observacion = Column(String(250), nullable=True)

    product = relationship("ProductDB")
    warehouse = relationship("WarehouseDB")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StockMaster ERP Lite", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class ProductCreate(BaseModel):
    sku: str = Field(..., min_length=2, max_length=50)
    nombre: str = Field(..., min_length=3, max_length=150)
    descripcion: Optional[str] = None
    costo: float = Field(..., ge=0.0)
    precio: float = Field(..., ge=0.0)
    stock_minimo: int = Field(default=0, ge=0)
    categoria: Optional[str] = None
    marca: Optional[str] = None
    unidad_medida: Optional[str] = "unidades"

class ProductResponse(BaseModel):
    id: int
    sku: str
    nombre: str
    descripcion: Optional[str] = None
    costo: float
    precio: float
    stock_disponible: int
    stock_minimo: int
    categoria: Optional[str] = None
    marca: Optional[str] = None
    unidad_medida: Optional[str] = "unidades"
    class Config:
        orm_mode = True

class WarehouseCreate(BaseModel):
    codigo: str = Field(..., min_length=2, max_length=20)
    nombre: str = Field(..., min_length=3, max_length=100)
    direccion: Optional[str] = None
    encargado: Optional[str] = None

class WarehouseResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    direccion: Optional[str] = None
    encargado: Optional[str] = None
    class Config:
        orm_mode = True

class MovementCreate(BaseModel):
    product_id: int
    warehouse_id: int
    cantidad: int = Field(..., gt=0)
    tipo: str # entrada, salida, transferencia
    target_warehouse_id: Optional[int] = None
    documento_referencia: Optional[str] = None
    observacion: Optional[str] = None

class MovementResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    cantidad: int
    tipo: str
    documento_referencia: Optional[str] = None
    usuario: str
    fecha: datetime
    observacion: Optional[str] = None
    class Config:
        orm_mode = True

# API endpoints
@app.get("/api/products", response_model=List[ProductResponse])
def get_products():
    db = SessionLocal()
    products = db.query(ProductDB).all()
    db.close()
    return products

@app.post("/api/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    db = SessionLocal()
    exists = db.query(ProductDB).filter(ProductDB.sku == product.sku.strip()).first()
    if exists:
        db.close()
        raise HTTPException(status_code=400, detail="El SKU ya se encuentra registrado.")
    
    db_product = ProductDB(
        sku=product.sku.strip(),
        nombre=product.nombre.strip(),
        descripcion=product.descripcion,
        costo=product.costo,
        precio=product.precio,
        stock_disponible=0,
        stock_minimo=product.stock_minimo,
        categoria=product.categoria,
        marca=product.marca,
        unidad_medida=product.unidad_medida
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product

@app.put("/api/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductCreate):
    db = SessionLocal()
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        db.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    
    if db_product.sku != product_data.sku.strip():
        exists = db.query(ProductDB).filter(ProductDB.sku == product_data.sku.strip()).first()
        if exists:
            db.close()
            raise HTTPException(status_code=400, detail="El SKU ya se encuentra registrado por otro producto.")
            
    db_product.sku = product_data.sku.strip()
    db_product.nombre = product_data.nombre.strip()
    db_product.descripcion = product_data.descripcion
    db_product.costo = product_data.costo
    db_product.precio = product_data.precio
    db_product.stock_minimo = product_data.stock_minimo
    db_product.categoria = product_data.categoria
    db_product.marca = product_data.marca
    db_product.unidad_medida = product_data.unidad_medida
    
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        db.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    
    has_movements = db.query(StockMovementDB).filter(StockMovementDB.product_id == product_id).first()
    if has_movements:
        db.close()
        raise HTTPException(status_code=400, detail="No se puede eliminar un producto con historial de movimientos transaccionales.")
        
    db.delete(db_product)
    db.commit()
    db.close()
    return {"status": "deleted", "id": product_id}

@app.get("/api/warehouses", response_model=List[WarehouseResponse])
def get_warehouses():
    db = SessionLocal()
    warehouses = db.query(WarehouseDB).all()
    db.close()
    return warehouses

@app.post("/api/warehouses", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse(warehouse: WarehouseCreate):
    db = SessionLocal()
    exists = db.query(WarehouseDB).filter(WarehouseDB.codigo == warehouse.codigo.strip().upper()).first()
    if exists:
        db.close()
        raise HTTPException(status_code=400, detail="El código de bodega ya se encuentra registrado.")
        
    db_warehouse = WarehouseDB(
        codigo=warehouse.codigo.strip().upper(),
        nombre=warehouse.nombre.strip(),
        direccion=warehouse.direccion,
        encargado=warehouse.encargado
    )
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    db.close()
    return db_warehouse

@app.get("/api/movements")
def get_movements():
    db = SessionLocal()
    movements = db.query(StockMovementDB).order_by(StockMovementDB.fecha.desc()).all()
    result = []
    for m in movements:
        result.append({
            "id": m.id,
            "product_id": m.product_id,
            "product_name": m.product.nombre,
            "product_sku": m.product.sku,
            "warehouse_id": m.warehouse_id,
            "warehouse_name": m.warehouse.nombre,
            "cantidad": m.cantidad,
            "tipo": m.tipo,
            "documento_referencia": m.documento_referencia,
            "usuario": m.usuario,
            "fecha": m.fecha.isoformat(),
            "observacion": m.observacion
        })
    db.close()
    return result

@app.post("/api/movements", response_model=MovementResponse, status_code=status.HTTP_201_CREATED)
def create_movement(mov: MovementCreate):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.id == mov.product_id).first()
    if not product:
        db.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    
    warehouse = db.query(WarehouseDB).filter(WarehouseDB.id == mov.warehouse_id).first()
    if not warehouse:
        db.close()
        raise HTTPException(status_code=404, detail="Bodega de origen no encontrada.")
        
    if mov.tipo not in ["entrada", "salida", "transferencia"]:
        db.close()
        raise HTTPException(status_code=400, detail="Tipo de movimiento inválido.")
        
    if mov.tipo == "entrada":
        product.stock_disponible += mov.cantidad
        db_mov = StockMovementDB(
            product_id=mov.product_id,
            warehouse_id=mov.warehouse_id,
            cantidad=mov.cantidad,
            tipo="entrada",
            documento_referencia=mov.documento_referencia,
            observacion=mov.observacion
        )
        db.add(db_mov)
        
    elif mov.tipo == "salida":
        if product.stock_disponible < mov.cantidad:
            db.close()
            raise HTTPException(status_code=400, detail="Stock insuficiente. Transacción rechazada para evitar saldo negativo.")
        product.stock_disponible -= mov.cantidad
        db_mov = StockMovementDB(
            product_id=mov.product_id,
            warehouse_id=mov.warehouse_id,
            cantidad=mov.cantidad,
            tipo="salida",
            documento_referencia=mov.documento_referencia,
            observacion=mov.observacion
        )
        db.add(db_mov)
        
    elif mov.tipo == "transferencia":
        if not mov.target_warehouse_id:
            db.close()
            raise HTTPException(status_code=400, detail="La bodega de destino es obligatoria para transferencias.")
        if mov.warehouse_id == mov.target_warehouse_id:
            db.close()
            raise HTTPException(status_code=400, detail="La bodega de origen y destino no pueden ser iguales.")
            
        target_warehouse = db.query(WarehouseDB).filter(WarehouseDB.id == mov.target_warehouse_id).first()
        if not target_warehouse:
            db.close()
            raise HTTPException(status_code=404, detail="Bodega de destino no encontrada.")
            
        if product.stock_disponible < mov.cantidad:
            db.close()
            raise HTTPException(status_code=400, detail="Stock insuficiente en bodega de origen para realizar la transferencia.")
            
        product.stock_disponible -= mov.cantidad
        db_mov_out = StockMovementDB(
            product_id=mov.product_id,
            warehouse_id=mov.warehouse_id,
            cantidad=mov.cantidad,
            tipo="salida_transferencia",
            documento_referencia=mov.documento_referencia,
            observacion=f"Transferencia hacia {target_warehouse.nombre}. {mov.observacion or ''}"
        )
        db.add(db_mov_out)
        
        product.stock_disponible += mov.cantidad
        db_mov_in = StockMovementDB(
            product_id=mov.product_id,
            warehouse_id=mov.target_warehouse_id,
            cantidad=mov.cantidad,
            tipo="entrada_transferencia",
            documento_referencia=mov.documento_referencia,
            observacion=f"Recibido de {warehouse.nombre}. {mov.observacion or ''}"
        )
        db.add(db_mov_in)
        db_mov = db_mov_out

    db.commit()
    db.refresh(db_mov)
    db.close()
    return db_mov

@app.get("/api/dashboard")
def get_dashboard():
    db = SessionLocal()
    products = db.query(ProductDB).all()
    warehouses = db.query(WarehouseDB).all()
    movements = db.query(StockMovementDB).order_by(StockMovementDB.fecha.desc()).limit(5).all()
    
    total_products = len(products)
    total_stock = sum(p.stock_disponible for p in products)
    total_valuation = sum(p.stock_disponible * p.costo for p in products)
    
    low_stock_products = []
    for p in products:
        if p.stock_disponible <= p.stock_minimo:
            low_stock_products.append({
                "id": p.id,
                "sku": p.sku,
                "nombre": p.nombre,
                "stock_disponible": p.stock_disponible,
                "stock_minimo": p.stock_minimo
            })
            
    recent_movements = []
    for m in movements:
        recent_movements.append({
            "id": m.id,
            "product_name": m.product.nombre,
            "warehouse_name": m.warehouse.nombre,
            "cantidad": m.cantidad,
            "tipo": m.tipo,
            "fecha": m.fecha.isoformat()
        })
        
    db.close()
    return {
        "total_products": total_products,
        "total_warehouses": len(warehouses),
        "total_stock": total_stock,
        "total_valuation": total_valuation,
        "low_stock_alerts_count": len(low_stock_products),
        "low_stock_products": low_stock_products,
        "recent_movements": recent_movements
    }
"""
            with open(os.path.join(backend_dir, "app", "main.py"), "w", encoding="utf-8") as f:
                f.write(main_py.strip())

            # 2. Write StockMaster ERP Lite backend/tests/test_main.py (Pytest suite)
            test_main_py = """import pytest
from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app, engine, Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

def test_create_product_success():
    response = client.post(
        "/api/products",
        json={"sku": "PROD001", "nombre": "Teclado Mecanico", "descripcion": "RGB switch blue", "costo": 25.0, "precio": 49.99, "stock_minimo": 5}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["sku"] == "PROD001"
    assert data["stock_disponible"] == 0

def test_create_product_duplicate_sku():
    client.post(
        "/api/products",
        json={"sku": "DUPL001", "nombre": "Mouse Gamer", "costo": 15.0, "precio": 29.90, "stock_minimo": 2}
    )
    response = client.post(
        "/api/products",
        json={"sku": "DUPL001", "nombre": "Mouse Premium", "costo": 18.0, "precio": 35.0, "stock_minimo": 3}
    )
    assert response.status_code == 400

def test_create_product_invalid_values():
    response = client.post(
        "/api/products",
        json={"sku": "NEG001", "nombre": "Audifonos", "costo": -10.0, "precio": 20.0}
    )
    assert response.status_code == 422

def test_create_warehouse():
    response = client.post(
        "/api/warehouses",
        json={"codigo": "BOD01", "nombre": "Bodega Principal", "direccion": "Santiago", "encargado": "Ricardo"}
    )
    assert response.status_code == 201
    assert response.json()["codigo"] == "BOD01"

def test_movement_stock_in():
    p_resp = client.post("/api/products", json={"sku": "MOV01", "nombre": "Pantalla 24", "costo": 80.0, "precio": 150.0})
    w_resp = client.post("/api/warehouses", json={"codigo": "WH01", "nombre": "Bodega A"})
    
    p_id = p_resp.json()["id"]
    w_id = w_resp.json()["id"]
    
    m_resp = client.post("/api/movements", json={"product_id": p_id, "warehouse_id": w_id, "cantidad": 20, "tipo": "entrada"})
    assert m_resp.status_code == 201
    
    prod_resp = client.get("/api/products")
    prods = prod_resp.json()
    this_p = next(p for p in prods if p["id"] == p_id)
    assert this_p["stock_disponible"] == 20

def test_movement_stock_out_insufficient():
    p_resp = client.post("/api/products", json={"sku": "MOV02", "nombre": "Webcam 1080p", "costo": 30.0, "precio": 60.0})
    w_resp = client.post("/api/warehouses", json={"codigo": "WH02", "nombre": "Bodega B"})
    p_id = p_resp.json()["id"]
    w_id = w_resp.json()["id"]
    
    m_resp = client.post("/api/movements", json={"product_id": p_id, "warehouse_id": w_id, "cantidad": 10, "tipo": "salida"})
    assert m_resp.status_code == 400

def test_dashboard_kpis():
    p_resp = client.post("/api/products", json={"sku": "KPI01", "nombre": "CPU Ryzen 5", "costo": 150.0, "precio": 250.0, "stock_minimo": 10})
    w_resp = client.post("/api/warehouses", json={"codigo": "WHKPI", "nombre": "Bodega KPI"})
    p_id = p_resp.json()["id"]
    w_id = w_resp.json()["id"]
    
    client.post("/api/movements", json={"product_id": p_id, "warehouse_id": w_id, "cantidad": 5, "tipo": "entrada"})
    
    dash_resp = client.get("/api/dashboard")
    dash = dash_resp.json()
    
    assert dash["total_stock"] >= 5
    assert dash["total_valuation"] >= 750.0
    assert dash["low_stock_alerts_count"] >= 1
"""
            with open(os.path.join(backend_dir, "tests", "test_main.py"), "w", encoding="utf-8") as f:
                f.write(test_main_py.strip())

            # 3. Write StockMaster ERP Lite frontend/index.html (Bootstrap 5 Dark Mode Glassmorphism)
            index_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StockMaster ERP Lite — Sistema Web de Inventario</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #020617;
            --bg-glass: rgba(15, 23, 42, 0.7);
            --border-glass: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-purple: #8b5cf6;
            --accent-cyan: #06b6d4;
            --accent-green: #10b981;
        }
        body {
            font-family: 'Outfit', sans-serif;
            background: radial-gradient(circle at top left, #0f172a 0%, #020617 80%);
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 50px;
        }
        .navbar-custom {
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-glass);
        }
        .logo-text {
            font-weight: 800;
            background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        .glass-card {
            background: var(--bg-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .interactive-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(6,182,212,0.15);
            border-color: rgba(6,182,212,0.3);
        }
        .form-control, .form-select {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: var(--text-main) !important;
            border-radius: 10px;
        }
        .form-control:focus, .form-select:focus {
            box-shadow: 0 0 0 2px rgba(6,182,212,0.4) !important;
            border-color: var(--accent-cyan) !important;
        }
        .btn-cyan {
            background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
            border: none;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            transition: all 0.3s;
        }
        .btn-cyan:hover {
            opacity: 0.95;
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(6,182,212,0.4);
            color: white;
        }
        .nav-tabs {
            border-bottom: 1px solid var(--border-glass);
        }
        .nav-link {
            color: var(--text-secondary);
            border: none !important;
            font-weight: 600;
            padding: 12px 20px;
            transition: all 0.2s;
        }
        .nav-link:hover {
            color: var(--text-main);
        }
        .nav-link.active {
            color: var(--accent-cyan) !important;
            background-color: transparent !important;
            border-bottom: 3px solid var(--accent-cyan) !important;
            border-radius: 0;
        }
        .kpi-card {
            border-left: 4px solid var(--accent-purple);
        }
        .kpi-valuation {
            border-left: 4px solid var(--accent-green);
        }
        .kpi-alert {
            border-left: 4px solid #ef4444;
        }
        .table {
            color: #cbd5e1;
        }
        .table-dark {
            --bs-table-bg: rgba(15, 23, 42, 0.4);
            --bs-table-border-color: rgba(255, 255, 255, 0.05);
        }
        .badge-danger {
            background-color: rgba(239, 68, 68, 0.2);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }
    </style>
</head>
<body>
    <div id="root"></div>

    <!-- React, ReactDOM, Babel UMD Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js" crossorigin></script>
    <script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
    <script src="https://cdn.jsdelivr.net/npm/@babel/standalone/babel.min.js"></script>

    <script type="text/babel">
        const { useState, useEffect } = React;
        const API_BASE = 'http://localhost:8000/api';

        function App() {
            const [activeTab, setActiveTab] = useState('dashboard');
            const [products, setProducts] = useState([]);
            const [warehouses, setWarehouses] = useState([]);
            const [movements, setMovements] = useState([]);
            const [dashboard, setDashboard] = useState({
                total_products: 0,
                total_warehouses: 0,
                total_stock: 0,
                total_valuation: 0.0,
                low_stock_alerts_count: 0,
                low_stock_products: [],
                recent_movements: []
            });

            // Product Form State
            const [sku, setSku] = useState('');
            const [nombre, setNombre] = useState('');
            const [descripcion, setDescripcion] = useState('');
            const [costo, setCosto] = useState(0);
            const [precio, setPrecio] = useState(0);
            const [stockMinimo, setStockMinimo] = useState(0);
            const [categoria, setCategoria] = useState('');
            const [marca, setMarca] = useState('');
            const [unidadMedida, setUnidadMedida] = useState('unidades');
            const [editingProductId, setEditingProductId] = useState(null);

            // Warehouse Form State
            const [wCodigo, setWCodigo] = useState('');
            const [wNombre, setWNombre] = useState('');
            const [wDireccion, setWDireccion] = useState('');
            const [wEncargado, setWEncargado] = useState('');

            // Movement Form State
            const [mProductId, setMProductId] = useState('');
            const [mWarehouseId, setMWarehouseId] = useState('');
            const [mCantidad, setMCantidad] = useState(1);
            const [mTipo, setMTipo] = useState('entrada');
            const [mTargetWarehouseId, setMTargetWarehouseId] = useState('');
            const [mDocRef, setMDocRef] = useState('');
            const [mObs, setMObs] = useState('');

            const [toast, setToast] = useState(null);

            useEffect(() => {
                fetchInitialData();
            }, []);

            const showToast = (msg, type = 'success') => {
                setToast({ msg, type });
                setTimeout(() => setToast(null), 4000);
            };

            const fetchInitialData = async () => {
                try {
                    const [prodRes, warRes, movRes, dashRes] = await Promise.all([
                        fetch(`${API_BASE}/products`),
                        fetch(`${API_BASE}/warehouses`),
                        fetch(`${API_BASE}/movements`),
                        fetch(`${API_BASE}/dashboard`)
                    ]);
                    
                    if (prodRes.ok) setProducts(await prodRes.json());
                    if (warRes.ok) setWarehouses(await warRes.json());
                    if (movRes.ok) setMovements(await movRes.json());
                    if (dashRes.ok) setDashboard(await dashRes.json());
                } catch (err) {
                    showToast('Error al conectar con la API de inventarios', 'danger');
                }
            };

            const handleProductSubmit = async (e) => {
                e.preventDefault();
                if (costo < 0 || precio < 0 || stockMinimo < 0) {
                    showToast('Los valores numéricos no pueden ser negativos', 'danger');
                    return;
                }
                const payload = {
                    sku: sku.trim(),
                    nombre: nombre.trim(),
                    descripcion: descripcion.trim() || null,
                    costo: parseFloat(costo),
                    precio: parseFloat(precio),
                    stock_minimo: parseInt(stockMinimo),
                    categoria: categoria.trim() || null,
                    marca: marca.trim() || null,
                    unidad_medida: unidadMedida
                };

                try {
                    let res;
                    if (editingProductId) {
                        res = await fetch(`${API_BASE}/products/${editingProductId}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                    } else {
                        res = await fetch(`${API_BASE}/products`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                    }

                    if (res.ok) {
                        showToast(editingProductId ? 'Producto actualizado' : 'Producto creado con éxito');
                        setSku(''); setNombre(''); setDescripcion(''); setCosto(0); setPrecio(0); setStockMinimo(0);
                        setCategoria(''); setMarca(''); setUnidadMedida('unidades'); setEditingProductId(null);
                        fetchInitialData();
                    } else {
                        const err = await res.json();
                        showToast(err.detail || 'Error al guardar producto', 'danger');
                    }
                } catch (err) {
                    showToast('Error de red', 'danger');
                }
            };

            const handleWarehouseSubmit = async (e) => {
                e.preventDefault();
                const payload = {
                    codigo: wCodigo.trim().upper(),
                    nombre: wNombre.trim(),
                    direccion: wDireccion.trim() || null,
                    encargado: wEncargado.trim() || null
                };

                try {
                    const res = await fetch(`${API_BASE}/warehouses`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (res.ok) {
                        showToast('Bodega física registrada');
                        setWCodigo(''); setWNombre(''); setWDireccion(''); setWEncargado('');
                        fetchInitialData();
                    } else {
                        const err = await res.json();
                        showToast(err.detail || 'Error al guardar bodega', 'danger');
                    }
                } catch (err) {
                    showToast('Error de red', 'danger');
                }
            };

            const handleMovementSubmit = async (e) => {
                e.preventDefault();
                if (mCantidad <= 0) {
                    showToast('La cantidad debe ser mayor que cero', 'danger');
                    return;
                }
                const payload = {
                    product_id: parseInt(mProductId),
                    warehouse_id: parseInt(mWarehouseId),
                    cantidad: parseInt(mCantidad),
                    tipo: mTipo,
                    target_warehouse_id: mTipo === 'transferencia' ? parseInt(mTargetWarehouseId) : null,
                    documento_referencia: mDocRef.trim() || null,
                    observacion: mObs.trim() || null
                };

                try {
                    const res = await fetch(`${API_BASE}/movements`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (res.ok) {
                        showToast('Movimiento registrado e inventario actualizado');
                        setMProductId(''); setMWarehouseId(''); setMCantidad(1); setMTipo('entrada'); setMTargetWarehouseId(''); setMDocRef(''); setMObs('');
                        fetchInitialData();
                    } else {
                        const err = await res.json();
                        showToast(err.detail || 'Error en la transacción de stock', 'danger');
                    }
                } catch (err) {
                    showToast('Error de red', 'danger');
                }
            };

            const handleEditClick = (p) => {
                setEditingProductId(p.id);
                setSku(p.sku);
                setNombre(p.nombre);
                setDescripcion(p.descripcion || '');
                setCosto(p.costo);
                setPrecio(p.precio);
                setStockMinimo(p.stock_minimo);
                setCategoria(p.categoria || '');
                setMarca(p.marca || '');
                setUnidadMedida(p.unidad_medida || 'unidades');
                setActiveTab('products');
            };

            return (
                <div>
                    {/* Premium Glass Navbar */}
                    <nav className="navbar navbar-dark navbar-custom mb-5 py-3">
                        <div className="container d-flex justify-content-between align-items-center">
                            <span className="navbar-brand d-flex align-items-center gap-2">
                                <i className="bi bi-box-seam fs-3" style={{color: '#06b6d4'}}></i>
                                <span className="logo-text fs-3">StockMaster ERP Lite</span>
                            </span>
                            <span className="badge bg-secondary py-2 px-3 border border-dark rounded-pill fs-7 d-flex align-items-center gap-1">
                                <i className="bi bi-cpu text-info"></i> Fábrica de Software SDD
                            </span>
                        </div>
                    </nav>

                    <div className="container">
                        {toast && (
                            <div className={`alert alert-${toast.type} d-flex align-items-center gap-2 border-0 rounded-4 py-3 shadow-lg mb-4`} role="alert">
                                <i className={`bi ${toast.type === 'danger' ? 'bi-exclamation-triangle-fill' : 'bi-check-circle-fill'}`}></i>
                                <div className="fw-semibold">{toast.msg}</div>
                            </div>
                        )}

                        {/* Custom Tabs Navigation */}
                        <ul className="nav nav-tabs mb-4">
                            <li className="nav-item">
                                <button className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
                                    <i className="bi bi-grid-1x2-fill me-1"></i> Dashboard
                                </button>
                            </li>
                            <li className="nav-item">
                                <button className={`nav-link ${activeTab === 'products' ? 'active' : ''}`} onClick={() => setActiveTab('products')}>
                                    <i className="bi bi-tags-fill me-1"></i> Productos
                                </button>
                            </li>
                            <li className="nav-item">
                                <button className={`nav-link ${activeTab === 'warehouses' ? 'active' : ''}`} onClick={() => setActiveTab('warehouses')}>
                                    <i className="bi bi-house-door-fill me-1"></i> Bodegas
                                </button>
                            </li>
                            <li className="nav-item">
                                <button className={`nav-link ${activeTab === 'movements' ? 'active' : ''}`} onClick={() => setActiveTab('movements')}>
                                    <i className="bi bi-arrow-left-right me-1"></i> Movimientos
                                </button>
                            </li>
                        </ul>

                        {/* TAB CONTENT: DASHBOARD */}
                        {activeTab === 'dashboard' && (
                            <div className="row">
                                {/* KPI Cards */}
                                <div className="col-md-3 mb-4">
                                    <div className="glass-card kpi-card p-4">
                                        <div className="text-secondary small fw-bold">PRODUCTOS ACTIVOS</div>
                                        <div className="fs-1 fw-bold my-2 text-cyan" style={{color: '#06b6d4'}}>{dashboard.total_products}</div>
                                        <div className="small text-secondary">Catálogo maestro registrado</div>
                                    </div>
                                </div>
                                <div className="col-md-3 mb-4">
                                    <div className="glass-card kpi-card p-4">
                                        <div className="text-secondary small fw-bold">STOCK FÍSICO TOTAL</div>
                                        <div className="fs-1 fw-bold my-2 text-purple" style={{color: '#8b5cf6'}}>{dashboard.total_stock}</div>
                                        <div className="small text-secondary">Unidades globales en bodegas</div>
                                    </div>
                                </div>
                                <div className="col-md-3 mb-4">
                                    <div className="glass-card kpi-valuation p-4">
                                        <div className="text-secondary small fw-bold">VALORIZACIÓN INVENTARIO</div>
                                        <div className="fs-1 fw-bold my-2 text-success" style={{color: '#10b981'}}>${dashboard.total_valuation.toFixed(2)}</div>
                                        <div className="small text-secondary">Calculado al costo unitario</div>
                                    </div>
                                </div>
                                <div className="col-md-3 mb-4">
                                    <div className="glass-card kpi-alert p-4">
                                        <div className="text-secondary small fw-bold">ALERTA STOCK MÍNIMO</div>
                                        <div className="fs-1 fw-bold my-2 text-danger" style={{color: '#ef4444'}}>{dashboard.low_stock_alerts_count}</div>
                                        <div className="small text-secondary">Productos bajo stock requerido</div>
                                    </div>
                                </div>

                                {/* Alerts table & Recent movements */}
                                <div className="col-lg-6 mb-4">
                                    <div className="glass-card p-4 h-100">
                                        <h5 className="mb-4 d-flex align-items-center gap-2 text-danger">
                                            <i className="bi bi-exclamation-octagon-fill"></i>
                                            <span>Alertas de Stock Críticas</span>
                                        </h5>
                                        <div className="table-responsive">
                                            <table className="table table-dark table-striped table-hover align-middle">
                                                <thead>
                                                    <tr>
                                                        <th>SKU</th>
                                                        <th>Producto</th>
                                                        <th>Stock Actual</th>
                                                        <th>Mínimo</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {dashboard.low_stock_products.length === 0 ? (
                                                        <tr><td colSpan="4" className="text-center text-muted small py-4">Sin alertas críticas activas</td></tr>
                                                    ) : (
                                                        dashboard.low_stock_products.map(p => (
                                                            <tr key={p.id}>
                                                                <td><code>{p.sku}</code></td>
                                                                <td><strong>{p.nombre}</strong></td>
                                                                <td><span className="badge badge-danger">{p.stock_disponible}</span></td>
                                                                <td><span className="badge bg-secondary">{p.stock_minimo}</span></td>
                                                            </tr>
                                                        ))
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>

                                <div className="col-lg-6 mb-4">
                                    <div className="glass-card p-4 h-100">
                                        <h5 className="mb-4 d-flex align-items-center gap-2 text-cyan">
                                            <i className="bi bi-clock-history"></i>
                                            <span>Movimientos Recientes</span>
                                        </h5>
                                        <div className="table-responsive">
                                            <table className="table table-dark table-striped table-hover align-middle">
                                                <thead>
                                                    <tr>
                                                        <th>Fecha</th>
                                                        <th>Producto</th>
                                                        <th>Bodega</th>
                                                        <th>Cantidad</th>
                                                        <th>Tipo</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {dashboard.recent_movements.length === 0 ? (
                                                        <tr><td colSpan="5" className="text-center text-muted small py-4">No se han registrado transacciones de stock</td></tr>
                                                    ) : (
                                                        dashboard.recent_movements.map(m => (
                                                            <tr key={m.id}>
                                                                <td className="small text-muted">{new Date(m.fecha).toLocaleTimeString()}</td>
                                                                <td><strong>{m.product_name}</strong></td>
                                                                <td>{m.warehouse_name}</td>
                                                                <td>{m.cantidad}</td>
                                                                <td>
                                                                    <span className={`badge ${m.tipo.includes('entrada') ? 'bg-success' : 'bg-danger'}`}>
                                                                        {m.tipo.toUpperCase()}
                                                                    </span>
                                                                </td>
                                                            </tr>
                                                        ))
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* TAB CONTENT: PRODUCTS */}
                        {activeTab === 'products' && (
                            <div className="row">
                                <div className="col-lg-4 mb-4">
                                    <div className="glass-card p-4">
                                        <h4 className="mb-4 d-flex align-items-center gap-2">
                                            <i className={`bi ${editingProductId ? 'bi-pencil-square text-warning' : 'bi-plus-circle-fill text-cyan'}`}></i>
                                            <span>{editingProductId ? 'Editar Producto' : 'Nuevo Producto'}</span>
                                        </h4>
                                        <form onSubmit={handleProductSubmit}>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">SKU Único *</label>
                                                <input type="text" className="form-control" value={sku} onChange={e => setSku(e.target.value)} placeholder="Ej. SKU-1002" required />
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Nombre *</label>
                                                <input type="text" className="form-control" value={nombre} onChange={e => setNombre(e.target.value)} placeholder="Ej. Cpu Intel Core i7" required />
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Descripción</label>
                                                <textarea className="form-control" value={descripcion} onChange={e => setDescripcion(e.target.value)} rows="2"></textarea>
                                            </div>
                                            <div className="row">
                                                <div className="col-6 mb-3">
                                                    <label className="form-label text-secondary small">Costo Unitario ($) *</label>
                                                    <input type="number" step="0.01" className="form-control" value={costo} onChange={e => setCosto(e.target.value)} required />
                                                </div>
                                                <div className="col-6 mb-3">
                                                    <label className="form-label text-secondary small">Precio Venta ($) *</label>
                                                    <input type="number" step="0.01" className="form-control" value={precio} onChange={e => setPrecio(e.target.value)} required />
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col-6 mb-3">
                                                    <label className="form-label text-secondary small">Stock Mínimo *</label>
                                                    <input type="number" className="form-control" value={stockMinimo} onChange={e => setStockMinimo(e.target.value)} required />
                                                </div>
                                                <div className="col-6 mb-3">
                                                    <label className="form-label text-secondary small">Unidad de Medida</label>
                                                    <input type="text" className="form-control" value={unidadMedida} onChange={e => setUnidadMedida(e.target.value)} />
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col-6 mb-3">
                                                    <label className="form-label text-secondary small">Categoría</label>
                                                    <input type="text" className="form-control" value={categoria} onChange={e => setCategoria(e.target.value)} placeholder="Ej. Computación" />
                                                </div>
                                                <div className="col-6 mb-3">
                                                    <label className="form-label text-secondary small">Marca</label>
                                                    <input type="text" className="form-control" value={marca} onChange={e => setMarca(e.target.value)} placeholder="Ej. Asus" />
                                                </div>
                                            </div>
                                            <button type="submit" className="btn btn-cyan w-100 py-2.5 mt-3">
                                                <i className="bi bi-save"></i> {editingProductId ? 'Guardar Cambios' : 'Registrar Producto'}
                                            </button>
                                            {editingProductId && (
                                                <button type="button" className="btn btn-outline-secondary w-100 py-2 mt-2" onClick={() => {
                                                    setEditingProductId(null); setSku(''); setNombre(''); setDescripcion(''); setCosto(0); setPrecio(0); setStockMinimo(0);
                                                }}>Cancelar Edición</button>
                                            )}
                                        </form>
                                    </div>
                                </div>

                                <div className="col-lg-8">
                                    <div className="glass-card p-4">
                                        <h5 className="mb-4">Catálogo de Productos Registrados</h5>
                                        <div className="table-responsive">
                                            <table className="table table-dark table-striped table-hover align-middle">
                                                <thead>
                                                    <tr>
                                                        <th>SKU</th>
                                                        <th>Nombre</th>
                                                        <th>Costo</th>
                                                        <th>Precio</th>
                                                        <th>Stock Disp.</th>
                                                        <th>Acciones</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {products.length === 0 ? (
                                                        <tr><td colSpan="6" className="text-center text-muted small py-4">Sin productos en el catálogo maestro</td></tr>
                                                    ) : (
                                                        products.map(p => (
                                                            <tr key={p.id}>
                                                                <td><code>{p.sku}</code></td>
                                                                <td>
                                                                    <strong>{p.nombre}</strong>
                                                                    <div className="small text-muted">{p.categoria || 'Sin Categoría'} | {p.marca || 'Sin Marca'}</div>
                                                                </td>
                                                                <td>${p.costo.toFixed(2)}</td>
                                                                <td>${p.precio.toFixed(2)}</td>
                                                                <td>
                                                                    <span className={`badge ${p.stock_disponible <= p.stock_minimo ? 'bg-danger' : 'bg-success'}`}>
                                                                        {p.stock_disponible} / Mín: {p.stock_minimo}
                                                                    </span>
                                                                </td>
                                                                <td>
                                                                    <button className="btn btn-sm btn-outline-warning me-2" onClick={() => handleEditClick(p)}>
                                                                        <i className="bi bi-pencil"></i>
                                                                    </button>
                                                                </td>
                                                            </tr>
                                                        ))
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* TAB CONTENT: WAREHOUSES */}
                        {activeTab === 'warehouses' && (
                            <div className="row">
                                <div className="col-lg-4 mb-4">
                                    <div className="glass-card p-4">
                                        <h4 className="mb-4 d-flex align-items-center gap-2">
                                            <i className="bi bi-house-add-fill text-cyan"></i>
                                            <span>Nueva Bodega</span>
                                        </h4>
                                        <form onSubmit={handleWarehouseSubmit}>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Código Bodega *</label>
                                                <input type="text" className="form-control" value={wCodigo} onChange={e => setWCodigo(e.target.value)} placeholder="Ej. BOD-A" required />
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Nombre *</label>
                                                <input type="text" className="form-control" value={wNombre} onChange={e => setWNombre(e.target.value)} placeholder="Ej. Almacen Central" required />
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Dirección</label>
                                                <input type="text" className="form-control" value={wDireccion} onChange={e => setWDireccion(e.target.value)} placeholder="Ej. Av. Américo Vespucio 1500" />
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Encargado</label>
                                                <input type="text" className="form-control" value={wEncargado} onChange={e => setWEncargado(e.target.value)} placeholder="Ej. Ricardo" />
                                            </div>
                                            <button type="submit" className="btn btn-cyan w-100 py-2.5 mt-3">
                                                <i className="bi bi-save"></i> Registrar Bodega
                                            </button>
                                        </form>
                                    </div>
                                </div>

                                <div className="col-lg-8">
                                    <div className="glass-card p-4">
                                        <h5 className="mb-4">Bodegas y Centros de Almacenamiento</h5>
                                        <div className="table-responsive">
                                            <table className="table table-dark table-striped table-hover align-middle">
                                                <thead>
                                                    <tr>
                                                        <th>Código</th>
                                                        <th>Nombre</th>
                                                        <th>Dirección</th>
                                                        <th>Encargado</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {warehouses.length === 0 ? (
                                                        <tr><td colSpan="4" className="text-center text-muted small py-4">Sin bodegas registradas</td></tr>
                                                    ) : (
                                                        warehouses.map(w => (
                                                            <tr key={w.id}>
                                                                <td><code>{w.codigo}</code></td>
                                                                <td><strong>{w.nombre}</strong></td>
                                                                <td>{w.direccion || '-'}</td>
                                                                <td>{w.encargado || '-'}</td>
                                                            </tr>
                                                        ))
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* TAB CONTENT: MOVEMENTS */}
                        {activeTab === 'movements' && (
                            <div className="row">
                                <div className="col-lg-4 mb-4">
                                    <div className="glass-card p-4">
                                        <h4 className="mb-4 d-flex align-items-center gap-2">
                                            <i className="bi bi-arrow-left-right text-cyan"></i>
                                            <span>Transacción de Stock</span>
                                        </h4>
                                        <form onSubmit={handleMovementSubmit}>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Producto Seleccionado *</label>
                                                <select className="form-select" value={mProductId} onChange={e => setMProductId(e.target.value)} required>
                                                    <option value="">Seleccione producto...</option>
                                                    {products.map(p => (
                                                        <option key={p.id} value={p.id}>{p.nombre} (SKU: {p.sku} | Disp: {p.stock_disponible})</option>
                                                    ))}
                                                </select>
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Tipo Movimiento *</label>
                                                <select className="form-select" value={mTipo} onChange={e => setMTipo(e.target.value)} required>
                                                    <option value="entrada">ENTRADA (Ingreso de stock)</option>
                                                    <option value="salida">SALIDA (Merma, Venta, etc.)</option>
                                                    <option value="transferencia">TRANSFERENCIA (Entre Bodegas)</option>
                                                </select>
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">
                                                    {mTipo === 'transferencia' ? 'Bodega de Origen *' : 'Bodega Operativa *'}
                                                </label>
                                                <select className="form-select" value={mWarehouseId} onChange={e => setMWarehouseId(e.target.value)} required>
                                                    <option value="">Seleccione bodega...</option>
                                                    {warehouses.map(w => (
                                                        <option key={w.id} value={w.id}>{w.nombre} ({w.codigo})</option>
                                                    ))}
                                                </select>
                                            </div>
                                            {mTipo === 'transferencia' && (
                                                <div className="mb-3">
                                                    <label className="form-label text-secondary small">Bodega Destino *</label>
                                                    <select className="form-select" value={mTargetWarehouseId} onChange={e => setMTargetWarehouseId(e.target.value)} required>
                                                        <option value="">Seleccione destino...</option>
                                                        {warehouses.filter(w => w.id !== parseInt(mWarehouseId)).map(w => (
                                                            <option key={w.id} value={w.id}>{w.nombre} ({w.codigo})</option>
                                                        ))}
                                                    </select>
                                                </div>
                                            )}
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Cantidad *</label>
                                                <input type="number" className="form-control" value={mCantidad} onChange={e => setMCantidad(e.target.value)} min="1" required />
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Documento Referencia (Factura, etc.)</label>
                                                <input type="text" className="form-control" value={mDocRef} onChange={e => setMDocRef(e.target.value)} placeholder="Ej. FAC-1002" />
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label text-secondary small">Observación</label>
                                                <input type="text" className="form-control" value={mObs} onChange={e => setMObs(e.target.value)} />
                                            </div>
                                            <button type="submit" className="btn btn-cyan w-100 py-2.5 mt-3">
                                                <i className="bi bi-check-lg"></i> Confirmar Transacción
                                            </button>
                                        </form>
                                    </div>
                                </div>

                                <div className="col-lg-8">
                                    <div className="glass-card p-4">
                                        <h5 className="mb-4">Kardex y Registro Operacional Histórico</h5>
                                        <div className="table-responsive">
                                            <table className="table table-dark table-striped table-hover align-middle">
                                                <thead>
                                                    <tr>
                                                        <th>Fecha</th>
                                                        <th>SKU</th>
                                                        <th>Producto</th>
                                                        <th>Bodega</th>
                                                        <th>Cant.</th>
                                                        <th>Tipo</th>
                                                        <th>Ref. Doc</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {movements.length === 0 ? (
                                                        <tr><td colSpan="7" className="text-center text-muted small py-4">Historial de Kardex vacío</td></tr>
                                                    ) : (
                                                        movements.map(m => (
                                                            <tr key={m.id}>
                                                                <td className="small text-muted">{new Date(m.fecha).toLocaleDateString()}</td>
                                                                <td><code>{m.product_sku}</code></td>
                                                                <td><strong>{m.product_name}</strong></td>
                                                                <td>{m.warehouse_name}</td>
                                                                <td>{m.cantidad}</td>
                                                                <td>
                                                                    <span className={`badge ${m.tipo.includes('entrada') ? 'bg-success' : 'bg-danger'}`}>
                                                                        {m.tipo.toUpperCase()}
                                                                    </span>
                                                                </td>
                                                                <td className="small">{m.documento_referencia || '-'}</td>
                                                            </tr>
                                                        ))
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""
            with open(os.path.join(frontend_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(index_html.strip())

            self.logger.log_event("implementer_agent", "implement", "Estructura de backend, tests y frontend de StockMaster ERP Lite implementada con éxito en sandbox", "success")
            return backend_dir, frontend_dir
        else:
            # Original item implementation fallback
            # 1. Write backend/app/main.py
            main_py = """import os
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
"""
            with open(os.path.join(backend_dir, "app", "main.py"), "w", encoding="utf-8") as f:
                f.write(main_py.strip())

            # 2. Write backend/tests/test_main.py (Pytest)
            test_main_py = """import pytest
from fastapi.testclient import TestClient
import os
import sys

# Append parent dir to PYTHONPATH to find app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app, engine, Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

def test_create_item():
    response = client.post(
        "/api/items",
        json={"nombre": "Tornillos", "descripcion": "Tornillos de acero", "cantidad": 100, "precio": 2.50}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Tornillos"
    assert data["precio"] == 2.50
    assert data["id"] is not None

def test_validate_negative_price():
    response = client.post(
        "/api/items",
        json={"nombre": "Martillo", "descripcion": "Martillo pesado", "cantidad": 10, "precio": -15.0}
    )
    assert response.status_code == 422 # Unprocessable Entity due to Field ge=0.0

def test_get_items():
    response = client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
"""
            with open(os.path.join(backend_dir, "tests", "test_main.py"), "w", encoding="utf-8") as f:
                f.write(test_main_py.strip())

            # 3. Write frontend/index.html (Bootstrap Web Client Dashboard)
            index_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Control Transaccional</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
        }
        .navbar-brand {
            font-weight: 700;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            color: #f8fafc;
        }
        .table {
            color: #cbd5e1;
        }
        .table-dark {
            --bs-table-bg: #1e293b;
        }
        .btn-gradient {
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            color: #ffffff;
            font-weight: 600;
            border: none;
            transition: opacity 0.2s;
        }
        .btn-gradient:hover {
            opacity: 0.9;
            color: #ffffff;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-slate-900 border-bottom border-secondary mb-4">
        <div class="container">
            <span class="navbar-brand fs-4">FabricaWebTransaccionalSDD</span>
            <span class="badge bg-primary">Proyecto: ID-SIMULATED</span>
        </div>
    </nav>

    <div class="container">
        <div class="row">
            <!-- Formulario de Creación -->
            <div class="col-md-4 mb-4">
                <div class="card p-4">
                    <h4 class="mb-3 text-sky-400">Nuevo Registro</h4>
                    <form id="itemForm">
                        <div class="mb-3">
                            <label for="nombre" class="form-label">Nombre del Item</label>
                            <input type="text" class="form-control bg-dark text-white border-secondary" id="nombre" required>
                        </div>
                        <div class="mb-3">
                            <label for="descripcion" class="form-label">Descripción</label>
                            <textarea class="form-control bg-dark text-white border-secondary" id="descripcion" rows="2"></textarea>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="cantidad" class="form-label">Cantidad</label>
                                <input type="number" class="form-control bg-dark text-white border-secondary" id="cantidad" value="0" min="0" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="precio" class="form-label">Precio ($)</label>
                                <input type="number" step="0.01" class="form-control bg-dark text-white border-secondary" id="precio" value="0.00" min="0" required>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-gradient w-100">Guardar Transacción</button>
                    </form>
                </div>
            </div>

            <!-- Tabla de Registros -->
            <div class="col-md-8">
                <div class="card p-4">
                    <h4 class="mb-3 text-sky-400">Listado Transaccional</h4>
                    <div class="table-responsive">
                        <table class="table table-dark table-striped table-hover mt-2">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nombre</th>
                                    <th>Descripción</th>
                                    <th>Cantidad</th>
                                    <th>Precio</th>
                                    <th>Acción</th>
                                </tr>
                            </thead>
                            <tbody id="itemsTableBody">
                                <!-- Filas cargadas dinámicamente -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- JavaScript logic -->
    <script>
        const API_URL = 'http://localhost:8000/api/items';

        async function fetchItems() {
            try {
                const res = await fetch(API_URL);
                if (!res.ok) throw new Error('Error al consultar API');
                const items = await res.json();
                const body = document.getElementById('itemsTableBody');
                body.innerHTML = '';
                if (items.length === 0) {
                    body.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Sin transacciones registradas</td></tr>';
                    return;
                }
                items.forEach(item => {
                    body.innerHTML += `
                        <tr>
                            <td>${item.id}</td>
                            <td><strong>${item.nombre}</strong></td>
                            <td>${item.descripcion || '-'}</td>
                            <td><span class="badge bg-secondary">${item.cantidad}</span></td>
                            <td>$${item.precio.toFixed(2)}</td>
                            <td>
                                <button class="btn btn-danger btn-sm" onclick="deleteItem(${item.id})">Borrar</button>
                            </td>
                        </tr>
                    `;
                });
            } catch (err) {
                console.error(err);
            }
        }

        document.getElementById('itemForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                nombre: document.getElementById('nombre').value,
                descripcion: document.getElementById('descripcion').value,
                cantidad: parseInt(document.getElementById('cantidad').value),
                precio: parseFloat(document.getElementById('precio').value)
            };

            try {
                const res = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (res.status === 201) {
                    document.getElementById('itemForm').reset();
                    fetchItems();
                } else {
                    const errData = await res.json();
                    alert('Error de Validación: ' + JSON.stringify(errData.detail));
                }
            } catch (err) {
                alert('No se pudo conectar con el servidor.');
            }
        });

        async function deleteItem(id) {
            if (!confirm('¿Confirma borrar este registro?')) return;
            try {
                await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
                fetchItems();
            } catch (err) {
                alert('Error al eliminar registro');
            }
        }

        // Carga inicial
        fetchItems();
    </script>
</body>
</html>
"""
            with open(os.path.join(frontend_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(index_html.strip())

            self.logger.log_event("implementer_agent", "implement", "Estructura de backend y frontend original implementada con éxito", "success")
            return backend_dir, frontend_dir
