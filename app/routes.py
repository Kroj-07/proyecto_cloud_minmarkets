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


# ---------------- Productos: CRUD completo ----------------

@router.get("/productos", response_model=list[schemas.ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()


@router.get("/productos/{producto_id}", response_model=schemas.ProductoOut)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.get("/productos/{producto_id}/stock", response_model=schemas.ProductoStockOut)
def consultar_stock(producto_id: int, db: Session = Depends(get_db)):
    """Contrato consumido por prediccion-service y alertas-service. No renombrar campos."""
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/productos", response_model=schemas.ProductoOut, status_code=201)
def crear_producto(datos: schemas.ProductoCrear, db: Session = Depends(get_db)):
    producto = models.Producto(**datos.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@router.put("/productos/{producto_id}", response_model=schemas.ProductoOut)
def editar_producto(producto_id: int, datos: schemas.ProductoActualizar, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto


@router.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """OJO: si el producto ya tiene movimientos (FK), esto falla por integridad.
    Para la demo de CRUD, usa un producto recién creado con POST, que no tiene
    movimientos asociados todavía."""
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    tiene_movimientos = (
        db.query(models.MovimientoInventario)
        .filter(models.MovimientoInventario.producto_id == producto_id)
        .first()
    )
    if tiene_movimientos:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar: el producto tiene movimientos registrados",
        )
    db.delete(producto)
    db.commit()
    return None


# ---------------- Movimientos ----------------

@router.post("/movimientos", response_model=schemas.MovimientoOut, status_code=201)
def registrar_movimiento(mov: schemas.MovimientoIn, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == mov.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    nuevo = models.MovimientoInventario(**mov.model_dump())
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
