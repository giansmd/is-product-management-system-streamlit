import os

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://product_backend:8000")
API_BASE = f"{BACKEND_URL}/api/v1"


def _get(path: str, params: dict | None = None) -> dict:
    resp = requests.get(f"{API_BASE}{path}", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _post(path: str, data: dict) -> dict:
    resp = requests.post(f"{API_BASE}{path}", json=data, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _put(path: str, data: dict) -> dict:
    resp = requests.put(f"{API_BASE}{path}", json=data, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _delete(path: str) -> None:
    resp = requests.delete(f"{API_BASE}{path}", timeout=10)
    resp.raise_for_status()


def _get_bytes(path: str, params: dict | None = None) -> bytes:
    resp = requests.get(f"{API_BASE}{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.content


# Products
def list_products(
    skip: int = 0,
    limit: int = 100,
    nombre: str | None = None,
    sku: str | None = None,
    categoria: str | None = None,
) -> dict:
    params: dict = {"skip": skip, "limit": limit}
    if nombre:
        params["nombre"] = nombre
    if sku:
        params["sku"] = sku
    if categoria:
        params["categoria"] = categoria
    return _get("/products/", params)


def get_product(product_id: int) -> dict:
    return _get(f"/products/{product_id}")


def create_product(data: dict) -> dict:
    return _post("/products/", data)


def update_product(product_id: int, data: dict) -> dict:
    return _put(f"/products/{product_id}", data)


def delete_product(product_id: int) -> None:
    _delete(f"/products/{product_id}")


def list_low_stock() -> dict:
    return _get("/products/low-stock")


# Analytics
def get_analytics() -> dict:
    return _get("/analytics/")


def get_kpis() -> dict:
    return _get("/analytics/kpis")


# Reports
def download_inventory_pdf(categoria: str | None = None) -> bytes:
    params = {}
    if categoria:
        params["categoria"] = categoria
    return _get_bytes("/reports/inventory/pdf", params)
