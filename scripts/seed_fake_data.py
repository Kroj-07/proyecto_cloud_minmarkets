import sys
import os
from faker import Faker
import random

# Esto fuerza a Python a encontrar la carpeta 'app' 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Producto, MovimientoInventario

Base.metadata.create_all(bind=engine)
fake = Faker("es_ES")
db = SessionLocal()

# Crea ~200 productos
productos = []
for _ in range(200):
    p = Producto(
        nombre=fake.word().capitalize() + " " + fake.word(),
        categoria=random.choice(["Abarrotes", "Bebidas", "Limpieza", "Snacks", "Lácteos"]),
        stock_actual=random.randint(0, 100),
        stock_minimo=random.randint(3, 15),
        precio_unitario=round(random.uniform(1.5, 50), 2),
    )
    db.add(p)
    productos.append(p)
db.commit()

# Genera 20,000+ movimientos
movimientos = []
for _ in range(20000):
    movimientos.append(MovimientoInventario(
        producto_id=random.choice(productos).id,
        tipo_movimiento=random.choice(["entrada", "salida"]),
        cantidad=random.randint(1, 50),
    ))
db.bulk_save_objects(movimientos)
db.commit()

print("Carga completa.")