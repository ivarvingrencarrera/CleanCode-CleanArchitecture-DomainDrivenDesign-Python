import json

import requests
from fastapi import FastAPI

from src.currency_gateway import CurrencyGateway

app = FastAPI()


class CurrencyGatewayHttp(CurrencyGateway):
    async def get_currencies(self) -> json:
        response = requests.get('http://localhost:3001/currencies')
        response.raise_for_status()
        return response.json()
