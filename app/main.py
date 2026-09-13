from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import router

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio de Inventario")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se especifica el dominio de React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def read_root():
    return {"mensaje": "API de Inventario corriendo correctamente"}
