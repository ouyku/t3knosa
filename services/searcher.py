import os
import requests
from dotenv import load_dotenv
from typing import Optional, List

load_dotenv()  # reads the .env file and loads the keys into the environment

API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")

SEARCH_URL = "https://www.googleapis.com/customsearch/v1"


def search_images(query: str) -> List[dict]:
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "searchType": "image",
        "num": 5
    }

    response = requests.get(SEARCH_URL, params=params)
    data = response.json()

    # TODO: extract image_url, source_url, title from each result and return
    pass

