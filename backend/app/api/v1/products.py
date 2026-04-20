from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.get("/", response_model=ProductListResponse)
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    nombre: str | None = Query(None),
    sku: str | None = Query(None),
    categoria: str | None = Query(None),
    service: ProductService = Depends(get_service),
):
    return service.list_products(skip=skip, limit=limit, nombre=nombre, sku=sku, categoria=categoria)


@router.get("/low-stock", response_model=ProductListResponse)
def list_low_stock(service: ProductService = Depends(get_service)):
    return service.get_low_stock_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, service: ProductService = Depends(get_service)):
    return service.get_product(product_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, service: ProductService = Depends(get_service)):
    return service.create_product(data)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, data: ProductUpdate, service: ProductService = Depends(get_service)
):
    return service.update_product(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: ProductService = Depends(get_service)):
    service.delete_product(product_id)
