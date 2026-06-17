from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "t3knosa"}
    
product = "Nothing Headphone 1 B170"


def generate_queries(product):
    return [
        product,
        product + " official image",
        product + " tr.nothing.tech"
    ]


queries = generate_queries(product)

for q in queries:
    print(q)
