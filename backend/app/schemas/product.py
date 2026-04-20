import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    sku: str = Field(..., min_length=1, max_length=100)
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: str | None = None
    categoria: str = Field(..., min_length=1, max_length=100)
    precio_compra: Decimal = Field(..., ge=0)
    precio_venta: Decimal = Field(..., ge=0)
    stock_actual: int = Field(..., ge=0)
    stock_minimo: int = Field(..., ge=0)
    proveedor: str | None = None

    @field_validator("precio_compra", "precio_venta")
    @classmethod
    def validate_precio(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v

    @field_validator("stock_actual", "stock_minimo")
    @classmethod
    def validate_stock(cls, v: int) -> int:
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: str | None = Field(None, min_length=1, max_length=100)
    nombre: str | None = Field(None, min_length=1, max_length=255)
    descripcion: str | None = None
    categoria: str | None = Field(None, min_length=1, max_length=100)
    precio_compra: Decimal | None = Field(None, ge=0)
    precio_venta: Decimal | None = Field(None, ge=0)
    stock_actual: int | None = Field(None, ge=0)
    stock_minimo: int | None = Field(None, ge=0)
    proveedor: str | None = None


class ProductResponse(ProductBase):
    id: int
    fecha_creacion: datetime.datetime
    fecha_actualizacion: datetime.datetime

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    total: int
    items: list[ProductResponse]


class KPIsResponse(BaseModel):
    total_productos: int
    valor_inventario: Decimal
    productos_bajo_stock: int
    producto_mas_valioso: ProductResponse | None


class CategoryAggregation(BaseModel):
    categoria: str
    total_productos: int
    valor_total: Decimal


class CategoryDistribution(BaseModel):
    categoria: str
    porcentaje: float
    total_productos: int


class AnalyticsResponse(BaseModel):
    kpis: KPIsResponse
    top_categorias: list[CategoryAggregation]
    distribucion_categorias: list[CategoryDistribution]
