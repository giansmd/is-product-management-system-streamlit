from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@product_db:5432/products_db"
    app_name: str = "Product Management System"
    app_version: str = "1.0.0"
    debug: bool = False
    api_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
