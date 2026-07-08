import os
import base64
import requests
from urllib.parse import quote
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "global"
MODEL_ID = "gemini-3.1-flash-image"

# enterprise=True uses GCP project credits (Agent Platform)
client = genai.Client(enterprise=True, project=PROJECT_ID, location=LOCATION)

# fallback: pollinations for text-only generation
POLLINATIONS_URL = "https://image.pollinations.ai/prompt"


def build_prompt(product: str, product_code: Optional[str] = None, style: str = "catalog") -> str:
    name = f"{product} {product_code}" if product_code else product

    if style == "lifestyle":
        return (
            f"Lifestyle photo of {name} being used in everyday life. "
            "Natural indoor or outdoor setting, warm ambient lighting, realistic environment. "
            "Show the product in context — someone using it, or placed naturally in a room or scene. "
            "Candid, authentic feel. No studio backgrounds. No text, no watermarks."
        )

    # default: catalog style
    return (
        f"Professional studio product photograph of {name}. "
        "Pure white background, soft even studio lighting, sharp focus, "
        "commercial product photography style. "
        "Show the product clearly from a slight front angle. "
        "No text, no logos, no watermarks, no people, no shadows."
    )

def generate_image(
    product: str,
    product_code: Optional[str] = None,
    reference_image_url: Optional[str] = None,
    style: str = "catalog"  # "catalog" or "lifestyle"
) -> str:
    prompt = build_prompt(product, product_code, style)

    try:
        if reference_image_url:
            # img2img mode — download reference and pass as input image
            ref_response = requests.get(reference_image_url, timeout=15)
            ref_response.raise_for_status()
            b64_ref = base64.b64encode(ref_response.content).decode()

            edit_prompt = (
                "This is a product image. Generate a NEW studio photo of the SAME product "
                "from a completely different angle or perspective. "
                "IMPORTANT: Do NOT add, remove, or change any physical parts of the product. "
                "The product must have exactly the same components as in the reference image. "
                "Pure white background, soft studio lighting, sharp focus, "
                "professional commercial photography. No text, no watermarks, no shadows."
            )

            contents = [
                types.Part(inline_data=types.Blob(
                    mime_type="image/jpeg",
                    data=base64.b64decode(b64_ref)
                )),
                types.Part(text=edit_prompt)
            ]
        else:
            contents = [types.Part(text=prompt)]

        response = client.models.generate_content(
            model=MODEL_ID,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
                thinking_config=types.ThinkingConfig(thinking_budget=1024)  # high thinking so it's more accurate
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_bytes = part.inline_data.data
                b64 = base64.b64encode(image_bytes).decode()
                return f"data:image/png;base64,{b64}"

        raise Exception("no image in response")

    except Exception as e:
        # fallback to Pollinations if Gemini fails
        print(f"Gemini failed, falling back to Pollinations: {e}")
        encoded = quote(prompt)
        url = f"{POLLINATIONS_URL}/{encoded}?width=512&height=512&nologo=true"
        resp = requests.get(url, timeout=90)
        if resp.status_code != 200:
            raise Exception(f"All generation methods failed. Last error: {e}")
        b64 = base64.b64encode(resp.content).decode()
        return f"data:image/jpeg;base64,{b64}"

    # TODO: optionally save generated image to disk or cloud storage
