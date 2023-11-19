from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_orm import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    # put the star to allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# database connection
redis = get_redis_connection(
    host="redis-12111.c10.us-east-1-4.ec2.cloud.redislabs.com:12111",
    port=11844,
    password="2MdfZXQdBREeD18M9RFUwB2oM6pFR72B",
    decode_responses=True
)

# default value
@app.get("/")
async def root():
    return {"message": "Hello World"}

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis



#endpoints
@app.get("/products")   
def all():
    return [format(pk) for pk in Product.all()]

def format(pk:str):
    product = Product.get(pk)
    return {
        "id": pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }

@app.post("/products")
def create(products: Product):
    return product.save()

@app.get("/products/{pk}")
def get(pk: str):
    return product.get(pk)


@app.delete("/products/{pk}")
def delete(pk: str):
    return product.delete(pk)
