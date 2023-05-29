from abc import ABC, abstractmethod


class HttpClient(ABC):
    @abstractmethod
    def get(self, url: str) -> None:
        pass

    @abstractmethod
    def post(self, url: str, body: dict) -> None:
        pass
