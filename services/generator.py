import os
import base64
import requests
from urllib.parse import quote
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

POLLINATIONS_URL = "https://image.pollinations.ai/prompt"


def build_prompt(product: str, product_code: Optional[str] = None) -> str:
    name = f"{product} {product_code}" if product_code else product
    return (
        f"Professional studio product photograph of {name}. "
        "Pure white background, soft even studio lighting, sharp focus, "
        "commercial product photography style. "
        "Show the product clearly from a slight front angle. "
        "No text, no logos, no watermarks, no people, no shadows."
    )
    # TODO: refine prompt based on product category (electronics, clothing, food etc.)


def generate_image(
    product: str,
    product_code: Optional[str] = None,
    reference_image_url: Optional[str] = None  # best-scored real image from find-images
) -> str:
    prompt = build_prompt(product, product_code)
    encoded = quote(prompt)

    if reference_image_url:
        # img2img mode — model sees the real product before generating
        encoded_ref = quote(reference_image_url)
        url = f"{POLLINATIONS_URL}/{encoded}?model=flux-dev&image={encoded_ref}&width=512&height=512&nologo=true"
    else:
        # text-only fallback — used when no reference image is available
        url = f"{POLLINATIONS_URL}/{encoded}?width=512&height=512&nologo=true"

    response = requests.get(url, timeout=90)

    if response.status_code != 200:
        raise Exception(f"Pollinations API error: {response.status_code}")

    image_bytes = response.content
    b64 = base64.b64encode(image_bytes).decode()
    return f"data:image/jpeg;base64,{b64}"

    # TODO: optionally save generated image to disk or cloud storage
