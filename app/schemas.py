from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---- Salidas (lo que consumen Predicción / Alertas: contrato en camelCase) ----

class ProductoOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    nombre: str
    categoria: Optional[str] = None
    stock_actual: int = Field(alias="stockActual")
    stock_minimo: int = Field(alias="stockMinimo")
    precio_unitario: Optional[float] = Field(default=None, alias="precioUnitario")


class ProductoStockOut(BaseModel):
    """Forma exacta que espera prediccion-service (httpClients.js) y Alertas."""
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int = Field(alias="productoId")
    nombre: str
    stock_actual: int = Field(alias="stockActual")


class MovimientoOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    producto_id: int = Field(alias="productoId")
    tipo_movimiento: str = Field(alias="tipoMovimiento")
    cantidad: int
    fecha: datetime


# ---- Entradas ----

class ProductoCrear(BaseModel):
    nombre: str
    categoria: Optional[str] = None
    stock_actual: int = 0
    stock_minimo: int = 5
    precio_unitario: Optional[float] = None


class ProductoActualizar(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    stock_minimo: Optional[int] = None
    precio_unitario: Optional[float] = None


class MovimientoIn(BaseModel):
    producto_id: int
    tipo_movimiento: Literal["entrada", "salida"]
    cantidad: int
