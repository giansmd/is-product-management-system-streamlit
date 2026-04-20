from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import AnalyticsResponse, KPIsResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.get("/kpis", response_model=KPIsResponse)
def get_kpis(service: ProductService = Depends(get_service)):
    return service.get_kpis()


@router.get("/", response_model=AnalyticsResponse)
def get_analytics(service: ProductService = Depends(get_service)):
    return service.get_analytics()
