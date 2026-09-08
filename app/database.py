from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Cambia "root" y "tu_contraseña" por tus credenciales de Docker. 
# El nombre de la base de datos al final debe ser "inventario" (o el que hayas creado)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:pass@127.0.0.1:3306/inventario_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
