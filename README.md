# Sistema de Gestión de Productos

Sistema de gestión de inventario y análisis de productos construido con:

- **Backend**: FastAPI + SQLAlchemy 2.x + PostgreSQL
- **Frontend**: Streamlit
- **Infraestructura**: Docker + docker-compose

## Arquitectura

```
product_frontend (Streamlit :8501)
        ↕ HTTP
product_backend  (FastAPI   :8000)
        ↕ SQL
product_db       (PostgreSQL:5432)
```

## Estructura del proyecto

```
├── backend/
│   ├── app/
│   │   ├── api/v1/          # Endpoints REST
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── repository/      # Acceso a datos
│   │   ├── schemas/         # Schemas Pydantic
│   │   ├── services/        # Lógica de negocio + PDF
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── wait_for_db.py       # Espera activa hasta que PostgreSQL esté listo
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── pages/
│   │   ├── 1_Dashboard.py   # KPIs, gráficas y bajo stock
│   │   └── 2_Productos.py   # CRUD de productos
│   ├── utils/
│   │   └── api_client.py    # HTTP client para el backend
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## Inicio rápido

```bash
# 1. Clonar el repositorio
git clone <url>
cd is-product-management-system-streamlit

# 2. Copiar variables de entorno
cp .env.example .env

# 3. Levantar los servicios
docker-compose up --build

# Frontend: http://localhost:8501
# Backend API docs: http://localhost:8000/docs
```

## API Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/products/` | Listar productos (filtros opcionales) |
| POST | `/api/v1/products/` | Crear producto |
| GET | `/api/v1/products/{id}` | Obtener producto por ID |
| PUT | `/api/v1/products/{id}` | Actualizar producto |
| DELETE | `/api/v1/products/{id}` | Eliminar producto |
| GET | `/api/v1/products/low-stock` | Productos con bajo stock |
| GET | `/api/v1/analytics/kpis` | KPIs del inventario |
| GET | `/api/v1/analytics/` | Analytics completo |
| GET | `/api/v1/reports/inventory/pdf` | Reporte PDF de inventario |

## Variables de entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `POSTGRES_USER` | `postgres` | Usuario PostgreSQL |
| `POSTGRES_PASSWORD` | `postgres` | Contraseña PostgreSQL |
| `POSTGRES_DB` | `products_db` | Nombre de la base de datos |
| `BACKEND_PORT` | `8000` | Puerto del backend |
| `FRONTEND_PORT` | `8501` | Puerto del frontend |

## Funcionalidades

### Dashboard
- KPIs: total productos, valor del inventario, productos con bajo stock, producto más valioso
- Gráfico de barras: top categorías
- Gráfico de torta: distribución por categoría
- Tabla de productos con bajo stock
- Descarga de reporte PDF

### Gestión de Productos
- Listar productos con filtros (nombre, SKU, categoría)
- Crear nuevos productos
- Editar productos existentes
- Eliminar productos