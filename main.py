from fastapi import FastAPI

app = FastAPI(
    title="T3knosa — Product Image Finder API",
    description="Find exact product image URLs by product name and optional code.",
    version="0.1.0"
)


# health check — confirms the API is running
@app.get("/")
def home():
    return {"status": "ok"}
