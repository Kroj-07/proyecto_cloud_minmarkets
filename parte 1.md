# Microservicio Inventario — ERP Bodega Inteligente
## Integrante 1 — CS2032 Cloud Computing


---

## 1. Qué hace este microservicio

Lleva el registro de stock de cada producto de la bodega (entradas y salidas de mercadería) y expone esa información vía API REST para que otros microservicios del sistema (Predicción, Alertas) y el frontend puedan consultarla.

---

## 2. Datos que maneja (entidades / tablas y campos principales)

### Tabla `productos`
| Campo | Tipo | Descripción |
|---|---|---|
| id | INT (PK, autoincremental) | Identificador único del producto — es el `producto_id` que usan todos los demás microservicios del sistema |
| nombre | VARCHAR(150) | Nombre del producto |
| categoria | VARCHAR(80) | Categoría (Abarrotes, Bebidas, Limpieza, etc.) |
| stock_actual | INT | Stock disponible actualmente |
| stock_minimo | INT | Umbral mínimo antes de considerar riesgo de quiebre |
| precio_unitario | DECIMAL(10,2) | Precio de venta unitario |
| creado_en | DATETIME | Fecha de creación del registro |

### Tabla `movimientos_inventario`
| Campo | Tipo | Descripción |
|---|---|---|
| id | INT (PK, autoincremental) | Identificador del movimiento |
| producto_id | INT (FK → productos.id) | Producto asociado al movimiento |
| tipo_movimiento | ENUM('entrada','salida') | Tipo de movimiento de stock |
| cantidad | INT | Cantidad movida |
| fecha | DATETIME | Fecha y hora del movimiento |

---

## 3. Base de datos

- **Motor:** MySQL 8.0
- **Nombre de la base de datos:** `inventario_db`
- **Usuario:** `user`
- **Puerto:** `3306`
- **Estructura de tablas:** ver sección 2 arriba. Script completo en [`/db/schema.sql`](./db/schema.sql).

Diagrama Entidad/Relación: `/docs/er_inventario.png` — 2 tablas relacionadas por `producto_id`.

---

## 4. Cómo se llena la base de datos

- Existe un script de carga inicial: [`/scripts/seed_fake_data.py`](./scripts/seed_fake_data.py), que usa la librería `Faker`.
- Genera ~200 productos ficticios y **≥ 20,000 registros** en `movimientos_inventario` (cumple el mínimo exigido por el enunciado del curso).
- Es una **carga única** (one-time bulk load), no continua. Para correrla:
  ```bash
  python scripts/seed_fake_data.py
  ```
- Fuera de esa carga inicial, el resto de movimientos se generan cuando alguien llama al endpoint `POST /movimientos` (pruebas manuales o eventualmente otros clientes).

---

## 5. Endpoints disponibles (API REST)

Documentados automáticamente en Swagger-UI: `http://localhost:8000/docs`

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/movimientos` | Registra un movimiento de stock (entrada/salida). Actualiza `stock_actual` del producto. |
| `GET` | `/productos/{producto_id}/stock` | Devuelve el stock actual de un producto puntual. |
| `GET` | `/productos` | Lista todos los productos. |

**Ejemplo de respuesta de `GET /productos/{id}/stock`:**
```json
{
  "producto_id": 1,
  "nombre": "Producto ejemplo",
  "stock_actual": 42
}
```

---

## 6. ¿Los datos cambian constantemente o se cargan una sola vez?

- `productos`: relativamente **estático** — se crea una vez con el seed y rara vez cambia.
- `movimientos_inventario`: en teoría **crece con cada movimiento registrado**, pero en la práctica del proyecto la mayor parte del volumen viene de la carga masiva inicial (20,000+ registros), más algunos movimientos de prueba manuales.

---

## 7. Campos para cargas incrementales

- `movimientos_inventario.fecha` — se puede filtrar con `fecha > último_timestamp_extraído` para pulls incrementales.
- `productos.creado_en` — equivalente para la tabla de productos.

> Nota: el enunciado del curso pide que el pipeline de ingesta (Data Science) haga **pull del 100% de los registros**, no necesariamente incremental. Estos campos quedan disponibles por si se necesitan, pero probablemente no son obligatorios para el entregable.

---

## 8. Configuración y despliegue

- **Archivo de configuración:** `.env`, con la variable `DATABASE_URL`.
- **Puerto del servicio:** `8000`
- **Comando para levantarlo:**
  ```bash
  docker compose up --build
  ```
- **Documentación interactiva:** una vez levantado, disponible en `http://localhost:8000/docs`.

### Estado del despliegue en AWS
`solo local`


---

## 10. Fuera de alcance de este README

Las preguntas sobre los microservicios **Proveedores** y **Alertas** (datos que manejan, base de datos, endpoints, cómo se disparan las alertas, qué debería guardar la capa histórica en S3) corresponden a **Integrante 3** — este readme solo cubre Inventario, que es la parte de la que me encargué.
