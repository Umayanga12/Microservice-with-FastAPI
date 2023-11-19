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

# database connection - need to use another database for each an every microservice
redis = get_redis_connection(
    host="redis-12111.c10.us-east-1-4.ec2.cloud.redislabs.com:12111",
    port=11844,
    password="2MdfZXQdBREeD18M9RFUwB2oM6pFR72B",
    decode_responses=True
)


class order(HashModel):
    product_id : str
    proce : str
    fee: float
    total: float
    quantity: int
    status: str


    class Meta:
        database = redis


@app.post("/order")
async def create(request: Request):
    body = await request.json()
    req = request.get('http://localhost:8000/products/%s' % body['id'])
    
    product =  req.json()

    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.2*product['price'],
        totla = 1.2*product['price'],
        quantity = body['quantity'],
        status = 'pending'
    )

    order.save()
    return order



def order_completed(pk: str):
    order = Order.get(pk)
    order.status = 'completed'
    order.save()
    return order

