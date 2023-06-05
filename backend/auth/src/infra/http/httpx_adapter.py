import httpx
from requests import Response

from auth.src.infra.http.http_client import HttpClient


class HttpxAdapter(HttpClient):
    async def get(self, url: str, body: dict) -> Response:
        timeout = httpx.Timeout(10.0)
        async with httpx.AsyncClient() as client:
            return await client.get(url, json=body, timeout=timeout)   # type: ignore

    async def post(self, url: str, body: dict) -> Response:
        timeout = httpx.Timeout(10.0)
        async with httpx.AsyncClient() as client:
            return await client.post(url, json=body, timeout=timeout)   # type: ignore
