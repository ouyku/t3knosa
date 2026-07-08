from fastapi import FastAPI, HTTPException
from typing import Optional
from services.query_builder import build_queries
from services.searcher import search_images
from services.matcher import score_result
from services.generator import generate_image
from models.schemas import SearchResponse, ImageResult

GENERATE_THRESHOLD = 0.3  # auto-generate if best score is below this

app = FastAPI(
    title="T3knosa — product image finder API",
    description="find exact product image urls by product name and optional code."
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

    # sort by confidence_score highest first
    results.sort(key=lambda x: x.confidence_score, reverse=True)

    # if no results or best score is too low, auto-generate
    if not results or results[0].confidence_score < GENERATE_THRESHOLD:
        image_url = generate_image(product, product_code)
        results.insert(0, ImageResult(
            image_url=image_url,
            source_url=None,
            title=f"{product} — AI generated",
            confidence_score=1.0,
            is_generated=True
        ))

    # return as SearchResponse
    return SearchResponse(
        product=product,
        product_code=product_code,
        results=results
    )


@app.get("/generate-image", response_model=SearchResponse)
def generate(
    product: str,
    product_code: Optional[str] = None,
    reference_image_url: Optional[str] = None,
    style: str = "catalog"  # "catalog" or "lifestyle"
):
    # manual trigger — always generates, uses reference image if provided for img2img
    try:
        image_url = generate_image(product, product_code, reference_image_url, style)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return SearchResponse(
        product=product,
        product_code=product_code,
        results=[ImageResult(
            image_url=image_url,
            source_url=None,
            title=f"{product} — AI generated ({style})",
            confidence_score=1.0,
            is_generated=True
        )]
    )
