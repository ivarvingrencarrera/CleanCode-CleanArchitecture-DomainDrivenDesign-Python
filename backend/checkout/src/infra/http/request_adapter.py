import requests

from checkout.src.infra.http.http_client import HttpClient


class RequestAdapter(HttpClient):
    async def get(self, url: str):
        timeout = 10
        return requests.get(url, timeout=timeout)

    async def post(self, url: str, body):
        timeout = 10
        return requests.post(url, json=body, timeout=timeout)
