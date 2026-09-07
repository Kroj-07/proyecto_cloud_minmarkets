from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    categoria = Column(String(80))
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)
    precio_unitario = Column(Numeric(10, 2))
    creado_en = Column(DateTime, server_default=func.now())

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    tipo_movimiento = Column(Enum("entrada", "salida", name="tipo_mov"))
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime, server_default=func.now())
