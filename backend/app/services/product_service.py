from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repository.product_repository import ProductRepository
from app.schemas.product import (
    AnalyticsResponse,
    CategoryAggregation,
    CategoryDistribution,
    KPIsResponse,
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def list_products(
        self,
        skip: int = 0,
        limit: int = 100,
        nombre: str | None = None,
        sku: str | None = None,
        categoria: str | None = None,
    ) -> ProductListResponse:
        items, total = self.repo.get_all(skip=skip, limit=limit, nombre=nombre, sku=sku, categoria=categoria)
        return ProductListResponse(
            total=total,
            items=[ProductResponse.model_validate(p) for p in items],
        )

    def get_product(self, product_id: int) -> ProductResponse:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {product_id} no encontrado",
            )
        return ProductResponse.model_validate(product)

    def create_product(self, data: ProductCreate) -> ProductResponse:
        existing = self.repo.get_by_sku(data.sku)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un producto con SKU '{data.sku}'",
            )
        product = self.repo.create(data)
        return ProductResponse.model_validate(product)

    def update_product(self, product_id: int, data: ProductUpdate) -> ProductResponse:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {product_id} no encontrado",
            )
        if data.sku and data.sku != product.sku:
            existing = self.repo.get_by_sku(data.sku)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un producto con SKU '{data.sku}'",
                )
        updated = self.repo.update(product, data)
        return ProductResponse.model_validate(updated)

    def delete_product(self, product_id: int) -> None:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {product_id} no encontrado",
            )
        self.repo.delete(product)

    def get_kpis(self) -> KPIsResponse:
        total = self.repo.count_total()
        valor = self.repo.sum_inventory_value()
        bajo_stock = self.repo.count_low_stock()
        mas_valioso = self.repo.get_most_valuable()
        return KPIsResponse(
            total_productos=total,
            valor_inventario=valor,
            productos_bajo_stock=bajo_stock,
            producto_mas_valioso=ProductResponse.model_validate(mas_valioso) if mas_valioso else None,
        )

    def get_low_stock_products(self) -> ProductListResponse:
        items = self.repo.get_low_stock_products()
        return ProductListResponse(
            total=len(items),
            items=[ProductResponse.model_validate(p) for p in items],
        )

    def get_analytics(self) -> AnalyticsResponse:
        kpis = self.get_kpis()
        aggs = self.repo.get_category_aggregations()
        total_products = kpis.total_productos or 1

        top_categorias = [
            CategoryAggregation(**agg) for agg in aggs
        ]

        distribucion = [
            CategoryDistribution(
                categoria=agg["categoria"],
                total_productos=agg["total_productos"],
                porcentaje=round((agg["total_productos"] / total_products) * 100, 2),
            )
            for agg in aggs
        ]

        return AnalyticsResponse(
            kpis=kpis,
            top_categorias=top_categorias,
            distribucion_categorias=distribucion,
        )
