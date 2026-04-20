from fastapi import APIRouter

from app.api.v1 import analytics, products, reports

api_router = APIRouter()
api_router.include_router(products.router)
api_router.include_router(analytics.router)
api_router.include_router(reports.router)
