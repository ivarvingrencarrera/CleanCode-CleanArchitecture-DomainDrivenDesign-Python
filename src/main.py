from datetime import datetime
import os

import asyncpg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.cpf import CPF

load_dotenv()
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


class Item(BaseModel):
    id_product: int
    quantity: int


class Input(BaseModel):
    cpf: str
    items: list[Item] | None = None
    coupon: str | None = None


class Output(BaseModel):
    total: float

class ProductData(BaseModel):
    id_product: int
    description: str
    price: float


class CouponData(BaseModel):
    code: str
    percentage: float
    expire_date: datetime


app = FastAPI()


@app.post('/checkout')
async def checkout(input_: Input) -> Output:
    try:
        output = Output(total=0)
        cpf = CPF(input_.cpf)
        if not cpf.is_valid():
            raise ValueError('Invalid cpf')
        async with asyncpg.create_pool(
                    database=db_name, host=db_host, port=db_port, user=db_user, password=db_password
                ) as pool:
            async with pool.acquire() as connection:
                if input_.items:
                    items = []
                    async with connection.transaction():
                        for item in input_.items:
                            if item.quantity <= 0: raise ValueError('Invalid quantity')
                            if item.id_product in items: raise ValueError('Duplicated item')
                            row = await connection.fetchrow(
                                'SELECT * FROM ecommerce.product WHERE id_product = $1;',
                                item.id_product,
                            )
                            product_data = ProductData(
                                id_product=row[0], description=row[1], price=row[2]
                            )
                            output.total += product_data.price * item.quantity
                            items.append(item.id_product)
                if input_.coupon:
                    async with connection.transaction():
                        row = await connection.fetchrow(
                            'SELECT * FROM ecommerce.coupon WHERE code = $1;', input_.coupon
                        )
                        coupon_data = CouponData(code=row[0], percentage=row[1], expire_date=row[2])
                        if coupon_data.expire_date > datetime.now():
                            output.total -= (output.total * coupon_data.percentage) / 100
            return output
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
        
