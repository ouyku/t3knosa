import os
import base64
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


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


def generate_image(product: str, product_code: Optional[str] = None) -> str:
    prompt = build_prompt(product, product_code)

    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config=types.GenerateImagesConfig(number_of_images=1)
    )

    image_bytes = response.generated_images[0].image.image_bytes

    # encode as base64 data url so it can be used directly as image src
    b64 = base64.b64encode(image_bytes).decode()
    return f"data:image/png;base64,{b64}"
    # TODO: add error handling if generation fails
    # TODO: optionally save generated image to disk or cloud storage
