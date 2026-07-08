import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

# use a text model for translation — not the image model
client = genai.Client(enterprise=True, project=PROJECT_ID, location="global")


def translate_to_english(product: str) -> str:
    """
    If the product name contains non-English words, translate them to English.
    Returns the English version of the product name.
    Keeps brand names, model codes, and numbers as-is.
    """
    prompt = (
        f"Translate this product name to English. "
        "Keep brand names, model codes, and numbers exactly as they are. "
        "If it is already in English, return it unchanged. "
        "Return ONLY the translated product name, nothing else.\n\n"
        f"Product: {product}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        translated = response.text.strip()
        return translated if translated else product
    except Exception as e:
        print(f"Translation failed, using original: {e}")
        return product  # fallback to original if translation fails
