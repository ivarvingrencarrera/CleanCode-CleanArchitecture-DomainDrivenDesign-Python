from fastapi import FastAPI, HTTPException

from src.application.usecase.checkout import Checkout, Input

app = FastAPI()


@app.post('/checkout')
async def checkout(input_: Input):
    try:
        checkout = Checkout()
        return await checkout.execute(input_)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
