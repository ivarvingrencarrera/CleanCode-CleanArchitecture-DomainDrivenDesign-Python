import json

import requests
from pydantic import BaseModel

from src.currency_gateway import CurrencyGateway


class CurrencyData(BaseModel):
    currency: str
    symbol: str
    name: str
    rates: float


class CurrencyGatewayHttp(CurrencyGateway):
    async def get_currencies(self) -> json:
        response = requests.get('http://localhost:3001/currencies', timeout=10)
        response.raise_for_status()
        currency_json = response.json()
        return CurrencyData(
            currency=currency_json['currency'],
            symbol=currency_json['symbol'],
            name=currency_json['name'],
            rates=currency_json['rates'],
        )
