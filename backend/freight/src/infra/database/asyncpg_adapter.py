import os

import asyncpg
from dotenv import load_dotenv

from freight.src.infra.database.connection import Connection

load_dotenv()
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


class AsyncPGAdapter(Connection):
    def __init__(self) -> None:
        self.connection: asyncpg = None

    async def connect(self) -> None:
        self.connection = await asyncpg.connect(
            database=db_name, host=db_host, port=db_port, user=db_user, password=db_password
        )

    async def disconnect(self) -> None:
        await self.connection.close()

    async def insert(self, query: str, *params: str) -> None:
        await self.connect()
        try:
            await self.connection.execute(query, *params)
        finally:
            await self.disconnect()

    async def select(self, query: str, *params: str) -> list:
        await self.connect()
        try:
            return await self.connection.fetch(query, *params)
        finally:
            await self.disconnect()
