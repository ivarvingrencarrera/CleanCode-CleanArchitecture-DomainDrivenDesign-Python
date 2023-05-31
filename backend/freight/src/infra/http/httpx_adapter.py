import httpx
from httpx import Response

from freight.src.infra.http.http_client import HttpClient


class HttpxAdapter(HttpClient):
    async def get(self, url: str) -> Response:
        timeout = httpx.Timeout(10.0)
        async with httpx.AsyncClient() as client:
            return await client.get(url, timeout=timeout)

    async def post(self, url: str, json: dict) -> Response:
        timeout = httpx.Timeout(10.0)
        async with httpx.AsyncClient() as client:
            return await client.post(url, json=json, timeout=timeout)
