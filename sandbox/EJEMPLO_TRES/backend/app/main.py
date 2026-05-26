import os
import uuid
from fastapi import FastAPI, HTTPException, status, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from jose import JWTError, jwt
from passlib.context import CryptContext

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Cryptography & JWT
SECRET_KEY = "eventpass-super-secret-key-for-academic-purposes-only"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# SQLAlchemy Models
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class EventDB(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    categoria = Column(String, nullable=False) # concierto, deporte, teatro, conferencia, festival
    fecha_evento = Column(DateTime, nullable=False)
    ubicacion = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    entradas_total = Column(Integer, nullable=False)
    entradas_disp = Column(Integer, nullable=False)
    imagen_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ReservationDB(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    codigo_conf = Column(String, unique=True, nullable=False)
    estado = Column(String, default="confirmada") # confirmada, cancelada
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='_user_event_uc'),)

    user = relationship("UserDB")
    event = relationship("EventDB")

Base.metadata.create_all(bind=engine)

# Seed Data (Events)
def seed_events():
    db = SessionLocal()
    if db.query(EventDB).count() == 0:
        events = [
            EventDB(nombre="Concierto Rock Nacional 2026", categoria="concierto", fecha_evento=datetime.strptime("2026-07-15 20:00", "%Y-%m-%d %H:%M"), ubicacion="Estadio Nacional", precio=45.00, entradas_total=500, entradas_disp=120),
            EventDB(nombre="Final Campeonato de Fútbol", categoria="deporte", fecha_evento=datetime.strptime("2026-06-28 18:30", "%Y-%m-%d %H:%M"), ubicacion="Estadio Olímpico", precio=35.00, entradas_total=1000, entradas_disp=0),
            EventDB(nombre="Obra de Teatro: El Quijote Moderno", categoria="teatro", fecha_evento=datetime.strptime("2026-08-05 19:00", "%Y-%m-%d %H:%M"), ubicacion="Teatro Municipal", precio=25.00, entradas_total=150, entradas_disp=45),
            EventDB(nombre="Tech Summit Ecuador 2026", categoria="conferencia", fecha_evento=datetime.strptime("2026-09-12 09:00", "%Y-%m-%d %H:%M"), ubicacion="Centro de Convenciones", precio=15.00, entradas_total=300, entradas_disp=210),
            EventDB(nombre="Festival de Jazz de Verano", categoria="festival", fecha_evento=datetime.strptime("2026-07-22 16:00", "%Y-%m-%d %H:%M"), ubicacion="Parque Central", precio=30.00, entradas_total=800, entradas_disp=0),
            EventDB(nombre="Concierto Sinfónico: Beethoven", categoria="concierto", fecha_evento=datetime.strptime("2026-10-01 20:00", "%Y-%m-%d %H:%M"), ubicacion="Auditorio Nacional", precio=55.00, entradas_total=200, entradas_disp=180),
            EventDB(nombre="Maratón Ciudad Capital 10K", categoria="deporte", fecha_evento=datetime.strptime("2026-08-18 07:00", "%Y-%m-%d %H:%M"), ubicacion="Avenida Principal", precio=10.00, entradas_total=2000, entradas_disp=1500),
            EventDB(nombre="Stand-Up Comedy Night", categoria="teatro", fecha_evento=datetime.strptime("2026-06-30 21:00", "%Y-%m-%d %H:%M"), ubicacion="Bar Cultural La Ronda", precio=20.00, entradas_total=80, entradas_disp=12)
        ]
        db.add_all(events)
        db.commit()
    db.close()

seed_events()

# FastAPI application
app = FastAPI(title="EventPass — Sistema de Reserva de Entradas", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class UserRegister(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("El correo electrónico debe tener un formato válido.")
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("La contraseña debe tener mínimo 6 caracteres.")
        return v

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: int
    created_at: datetime
    class Config:
        orm_mode = True

class EventResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    categoria: str
    fecha_evento: datetime
    ubicacion: str
    precio: float
    entradas_total: int
    entradas_disp: int
    imagen_url: Optional[str] = None
    agotado: bool
    created_at: datetime

    class Config:
        orm_mode = True

class ReservationCreate(BaseModel):
    event_id: int

class ReservationResponse(BaseModel):
    id: int
    codigo_conf: str
    evento_nombre: str
    fecha_evento: datetime
    ubicacion: str
    precio: float
    estado: str
    created_at: datetime

    class Config:
        orm_mode = True

# JWT Dependency
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.email == email).first()
    db.close()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )
    return user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db=Depends(get_db)):
    if "@" not in user_in.email or "." not in user_in.email:
        raise HTTPException(status_code=422, detail="Formato de correo inválido.")
    if len(user_in.password) < 6:
        raise HTTPException(status_code=422, detail="Contraseña muy corta.")

    exists = db.query(UserDB).filter(UserDB.email == user_in.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    
    new_user = UserDB(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Cuenta creada exitosamente", "user_id": new_user.id}

@app.post("/api/auth/login")
def login(credentials: UserLogin, db=Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user

@app.get("/api/events", response_model=List[EventResponse])
def get_events(
    categoria: Optional[str] = Query(None),
    disponibilidad: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db=Depends(get_db)
):
    query = db.query(EventDB)
    if categoria and categoria.lower() != "todas":
        query = query.filter(EventDB.categoria == categoria.lower())
    
    if disponibilidad:
        if disponibilidad.lower() == "disponibles":
            query = query.filter(EventDB.entradas_disp > 0)
        elif disponibilidad.lower() == "agotados":
            query = query.filter(EventDB.entradas_disp <= 0)
            
    if search:
        query = query.filter(EventDB.nombre.ilike(f"%{search}%"))
        
    events = query.order_by(EventDB.fecha_evento.asc()).all()
    
    res = []
    for e in events:
        res.append({
            "id": e.id,
            "nombre": e.nombre,
            "descripcion": e.descripcion,
            "categoria": e.categoria,
            "fecha_evento": e.fecha_evento,
            "ubicacion": e.ubicacion,
            "precio": e.precio,
            "entradas_total": e.entradas_total,
            "entradas_disp": e.entradas_disp,
            "imagen_url": e.imagen_url,
            "agotado": e.entradas_disp <= 0,
            "created_at": e.created_at
        })
    return res

@app.get("/api/events/{event_id}", response_model=EventResponse)
def get_event_detail(event_id: int, db=Depends(get_db)):
    e = db.query(EventDB).filter(EventDB.id == event_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return {
        "id": e.id,
        "nombre": e.nombre,
        "descripcion": e.descripcion,
        "categoria": e.categoria,
        "fecha_evento": e.fecha_evento,
        "ubicacion": e.ubicacion,
        "precio": e.precio,
        "entradas_total": e.entradas_total,
        "entradas_disp": e.entradas_disp,
        "imagen_url": e.imagen_url,
        "agotado": e.entradas_disp <= 0,
        "created_at": e.created_at
    }

@app.post("/api/reservations", status_code=status.HTTP_201_CREATED)
def reserve_ticket(req: ReservationCreate, current_user=Depends(get_current_user), db=Depends(get_db)):
    event = db.query(EventDB).filter(EventDB.id == req.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
        
    if event.entradas_disp <= 0:
        raise HTTPException(status_code=400, detail="No hay entradas disponibles")
        
    existing = db.query(ReservationDB).filter(
        ReservationDB.user_id == current_user.id,
        ReservationDB.event_id == req.event_id,
        ReservationDB.estado == "confirmada"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya tienes una reserva para este evento")
        
    code = f"EVP-{uuid.uuid4().hex[:8].upper()}"
    
    res = ReservationDB(
        user_id=current_user.id,
        event_id=req.event_id,
        codigo_conf=code,
        estado="confirmada"
    )
    db.add(res)
    
    event.entradas_disp -= 1
    db.commit()
    db.refresh(res)
    
    return {
        "message": "Reserva confirmada",
        "reservation_id": res.id,
        "codigo_confirmacion": res.codigo_conf,
        "evento": event.nombre,
        "fecha_evento": event.fecha_evento
    }

@app.get("/api/reservations/me", response_model=List[ReservationResponse])
def get_my_reservations(current_user=Depends(get_current_user), db=Depends(get_db)):
    reservations = db.query(ReservationDB).filter(ReservationDB.user_id == current_user.id).order_by(ReservationDB.created_at.desc()).all()
    res = []
    for r in reservations:
        event = db.query(EventDB).filter(EventDB.id == r.event_id).first()
        res.append({
            "id": r.id,
            "codigo_conf": r.codigo_conf,
            "evento_nombre": event.nombre if event else "Desconocido",
            "fecha_evento": event.fecha_evento if event else datetime.now(),
            "ubicacion": event.ubicacion if event else "Desconocido",
            "precio": event.precio if event else 0.0,
            "estado": r.estado,
            "created_at": r.created_at
        })
    return res

@app.put("/api/reservations/{reservation_id}/cancel")
def cancel_reservation(reservation_id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    res = db.query(ReservationDB).filter(ReservationDB.id == reservation_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
    if res.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para cancelar esta reserva")
        
    if res.estado == "cancelada":
        raise HTTPException(status_code=400, detail="La reserva ya se encuentra cancelada")
        
    event = db.query(EventDB).filter(EventDB.id == res.event_id).first()
    if event:
        if event.fecha_evento < datetime.utcnow():
            raise HTTPException(status_code=400, detail="No se puede cancelar una reserva si el evento ya pasó")
        event.entradas_disp += 1
        
    res.estado = "cancelada"
    db.commit()
    return {"message": "Reserva cancelada exitosamente", "reservation_id": res.id}