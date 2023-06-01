from abc import ABC, abstractmethod

from requests import Response


class HttpClient(ABC):
    @abstractmethod
    async def get(self, url: str, body: dict) -> Response:
        pass

    @abstractmethod
    async def post(self, url: str, body: dict) -> Response:
        pass
