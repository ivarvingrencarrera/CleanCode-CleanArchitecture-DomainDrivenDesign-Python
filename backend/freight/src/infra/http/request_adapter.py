import requests

from freight.src.infra.http.http_client import HttpClient


class RequestAdapter(HttpClient):
    def get(self, url: str) -> None:
        timeout = 10
        requests.get(url, timeout=timeout)

    def post(self, url: str, body: dict) -> None:
        timeout = 10
        requests.post(url, json=body, timeout=timeout)
