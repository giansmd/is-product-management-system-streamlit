from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        nombre: str | None = None,
        sku: str | None = None,
        categoria: str | None = None,
    ) -> tuple[list[Product], int]:
        query = self.db.query(Product)
        if nombre:
            query = query.filter(Product.nombre.ilike(f"%{nombre}%"))
        if sku:
            query = query.filter(Product.sku.ilike(f"%{sku}%"))
        if categoria:
            query = query.filter(Product.categoria == categoria)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_by_sku(self, sku: str) -> Product | None:
        return self.db.query(Product).filter(Product.sku == sku).first()

    def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, data: ProductUpdate) -> Product:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()

    def count_total(self) -> int:
        return self.db.query(func.count(Product.id)).scalar() or 0

    def sum_inventory_value(self) -> Decimal:
        result = self.db.query(
            func.sum(Product.precio_venta * Product.stock_actual)
        ).scalar()
        return Decimal(str(result)) if result is not None else Decimal("0")

    def count_low_stock(self) -> int:
        return (
            self.db.query(func.count(Product.id))
            .filter(Product.stock_actual <= Product.stock_minimo)
            .scalar()
            or 0
        )

    def get_most_valuable(self) -> Product | None:
        return (
            self.db.query(Product)
            .order_by((Product.precio_venta * Product.stock_actual).desc())
            .first()
        )

    def get_low_stock_products(self) -> list[Product]:
        return (
            self.db.query(Product)
            .filter(Product.stock_actual <= Product.stock_minimo)
            .all()
        )

    def get_category_aggregations(self) -> list[dict]:
        rows = (
            self.db.query(
                Product.categoria,
                func.count(Product.id).label("total_productos"),
                func.sum(Product.precio_venta * Product.stock_actual).label("valor_total"),
            )
            .group_by(Product.categoria)
            .order_by(func.count(Product.id).desc())
            .all()
        )
        return [
            {
                "categoria": r.categoria,
                "total_productos": r.total_productos,
                "valor_total": Decimal(str(r.valor_total)) if r.valor_total else Decimal("0"),
            }
            for r in rows
        ]
