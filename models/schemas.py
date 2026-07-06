# pydantic validates data shapes automatically — if a field is missing or the wrong type,
# fastapi will reject the request and return a clear error before our code even runs
from pydantic import BaseModel
from typing import Optional, List


# shape of a single image result
class ImageResult(BaseModel):
    image_url: str
    source_url: Optional[str] = None
    title: str
    confidence_score: float  # 0.0 (low confidence) to 1.0 (high confidence)
    is_generated: bool = False  # true if this image was AI-generated, not found online



# shape of the full response from /find-images
class SearchResponse(BaseModel):
    product: str
    product_code: Optional[str] = None
    results: List[ImageResult]
