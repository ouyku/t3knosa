from fastapi import FastAPI

app = FastAPI(
    title="T3knosa — product image finder API",
    description="find exact product image urls by product name and optional code.",
    version="0.1.0"
)


# health check — confirms the API is running
@app.get("/")
def home():
    return {"status": "ok"}
