import os
import requests
from dotenv import load_dotenv
from typing import List

load_dotenv()  # reads the .env file and loads the keys into the environment

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

SEARCH_URL = "https://serpapi.com/search"


def search_images(query: str) -> List[dict]:
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google_images",
        "q": query,
        "num": 5
    }

    response = requests.get(SEARCH_URL, params=params)
    data = response.json()

    results = []
    for item in data.get("images_results", []):
        results.append({
            "image_url": item.get("original"),
            "source_url": item.get("link"),
            "title": item.get("title")
        })

    return results
