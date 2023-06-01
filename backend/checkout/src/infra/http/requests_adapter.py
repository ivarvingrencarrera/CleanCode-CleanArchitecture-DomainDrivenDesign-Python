import requests
from requests import Response

from checkout.src.infra.http.http_client import HttpClient


class RequestsAdapter(HttpClient):

    async def get(self, url: str, body: dict) -> Response:
        timeout = 10.0
        response = requests.get(url, json=body, timeout=timeout)
        if response.status_code == 422:
            raise ValueError(response.json()['detail'])
        return response

    async def post(self, url: str, body: dict) -> Response:
        timeout = 10.0
        response = requests.post(url, json=body, timeout=timeout)
        if response.status_code == 422:
           raise ValueError(response.json()['detail'])
            
        return response
