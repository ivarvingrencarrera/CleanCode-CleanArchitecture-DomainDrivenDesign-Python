import os
from datetime import datetime

import asyncpg
from dotenv import load_dotenv
from pydantic import BaseModel

from src.coupon_repository import CouponRepository

load_dotenv()
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


class CouponData(BaseModel):
    code: str
    percentage: float
    expire_date: datetime


class CouponRepositoryDatabase(CouponRepository):
    async def get_coupon(self, coupon: str) -> CouponData:
        async with asyncpg.create_pool(
            database=db_name, host=db_host, port=db_port, user=db_user, password=db_password
        ) as pool:
            async with pool.acquire() as connection:
                row = await connection.fetchrow(
                    'SELECT * FROM ecommerce.coupon WHERE code = $1;', coupon
                )
                return CouponData(code=row[0], percentage=row[1], expire_date=row[2])
