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
    reference_image_url: Optional[str] = None  # TODO: pass the best-scored real image from find-images as reference
) -> str:
    prompt = build_prompt(product, product_code)
    encoded = quote(prompt)

    # TODO: if reference_image_url is provided, switch to image-to-image mode:
    #   - encode reference_image_url and pass as ?image= param to Pollinations
    #   - this lets the model see the actual product before generating
    #   - example: url = f"{POLLINATIONS_URL}/{encoded}?image={quote(reference_image_url)}&model=flux-dev&width=512&height=512&nologo=true"
    #   - result will look much closer to the real product

    url = f"{POLLINATIONS_URL}/{encoded}?width=512&height=512&nologo=true"
    response = requests.get(url, timeout=60)

    if response.status_code != 200:
        raise Exception(f"Pollinations API error: {response.status_code}")

    image_bytes = response.content
    b64 = base64.b64encode(image_bytes).decode()
    return f"data:image/jpeg;base64,{b64}"

    # TODO: add error handling if generation fails
    # TODO: optionally save generated image to disk or cloud storage
