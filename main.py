from fastapi import FastAPI

app = FastAPI()

   
product = "Nothing Headphone 1 B170"


def generate_queries(product):
    return [
        product,
        product + " official image",
        product + " tr.nothing.tech"
    ]


@app.get("/")
def home():
    return {"queries = generate_queries(product)"}
 
