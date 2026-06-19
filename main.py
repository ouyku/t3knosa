from fastapi import FastAPI
from typing import Optional
from services.query_builder import build_queries

app = FastAPI(
    title="T3knosa — product image finder API",
    description="find exact product image urls by product name and optional code.",
    version="0.1.0"
)


# health check — confirms the API is running
@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/queries")
def queries(product: str, product_code: Optional[str] = None, brand_site: Optional[str] = None):
    return {"queries": build_queries(product, product_code, brand_site)}
