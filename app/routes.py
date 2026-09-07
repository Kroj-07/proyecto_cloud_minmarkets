from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/movimientos", response_model=schemas.MovimientoOut)
def registrar_movimiento(mov: schemas.MovimientoIn, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == mov.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    nuevo = models.MovimientoInventario(**mov.dict())
    db.add(nuevo)

    if mov.tipo_movimiento == "entrada":
        producto.stock_actual += mov.cantidad
    else:
        if producto.stock_actual < mov.cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        producto.stock_actual -= mov.cantidad

    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/productos/{producto_id}/stock")
def consultar_stock(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"producto_id": producto.id, "nombre": producto.nombre, "stock_actual": producto.stock_actual}

@router.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()
