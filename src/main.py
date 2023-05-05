import os

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI
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
    message: str | None = None


class ProductData(BaseModel):
    id_product: int
    description: str
    price: float


class CouponData(BaseModel):
    code: str
    percentage: float


app = FastAPI()


@app.post('/checkout')
async def checkout(input_: Input) -> Output:
    output = Output(total=0)
    connection = psycopg2.connect(
        dbname='root', user=db_user, password=db_password, host=db_host, port=db_port
    )
    cursor = connection.cursor()
    if input_.items:
        for item in input_.items:
            cursor.execute(
                'SELECT * FROM ecommerce.product WHERE id_product = %s;', (item.id_product,)
            )
            row = cursor.fetchone()
            product_data = ProductData(id_product=row[0], description=row[1], price=row[2])
            output.total += product_data.price * item.quantity
    if input_.coupon:
        cursor.execute('SELECT * FROM ecommerce.coupon WHERE code = %s;', (input_.coupon,))
        row = cursor.fetchone()
        coupon_data = CouponData(code=row[0], percentage=row[1])
        output.total -= (output.total * coupon_data.percentage) / 100
    cursor.close()
    connection.close()
    cpf = CPF(input_.cpf)
    is_valid = cpf.is_valid()
    if not is_valid:
        output.message = 'Invalid cpf'
    return output
