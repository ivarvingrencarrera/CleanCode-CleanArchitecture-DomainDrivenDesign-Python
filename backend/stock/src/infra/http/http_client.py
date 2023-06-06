from abc import ABC, abstractmethod

from httpx import Response


class HttpClient(ABC):
    @abstractmethod
    async def get(self, url: str) -> Response:
        pass

    @abstractmethod
    async def post(self, url: str, body: dict) -> Response:
        pass
