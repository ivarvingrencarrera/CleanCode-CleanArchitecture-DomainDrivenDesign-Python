import requests
from fastapi import FastAPI

app = FastAPI()


class CurrencyGatewayHttp:
    async def get_currencies(self):
        response = requests.get('http://localhost:3001/currencies')
        response.raise_for_status()
        return response.json()
