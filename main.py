from fastapi import FastAPI
from typing import Optional
from services.query_builder import build_queries
from services.searcher import search_images
from services.matcher import score_result
from models.schemas import SearchResponse, ImageResult

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


@app.get("/find-images", response_model=SearchResponse)
def find_images(product: str, product_code: Optional[str] = None, brand_site: Optional[str] = None):
    queries = build_queries(product, product_code, brand_site)

    # call search_images for each query and collect results
    raw_results = []
    for query in queries:
        raw_results += search_images(query)

    # remove duplicate image_urls
    seen = set()
    unique_results = []
    for item in raw_results:
        if item["image_url"] not in seen:
            seen.add(item["image_url"])
            unique_results.append(item)

    # score each result and build ImageResult objects
    results = []
    for item in unique_results:
        results.append(ImageResult(
            image_url=item["image_url"],
            source_url=item["source_url"],
            title=item["title"],
            confidence_score=score_result(item["title"], product, product_code)
        ))

    # TODO: sort by confidence_score highest first
    # TODO: return as SearchResponse
    pass
