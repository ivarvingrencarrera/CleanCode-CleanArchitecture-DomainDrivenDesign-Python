from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.checkout import Checkout


class Item(BaseModel):
    id_product: int
    quantity: int
    price: float | None = None


class Input(BaseModel):
    uuid: str | None = None
    cpf: str
    items: list[Item] | None = None
    coupon: str | None = None
    origin: str | None = None
    destination: str | None = None


app = FastAPI()


@app.post('/checkout')
async def checkout(input_: Input):
    try:
        checkout = Checkout()
        return await checkout.execute(input_)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
